#!/usr/bin/env python3
"""
C++ Unit Test Generator using AI Models
Main script for generating, refining, and optimizing unit tests
"""

import argparse
import os
import sys
import yaml
import json
import time
from pathlib import Path
from typing import List, Dict, Optional
import re

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent))

from scripts.llm_client import LLMClient
from scripts.cpp_analyzer import CppAnalyzer
from scripts.build_manager import BuildManager
from scripts.coverage_analyzer import CoverageAnalyzer

class TestGenerator:
    """Main test generator class"""
    
    def __init__(self, config_path: str = "config/llm_config.yaml"):
        self.config = self._load_config(config_path)
        self.llm_client = LLMClient(self.config)
        self.cpp_analyzer = CppAnalyzer()
        self.build_manager = BuildManager()
        self.coverage_analyzer = CoverageAnalyzer()
        self.instructions = self._load_instructions()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Config file not found: {config_path}")
            return self._get_default_config()
            
    def _get_default_config(self) -> Dict:
        """Return default configuration"""
        return {
            'llm_settings': {
                'provider': 'ollama',
                'ollama': {
                    'base_url': 'http://localhost:11434',
                    'model': 'codellama:13b',
                    'timeout': 300
                }
            }
        }
    
    def _load_instructions(self) -> Dict:
        """Load YAML instruction files"""
        instructions = {}
        instruction_dir = Path("yaml_instructions")
        
        if instruction_dir.exists():
            for yaml_file in instruction_dir.glob("*.yaml"):
                with open(yaml_file, 'r') as f:
                    instructions[yaml_file.stem] = yaml.safe_load(f)
                
        return instructions
    
    def generate_tests(self, input_dir: str, output_dir: str) -> bool:
        """Main test generation workflow"""
        print("🚀 Starting C++ Unit Test Generation")
        
        # Step 1: Analyze C++ source files
        print("\n📁 Analyzing C++ source files...")
        cpp_files = self.cpp_analyzer.find_cpp_files(input_dir)
        
        if not cpp_files:
            print("❌ No C++ files found in the input directory")
            return False
            
        print(f"Found {len(cpp_files)} C++ files")
        
        # Step 2: Generate initial tests
        print("\n🧪 Generating initial unit tests...")
        generated_tests = {}
        
        for cpp_file in cpp_files:
            print(f"  Processing: {cpp_file}")
            test_code = self._generate_initial_test(cpp_file)
            
            if test_code:
                test_filename = f"test_{Path(cpp_file).stem}.cpp"
                generated_tests[test_filename] = {
                    'code': test_code,
                    'source_file': cpp_file
                }
                
        if not generated_tests:
            print("❌ Failed to generate any tests")
            return False
            
        # Step 3: Save tests to output directory
        print(f"\n💾 Saving tests to {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
        
        for test_filename, test_data in generated_tests.items():
            test_path = os.path.join(output_dir, test_filename)
            with open(test_path, 'w') as f:
                f.write(test_data['code'])
        
        # Step 4: Create CMakeLists.txt
        self._create_cmake_file(input_dir, output_dir)
        
        print("\n✅ Test generation completed!")
        return True
    
    def _generate_initial_test(self, cpp_file: str) -> Optional[str]:
        """Generate initial unit test for a C++ file"""
        try:
            # Read the C++ source code
            with open(cpp_file, 'r') as f:
                code_content = f.read()
                
            # Create a simple prompt if no instruction file exists
            if 'initial_generation' in self.instructions:
                instruction = self.instructions['initial_generation']
                prompt_template = instruction.get('prompt_template', '')
                filename = Path(cpp_file).stem
                prompt = prompt_template.format(code_content=code_content, original_filename=filename)
            else:
                prompt = f"""Generate comprehensive unit tests for the following C++ code using Google Test framework:

```cpp
{code_content}
```

Requirements:
- Use Google Test (gtest) framework
- Include all necessary headers
- Test all public methods and functions
- Cover edge cases and error conditions
- Use descriptive test names

Generate only the test code without explanations."""
            
            # Generate test using LLM
            response = self.llm_client.generate(prompt)
            
            if response:
                return self._extract_cpp_code(response)
                
        except Exception as e:
            print(f"Error generating test for {cpp_file}: {e}")
            
        return None
    
    def _extract_cpp_code(self, response: str) -> str:
        """Extract C++ code from LLM response"""
        # Look for code blocks
        cpp_pattern = r'```(?:cpp|c\+\+)?\s*(.*?)\s*```'
        matches = re.findall(cpp_pattern, response, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # If no code blocks found, return the response as-is
        return response.strip()
    
    def _create_cmake_file(self, input_dir: str, output_dir: str):
        """Create CMakeLists.txt for building tests"""
        cmake_content = """cmake_minimum_required(VERSION 3.16)
project(UnitTests)

set(CMAKE_CXX_STANDARD 17)

# Find GTest
find_package(GTest REQUIRED)
find_package(Threads REQUIRED)

# Enable coverage
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -O0 --coverage")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} --coverage")

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../src)

# Find source files
file(GLOB_RECURSE SOURCE_FILES "../src/*.cpp")
file(GLOB_RECURSE TEST_FILES "test_*.cpp")

# Create test executable
add_executable(run_tests ${TEST_FILES} ${SOURCE_FILES})

# Link libraries
target_link_libraries(run_tests 
    GTest::GTest 
    GTest::Main
    Threads::Threads
    gcov
)

# Enable testing
enable_testing()
add_test(NAME unit_tests COMMAND run_tests)
"""
        
        cmake_path = os.path.join(output_dir, "CMakeLists.txt")
        with open(cmake_path, 'w') as f:
            f.write(cmake_content)

def main():
    parser = argparse.ArgumentParser(description='C++ Unit Test Generator')
    parser.add_argument('--input', '-i', required=True, 
                       help='Input directory containing C++ source files')
    parser.add_argument('--output', '-o', default='tests',
                       help='Output directory for generated tests')
    parser.add_argument('--config', '-c', default='config/llm_config.yaml',
                       help='Configuration file path')
    
    args = parser.parse_args()
    
    # Validate input directory
    if not os.path.isdir(args.input):
        print(f"❌ Input directory does not exist: {args.input}")
        sys.exit(1)
    
    # Create generator and run
    generator = TestGenerator(args.config)
    success = generator.generate_tests(args.input, args.output)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 