from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
import pagarme
import os
import json
import time
from datetime import datetime
import logging
import base64
import requests

from .. import db
from .models import Payment, CoursePrice
from .utils import (
    validate_card_number, validate_expiry, validate_cvv,
    format_amount, format_card_data, get_payment_status_display
)

from . import payments_bp

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='pagarme.log'
)
logger = logging.getLogger(__name__)

# Configurações para Pagar.me API v5 (para Pix)
PAGARME_API_URL = 'https://api.pagar.me/core/v5/orders'

def get_pagarme_headers():
    """Função para obter headers com a chave da API."""
    api_key = current_app.config['PAGARME_API_KEY']
    return {
        'Authorization': 'Basic ' + base64.b64encode(f'{api_key}:'.encode()).decode(),
        'Content-Type': 'application/json'
    }

@payments_bp.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    """Página de pagamento com integração Pagar.me."""
    # Verificar se o usuário é aluno
    if current_user.role != 'n':
        flash('Acesso à página de pagamento é exclusivo para alunos.', 'warning')
        return redirect(url_for('lessons.dashboard'))

    # Verificar se o usuário já tem um pagamento confirmado
    existing_payment = Payment.query.filter_by(user_id=current_user.id).filter(
        Payment.payment_status.in_(['paid', 'authorized'])
    ).first()
    if existing_payment:
        flash('Você já possui um pagamento confirmado.', 'info')
        return redirect(url_for('lessons.dashboard'))

    # Obter preço do curso do banco de dados
    course_price = CoursePrice.query.first()
    if not course_price:
        # Criar um registro padrão se não houver preço configurado
        course_price = CoursePrice(price=29.90)
        db.session.add(course_price)
        db.session.commit()
        flash('Preço do curso não estava configurado. Um valor padrão de R$ 29,90 foi definido. O administrador pode ajustá-lo.', 'warning')
    price = course_price.price

    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        
        # Obter dados do formulário
        street = request.form.get('street', current_user.address)
        street_number = request.form.get('street_number')
        neighborhood = request.form.get('neighborhood')
        zipcode = request.form.get('zipcode', current_user.cep)
        city = request.form.get('city')
        state = request.form.get('state')
        
        # Validar campos obrigatórios
        if not all([street, street_number, neighborhood, zipcode, city, state]):
            flash('Por favor, preencha todos os campos de endereço.', 'danger')
            return redirect(url_for('payments.payment'))
        
        # Dados para customer (sem address)
        customer_data = {
            'external_id': str(current_user.id),
            'type': 'individual',
            'country': 'br',
            'name': current_user.name,
            'email': current_user.email,
            'documents': [{
                'type': 'cpf',
                'number': current_user.cpf
            }],
            'phone_numbers': [current_user.phone_number]
        }

        # Dados para billing (com address)
        billing_data = {
            'name': current_user.name,
            'address': {
                'street': street,
                'zipcode': zipcode,
                'country': 'br',
                'street_number': street_number,
                'neighborhood': neighborhood,
                'city': city,
                'state': state
            }
        }

        if payment_method == 'credit_card':
            card_number = request.form.get('card_number')
            card_holder = request.form.get('card_holder')
            card_expiry = request.form.get('card_expiry')
            card_cvv = request.form.get('card_cvv')
            
            # Validações
            if not all([card_number, card_holder, card_expiry, card_cvv]):
                flash('Por favor, preencha todos os campos do cartão.', 'danger')
                return redirect(url_for('payments.payment'))
            
            if not validate_card_number(card_number):
                flash('Número de cartão inválido.', 'danger')
                return redirect(url_for('payments.payment'))
            
            if not validate_expiry(card_expiry):
                flash('Data de expiração inválida.', 'danger')
                return redirect(url_for('payments.payment'))
            
            if not validate_cvv(card_cvv):
                flash('Código de segurança inválido.', 'danger')
                return redirect(url_for('payments.payment'))
            
            # Processar pagamento com cartão de crédito
            try:
                logger.info("Iniciando criação de transação de cartão de crédito para usuário %s", current_user.id)
                # Configurar API key
                pagarme.authentication_key(current_app.config['PAGARME_API_KEY'])
                
                # Formatar dados do cartão
                card_data = format_card_data(card_number, card_holder, card_expiry, card_cvv)
                
                # Criar transação
                transaction = pagarme.transaction.create({
                    'amount': format_amount(price),
                    'card_number': card_data['card_number'],
                    'card_holder_name': card_data['card_holder_name'],
                    'card_expiration_date': card_data['card_expiration_date'],
                    'card_cvv': card_data['card_cvv'],
                    'payment_method': 'credit_card',
                    'customer': customer_data,
                    'billing': billing_data,
                    'items': [
                        {
                            'id': '1',
                            'title': 'Curso Básico de Hebraico',
                            'unit_price': format_amount(price),
                            'quantity': 1,
                            'tangible': False
                        }
                    ],
                    'metadata': {
                        'user_id': current_user.id
                    },
                    'async': False  # Processar síncronamente para testes
                })
                
                logger.info("Transação criada com sucesso: %s", transaction)
                
                # Registrar pagamento no banco de dados
                payment = Payment(
                    user_id=current_user.id,
                    amount=price,
                    payment_method='credit_card',
                    payment_status=transaction['status'],
                    transaction_id=transaction['id']
                )
                db.session.add(payment)
                db.session.commit()
                
                return redirect(url_for('payments.payment_status', transaction_id=transaction['id']))
            
            except Exception as e:
                logger.error("Erro ao criar transação de cartão: %s", str(e))
                flash(f'Erro ao processar pagamento: {str(e)}', 'danger')
                return redirect(url_for('payments.payment'))
        
        elif payment_method == 'boleto':
            try:
                logger.info("Iniciando criação de transação de boleto para usuário %s", current_user.id)
                # Configurar API key
                pagarme.authentication_key(current_app.config['PAGARME_API_KEY'])
                
                # Criar transação com boleto
                transaction = pagarme.transaction.create({
                    'amount': format_amount(price),
                    'payment_method': 'boleto',
                    'customer': customer_data,
                    'billing': billing_data,
                    'items': [
                        {
                            'id': '1',
                            'title': 'Curso Básico de Hebraico',
                            'unit_price': format_amount(price),
                            'quantity': 1,
                            'tangible': False
                        }
                    ],
                    'metadata': {
                        'user_id': current_user.id
                    },
                    'async': False  # Processar síncronamente para testes
                })
                
                logger.info("Transação de boleto criada com sucesso: %s", transaction)
                
                # Registrar pagamento no banco de dados
                payment = Payment(
                    user_id=current_user.id,
                    amount=price,
                    payment_method='boleto',
                    payment_status=transaction['status'],
                    transaction_id=transaction['id']
                )
                db.session.add(payment)
                db.session.commit()
                
                return redirect(url_for('payments.payment_status', transaction_id=transaction['id']))
            
            except Exception as e:
                logger.error("Erro ao criar transação de boleto: %s", str(e))
                flash(f'Erro ao gerar boleto: {str(e)}', 'danger')
                return redirect(url_for('payments.payment'))
        
        elif payment_method == 'pix':
            try:
                logger.info("Iniciando criação de ordem Pix para usuário %s", current_user.id)
                
                # Montar payload para API v5
                pix_payload = {
                    'code': f'order_{int(time.time())}',
                    'closed': False,
                    'items': [
                        {
                            'amount': format_amount(price),
                            'description': 'Curso Básico de Hebraico',
                            'quantity': 1
                        }
                    ],
                    'customer': {
                        'name': current_user.name,
                        'email': current_user.email,
                        'type': 'individual',
                        'document': current_user.cpf,
                        'document_type': 'cpf',
                        'phones': {
                            'home_phone': {
                                'country_code': '55',
                                'number': current_user.phone_number.replace('+55', '').replace(' ', '')[-9:],
                                'area_code': current_user.phone_number.replace('+55', '').replace(' ', '')[:2]
                            }
                        },
                        'address': {
                            'street': street,
                            'street_number': street_number,
                            'zip_code': zipcode.replace('-', ''),
                            'neighborhood': neighborhood,
                            'city': city,
                            'state': state,
                            'country': 'BR'
                        }
                    },
                    'payments': [
                        {
                            'payment_method': 'pix',
                            'pix': {
                                'expires_in': 3600,
                                'additional_information': [
                                    {
                                        'name': 'Curso',
                                        'value': 'Hebraico Básico'
                                    }
                                ]
                            }
                        }
                    ]
                }
                
                # Criar ordem via API v5
                response = requests.post(PAGARME_API_URL, json=pix_payload, headers=get_pagarme_headers())
                response.raise_for_status()
                result = response.json()
                
                logger.info("Ordem Pix criada com sucesso: %s", result)
                
                # Registrar pagamento no banco de dados
                payment = Payment(
                    user_id=current_user.id,
                    amount=price,
                    payment_method='pix',
                    payment_status='waiting_payment',
                    transaction_id=result['id']
                )
                db.session.add(payment)
                db.session.commit()
                
                return redirect(url_for('payments.payment_status', transaction_id=result['id']))
            
            except requests.RequestException as e:
                logger.error("Erro ao criar ordem Pix: %s", str(e))
                flash(f'Erro ao gerar Pix: {str(e)}', 'danger')
                return redirect(url_for('payments.payment'))
        
        else:
            flash('Método de pagamento inválido.', 'danger')
            return redirect(url_for('payments.payment'))
    
    return render_template('payments/payment.html', price=price)

