# Guia de Instalação e Uso - HebraicoFacil 2.0 Modularizado

Este documento contém instruções para instalar e executar a versão modularizada do HebraicoFacil 2.0.

## Estrutura do Projeto

O projeto foi reorganizado seguindo as melhores práticas de desenvolvimento Flask, utilizando uma estrutura modular com Blueprints:

```
hebraicofacil/
├── __init__.py           # Arquivo principal da aplicação (factory pattern)
├── auth/                 # Módulo de autenticação
│   ├── __init__.py
│   ├── models.py         # Modelos de usuário e progresso
│   ├── routes.py         # Rotas de autenticação (login, registro, etc.)
│   └── utils.py          # Funções auxiliares para autenticação
├── payments/             # Módulo de pagamentos
│   ├── __init__.py
│   ├── models.py         # Modelo de pagamento
│   ├── routes.py         # Rotas de pagamento
│   └── utils.py          # Funções auxiliares para pagamentos
├── lessons/              # Módulo de lições
│   ├── __init__.py
│   ├── models.py         # Modelo de módulo de aprendizado
│   ├── routes.py         # Rotas de lições
│   └── utils.py          # Mapeamentos hebraicos e funções auxiliares
└── admin/                # Módulo de administração
    ├── __init__.py
    ├── models.py         # (Vazio, usa modelos de outros módulos)
    ├── routes.py         # Rotas de administração
    └── utils.py          # Funções auxiliares para administração
```

## Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Todas as dependências listadas em `requirements.txt`

## Instalação

1. Extraia o arquivo ZIP em um diretório de sua escolha:
   ```
   unzip hebraicofacil-modular.zip
   cd projeto_modular
   ```

2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   ```
   cp .env.example .env
   ```
   Edite o arquivo `.env` com suas configurações (chave secreta, credenciais de e-mail, etc.)

## Execução

Para executar a aplicação em modo de desenvolvimento:

```
python wsgi.py
```

A aplicação estará disponível em `http://localhost:5000`

## Implantação em Produção

Para implantação em produção, recomendamos:

1. Usar Gunicorn como servidor WSGI:
   ```
   gunicorn wsgi:app
   ```

2. Configurar um servidor proxy reverso (Nginx ou Apache) na frente do Gunicorn

3. Garantir que todas as variáveis de ambiente estejam configuradas corretamente

## Benefícios da Modularização

A nova estrutura modular traz os seguintes benefícios:

1. **Manutenibilidade**: Código organizado por funcionalidade, facilitando a manutenção
2. **Escalabilidade**: Fácil adição de novos módulos e funcionalidades
3. **Testabilidade**: Estrutura que facilita a criação de testes unitários
4. **Legibilidade**: Código mais limpo e organizado
5. **Colaboração**: Múltiplos desenvolvedores podem trabalhar em módulos diferentes simultaneamente

## Próximos Passos Recomendados

1. Adicionar testes unitários para cada módulo
2. Implementar um sistema de migração de banco de dados (Flask-Migrate)
3. Melhorar a documentação do código
4. Implementar um sistema de logging mais robusto
5. Adicionar validação de formulários com Flask-WTF
# projeto_modular
# ivaldi
