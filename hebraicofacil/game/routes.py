from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from flask_login import login_required
import random
import logging
from datetime import timedelta, datetime

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s [%(levelname)s] %(message)s',
)
logger = logging.getLogger(__name__)

alfabeto_hebraico = {
    "א": {"nome": "Aleph", "translit": "nada"},
    "בּ": {"nome": "Bet com dagesh", "translit": "b"},
    "ב": {"nome": "Vet", "translit": "v"},
    "גּ": {"nome": "Gimel com dagesh", "translit": "g"},
    "ג": {"nome": "Gimel", "translit": "g (leve)"},
    "דּ": {"nome": "Dalet com dagesh", "translit": "d"},
    "ד": {"nome": "Dalet", "translit": "d (leve)"},
    "ה": {"nome": "He", "translit": "h"},
    "ו": {"nome": "Vav", "translit": ["v", "w"]},
    "וּ": {"nome": "Vav com dagesh", "translit": "u"},
    "וֹ": {"nome": "Vav com Holam", "translit": "o"},
    "ז": {"nome": "Zayin", "translit": "z"},
    "ח": {"nome": "Het", "translit": ["ch", "rrr"]},
    "ט": {"nome": "Tet", "translit": "t"},
    "י": {"nome": "Yod", "translit": "y"},
    "כּ": {"nome": "Kaf com dagesh", "translit": "k"},
    "כ": {"nome": "Khaf", "translit": ["kh", "rrr"]},
    "ך": {"nome": "Khaf sofit", "translit": "ch final"},
    "ל": {"nome": "Lamed", "translit": "l"},
    "מ": {"nome": "Mem", "translit": ["m", "m normal"]},
    "ם": {"nome": "Mem sofit", "translit": "m final"},
    "נ": {"nome": "Nun", "translit": "n"},
    "ן": {"nome": "Nun sofit", "translit": "n final"},
    "ס": {"nome": "Samekh", "translit": "s"},
    "ע": {"nome": "Ayin", "translit": "nada"},
    "פּ": {"nome": "Pe com dagesh", "translit": "p"},
    "פ": {"nome": "Fe", "translit": "f"},
    "ף": {"nome": "Fe sofit", "translit": "f final"},
    "צ": {"nome": "Tsade", "translit": "ts"},
    "ץ": {"nome": "Tsade sofit", "translit": "ts final"},
    "ק": {"nome": "Qof", "translit": "q"},
    "ר": {"nome": "Resh", "translit": "r"},
    "שׁ": {"nome": "Shin", "translit": "sh"},
    "שׂ": {"nome": "Sin", "translit": "s"},
    "תּ": {"nome": "Tav com dagesh", "translit": "t"},
    "ת": {"nome": "Tav", "translit": "t (leve)"},
    "ַ": {"nome": "Patach", "translit": "a"},
    "ָ": {"nome": "Kamatz", "translit": "a"},
    "ֵ": {"nome": "Tsere", "translit": "e"},
    "ֶ": {"nome": "Segol", "translit": "e"},
    "ִ": {"nome": "Hirik", "translit": "i"},
    "ְ": {"nome": "Shva", "translit": "e (leve)"}
}

game_bp = Blueprint('game', __name__, template_folder='templates')

def initialize_session():
    if 'letters' not in session:
        session.permanent = True
        session['letters'] = list(alfabeto_hebraico.keys())
        random.shuffle(session['letters'])
        session['pending_letters'] = session['letters'].copy()
        session['index'] = 0
        session['errors'] = {letra: 0 for letra in session['letters']}
        session['feedback'] = None
        session['is_correct'] = None
        session['show_next'] = False
        session['show_skip'] = False
        session['start_time'] = datetime.now().timestamp()
        session['retry_mode'] = False
        session['paused_time'] = 0
        session['is_paused'] = False
        session['pause_start'] = None
        session.modified = True