@payments_bp.route('/payment/status/<transaction_id>')
@login_required
def payment_status(transaction_id):
    try:
        logger.info("Consultando status da transação %s", transaction_id)
        
        # Verificar se é Pix (API v5) ou outro método (API v4)
        payment = Payment.query.filter_by(transaction_id=transaction_id).first()
        if not payment:
            logger.error("Pagamento %s não encontrado", transaction_id)
            return redirect(url_for('payments.payment'))
        
        if payment.payment_method == 'pix':
            # Consultar ordem na API v5
            response = requests.get(f'{PAGARME_API_URL}/{transaction_id}', headers=get_pagarme_headers())
            response.raise_for_status()
            transaction = response.json()
            
            # Atualizar status
            payment_status = transaction.get('status', 'waiting_payment')
            payment.payment_status = payment_status
            db.session.commit()
            
            # Preparar dados para exibição
            payment_data = {
                'status': get_payment_status_display(payment_status),
                'amount': f"R$ {transaction['amount'] / 100:.2f}",
                'payment_method': 'Pix',
                'pix_qr_code': transaction.get('charges', [{}])[0].get('last_transaction', {}).get('qr_code', ''),
                'pix_qr_code_url': transaction.get('charges', [{}])[0].get('last_transaction', {}).get('qr_code_url', '')
            }
        
        else:
            # Consultar transação na API v4
            pagarme.authentication_key(current_app.config['PAGARME_API_KEY'])
            transactions = pagarme.transaction.find_by({'id': transaction_id})
            
            if not transactions or len(transactions) == 0:
                logger.error("Transação %s não encontrada", transaction_id)
                return redirect(url_for('payments.payment'))
            
            transaction = transactions[0]
            
            # Atualizar status
            payment.payment_status = transaction['status']
            db.session.commit()
            
            # Preparar dados para exibição
            payment_data = {
                'status': get_payment_status_display(transaction['status']),
                'amount': f"R$ {transaction['amount'] / 100:.2f}",
                'payment_method': 'Cartão de Crédito' if transaction['payment_method'] == 'credit_card' else 'Boleto',
                'boleto_url': transaction.get('boleto_url', ''),
                'boleto_barcode': transaction.get('boleto_barcode', '')
            }
        
        logger.info("Status da transação %s: %s", transaction_id, payment_data['status'])
        return render_template('payments/payment_status.html', payment=payment_data)
    
    except Exception as e:
        logger.error("Erro ao consultar status da transação %s: %s", transaction_id, str(e))
        return redirect(url_for('payments.payment'))

