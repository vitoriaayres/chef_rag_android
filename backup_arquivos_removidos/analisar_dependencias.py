#!/usr/bin/env python3
"""
Script para analisar dependências reais do Chef RAG v2
Identifica quais arquivos são necessários para o funcionamento do main.py
"""

import os
import sys
import ast
import importlib.util
from pathlib import Path

class DependencyAnalyzer:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.used_files = set()
        self.imports_found = set()
        
    def analyze_file(self, file_path):
        """Analisa um arquivo Python e extrai seus imports"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        if module:
                            imports.append(f"{module}.{alias.name}")
                        else:
                            imports.append(alias.name)
            
            return imports
        except Exception as e:
            print(f"Erro ao analisar {file_path}: {e}")
            return []
    
    def resolve_local_import(self, import_name):
        """Resolve imports locais para arquivos"""
        # Casos especiais
        if import_name.startswith('core_logic'):
            parts = import_name.split('.')
            if len(parts) >= 2:
                module_name = parts[1]
                file_path = self.root_dir / 'core_logic' / f"{module_name}.py"
                if file_path.exists():
                    return file_path
        
        # Arquivo na raiz
        file_path = self.root_dir / f"{import_name}.py"
        if file_path.exists():
            return file_path
        
        # Arquivo como módulo
        module_path = self.root_dir / import_name / "__init__.py"
        if module_path.exists():
            return module_path
        
        return None
    
    def trace_dependencies(self, start_file):
        """Rastreia todas as dependências recursivamente"""
        to_analyze = [start_file]
        analyzed = set()
        
        while to_analyze:
            current_file = to_analyze.pop(0)
            
            if current_file in analyzed:
                continue
            
            analyzed.add(current_file)
            self.used_files.add(current_file)
            
            print(f"📁 Analisando: {current_file.relative_to(self.root_dir)}")
            
            imports = self.analyze_file(current_file)
            
            for imp in imports:
                self.imports_found.add(imp)
                local_file = self.resolve_local_import(imp)
                
                if local_file and local_file not in analyzed:
                    to_analyze.append(local_file)
    
    def find_unused_files(self):
        """Encontra arquivos Python não utilizados"""
        all_py_files = set()
        
        # Arquivos na raiz
        for file in self.root_dir.glob("*.py"):
            all_py_files.add(file)
        
        # Arquivos no core_logic
        core_logic_dir = self.root_dir / 'core_logic'
        if core_logic_dir.exists():
            for file in core_logic_dir.glob("*.py"):
                if file.name != "__init__.py":
                    all_py_files.add(file)
        
        unused_files = all_py_files - self.used_files
        return unused_files
    
    def generate_report(self):
        """Gera relatório de uso de arquivos"""
        print("\n" + "="*60)
        print("📊 RELATÓRIO DE DEPENDÊNCIAS - CHEF RAG V2")
        print("="*60)
        
        print(f"\n🟢 ARQUIVOS UTILIZADOS ({len(self.used_files)}):")
        for file in sorted(self.used_files):
            rel_path = file.relative_to(self.root_dir)
            size = file.stat().st_size / 1024  # KB
            print(f"  ✅ {rel_path} ({size:.1f}KB)")
        
        unused = self.find_unused_files()
        print(f"\n🔴 ARQUIVOS NÃO UTILIZADOS ({len(unused)}):")
        total_unused_size = 0
        for file in sorted(unused):
            rel_path = file.relative_to(self.root_dir)
            size = file.stat().st_size / 1024  # KB
            total_unused_size += size
            print(f"  ❌ {rel_path} ({size:.1f}KB)")
        
        print(f"\n💾 ECONOMIA POSSÍVEL: {total_unused_size:.1f}KB")
        
        print(f"\n📦 IMPORTS EXTERNOS DETECTADOS:")
        external_imports = sorted([imp for imp in self.imports_found 
                                 if not self.resolve_local_import(imp)])
        for imp in external_imports[:20]:  # Primeiros 20
            if not imp.startswith('_') and '.' not in imp:
                print(f"  📥 {imp}")
        
        if len(external_imports) > 20:
            print(f"  ... e mais {len(external_imports) - 20} imports")
        
        return unused

def main():
    root_dir = Path(__file__).parent
    analyzer = DependencyAnalyzer(root_dir)
    
    # Começar pelo main.py
    main_file = root_dir / "main.py"
    
    if not main_file.exists():
        print("❌ main.py não encontrado!")
        return
    
    print("🔍 Iniciando análise de dependências...")
    print(f"📁 Diretório raiz: {root_dir}")
    
    analyzer.trace_dependencies(main_file)
    unused_files = analyzer.generate_report()
    
    # Salvar lista de arquivos não utilizados
    unused_list = root_dir / "arquivos_nao_utilizados.txt"
    with open(unused_list, 'w', encoding='utf-8') as f:
        f.write("# Arquivos Python não utilizados pelo main.py\n\n")
        for file in sorted(unused_files):
            f.write(f"{file.relative_to(root_dir)}\n")
    
    print(f"\n📝 Lista detalhada salva em: {unused_list}")
    
    # Perguntar se deseja criar script de limpeza
    print(f"\n❓ Deseja criar um script de limpeza automática? (s/n): ", end="")

if __name__ == "__main__":
    main()