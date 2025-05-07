from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from flask_mail import Mail
from flask_caching import Cache
import logging
import os
from dotenv import load_dotenv
import sys
from sqlalchemy import inspect

# Inicialização de objetos globais
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
cache = Cache(config={'CACHE_TYPE': 'simple'})

def create_app(test_config=None):
    # Carregar variáveis do arquivo .env
    load_dotenv()
    
    # Configuração do logging
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    logger = logging.getLogger(__name__)
    
    # Criar e configurar a aplicação
    app = Flask(__name__)
    
    # Configurações básicas
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-for-development')
    
    # Configurações de sessão
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # Configuração do e-mail
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    
    # Configuração do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/hebraicofacil.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuração do Pagarme
    app.config['PAGARME_API_KEY'] = os.getenv('PAGARME_API_KEY', 'dev-key-for-development')
    
    # Configuração de segurança
    app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT', 'email-confirm-salt')
    
    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    mail.init_app(app)
    cache.init_app(app)
    
    # Registrar blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from .payments import payments_bp
    app.register_blueprint(payments_bp)
    
    from .lessons import lessons_bp
    app.register_blueprint(lessons_bp)
    
    from .admin import admin_bp
    app.register_blueprint(admin_bp)
    
    from .bible import bible_bp
    app.register_blueprint(bible_bp, url_prefix='/bible')

    from .game import game_bp
    app.register_blueprint(game_bp, url_prefix='/game')

    
    # Importar CoursePrice apenas dentro da função para evitar circular import
    from .payments.models import CoursePrice
    from .auth.models import GameConfig

     # Configurar GameConfig como global no Jinja2
    app.jinja_env.globals['GameConfig'] = GameConfig
    
    # Rota principal
    @app.route('/')
    def index():
        # Buscar preço do curso do banco de dados
        course_price = CoursePrice.query.first()
        price = course_price.price if course_price else 29.90
        
        # Criar um plano de exemplo para exibir na página inicial
        plan = {
            'name': 'Plano Completo',
            'description': 'Acesso a todas as lições e recursos do HebraicoFacil',
            'duration': '1 mês',
            'price': f'R$ {price:.2f}'
        }
        return render_template('index.html', plan=plan)
    
    # Redirecionar para o dashboard no blueprint lessons
    @app.route('/dashboard')
    @login_required
    def dashboard():
        from flask import redirect, url_for
        return redirect(url_for('lessons.dashboard'))
    
    # Handlers de erro
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    # Inicializar o banco de dados (sem recriar tabelas)
    with app.app_context():
        # Verificar se as tabelas existem; criar apenas se necessário
        inspector = inspect(db.engine)
        if not inspector.has_table('course_price'):
            logger.warning("Tabelas não encontradas. Criando tabelas no banco de dados...")
            db.create_all()
            # Garantir que existe um preço inicial
            if not CoursePrice.query.first():
                logger.info("Adicionando preço padrão para CoursePrice")
                default_price = CoursePrice(price=29.90)
                db.session.add(default_price)
                db.session.commit()

            # Garantir que existe uma configuração para o jogo
            if not GameConfig.query.first():
                logger.info("Adicionando configuração padrão para GameConfig")
                game_config = GameConfig(visible=False)  # Jogo oculto por padrão
                db.session.add(game_config)
                db.session.commit()
        else:
            logger.info("Tabelas já existem. Nenhuma ação necessária.")

    return app

@login_manager.user_loader
def load_user(user_id):
    from .auth.models import User
    return User.query.get(int(user_id))