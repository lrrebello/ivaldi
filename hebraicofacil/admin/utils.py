def is_admin(user):
    """Verifica se o usuário é um administrador."""
    return user.role == 'a'

def is_teacher(user):
    """Verifica se o usuário é um professor."""
    return user.role == 's'

def format_user_role(role):
    """Formata o papel do usuário para exibição."""
    roles = {
        'a': 'Administrador',
        's': 'Professor',
        'n': 'Aluno'
    }
    return roles.get(role, 'Desconhecido')

def get_user_count_by_role():
    """Retorna a contagem de usuários por papel."""
    from ..auth.models import User
    
    admin_count = User.query.filter_by(role='a').count()
    teacher_count = User.query.filter_by(role='s').count()
    student_count = User.query.filter_by(role='n').count()
    
    return {
        'admin': admin_count,
        'teacher': teacher_count,
        'student': student_count,
        'total': admin_count + teacher_count + student_count
    }

def get_payment_stats():
    """Retorna estatísticas de pagamentos."""
    from ..payments.models import Payment
    
    total_payments = Payment.query.count()
    successful_payments = Payment.query.filter(Payment.payment_status.in_(['paid', 'authorized'])).count()
    pending_payments = Payment.query.filter(Payment.payment_status.in_(['pending', 'processing', 'waiting_payment'])).count()
    failed_payments = Payment.query.filter(Payment.payment_status.in_(['refused', 'chargedback'])).count()
    
    return {
        'total': total_payments,
        'successful': successful_payments,
        'pending': pending_payments,
        'failed': failed_payments
    }
