from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user

from .. import db
from .models import Module, TestResult
from .utils import get_hebrew_mappings, parse_module_data, get_character_info, calculate_progress
from ..auth.models import Progress
from ..payments.models import Payment

from . import lessons_bp

def is_student_or_teacher(user):
    return user.role in ['n', 's', 't']

@lessons_bp.route('/dashboard')
@login_required
def dashboard():
    """Página principal do aluno após login."""
    if not is_student_or_teacher(current_user):
        if current_user.role == 'a':
            return redirect(url_for('admin.admin_dashboard'))
        flash('Acesso restrito a alunos e professores.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Verificar se o usuário precisa de pagamento (apenas alunos)
    has_payment = True  # Professores e admins têm acesso total por padrão
    if current_user.role == 'n':  # Apenas alunos precisam de pagamento
        payment = Payment.query.filter_by(user_id=current_user.id).filter(
            Payment.payment_status.in_(['paid', 'authorized'])
        ).first()
        has_payment = bool(payment)
    
    # Buscar todos os módulos
    modules = Module.query.order_by(Module.module_number).all()
    
    # Filtrar módulos visíveis
    if has_payment:
        visible_modules = [parse_module_data(m) for m in modules if m.visible]
    else:
        visible_modules = []  # Não mostrar módulos se não houver pagamento
        if current_user.role == 'n':
            flash('Para acessar os módulos do curso, é necessário realizar o pagamento.', 'warning')
    
    # Verificar progresso do usuário
    progress = Progress.query.filter_by(user_id=current_user.id).first()
    if not progress:
        progress = Progress(user_id=current_user.id)
        db.session.add(progress)
        db.session.commit()
    
    # Calcular o progresso com base nos resultados dos testes
    progress_percentage = calculate_progress(current_user.id)
    
    return render_template('lessons/dashboard.html', 
                          modules=visible_modules, 
                          progress=progress, 
                          has_payment=has_payment,
                          current_user=current_user,
                          progress_percentage=progress_percentage)

@lessons_bp.route('/teacher_dashboard')
@login_required
def teacher_dashboard():
    """Página principal do professor após login."""
    if current_user.role != 's':
        flash('Acesso restrito a professores.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Buscar todos os módulos para o professor gerenciar
    modules = Module.query.order_by(Module.module_number).all()
    visible_modules = [parse_module_data(m) for m in modules if m.visible]
    
    # Exemplo de dados para o professor (pode ser expandido)
    from ..auth.models import User
    students = User.query.filter_by(role='n').all()  # Lista de alunos
    student_count = len(students)
    
    return render_template('lessons/teacher_dashboard.html', 
                          modules=visible_modules, 
                          students=students, 
                          student_count=student_count)

@lessons_bp.route('/module/<int:module_id>')
@login_required
def module_view(module_id):
    """Visualização de um módulo específico."""
    if not is_student_or_teacher(current_user):
        if current_user.role == 'a':
            return redirect(url_for('admin.admin_dashboard'))
        flash('Acesso restrito a alunos e professores.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Verificar se o usuário precisa de pagamento (apenas alunos)
    has_payment = True  # Professores e admins têm acesso total por padrão
    if current_user.role == 'n':  # Apenas alunos precisam de pagamento
        payment = Payment.query.filter_by(user_id=current_user.id).filter(
            Payment.payment_status.in_(['paid', 'authorized'])
        ).first()
        has_payment = bool(payment)
    
    module = Module.query.filter_by(id=module_id).first_or_404()
    
    # Verificar se o módulo está visível
    if not module.visible:
        flash('Este módulo ainda não está disponível.', 'warning')
        return redirect(url_for('lessons.dashboard'))
    
    # Verificar se o usuário tem acesso a este módulo
    if not has_payment and current_user.role == 'n':
        flash('Para acessar este módulo, é necessário realizar o pagamento.', 'warning')
        return redirect(url_for('payments.payment'))  # Redireciona para a página de pagamento
    
    module_data = parse_module_data(module)
    
    # Obter mapeamentos hebraicos
    hebrew_mappings = get_hebrew_mappings()
    
    return render_template('lessons/module.html', 
                          module=module_data, 
                          hebrew_mappings=hebrew_mappings,
                          has_payment=has_payment)

@lessons_bp.route('/lesson/<int:module_id>/<lesson_type>')
@login_required
def lesson(module_id, lesson_type):
    """Visualização de uma lição específica (consoantes, vogais ou sílabas)."""
    if not is_student_or_teacher(current_user):
        if current_user.role == 'a':
            return redirect(url_for('admin.admin_dashboard'))
        flash('Acesso restrito a alunos e professores.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Verificar se o usuário precisa de pagamento (apenas alunos)
    has_payment = True  # Professores e admins têm acesso total por padrão
    if current_user.role == 'n':  # Apenas alunos precisam de pagamento
        payment = Payment.query.filter_by(user_id=current_user.id).filter(
            Payment.payment_status.in_(['paid', 'authorized'])
        ).first()
        has_payment = bool(payment)
    
    module = Module.query.filter_by(id=module_id).first_or_404()
    
    # Verificar se o módulo está visível
    if not module.visible:
        flash('Este módulo ainda não está disponível.', 'warning')
        return redirect(url_for('lessons.dashboard'))
    
    # Verificar se o usuário tem acesso a este módulo
    if not has_payment and current_user.role == 'n':
        flash('Para acessar este módulo, é necessário realizar o pagamento.', 'warning')
        return redirect(url_for('payments.payment'))  # Redireciona para a página de pagamento
    
    module_data = parse_module_data(module)
    
    # Verificar tipo de lição
    if lesson_type not in ['consonants', 'vowels', 'syllables']:
        flash('Tipo de lição inválido.', 'danger')
        return redirect(url_for('lessons.module_view', module_id=module_id))
    
    # Obter mapeamentos hebraicos
    hebrew_mappings = get_hebrew_mappings()
    
    # Preparar dados da lição
    lesson_data = {
        'type': lesson_type,
        'module': module_data,
        'characters': []
    }
    
    if lesson_type == 'consonants':
        for char in module_data['consonants']:
            info = get_character_info(char)
            if info:
                # Garantir que 'caractere' esteja presente
                info_with_char = {'caractere': char, **info}
                lesson_data['characters'].append(info_with_char)
    
    elif lesson_type == 'vowels':
        for char in module_data['vowels']:
            info = get_character_info(char)
            if info:
                # Garantir que 'caractere' esteja presente
                info_with_char = {'caractere': char, **info}
                lesson_data['characters'].append(info_with_char)
    
    elif lesson_type == 'syllables':
        for syllable in module_data['syllables']:
            info = get_character_info(syllable)
            if info:
                # Garantir que 'caractere' esteja presente
                info_with_char = {'caractere': syllable, **info}
                lesson_data['characters'].append(info_with_char)
    
    return render_template('lessons/lesson.html', 
                          lesson=lesson_data, 
                          hebrew_mappings=hebrew_mappings,
                          has_payment=has_payment)

@lessons_bp.route('/test/<int:module_id>/<lesson_type>')
@login_required
def test_lesson(module_id, lesson_type):
    """Teste de conhecimento para uma lição específica."""
    if not is_student_or_teacher(current_user):
        if current_user.role == 'a':
            return redirect(url_for('admin.admin_dashboard'))
        flash('Acesso restrito a alunos e professores.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Verificar se o usuário precisa de pagamento (apenas alunos)
    has_payment = True  # Professores e admins têm acesso total por padrão
    if current_user.role == 'n':  # Apenas alunos precisam de pagamento
        payment = Payment.query.filter_by(user_id=current_user.id).filter(
            Payment.payment_status.in_(['paid', 'authorized'])
        ).first()
        has_payment = bool(payment)
    
    module = Module.query.filter_by(id=module_id).first_or_404()
    
    # Verificar se o módulo está visível
    if not module.visible:
        flash('Este módulo ainda não está disponível.', 'warning')
        return redirect(url_for('lessons.dashboard'))
    
    # Verificar se o usuário tem acesso a este módulo
    if not has_payment and current_user.role == 'n':
        flash('Para acessar este módulo, é necessário realizar o pagamento.', 'warning')
        return redirect(url_for('payments.payment'))  # Redireciona para a página de pagamento
    
    module_data = parse_module_data(module)
    
    # Verificar tipo de lição
    if lesson_type not in ['consonants', 'vowels', 'syllables']:
        flash('Tipo de lição inválido.', 'danger')
        return redirect(url_for('lessons.module_view', module_id=module_id))
    
    # Preparar dados do teste
    test_data = {
        'type': lesson_type,
        'module': module_data,
        'questions': []
    }
    
    # Obter mapeamentos hebraicos
    hebrew_mappings = get_hebrew_mappings()
    
    # Determinar os itens e a categoria com base no tipo de lição
    if lesson_type == 'consonants':
        items = module_data['consonants']
        category = 'consoantes'
    elif lesson_type == 'vowels':
        items = module_data['vowels']
        category = 'vogais'
    else:  # syllables
        items = module_data['syllables']
        category = None  # Sílabas têm seu próprio mapeamento (HEBREW_SYLLABLES)
    
    if not items:
        flash('Nenhum item disponível para este teste.', 'warning')
        return redirect(url_for('lessons.module_view', module_id=module_id))
    
    # Gerar perguntas com base no tipo de lição
    if lesson_type in ['consonants', 'vowels']:
        # Obter todas as transliterações disponíveis na categoria
        all_transliterations = []
        for item in items:
            info = get_character_info(item)
            if info and info['transliteracao']:
                all_transliterations.extend(info['transliteracao'])
        all_transliterations = list(set(all_transliterations))  # Remover duplicatas
        
        for char in items:
            info = get_character_info(char)
            if not info or not info['transliteracao']:
                continue  # Pular se não houver informações ou transliterações
            
            # Combinar todas as transliterações válidas em uma única string
            correct_translit = ' ou '.join(info['transliteracao'])  # Ex.: 'm ou m normal'
            
            # Gerar opções incorretas a partir das outras transliterações
            incorrect_options = [t for t in all_transliterations if t not in info['transliteracao']]
            incorrect_options = incorrect_options[:3]  # Pegar até 3 opções incorretas
            
            # Se não houver opções suficientes, preencher com transliterações genéricas
            while len(incorrect_options) < 3:
                incorrect_options.append('nada')  # Fallback para evitar erros
            
            # Combinar a resposta correta com as incorretas
            options = incorrect_options + [correct_translit]
            import random
            random.shuffle(options)
            
            test_data['questions'].append({
                'character': char,
                'options': options,
                'correct': correct_translit,
                'valid_transliterations': info['transliteracao']
            })
    
    elif lesson_type == 'syllables':
        # Obter todas as transliterações disponíveis para as sílabas do módulo
        all_transliterations = []
        for syllable in items:
            info = get_character_info(syllable)
            if info and info['transliteracao']:
                all_transliterations.extend(info['transliteracao'])
        all_transliterations = list(set(all_transliterations))  # Remover duplicatas
        
        for syllable in items:
            info = get_character_info(syllable)
            if not info or not info['transliteracao']:
                continue  # Pular se não houver informações ou transliterações
            
            # Combinar todas as transliterações válidas
            correct_translit = ' ou '.join(info['transliteracao'])
            
            # Gerar opções incorretas a partir das outras transliterações
            incorrect_options = [t for t in all_transliterations if t not in info['transliteracao']]
            incorrect_options = incorrect_options[:3]  # Pegar até 3 opções incorretas
            
            # Se não houver opções suficientes, preencher com transliterações genéricas
            while len(incorrect_options) < 3:
                incorrect_options.append('---')  # Fallback para sílabas
            
            # Combinar a resposta correta com as incorretas
            options = incorrect_options + [correct_translit]
            import random
            random.shuffle(options)
            
            test_data['questions'].append({
                'character': syllable,
                'options': options,
                'correct': correct_translit,
                'valid_transliterations': info['transliteracao']
            })
    
    if not test_data['questions']:
        flash('Não foi possível gerar perguntas para este teste.', 'warning')
        return redirect(url_for('lessons.module_view', module_id=module_id))
    
    return render_template('lessons/test_lesson.html', test=test_data, has_payment=has_payment)

@lessons_bp.route('/complete_test', methods=['POST'])
@login_required
def complete_test():
    """Processar a conclusão de um teste e salvar os resultados."""
    if not is_student_or_teacher(current_user):
        if current_user.role == 'a':
            return redirect(url_for('admin.admin_dashboard'))
        flash('Acesso restrito a alunos e professores.', 'danger')
        return redirect(url_for('auth.login'))
    
    data = request.get_json()
    #print("Dados recebidos:", data)
    
    #print(f"Usuário atual - ID: {current_user.id}, Role: {current_user.role}")
    
    if not data:
        #print("Erro: Dados inválidos - data é None")
        return jsonify({'success': False, 'message': 'Dados inválidos'}), 400
    
    module_id = data.get('module_id')
    lesson_type = data.get('lesson_type')
    correct_answers = data.get('correct_answers')  # Número de respostas corretas
    total_questions = data.get('total_questions')  # Total de questões no teste
    
    #print(f"module_id: {module_id}, lesson_type: {lesson_type}, correct_answers: {correct_answers}, total_questions: {total_questions}")
    
    if not module_id or not lesson_type or correct_answers is None or total_questions is None:
        #print("Erro: Dados incompletos")
        return jsonify({'success': False, 'message': 'Dados incompletos'}), 400
    
    module = Module.query.filter_by(id=module_id).first()
    if not module:
        #print(f"Erro: Módulo não encontrado - module_id: {module_id}")
        return jsonify({'success': False, 'message': 'Módulo não encontrado'}), 404
    
    # Buscar ou criar um registro de resultado do teste
    test_result = TestResult.query.filter_by(
        user_id=current_user.id,
        module_id=module_id,
        test_type=lesson_type
    ).first()

    if test_result:
        # Atualizar o resultado existente
        test_result.correct_answers = int(correct_answers)
        test_result.total_questions = int(total_questions)
    else:
        # Criar um novo resultado
        test_result = TestResult(
            user_id=current_user.id,
            module_id=module_id,
            test_type=lesson_type,
            correct_answers=int(correct_answers),
            total_questions=int(total_questions)
        )
        db.session.add(test_result)
    
    try:
        db.session.commit()
        #print("Resultado do teste salvo com sucesso")
    except Exception as e:
        #print(f"Erro ao salvar no banco de dados: {str(e)}")
        return jsonify({'success': False, 'message': 'Erro ao salvar resultado no banco de dados'}), 500
    
    # Calcular o novo progresso
    progress_percentage = calculate_progress(current_user.id)
    
    return jsonify({
        'success': True,
        'progress_percentage': progress_percentage
    })

def init_modules():
    """Inicializa os módulos no banco de dados."""
    from .utils import init_modules_data
    
    modules_data = init_modules_data()
    
    # Criar módulos apenas se não existirem
    for data in modules_data:
        if not Module.query.filter_by(module_number=data['module_number']).first():
            module = Module(
                module_number=data['module_number'],
                hebrew_text=data['hebrew_text'],
                consonants=data['consonants'],
                vowels=data['vowels'],
                syllables=data['syllables'],
                visible=True  # Tornar todos os módulos visíveis por padrão
            )
            db.session.add(module)
    
    db.session.commit()