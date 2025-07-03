"""
Build Manager for handling C++ compilation and build processes
"""

import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional

class BuildManager:
    """Manager for building C++ projects and tests"""
    
    def __init__(self):
        self.build_dir = "build"
        self.cmake_generator = "Unix Makefiles"  # Can be changed for Windows
        
    def build(self, test_dir: str) -> Dict:
        """Build the test project"""
        try:
            # Create build directory
            build_path = os.path.join(test_dir, self.build_dir)
            os.makedirs(build_path, exist_ok=True)
            
            # Run cmake configure
            cmake_result = self._run_cmake_configure(test_dir, build_path)
            if not cmake_result['success']:
                return cmake_result
            
            # Run build
            build_result = self._run_build(build_path)
            return build_result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'log': f"Build failed with exception: {e}"
            }
    
    def _run_cmake_configure(self, source_dir: str, build_dir: str) -> Dict:
        """Run cmake configuration"""
        try:
            cmd = [
                'cmake',
                '-S', source_dir,
                '-B', build_dir,
                '-G', self.cmake_generator,
                '-DCMAKE_BUILD_TYPE=Debug'
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'log': f"CMAKE STDOUT:\n{result.stdout}\n\nCMAKE STDERR:\n{result.stderr}"
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'CMake configuration timeout',
                'log': 'CMake configuration timed out after 120 seconds'
            }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'CMake not found',
                'log': 'CMake executable not found. Please install CMake.'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'log': f"CMake configuration failed: {e}"
            }
    
    def _run_build(self, build_dir: str) -> Dict:
        """Run the actual build"""
        try:
            cmd = ['cmake', '--build', build_dir, '--config', 'Debug']
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            log = f"BUILD STDOUT:\n{result.stdout}\n\nBUILD STDERR:\n{result.stderr}"
            
            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'log': log
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Build timeout',
                'log': 'Build timed out after 300 seconds'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'log': f"Build failed: {e}"
            }
    
    def run_tests(self, test_dir: str) -> Dict:
        """Run the compiled tests"""
        try:
            build_path = os.path.join(test_dir, self.build_dir)
            
            # Find test executable
            test_executable = self._find_test_executable(build_path)
            if not test_executable:
                return {
                    'success': False,
                    'error': 'Test executable not found',
                    'log': 'Could not find test executable in build directory'
                }
            
            # Run tests
            result = subprocess.run(
                [test_executable],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=build_path
            )
            
            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'log': f"TEST STDOUT:\n{result.stdout}\n\nTEST STDERR:\n{result.stderr}"
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Test timeout',
                'log': 'Tests timed out after 60 seconds'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'log': f"Test execution failed: {e}"
            }
    
    def _find_test_executable(self, build_dir: str) -> Optional[str]:
        """Find the test executable in build directory"""
        possible_names = ['run_tests', 'run_tests.exe', 'tests', 'tests.exe']
        
        for name in possible_names:
            exe_path = os.path.join(build_dir, name)
            if os.path.isfile(exe_path) and os.access(exe_path, os.X_OK):
                return exe_path
        
        # Search recursively
        for root, dirs, files in os.walk(build_dir):
            for file in files:
                if file in possible_names:
                    exe_path = os.path.join(root, file)
                    if os.access(exe_path, os.X_OK):
                        return exe_path
        
        return None
    
    def clean_build(self, test_dir: str):
        """Clean the build directory"""
        build_path = os.path.join(test_dir, self.build_dir)
        if os.path.exists(build_path):
            shutil.rmtree(build_path)
    
    def check_dependencies(self) -> Dict:
        """Check if required build dependencies are available"""
        dependencies = {
            'cmake': self._check_cmake(),
            'compiler': self._check_compiler(),
            'gtest': self._check_gtest()
        }
        
        all_available = all(dependencies.values())
        
        return {
            'all_available': all_available,
            'dependencies': dependencies
        }
    
    def _check_cmake(self) -> bool:
        """Check if CMake is available"""
        try:
            result = subprocess.run(['cmake', '--version'], capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def _check_compiler(self) -> bool:
        """Check if a C++ compiler is available"""
        compilers = ['g++', 'clang++', 'cl']
        
        for compiler in compilers:
            try:
                result = subprocess.run([compiler, '--version'], capture_output=True)
                if result.returncode == 0:
                    return True
            except:
                continue
        
        return False
    
    def _check_gtest(self) -> bool:
        """Check if Google Test is available"""
        # This is a simplified check - in reality, you'd want to check
        # if GTest can be found by CMake
        try:
            # Try to find gtest headers or library
            common_paths = [
                '/usr/include/gtest',
                '/usr/local/include/gtest',
                'C:/Program Files/googletest/include/gtest'
            ]
            
            for path in common_paths:
                if os.path.exists(path):
                    return True
            
            # Try pkg-config
            result = subprocess.run(['pkg-config', '--exists', 'gtest'], capture_output=True)
            return result.returncode == 0
            
        except:
            return False 