@game_bp.route('/')
@login_required
def index():
    try:
        initialize_session()
        if not session['pending_letters']:
            sorted_errors = sorted(
                session['errors'].items(),
                key=lambda x: (-x[1], x[0])
            )
            errors_list = "\n".join([
                f"{letra} ({alfabeto_hebraico[letra]['nome']}): {count} erro(s)"
                for letra, count in sorted_errors if count > 0
            ])
            start_time = session.get('start_time', datetime.now().timestamp())
            paused_time = session.get('paused_time', 0)
            total_seconds = int(datetime.now().timestamp() - start_time - paused_time)
            total_time = f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}:{total_seconds % 60:02d}"
            session['final_message'] = (
                f"Você completou o alfabeto hebraico!\n"
                f"Tempo ativo: {total_time}\n\n"
                f"Erros cometidos:\n{errors_list if errors_list else 'Nenhum erro!'}"
            )
            has_errors = any(count > 0 for count in session['errors'].values())
            if session.get('retry_mode', False):
                for letra in session['letters']:
                    if letra not in session['pending_letters']:
                        session['errors'][letra] = 0
                session['retry_mode'] = False
                has_errors = any(count > 0 for count in session['errors'].values())
            session.modified = True
            return render_template('game/complete.html', message=session['final_message'], has_errors=has_errors)

        if session['index'] >= len(session['pending_letters']):
            session['index'] = 0
        current_letter = session['pending_letters'][session['index']]
        start_time = session.get('start_time', datetime.now().timestamp())
        paused_time = session.get('paused_time', 0)
        is_paused = session.get('is_paused', False)
        return render_template('game/index.html',
                            current_letter=current_letter,
                            feedback=session.get('feedback'),
                            show_next=session.get('show_next', False),
                            show_skip=session.get('show_skip', False),
                            start_time=start_time,
                            paused_time=paused_time,
                            is_paused=is_paused)
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        return redirect(url_for('game.index'))

@game_bp.route('/verify', methods=['POST'])
@login_required
def verify():
    try:
        initialize_session()
        if not session['pending_letters'] or session['index'] >= len(session['pending_letters']):
            logger.warning("Invalid session state: pending_letters empty or index out of range")
            session['index'] = 0
            session['pending_letters'] = session['letters'].copy() if not session['pending_letters'] else session['pending_letters']
            session.modified = True
        current_index = session['index']
        current_letter = session['pending_letters'][current_index]
        
        answer = request.form.get('answer', '').strip().lower()
        if not answer:
            session['feedback'] = "Por favor, digite uma resposta!"
            session['is_correct'] = False
            session['show_next'] = False
            session['show_skip'] = True
            if session.get('is_paused', False):
                pause_duration = datetime.now().timestamp() - session.get('pause_start', datetime.now().timestamp())
                session['paused_time'] = session.get('paused_time', 0) + pause_duration
                session['is_paused'] = False
                session['pause_start'] = None
            session.modified = True
            return jsonify({
                'feedback': session['feedback'],
                'is_correct': session['is_correct'],
                'show_next': session['show_next'],
                'show_skip': session['show_skip'],
                'current_letter': current_letter,
                'is_paused': session['is_paused']
            })

        translit_correct = alfabeto_hebraico[current_letter]["translit"]
        is_correct = False

        def normalize_translit(text):
            return text.replace('(', '').replace(')', '').replace('  ', ' ').strip()

        if isinstance(translit_correct, list):
            is_correct = any(answer == ans.lower() for ans in translit_correct)
        else:
            normalized_answer = normalize_translit(answer)
            translit_lower = translit_correct.lower()
            if "final" in translit_lower:
                normalized_translit = normalize_translit(translit_lower)
                is_correct = normalized_answer == normalized_translit
            else:
                normalized_translit = normalize_translit(translit_lower)
                if "leve" in normalized_translit:
                    normalized_translit = normalized_translit.replace("leve", "").strip()
                is_correct = normalized_answer == normalized_translit

        if is_correct:
            session['feedback'] = f"Correto! Essa é a letra {alfabeto_hebraico[current_letter]['nome']}"
            session['is_correct'] = True
            session['show_next'] = True
            session['show_skip'] = False
            if not session.get('is_paused', False):
                session['is_paused'] = True
                session['pause_start'] = datetime.now().timestamp()
            if current_letter in session['pending_letters']:
                session['pending_letters'].pop(current_index)
                if current_index >= len(session['pending_letters']):
                    session['index'] = 0
                else:
                    session['index'] = current_index
        else:
            session['feedback'] = "Resposta incorreta!"
            session['is_correct'] = False
            session['show_next'] = False
            session['show_skip'] = True
            session['errors'][current_letter] = session['errors'].get(current_letter, 0) + 1
            if session.get('is_paused', False):
                pause_duration = datetime.now().timestamp() - session.get('pause_start', datetime.now().timestamp())
                session['paused_time'] = session.get('paused_time', 0) + pause_duration
                session['is_paused'] = False
                session['pause_start'] = None

        session.modified = True
        return jsonify({
            'feedback': session['feedback'],
            'is_correct': session['is_correct'],
            'show_next': session['show_next'],
            'show_skip': session['show_skip'],
            'current_letter': current_letter,
            'is_paused': session['is_paused']
        })
    except Exception as e:
        logger.error(f"Error in verify route: {str(e)}")
        return jsonify({
            'feedback': "Ocorreu um erro. Tente novamente.",
            'is_correct': False,
            'show_next': False,
            'show_skip': True,
            'current_letter': session.get('pending_letters', [session['letters'][0]])[session.get('index', 0)],
            'is_paused': False
        })

