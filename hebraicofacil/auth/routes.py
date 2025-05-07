from flask import render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash
import secrets
from datetime import datetime

from .. import db, mail
from .models import User, Progress
from .utils import (
    validate_cpf, validate_birth_date, validate_cep, validate_phone,
    hash_password, check_password, generate_confirmation_token, confirm_token
)

from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'a':
            return redirect(url_for('admin.admin_dashboard'))
        elif current_user.role == 's':
            return redirect(url_for('lessons.teacher_dashboard'))
        return redirect(url_for('lessons.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password(user.password, password):
            if not user.email_verified:
                flash('Por favor, verifique seu e-mail para ativar sua conta.', 'warning')
                return redirect(url_for('auth.resend_confirmation'))
            
            if not user.is_active:
                flash('Sua conta está desativada. Entre em contato com o suporte.', 'danger')
                return redirect(url_for('auth.login'))
            
            login_user(user, remember=remember)
            if user.role == 'a':
                return redirect(url_for('admin.admin_dashboard'))
            elif user.role == 's':
                return redirect(url_for('lessons.teacher_dashboard'))
            return redirect(url_for('lessons.dashboard'))
        
        flash('E-mail ou senha incorretos.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.role == 'a':
            return redirect(url_for('admin.admin_dashboard'))
        return redirect(url_for('lessons.dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        cpf = request.form.get('cpf')
        birth_date = request.form.get('birth_date')
        address = request.form.get('address')
        cep = request.form.get('cep')
        phone_number = request.form.get('phone_number')
        country = request.form.get('country')
        state = request.form.get('state')
        
        # Validações
        if not all([name, email, password, confirm_password, cpf, birth_date, address, cep, phone_number, country, state]):
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return render_template('auth/register.html')
        
        if not validate_cpf(cpf):
            flash('CPF inválido.', 'danger')
            return render_template('auth/register.html')
        
        if not validate_birth_date(birth_date):
            flash('Data de nascimento inválida. Você deve ter pelo menos 18 anos.', 'danger')
            return render_template('auth/register.html')
        
        if not validate_cep(cep):
            flash('CEP inválido.', 'danger')
            return render_template('auth/register.html')
        
        if not validate_phone(phone_number):
            flash('Número de telefone inválido. Use o formato correto para o país selecionado.', 'danger')
            return render_template('auth/register.html')
        
        # Verificar se o e-mail já está em uso
        if User.query.filter_by(email=email).first():
            flash('Este e-mail já está em uso.', 'danger')
            return render_template('auth/register.html')
        
        # Verificar se o CPF já está em uso
        if User.query.filter_by(cpf=cpf.replace('.', '').replace('-', '')).first():
            flash('Este CPF já está em uso.', 'danger')
            return render_template('auth/register.html')
        
        # Criar novo usuário
        confirmation_token = secrets.token_urlsafe(32)
        new_user = User(
            name=name,
            email=email,
            password=hash_password(password),
            cpf=cpf.replace('.', '').replace('-', ''),
            birth_date=birth_date,
            address=address,
            cep=cep.replace('-', ''),
            phone_number=phone_number,  # Already includes country code from form submission
            country=country,
            state=state,
            confirmation_token=confirmation_token,
            email_verified=False,  # Usuário precisa confirmar o email
            is_active=False        # Usuário precisa confirmar o email para ativar a conta
        )
        
        # Primeiro adicionar e fazer commit do usuário para obter o ID
        db.session.add(new_user)
        db.session.commit()
        
        # Agora criar o progresso usando o ID do usuário
        new_progress = Progress(user_id=new_user.id)
        db.session.add(new_progress)
        db.session.commit()
        
        # Gerar token e URL de confirmação
        token = generate_confirmation_token(email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        
        try:
            # Enviar e-mail de confirmação
            msg = Message(
                'Confirme seu cadastro - HebraicoFacil',
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[email]
            )
            msg.body = f'''Olá {name},

Obrigado por se cadastrar no HebraicoFacil! Para confirmar seu e-mail, clique no link abaixo:

{confirm_url}

Se você não solicitou este cadastro, ignore este e-mail.

Atenciosamente,
Equipe HebraicoFacil
'''
            mail.send(msg)
            flash('Um e-mail de confirmação foi enviado para o seu endereço. Por favor, verifique sua caixa de entrada.', 'info')
        except Exception as e:
            # Em caso de erro no envio do e-mail, fornecer o link diretamente
            flash(f'Não foi possível enviar o e-mail de confirmação. Por favor, use este link para confirmar sua conta: {confirm_url}', 'warning')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    
    if not email:
        flash('O link de confirmação é inválido ou expirou.', 'danger')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('auth.login'))
    
    if user.email_verified:
        flash('Sua conta já foi confirmada. Por favor, faça login.', 'info')
        return redirect(url_for('auth.login'))
    
    user.email_verified = True
    user.is_active = True
    user.confirmation_token = None
    db.session.commit()
    
    flash('Sua conta foi confirmada com sucesso! Agora você pode fazer login.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/resend')
def resend_confirmation():
    if current_user.is_authenticated:
        if current_user.role == 'a':
            return redirect(url_for('admin.admin_dashboard'))
        elif current_user.role == 's':
            return redirect(url_for('lessons.teacher_dashboard'))
        return redirect(url_for('lessons.dashboard'))
    
    return render_template('auth/resend.html')

@auth_bp.route('/resend', methods=['POST'])
def resend_confirmation_post():
    email = request.form.get('email')
    
    if not email:
        flash('Por favor, informe seu e-mail.', 'danger')
        return redirect(url_for('auth.resend_confirmation'))
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        flash('Não encontramos uma conta com este e-mail.', 'danger')
        return redirect(url_for('auth.resend_confirmation'))
    
    if user.email_verified:
        flash('Sua conta já foi confirmada. Por favor, faça login.', 'info')
        return redirect(url_for('auth.login'))
    
    # Gerar token e URL de confirmação
    token = generate_confirmation_token(email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    
    try:
        # Enviar e-mail de confirmação
        msg = Message(
            'Confirme seu cadastro - HebraicoFacil',
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[email]
        )
        msg.body = f'''Olá {user.name},

Para confirmar seu e-mail, clique no link abaixo:

{confirm_url}

Se você não solicitou este cadastro, ignore este e-mail.

Atenciosamente,
Equipe HebraicoFacil
'''
        mail.send(msg)
        flash('Um novo e-mail de confirmação foi enviado. Por favor, verifique sua caixa de entrada.', 'info')
    except Exception as e:
        # Em caso de erro no envio do e-mail, fornecer o link diretamente
        flash(f'Não foi possível enviar o e-mail de confirmação. Por favor, use este link para confirmar sua conta: {confirm_url}', 'warning')
    
    return redirect(url_for('auth.login'))

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        if current_user.role == 'a':
            return redirect(url_for('admin.admin_dashboard'))
        elif current_user.role == 's':
            return redirect(url_for('lessons.teacher_dashboard'))
        return redirect(url_for('lessons.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        
        if not email:
            flash('Por favor, informe seu e-mail.', 'danger')
            return render_template('auth/reset_password.html')
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('Não encontramos uma conta com este e-mail.', 'danger')
            return render_template('auth/reset_password.html')
        
        # Gerar token e URL de redefinição
        token = generate_confirmation_token(email)
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        
        try:
            # Enviar e-mail de redefinição de senha
            msg = Message(
                'Redefinição de Senha - HebraicoFacil',
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[email]
            )
            msg.body = f'''Olá {user.name},

Para redefinir sua senha, clique no link abaixo:

{reset_url}

Se você não solicitou a redefinição de senha, ignore este e-mail.

Atenciosamente,
Equipe HebraicoFacil
'''
            mail.send(msg)
            flash('Um e-mail com instruções para redefinir sua senha foi enviado. Por favor, verifique sua caixa de entrada.', 'info')
        except Exception as e:
            # Em caso de erro no envio do e-mail, fornecer o link diretamente
            flash(f'Não foi possível enviar o e-mail de redefinição. Por favor, use este link para redefinir sua senha: {reset_url}', 'warning')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        if current_user.role == 'a':
            return redirect(url_for('admin.admin_dashboard'))
        elif current_user.role == 's':
            return redirect(url_for('lessons.teacher_dashboard'))
        return redirect(url_for('lessons.dashboard'))
    
    email = confirm_token(token)
    
    if not email:
        flash('O link de redefinição de senha é inválido ou expirou.', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not password or not confirm_password:
            flash('Por favor, preencha todos os campos.', 'danger')
            return render_template('auth/reset_password_form.html', token=token)
        
        if password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return render_template('auth/reset_password_form.html', token=token)
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('Usuário não encontrado.', 'danger')
            return redirect(url_for('auth.login'))
        
        user.password = hash_password(password)
        db.session.commit()
        
        flash('Sua senha foi redefinida com sucesso! Agora você pode fazer login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password_form.html', token=token)

@auth_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        cep = request.form.get('cep')
        phone_number = request.form.get('phone_number')
        country = request.form.get('country')
        state = request.form.get('state')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validações básicas
        if not all([name, address, cep, phone_number, country, state]):
            flash('Os campos de nome, endereço, CEP, telefone, país e estado são obrigatórios.', 'danger')
            return redirect(url_for('auth.account'))
        
        if not validate_cep(cep):
            flash('CEP inválido.', 'danger')
            return redirect(url_for('auth.account'))
        
        if not validate_phone(phone_number):
            flash('Número de telefone inválido. Use o formato correto para o país selecionado.', 'danger')
            return redirect(url_for('auth.account'))
        
        # Atualizar informações básicas
        current_user.name = name
        current_user.address = address
        current_user.cep = cep.replace('-', '')
        current_user.phone_number = phone_number
        current_user.country = country
        current_user.state = state
        
        # Atualizar senha se fornecida
        if current_password and new_password and confirm_password:
            if not check_password(current_user.password, current_password):
                flash('Senha atual incorreta.', 'danger')
                return redirect(url_for('auth.account'))
            
            if new_password != confirm_password:
                flash('As novas senhas não coincidem.', 'danger')
                return redirect(url_for('auth.account'))
            
            current_user.password = hash_password(new_password)
        
        db.session.commit()
        flash('Suas informações foram atualizadas com sucesso!', 'success')
        return redirect(url_for('auth.account'))
    
    return render_template('auth/account.html')