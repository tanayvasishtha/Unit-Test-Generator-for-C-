"""
C++ Analyzer for finding and analyzing C++ source files
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional

class CppAnalyzer:
    """Analyzer for C++ source files"""
    
    def __init__(self):
        self.cpp_extensions = {'.cpp', '.cc', '.cxx', '.c++'}
        self.header_extensions = {'.h', '.hpp', '.hxx', '.h++'}
        
    def find_cpp_files(self, directory: str) -> List[str]:
        """Find all C++ source files in directory"""
        cpp_files = []
        
        for root, dirs, files in os.walk(directory):
            # Skip common build directories
            dirs[:] = [d for d in dirs if d not in {'build', 'cmake-build-debug', 'cmake-build-release', '.git'}]
            
            for file in files:
                if Path(file).suffix in self.cpp_extensions:
                    cpp_files.append(os.path.join(root, file))
                    
        return sorted(cpp_files)
    
    def find_header_files(self, directory: str) -> List[str]:
        """Find all C++ header files in directory"""
        header_files = []
        
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in {'build', 'cmake-build-debug', 'cmake-build-release', '.git'}]
            
            for file in files:
                if Path(file).suffix in self.header_extensions:
                    header_files.append(os.path.join(root, file))
                    
        return sorted(header_files)
    
    def analyze_file(self, file_path: str) -> Dict:
        """Analyze a C++ file for functions, classes, etc."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            return {
                'file_path': file_path,
                'functions': self._extract_functions(content),
                'classes': self._extract_classes(content),
                'includes': self._extract_includes(content),
                'namespaces': self._extract_namespaces(content)
            }
        except Exception as e:
            return {
                'file_path': file_path,
                'error': str(e),
                'functions': [],
                'classes': [],
                'includes': [],
                'namespaces': []
            }
    
    def _extract_functions(self, content: str) -> List[Dict]:
        """Extract function definitions from C++ code"""
        functions = []
        
        # Pattern for function definitions
        # This is a simplified pattern - real C++ parsing is much more complex
        function_pattern = r'(\w+\s+)*(\w+)\s*\(\s*([^)]*)\s*\)\s*(?:const\s*)?(?:override\s*)?(?:final\s*)?(?:noexcept\s*)?(?:\s*->\s*\w+)?\s*{'
        
        matches = re.finditer(function_pattern, content, re.MULTILINE)
        
        for match in matches:
            # Skip common C++ keywords that aren't function names
            function_name = match.group(2)
            if function_name in {'if', 'for', 'while', 'switch', 'catch', 'class', 'struct', 'enum'}:
                continue
                
            functions.append({
                'name': function_name,
                'parameters': match.group(3).strip(),
                'return_type': match.group(1).strip() if match.group(1) else 'auto',
                'line': content[:match.start()].count('\n') + 1
            })
            
        return functions
    
    def _extract_classes(self, content: str) -> List[Dict]:
        """Extract class definitions from C++ code"""
        classes = []
        
        # Pattern for class definitions
        class_pattern = r'class\s+(\w+)(?:\s*:\s*(?:public|private|protected)\s+[\w:]+)?\s*{'
        
        matches = re.finditer(class_pattern, content, re.MULTILINE)
        
        for match in matches:
            classes.append({
                'name': match.group(1),
                'line': content[:match.start()].count('\n') + 1
            })
            
        return classes
    
    def _extract_includes(self, content: str) -> List[str]:
        """Extract include statements from C++ code"""
        includes = []
        
        # Pattern for include statements
        include_pattern = r'#include\s*[<"]([^>"]+)[>"]'
        
        matches = re.findall(include_pattern, content)
        
        return list(set(matches))  # Remove duplicates
    
    def _extract_namespaces(self, content: str) -> List[str]:
        """Extract namespace declarations from C++ code"""
        namespaces = []
        
        # Pattern for namespace declarations
        namespace_pattern = r'namespace\s+(\w+)\s*{'
        
        matches = re.findall(namespace_pattern, content)
        
        return list(set(matches))  # Remove duplicates
    
    def get_project_info(self, directory: str) -> Dict:
        """Get overall project information"""
        cpp_files = self.find_cpp_files(directory)
        header_files = self.find_header_files(directory)
        
        total_functions = 0
        total_classes = 0
        all_includes = set()
        all_namespaces = set()
        
        for cpp_file in cpp_files:
            analysis = self.analyze_file(cpp_file)
            total_functions += len(analysis['functions'])
            total_classes += len(analysis['classes'])
            all_includes.update(analysis['includes'])
            all_namespaces.update(analysis['namespaces'])
        
        return {
            'cpp_files': len(cpp_files),
            'header_files': len(header_files),
            'total_functions': total_functions,
            'total_classes': total_classes,
            'common_includes': list(all_includes),
            'namespaces': list(all_namespaces)
        } 