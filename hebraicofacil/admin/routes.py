from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
import secrets
from .. import db
from ..auth.models import GameConfig  # Adicionando a importação de GameConfig
from . import admin_bp
from .utils import is_admin, is_teacher, format_user_role, get_user_count_by_role, get_payment_stats
from ..payments.models import CoursePrice  # Importar CoursePrice de payments.models

# Decorator personalizado para verificar se o usuário é administrador
def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not is_admin(current_user):
            flash('Acesso restrito a administradores.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Decorator personalizado para verificar se o usuário é professor
def teacher_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not is_teacher(current_user) and not is_admin(current_user):
            flash('Acesso restrito a professores e administradores.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/manage_users')
@admin_required
def manage_users():
    """Página de gerenciamento de usuários (apenas para administradores)."""
    from ..auth.models import User
    from .. import db
    
    users = User.query.all()
    user_stats = get_user_count_by_role()
    payment_stats = get_payment_stats()
    
    return render_template('admin/manage_users.html', 
                          users=users, 
                          format_user_role=format_user_role,
                          user_stats=user_stats,
                          payment_stats=payment_stats)

@admin_bp.route('/user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """Editar informações de um usuário (apenas para administradores)."""
    from ..auth.models import User
    from ..payments.models import Payment
    from .. import db
    
    user = User.query.get_or_404(user_id)
    payment = Payment.query.filter_by(user_id=user.id).first()  # Busca o pagamento associado, se existir
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        role = request.form.get('role')
        is_active = 'is_active' in request.form
        mark_as_paid = 'mark_as_paid' in request.form  # Novo campo do formulário
        
        # Validações básicas
        if not all([name, email, role]):
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('admin.edit_user', user_id=user_id))
        
        # Verificar se o e-mail já está em uso por outro usuário
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != user.id:
            flash('Este e-mail já está em uso por outro usuário.', 'danger')
            return redirect(url_for('admin.edit_user', user_id=user_id))
        
        # Atualizar informações do usuário
        user.name = name
        user.email = email
        user.role = role
        user.is_active = is_active
        
        # Se "Marcar como Pago" foi selecionado, criar ou atualizar o registro de pagamento
        if mark_as_paid:
            if payment:
                # Se já existe um pagamento, apenas atualiza o status
                payment.payment_status = 'paid'
                payment.payment_method = 'administrador'
                db.session.add(payment)
                flash('Usuário marcado como pago com sucesso!', 'success')
            else:
                # Se não existe, cria um novo registro
                new_payment = Payment(
                    user_id=user.id,
                    amount=0.0,  # Valor padrão para amount
                    payment_method='administrador',
                    payment_status='paid'
                )
                db.session.add(new_payment)
                flash('Novo pagamento criado e usuário marcado como pago com sucesso!', 'success')
        
        db.session.commit()
        flash('Informações do usuário atualizadas com sucesso!', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin/edit_user.html', user=user, payment=payment)

@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Excluir um usuário (apenas para administradores)."""
    from ..auth.models import User, Progress
    from ..payments.models import Payment
    from .. import db
    
    user = User.query.get_or_404(user_id)
    
    # Não permitir que um administrador exclua a si mesmo
    if user.id == current_user.id:
        flash('Você não pode excluir sua própria conta.', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    # Excluir progresso e pagamentos associados
    Progress.query.filter_by(user_id=user.id).delete()
    Payment.query.filter_by(user_id=user.id).delete()
    
    db.session.delete(user)
    db.session.commit()
    
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/manage_modules')
@teacher_required
def manage_modules():
    """Página de gerenciamento de módulos (para professores e administradores)."""
    from ..lessons.models import Module
    
    modules = Module.query.order_by(Module.module_number).all()
    return render_template('admin/manage_modules.html', modules=modules)

@admin_bp.route('/module/<int:module_id>', methods=['GET', 'POST'])
@teacher_required
def edit_module(module_id):
    """Editar informações de um módulo (para professores e administradores)."""
    from ..lessons.models import Module
    from .. import db
    
    module = Module.query.get_or_404(module_id)
    
    if request.method == 'POST':
        hebrew_text = request.form.get('hebrew_text')
        consonants = request.form.get('consonants')
        vowels = request.form.get('vowels')
        syllables = request.form.get('syllables')
        visible = 'visible' in request.form
        
        # Validações básicas
        if not hebrew_text:
            flash('Por favor, forneça o texto hebraico.', 'danger')
            return redirect(url_for('admin.edit_module', module_id=module_id))
        
        # Atualizar informações do módulo
        module.hebrew_text = hebrew_text
        module.consonants = consonants
        module.vowels = vowels
        module.syllables = syllables
        module.visible = visible
        
        db.session.commit()
        flash('Informações do módulo atualizadas com sucesso!', 'success')
        return redirect(url_for('admin.manage_modules'))
    
    return render_template('admin/edit_module.html', module=module)

@admin_bp.route('/create_user', methods=['GET', 'POST'])
@admin_required
def create_user():
    """Criar um novo usuário (apenas para administradores)."""
    from ..auth.models import User, Progress
    from ..auth.utils import hash_password
    from .. import db
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        role = request.form.get('role')
        cpf = request.form.get('cpf')
        birth_date = request.form.get('birth_date')
        address = request.form.get('address')
        cep = request.form.get('cep')
        phone_number = request.form.get('phone_number')
        
        # Validações básicas
        if not all([name, email, role, cpf, birth_date, address, cep, phone_number]):
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('admin.create_user'))
        
        # Verificar se o e-mail já está em uso
        if User.query.filter_by(email=email).first():
            flash('Este e-mail já está em uso.', 'danger')
            return redirect(url_for('admin.create_user'))
        
        # Verificar se o CPF já está em uso
        if User.query.filter_by(cpf=cpf.replace('.', '').replace('-', '')).first():
            flash('Este CPF já está em uso.', 'danger')
            return redirect(url_for('admin.create_user'))
        
        # Gerar senha aleatória
        password = secrets.token_urlsafe(8)
        
        # Criar novo usuário
        new_user = User(
            name=name,
            email=email,
            password=hash_password(password),
            role=role,
            cpf=cpf.replace('.', '').replace('-', ''),
            birth_date=birth_date,
            address=address,
            cep=cep.replace('-', ''),
            phone_number=phone_number,
            email_verified=True,
            is_active=True
        )
        
        # Primeiro adicionar e fazer commit do usuário para obter o ID
        db.session.add(new_user)
        db.session.commit()
        
        # Agora criar o progresso usando o ID do usuário
        new_progress = Progress(user_id=new_user.id)
        db.session.add(new_progress)
        db.session.commit()
        
        flash(f'Usuário criado com sucesso! Senha temporária: {password}', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin/create_user.html')

@admin_bp.route('/dashboard')
@admin_required
def admin_dashboard():
    """Painel de controle administrativo."""
    from ..auth.models import User
    from ..payments.models import Payment
    
    user_stats = get_user_count_by_role()
    payment_stats = get_payment_stats()
    
    recent_users = User.query.order_by(User.id.desc()).limit(5).all()
    recent_payments = Payment.query.order_by(Payment.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                          user_stats=user_stats,
                          payment_stats=payment_stats,
                          recent_users=recent_users,
                          recent_payments=recent_payments,
                          format_user_role=format_user_role)

@admin_bp.route('/manage_course_price', methods=['GET', 'POST'])
@admin_required
def manage_course_price():
    """Gerenciar o preço do curso (apenas para administradores)."""
    from .. import db
    
    course_price = CoursePrice.query.first()
    
    # Se não existe um preço configurado, criar um com valor padrão
    if not course_price:
        course_price = CoursePrice(price=29.90)
        db.session.add(course_price)
        db.session.commit()
    
    if request.method == 'POST':
        try:
            price = float(request.form.get('price'))
            if price <= 0:
                flash('O preço deve ser maior que zero.', 'danger')
                return redirect(url_for('admin.manage_course_price'))
            
            course_price.price = price
            db.session.commit()
            flash('Preço do curso atualizado com sucesso!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except ValueError:
            flash('Por favor, insira um valor numérico válido.', 'danger')
            return redirect(url_for('admin.manage_course_price'))
    
    return render_template('admin/manage_course_price.html', course_price=course_price)

@admin_bp.route('/toggle_game_visibility', methods=['POST'])
@login_required
def toggle_game_visibility():
    if current_user.role not in ['s', 'a']:
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('index'))
    
    game_config = GameConfig.query.first()
    if not game_config:
        game_config = GameConfig(visible=False)
        db.session.add(game_config)
    
    game_config.visible = not game_config.visible
    db.session.commit()
    
    flash(f"Jogo do Alfabeto agora está {'visível' if game_config.visible else 'oculto'}.", 'success')
    return redirect(url_for('admin.manage_modules'))