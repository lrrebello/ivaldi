import re
from datetime import datetime

def validate_card_number(card_number):
    """Valida um número de cartão de crédito."""
    card_number = ''.join(filter(str.isdigit, card_number))
    return len(card_number) == 16

def validate_expiry(card_expiry):
    """Valida a data de expiração de um cartão de crédito."""
    try:
        month, year = map(int, card_expiry.split('/'))
        if not (1 <= month <= 12):
            return False
        current_year = datetime.today().year % 100
        current_month = datetime.today().month
        if year < current_year or (year == current_year and month < current_month):
            return False
        return True
    except (ValueError, AttributeError):
        return False

def validate_cvv(cvv):
    """Valida o código de segurança de um cartão de crédito."""
    cvv = ''.join(filter(str.isdigit, cvv))
    return len(cvv) in (3, 4)

def format_amount(amount):
    """Formata o valor para o formato aceito pela API de pagamento."""
    return int(float(amount) * 100)

def format_card_data(card_number, card_holder, card_expiry, card_cvv):
    """Formata os dados do cartão para o formato aceito pela API de pagamento."""
    card_number = ''.join(filter(str.isdigit, card_number))
    month, year = map(int, card_expiry.split('/'))
    
    return {
        'card_number': card_number,
        'card_holder_name': card_holder,
        'card_expiration_date': f'{month:02d}{year:02d}',
        'card_cvv': card_cvv
    }

def get_payment_status_display(status):
    """Retorna o status de pagamento em formato legível."""
    status_map = {
        'pending': 'Pendente',
        'processing': 'Processando',
        'authorized': 'Autorizado',
        'paid': 'Pago',
        'refunded': 'Reembolsado',
        'waiting_payment': 'Aguardando pagamento',
        'refused': 'Recusado',
        'chargedback': 'Estornado',
        'analyzing': 'Em análise',
        'pending_refund': 'Reembolso pendente'
    }
    return status_map.get(status, status)