@payments_bp.route('/payment/webhook', methods=['POST'])
def payment_webhook():
    # Verificar assinatura do webhook (implementação simplificada)
    payload = request.get_json()
    
    if not payload:
        logger.error("Webhook: Payload inválido")
        return jsonify({'error': 'Invalid payload'}), 400
    
    # Processar notificação de pagamento
    try:
        transaction_id = payload.get('id')
        new_status = payload.get('current_status')
        
        if transaction_id and new_status:
            payment = Payment.query.filter_by(transaction_id=transaction_id).first()
            
            if payment:
                payment.payment_status = new_status
                db.session.commit()
                
                # Ativar acesso do usuário se o pagamento foi aprovado
                if new_status in ['paid', 'authorized']:
                    user = payment.user
                    if user:
                        user.is_active = True
                        db.session.commit()
                
                logger.info("Webhook: Transação %s atualizada para status %s", transaction_id, new_status)
                return jsonify({'success': True}), 200
            
            logger.error("Webhook: Pagamento não encontrado para transação %s", transaction_id)
            return jsonify({'error': 'Payment not found'}), 404
        
        logger.error("Webhook: Dados de transação inválidos")
        return jsonify({'error': 'Invalid transaction data'}), 400
    
    except Exception as e:
        logger.error("Webhook: Erro ao processar notificação: %s", str(e))
        return jsonify({'error': str(e)}), 500