@game_bp.route('/next', methods=['POST'])
@login_required
def next_letter():
    try:
        initialize_session()
        if session.get('is_paused', False):
            pause_duration = datetime.now().timestamp() - session.get('pause_start', datetime.now().timestamp())
            session['paused_time'] = session.get('paused_time', 0) + pause_duration
            session['is_paused'] = False
            session['pause_start'] = None
        if session['index'] + 1 < len(session['pending_letters']):
            session['index'] = min(session['index'] + 1, len(session['pending_letters']) - 1)
        else:
            session['index'] = 0
        session['feedback'] = None
        session['is_correct'] = None
        session['show_next'] = False
        session['show_skip'] = False
        session.modified = True
        return redirect(url_for('game.index'))
    except Exception as e:
        logger.error(f"Error in next_letter route: {str(e)}")
        return redirect(url_for('game.index'))

@game_bp.route('/skip', methods=['POST'])
@login_required
def skip_letter():
    try:
        initialize_session()
        if session.get('is_paused', False):
            pause_duration = datetime.now().timestamp() - session.get('pause_start', datetime.now().timestamp())
            session['paused_time'] = session.get('paused_time', 0) + pause_duration
            session['is_paused'] = False
            session['pause_start'] = None
        current_index = session['index']
        current_letter = session['pending_letters'][current_index]
        session['errors'][current_letter] = session['errors'].get(current_letter, 0) + 1
        if session['index'] + 1 < len(session['pending_letters']):
            session['index'] = min(session['index'] + 1, len(session['pending_letters']) - 1)
        else:
            session['index'] = 0
        session['feedback'] = None
        session['is_correct'] = None
        session['show_next'] = False
        session['show_skip'] = False
        session.modified = True
        return redirect(url_for('game.index'))
    except Exception as e:
        logger.error(f"Error in skip_letter route: {str(e)}")
        return redirect(url_for('game.index'))

@game_bp.route('/retry_errors')
@login_required
def retry_errors():
    try:
        initialize_session()
        error_letters = [letra for letra, count in session['errors'].items() if count > 0]
        if not error_letters:
            return redirect(url_for('game.index'))
        session['pending_letters'] = error_letters
        random.shuffle(session['pending_letters'])
        session['index'] = 0
        session['feedback'] = None
        session['is_correct'] = None
        session['show_next'] = False
        session['show_skip'] = False
        session['retry_mode'] = True
        if session.get('is_paused', False):
            pause_duration = datetime.now().timestamp() - session.get('pause_start', datetime.now().timestamp())
            session['paused_time'] = session.get('paused_time', 0) + pause_duration
            session['is_paused'] = False
            session['pause_start'] = None
        session.modified = True
        return redirect(url_for('game.index'))
    except Exception as e:
        logger.error(f"Error in retry_errors route: {str(e)}")
        return redirect(url_for('game.index'))

@game_bp.route('/reset')
@login_required
def reset():
    try:
        # Limpar apenas os dados do jogo na sessão
        game_session_keys = ['letters', 'pending_letters', 'index', 'errors', 'feedback', 'is_correct', 
                           'show_next', 'show_skip', 'start_time', 'retry_mode', 'paused_time', 
                           'is_paused', 'pause_start', 'final_message']
        for key in game_session_keys:
            if key in session:
                session.pop(key, None)
        # Reincializar a sessão do jogo
        initialize_session()
        return redirect(url_for('game.index'))
    except Exception as e:
        logger.error(f"Error in reset route: {str(e)}")
        return redirect(url_for('game.index'))