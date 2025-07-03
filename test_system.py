#!/usr/bin/env python3
"""
System Test Script for C++ Unit Test Generator
Comprehensive test of all functionality
"""

import os
import sys
import tempfile
import shutil
import subprocess
from pathlib import Path

class SystemTester:
    """Complete system test for the unit test generator"""
    
    def __init__(self):
        self.test_results = []
        self.temp_dir = None
        
    def log_test(self, test_name, success, message=""):
        """Log test result"""
        self.test_results.append({
            'name': test_name,
            'success': success,
            'message': message
        })
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"    {message}")
    
    def test_dependencies(self):
        """Test that all dependencies are available"""
        print("\n🔍 Testing Dependencies...")
        
        # Test Python version
        if sys.version_info >= (3, 8):
            self.log_test("Python Version", True, f"Python {sys.version_info.major}.{sys.version_info.minor}")
        else:
            self.log_test("Python Version", False, "Python 3.8+ required")
        
        # Test Python packages
        required_packages = ['requests', 'pyyaml']
        for package in required_packages:
            try:
                __import__(package)
                self.log_test(f"Package: {package}", True)
            except ImportError:
                self.log_test(f"Package: {package}", False, "Not installed")
        
        # Test CMake
        try:
            result = subprocess.run(['cmake', '--version'], capture_output=True)
            self.log_test("CMake", result.returncode == 0)
        except FileNotFoundError:
            self.log_test("CMake", False, "Not found")
        
        # Test C++ compiler
        compilers = ['g++', 'clang++', 'cl']
        compiler_found = False
        for compiler in compilers:
            try:
                result = subprocess.run([compiler, '--version'], capture_output=True)
                if result.returncode == 0:
                    self.log_test(f"C++ Compiler ({compiler})", True)
                    compiler_found = True
                    break
            except FileNotFoundError:
                continue
        
        if not compiler_found:
            self.log_test("C++ Compiler", False, "No compiler found")
    
    def test_project_structure(self):
        """Test that project structure is correct"""
        print("\n📁 Testing Project Structure...")
        
        required_dirs = ['src', 'scripts', 'yaml_instructions', 'config']
        for dir_name in required_dirs:
            exists = os.path.isdir(dir_name)
            self.log_test(f"Directory: {dir_name}", exists)
        
        required_files = [
            'README.md',
            'requirements.txt',
            'scripts/test_generator.py',
            'scripts/llm_client.py',
            'scripts/cpp_analyzer.py',
            'config/llm_config.yaml',
            'yaml_instructions/initial_generation.yaml'
        ]
        
        for file_path in required_files:
            exists = os.path.isfile(file_path)
            self.log_test(f"File: {file_path}", exists)
    
    def test_source_analysis(self):
        """Test C++ source analysis functionality"""
        print("\n🔍 Testing Source Analysis...")
        
        try:
            from scripts.cpp_analyzer import CppAnalyzer
            
            analyzer = CppAnalyzer()
            
            # Test finding C++ files
            cpp_files = analyzer.find_cpp_files('src')
            self.log_test("Find C++ files", len(cpp_files) > 0, f"Found {len(cpp_files)} files")
            
            # Test file analysis
            if cpp_files:
                analysis = analyzer.analyze_file(cpp_files[0])
                has_functions = len(analysis.get('functions', [])) > 0
                self.log_test("Analyze C++ file", has_functions, f"Found {len(analysis.get('functions', []))} functions")
            
        except Exception as e:
            self.log_test("Source Analysis", False, str(e))
    
    def test_llm_client(self):
        """Test LLM client functionality"""
        print("\n🤖 Testing LLM Client...")
        
        try:
            from scripts.llm_client import LLMClient
            
            # Load config
            with open('config/llm_config.yaml', 'r') as f:
                import yaml
                config = yaml.safe_load(f)
            
            client = LLMClient(config)
            self.log_test("LLM Client Creation", True)
            
            # Test connection (non-blocking test)
            connection_test = client.test_connection()
            self.log_test("LLM Connection", connection_test, 
                         "Connected" if connection_test else "Not available (configure LLM)")
            
        except Exception as e:
            self.log_test("LLM Client", False, str(e))
    
    def test_build_manager(self):
        """Test build manager functionality"""
        print("\n🔨 Testing Build Manager...")
        
        try:
            from scripts.build_manager import BuildManager
            
            manager = BuildManager()
            
            # Test dependency checking
            deps = manager.check_dependencies()
            self.log_test("Build Dependencies Check", True, 
                         f"Available: {list(k for k, v in deps['dependencies'].items() if v)}")
            
        except Exception as e:
            self.log_test("Build Manager", False, str(e))
    
    def test_end_to_end(self):
        """Test end-to-end workflow"""
        print("\n🚀 Testing End-to-End Workflow...")
        
        try:
            # Create temporary test directory
            self.temp_dir = tempfile.mkdtemp()
            test_src_dir = os.path.join(self.temp_dir, 'test_src')
            test_output_dir = os.path.join(self.temp_dir, 'test_output')
            
            os.makedirs(test_src_dir)
            
            # Create a simple test file
            test_cpp_content = '''
#include <iostream>

class SimpleClass {
public:
    int add(int a, int b) {
        return a + b;
    }
    
    bool isPositive(int n) {
        return n > 0;
    }
};
'''
            
            with open(os.path.join(test_src_dir, 'simple.cpp'), 'w') as f:
                f.write(test_cpp_content)
            
            # Test the generator script
            cmd = [
                sys.executable, 'scripts/test_generator.py',
                '--input', test_src_dir,
                '--output', test_output_dir
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                success = result.returncode == 0
                
                if success:
                    # Check if test files were generated
                    test_files = [f for f in os.listdir(test_output_dir) if f.endswith('.cpp')]
                    self.log_test("Test Generation", len(test_files) > 0, 
                                 f"Generated {len(test_files)} test files")
                    
                    # Check if CMakeLists.txt was created
                    cmake_exists = os.path.exists(os.path.join(test_output_dir, 'CMakeLists.txt'))
                    self.log_test("CMakeLists.txt Generation", cmake_exists)
                else:
                    self.log_test("Test Generation", False, "Generator script failed")
                    
            except subprocess.TimeoutExpired:
                self.log_test("Test Generation", False, "Timeout")
            except Exception as e:
                self.log_test("Test Generation", False, str(e))
            
        except Exception as e:
            self.log_test("End-to-End Test Setup", False, str(e))
    
    def cleanup(self):
        """Clean up temporary files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def print_summary(self):
        """Print test results summary"""
        print(f"\n{'='*60}")
        print("TEST RESULTS SUMMARY")
        print(f"{'='*60}")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for test in self.test_results if test['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\nFailed Tests:")
            for test in self.test_results:
                if not test['success']:
                    print(f"  ❌ {test['name']}: {test['message']}")
        
        return failed_tests == 0
    
    def run_all_tests(self):
        """Run all system tests"""
        print("🧪 C++ Unit Test Generator - System Tests")
        print("="*60)
        
        try:
            self.test_dependencies()
            self.test_project_structure()
            self.test_source_analysis()
            self.test_llm_client()
            self.test_build_manager()
            self.test_end_to_end()
            
            return self.print_summary()
            
        finally:
            self.cleanup()

def test_basic_functionality():
    """Test basic system functionality"""
    print("🧪 Running System Tests...")
    
    # Test 1: Check if main files exist
    required_files = [
        'scripts/test_generator.py',
        'scripts/llm_client.py',
        'scripts/cpp_analyzer.py',
        'config/llm_config.yaml'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    # Test 2: Try importing modules
    try:
        sys.path.append('scripts')
        from llm_client import LLMClient
        from cpp_analyzer import CppAnalyzer
        print("✅ Python modules import successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test 3: Test C++ file discovery
    try:
        analyzer = CppAnalyzer()
        cpp_files = analyzer.find_cpp_files('src')
        print(f"✅ Found {len(cpp_files)} C++ files")
    except Exception as e:
        print(f"❌ C++ analysis error: {e}")
        return False
    
    print("✅ All basic tests passed!")
    return True

def main():
    """Main test function"""
    if test_basic_functionality():
        print("\n🎉 System is ready! Try running:")
        print("   python demo.py")
        return True
    else:
        print("\n❌ System tests failed. Please check the setup.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 