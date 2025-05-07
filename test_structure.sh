#!/bin/bash

# Script para testar a estrutura modular do HebraicoFacil 2.0
echo "Testando a estrutura modular do HebraicoFacil 2.0..."

# Verificar se o diretório do projeto existe
if [ ! -d "/home/lucas/projeto_modular/hebraicofacil" ]; then
    echo "Erro: Diretório do projeto não encontrado!"
    exit 1
fi

# Verificar se todos os módulos foram criados
for module in auth payments lessons admin; do
    if [ ! -d "/home/lucas/projeto_modular/hebraicofacil/$module" ]; then
        echo "Erro: Módulo $module não encontrado!"
        exit 1
    fi
    
    # Verificar se os arquivos principais de cada módulo existem
    for file in __init__.py models.py routes.py utils.py; do
        if [ ! -f "/home/lucas/projeto_modular/hebraicofacil/$module/$file" ]; then
            echo "Erro: Arquivo $file não encontrado no módulo $module!"
            exit 1
        fi
    done
    
    echo "✓ Módulo $module verificado com sucesso!"
done

# Verificar se o arquivo principal da aplicação existe
if [ ! -f "/home/lucas/projeto_modular/hebraicofacil/__init__.py" ]; then
    echo "Erro: Arquivo principal da aplicação não encontrado!"
    exit 1
fi

# Verificar se o arquivo wsgi.py existe
if [ ! -f "/home/lucas/projeto_modular/wsgi.py" ]; then
    echo "Erro: Arquivo wsgi.py não encontrado!"
    exit 1
fi

# Verificar se o arquivo requirements.txt existe
if [ ! -f "/home/lucas/projeto_modular/requirements.txt" ]; then
    echo "Erro: Arquivo requirements.txt não encontrado!"
    exit 1
fi

echo "✓ Todos os arquivos principais verificados com sucesso!"
echo "A estrutura modular do HebraicoFacil 2.0 está correta!"
echo "Para testar a execução da aplicação, crie um ambiente virtual e instale as dependências:"
echo "  python -m venv venv"
echo "  source venv/bin/activate"
echo "  pip install -r requirements.txt"
echo "  python wsgi.py"
