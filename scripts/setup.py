#!/usr/bin/env python3
"""
Setup script for the C++ Unit Test Generator
Helps users configure the environment and check dependencies
"""

import os
import sys
import subprocess
import yaml
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    return True

def check_cmake():
    """Check if CMake is installed"""
    try:
        result = subprocess.run(['cmake', '--version'], capture_output=True)
        if result.returncode == 0:
            version_line = result.stdout.decode().split('\n')[0]
            print(f"✅ {version_line}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ CMake not found. Please install CMake 3.16 or higher")
    return False

def check_compiler():
    """Check if a C++ compiler is available"""
    compilers = [
        ('g++', 'GCC'),
        ('clang++', 'Clang'),
        ('cl', 'MSVC')
    ]
    
    for compiler, name in compilers:
        try:
            result = subprocess.run([compiler, '--version'], capture_output=True)
            if result.returncode == 0:
                print(f"✅ {name} compiler found")
                return True
        except FileNotFoundError:
            continue
    
    print("❌ No C++ compiler found. Please install GCC, Clang, or MSVC")
    return False

def check_gtest():
    """Check if Google Test is available"""
    # Try pkg-config first
    try:
        result = subprocess.run(['pkg-config', '--exists', 'gtest'], capture_output=True)
        if result.returncode == 0:
            print("✅ Google Test found via pkg-config")
            return True
    except FileNotFoundError:
        pass
    
    # Check common installation paths
    common_paths = [
        '/usr/include/gtest',
        '/usr/local/include/gtest',
        'C:/Program Files/googletest/include/gtest',
        '/opt/homebrew/include/gtest'  # macOS Homebrew
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            print(f"✅ Google Test found at {path}")
            return True
    
    print("❌ Google Test not found. Please install Google Test")
    print("   Ubuntu/Debian: sudo apt-get install libgtest-dev")
    print("   macOS: brew install googletest")
    print("   Windows: vcpkg install gtest")
    return False

def check_ollama():
    """Check if Ollama is running"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running")
            return True
    except:
        pass
    
    print("⚠️  Ollama not detected. Please install and start Ollama:")
    print("   Visit: https://ollama.ai")
    print("   Run: ollama pull codellama:13b")
    return False

def install_python_dependencies():
    """Install Python dependencies"""
    try:
        print("📦 Installing Python dependencies...")
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Python dependencies installed")
            return True
        else:
            print("❌ Failed to install Python dependencies")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_sample_config():
    """Create a sample configuration file"""
    config_path = Path("config/llm_config.yaml")
    
    if config_path.exists():
        print("✅ Configuration file already exists")
        return True
    
    config_path.parent.mkdir(exist_ok=True)
    
    sample_config = {
        'llm_settings': {
            'provider': 'ollama',
            'ollama': {
                'base_url': 'http://localhost:11434',
                'model': 'codellama:13b',
                'timeout': 300
            },
            'openai': {
                'api_key': 'your-openai-api-key',
                'model': 'gpt-4',
                'max_tokens': 4096,
                'temperature': 0.1
            },
            'github': {
                'api_key': 'your-github-token',
                'model': 'gpt-4',
                'base_url': 'https://models.inference.ai.azure.com'
            },
            'request_settings': {
                'max_retries': 3,
                'retry_delay': 2,
                'temperature': 0.1,
                'max_tokens': 4096
            }
        },
        'generation_settings': {
            'max_tests_per_function': 5,
            'include_edge_cases': True,
            'include_error_handling': True,
            'target_line_coverage': 80,
            'target_branch_coverage': 70,
            'build_timeout': 120,
            'test_timeout': 60
        }
    }
    
    try:
        with open(config_path, 'w') as f:
            yaml.dump(sample_config, f, default_flow_style=False, indent=2)
        print("✅ Sample configuration created at config/llm_config.yaml")
        return True
    except Exception as e:
        print(f"❌ Failed to create configuration: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 C++ Unit Test Generator Setup")
    print("=" * 40)
    
    checks = [
        ("Python Version", check_python_version),
        ("CMake", check_cmake),
        ("C++ Compiler", check_compiler),
        ("Google Test", check_gtest),
        ("Ollama", check_ollama)
    ]
    
    all_passed = True
    
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        if not check_func():
            all_passed = False
    
    print(f"\n📦 Setting up Python environment...")
    if not install_python_dependencies():
        all_passed = False
    
    print(f"\n⚙️  Creating configuration...")
    if not create_sample_config():
        all_passed = False
    
    print("\n" + "=" * 40)
    
    if all_passed:
        print("✅ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Configure your LLM provider in config/llm_config.yaml")
        print("2. Run: python scripts/test_generator.py --input src --output tests")
    else:
        print("⚠️  Setup completed with warnings")
        print("Please install missing dependencies before running the generator")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 