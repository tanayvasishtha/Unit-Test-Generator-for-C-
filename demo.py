#!/usr/bin/env python3
"""
Demonstration script for the C++ Unit Test Generator
Shows complete workflow from setup to test generation
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_step(step_num, title):
    """Print a formatted step header"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {title}")
    print(f"{'='*60}")

def run_command(cmd, description):
    """Run a command and show the result"""
    print(f"\n🔧 {description}")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout:
                print("Output:")
                print(result.stdout)
            return True
        else:
            print("❌ Failed!")
            if result.stderr:
                print("Error:")
                print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def demo_workflow():
    """Demonstrate the complete workflow"""
    print("🚀 C++ Unit Test Generator - Complete Demo")
    print("This demo shows the full workflow from setup to test generation")
    
    # Step 1: Environment Setup
    print_step(1, "Environment Setup and Dependency Check")
    
    if not run_command([sys.executable, "scripts/setup.py"], "Running setup script"):
        print("⚠️  Setup had issues, but continuing with demo...")
    
    # Step 2: Show Project Structure
    print_step(2, "Project Structure Overview")
    
    print("\n📁 Current project structure:")
    for root, dirs, files in os.walk("."):
        # Skip hidden directories and build directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'build']]
        
        level = root.replace(".", "").count(os.sep)
        indent = " " * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        
        sub_indent = " " * 2 * (level + 1)
        for file in files:
            if not file.startswith('.') and not file.endswith('.pyc'):
                print(f"{sub_indent}{file}")
    
    # Step 3: Analyze Source Code
    print_step(3, "Analyzing Source Code")
    
    print("\n📋 Source files to be tested:")
    src_files = []
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(('.cpp', '.cc', '.cxx')):
                file_path = os.path.join(root, file)
                src_files.append(file_path)
                print(f"  • {file_path}")
    
    if not src_files:
        print("❌ No C++ source files found in src/ directory")
        return False
    
    # Step 4: Generate Tests
    print_step(4, "Generating Unit Tests with AI")
    
    # Check if config exists
    config_path = "config/llm_config.yaml"
    if not os.path.exists(config_path):
        print("❌ Configuration file not found. Please run setup first.")
        return False
    
    # Generate tests
    cmd = [sys.executable, "scripts/test_generator.py", "--input", "src", "--output", "tests"]
    
    print("\n🤖 Generating tests using AI model...")
    print("This may take a few minutes depending on your LLM provider...")
    
    if run_command(cmd, "Generating unit tests"):
        print("\n📁 Generated test files:")
        if os.path.exists("tests"):
            for file in os.listdir("tests"):
                if file.endswith('.cpp'):
                    print(f"  • tests/{file}")
    else:
        print("❌ Test generation failed")
        print("This might be due to:")
        print("  • LLM service not available")
        print("  • Configuration issues")
        print("  • Network connectivity")
        return False
    
    # Step 5: Build Tests (Optional)
    print_step(5, "Building Generated Tests (Optional)")
    
    if os.path.exists("tests/CMakeLists.txt"):
        print("\n🔨 Attempting to build tests...")
        
        # Create build directory
        os.makedirs("tests/build", exist_ok=True)
        
        # Configure with CMake
        if run_command(
            ["cmake", "-S", "tests", "-B", "tests/build"],
            "Configuring build with CMake"
        ):
            # Build
            run_command(
                ["cmake", "--build", "tests/build"],
                "Building test executable"
            )
        else:
            print("⚠️  Build configuration failed (this is normal if dependencies are missing)")
    
    # Step 6: Show Results
    print_step(6, "Results Summary")
    
    print("\n📊 Demo Results:")
    print(f"  • Source files analyzed: {len(src_files)}")
    
    test_files = 0
    if os.path.exists("tests"):
        test_files = len([f for f in os.listdir("tests") if f.endswith('.cpp')])
    print(f"  • Test files generated: {test_files}")
    
    if os.path.exists("tests/build"):
        print("  • Build attempted: Yes")
    else:
        print("  • Build attempted: No")
    
    print("\n✅ Demo completed!")
    return True

def show_next_steps():
    """Show next steps for the user"""
    print(f"\n{'='*60}")
    print("NEXT STEPS")
    print(f"{'='*60}")
    
    print("\n🔧 To use this tool in your own project:")
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt")
    
    print("\n2. Configure your LLM provider:")
    print("   Edit config/llm_config.yaml")
    print("   Supported providers: Ollama, OpenAI, GitHub Models")
    
    print("\n3. Generate tests for your C++ code:")
    print("   python scripts/test_generator.py --input your_src_dir --output tests")
    
    print("\n4. Install build dependencies (for compilation):")
    print("   Ubuntu/Debian: sudo apt-get install cmake libgtest-dev")
    print("   macOS: brew install cmake googletest")
    print("   Windows: Install Visual Studio and vcpkg")
    
    print("\n📚 For more information:")
    print("   • Read README.md for detailed instructions")
    print("   • Check yaml_instructions/ for LLM prompt templates")
    print("   • Examine generated tests for quality and coverage")

def main():
    """Main demo function"""
    try:
        success = demo_workflow()
        show_next_steps()
        
        if success:
            print("\n🎉 Demo completed successfully!")
        else:
            print("\n⚠️  Demo completed with some issues")
            
        return success
        
    except KeyboardInterrupt:
        print("\n\n⛔ Demo interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 