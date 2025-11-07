#!/usr/bin/env python
"""
Script para criar todos os apps necessários do projeto
Execute na pasta raiz do projeto Django
"""

import os
import subprocess
import sys

def criar_app(nome_app):
    """Cria um app Django se ele não existir"""
    if os.path.exists(nome_app):
        print(f"• App '{nome_app}' já existe")
        return False
    
    try:
        subprocess.run(['python', 'manage.py', 'startapp', nome_app], check=True)
        print(f"✓ App '{nome_app}' criado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar app '{nome_app}': {e}")
        return False

def criar_init_py(pasta):
    """Cria arquivo __init__.py se não existir"""
    init_file = os.path.join(pasta, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('')
        print(f"✓ Arquivo __init__.py criado em {pasta}")

def main():
    print("=" * 60)
    print("🔧 CRIANDO APPS NECESSÁRIOS DO PROJETO")
    print("=" * 60)
    print()
    
    # Verifica se está na pasta correta
    if not os.path.exists('manage.py'):
        print("❌ ERRO: Execute este script na pasta raiz do projeto Django")
        print("   (onde está o arquivo manage.py)")
        sys.exit(1)
    
    print("✓ Pasta do projeto detectada!")
    print()
    
    # Lista de apps necessários
    apps = ['accounts', 'empresas', 'projetos', 'pesquisas', 'links']
    
    print("📝 Criando apps...")
    for app in apps:
        criar_app(app)
        # Garante que o __init__.py existe
        if os.path.exists(app):
            criar_init_py(app)
    
    print("\n" + "=" * 60)
    print("✅ APPS CRIADOS/VERIFICADOS COM SUCESSO!")
    print("=" * 60)
    print("\n📋 PRÓXIMOS PASSOS:")
    print("\n1. Execute novamente o script de correção:")
    print("   python corrigir_projeto.py")
    print("\n2. Ou prossiga com as migrações:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()