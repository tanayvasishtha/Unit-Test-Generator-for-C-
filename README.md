# C++ Unit Test Generator using AI Models

An automated tool that generates, refines, and optimizes unit tests for C++ applications using Large Language Models (LLM).

## Architecture

```
TASK5/
├── src/                     # Sample C++ application
├── tests/                   # Generated unit tests
├── yaml_instructions/       # YAML instruction files for LLM
├── scripts/                 # Main generator and utility scripts
├── config/                  # Configuration files
├── reports/                 # Coverage and build reports
├── requirements.txt         # Python dependencies
└── CMakeLists.txt          # Build configuration
```

## Features

- **Automated Test Generation**: Uses LLM to generate initial unit tests
- **Iterative Refinement**: Removes duplicates and improves test quality
- **Build Integration**: Handles build errors and coverage analysis
- **YAML-Driven Instructions**: Structured prompts for consistent results
- **Coverage Analysis**: Integrates with GNU coverage tools

## Quick Start

1. **Run the setup script:**
   ```bash
   python scripts/setup.py
   ```

2. **Try the demonstration:**
   ```bash
   python demo.py
   ```

3. **Configure your LLM provider** in `config/llm_config.yaml`:
   - For Ollama (local): Ensure Ollama is running with `codellama:13b` model
   - For OpenAI: Add your API key
   - For GitHub Models: Add your GitHub token

4. **Generate tests for your code:**
   ```bash
   python scripts/test_generator.py --input src/ --output tests/
   ```

5. **Build and run tests:**
   ```bash
   cd tests && mkdir build && cd build
   cmake .. && make
   ./run_tests
   ```

## Workflow

1. **Initial Generation**: Analyzes C++ code and generates basic unit tests
2. **Refinement**: Removes duplicates, adds proper libraries, improves structure
3. **Build & Test**: Compiles tests and handles any build issues
4. **Coverage Analysis**: Measures coverage and suggests improvements

## Examples

### Generated Test Structure
The tool generates comprehensive tests like this:

```cpp
#include <gtest/gtest.h>
#include "calculator.h"

class CalculatorTest : public ::testing::Test {
protected:
    Calculator calc;
};

TEST_F(CalculatorTest, AddPositiveNumbers) {
    EXPECT_EQ(5, calc.add(2, 3));
    EXPECT_EQ(0, calc.add(0, 0));
}

TEST_F(CalculatorTest, DivideByZeroThrowsException) {
    EXPECT_THROW(calc.divide(10, 0), std::invalid_argument);
}
```

### Command Line Options

```bash
# Basic usage
python scripts/test_generator.py --input src --output tests

# Custom configuration
python scripts/test_generator.py --input src --output tests --config my_config.yaml

# Help
python scripts/test_generator.py --help
```

## Troubleshooting

### Common Issues

1. **"LLM connection failed"**
   - For Ollama: Ensure `ollama serve` is running
   - For API services: Check your API key and internet connection

2. **"CMake not found"**
   - Install CMake: `sudo apt-get install cmake` (Ubuntu) or `brew install cmake` (macOS)

3. **"Google Test not found"**
   - Ubuntu: `sudo apt-get install libgtest-dev`
   - macOS: `brew install googletest`
   - Windows: Use vcpkg or manual installation

4. **"No C++ files found"**
   - Ensure your source files have `.cpp`, `.cc`, or `.cxx` extensions
   - Check that the input directory path is correct

### Performance Tips

- Use Ollama locally for faster generation
- Start with smaller codebases (< 10 files) for initial testing
- Adjust `max_tokens` in config for longer/shorter generated tests

## Requirements

- **System Requirements:**
  - Python 3.8+
  - CMake 3.16+
  - GCC/Clang with C++17 support
  - Google Test framework
  - gcov for coverage analysis

- **LLM Provider (choose one):**
  - **Ollama** (recommended for local use): Install from [ollama.ai](https://ollama.ai)
  - **OpenAI API**: Requires API key from [platform.openai.com](https://platform.openai.com)
  - **GitHub Models**: Requires GitHub token with appropriate access

## Configuration

### Ollama Setup (Recommended)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the CodeLlama model
ollama pull codellama:13b

# Start Ollama service
ollama serve
```

### OpenAI Setup
1. Get API key from [OpenAI Platform](https://platform.openai.com)
2. Edit `config/llm_config.yaml`:
   ```yaml
   llm_settings:
     provider: "openai"
     openai:
       api_key: "your-openai-api-key"
       model: "gpt-4"
   ```

### GitHub Models Setup
1. Get GitHub token with appropriate permissions
2. Edit `config/llm_config.yaml`:
   ```yaml
   llm_settings:
     provider: "github"
     github:
       api_key: "your-github-token"
       model: "gpt-4"
   ``` 