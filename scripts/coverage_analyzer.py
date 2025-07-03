"""Coverage Analyzer for measuring test coverage using gcov"""

import os
import subprocess
import re
import json
from pathlib import Path
from typing import Dict, List, Optional

class CoverageAnalyzer:
    """Analyzer for measuring test coverage"""
    
    def __init__(self):
        self.gcov_data_extensions = {'.gcda', '.gcno'}
    
    def analyze(self, source_dir: str, test_dir: str) -> Dict:
        """Analyze test coverage"""
        try:
            build_dir = os.path.join(test_dir, "build")
            
            # Check if coverage data exists
            if not self._has_coverage_data(build_dir):
                return {
                    'error': 'No coverage data found',
                    'line_coverage': 0.0,
                    'branch_coverage': 0.0,
                    'function_coverage': 0.0,
                    'files': []
                }
            
            # Generate coverage report
            coverage_data = self._generate_coverage_report(source_dir, build_dir)
            
            # Parse coverage data
            parsed_data = self._parse_coverage_data(coverage_data, source_dir)
            
            return parsed_data
            
        except Exception as e:
            return {
                'error': str(e),
                'line_coverage': 0.0,
                'branch_coverage': 0.0,
                'function_coverage': 0.0,
                'files': []
            }
    
    def _has_coverage_data(self, build_dir: str) -> bool:
        """Check if coverage data files exist"""
        for root, dirs, files in os.walk(build_dir):
            for file in files:
                if Path(file).suffix in self.gcov_data_extensions:
                    return True
        return False
    
    def _generate_coverage_report(self, source_dir: str, build_dir: str) -> str:
        """Generate coverage report using gcov"""
        try:
            # Find .gcda files
            gcda_files = []
            for root, dirs, files in os.walk(build_dir):
                for file in files:
                    if file.endswith('.gcda'):
                        gcda_files.append(os.path.join(root, file))
            
            if not gcda_files:
                return ""
            
            # Run gcov on the files
            coverage_output = ""
            
            for gcda_file in gcda_files:
                try:
                    # Change to the directory containing the .gcda file
                    gcda_dir = os.path.dirname(gcda_file)
                    
                    # Run gcov
                    result = subprocess.run(
                        ['gcov', '-b', '-c', gcda_file],
                        capture_output=True,
                        text=True,
                        cwd=gcda_dir,
                        timeout=60
                    )
                    
                    if result.returncode == 0:
                        coverage_output += result.stdout + "\n"
                    
                except subprocess.TimeoutExpired:
                    print(f"gcov timeout for {gcda_file}")
                except Exception as e:
                    print(f"gcov failed for {gcda_file}: {e}")
            
            return coverage_output
            
        except Exception as e:
            print(f"Error generating coverage report: {e}")
            return ""
    
    def _parse_coverage_data(self, coverage_output: str, source_dir: str) -> Dict:
        """Parse gcov output to extract coverage information"""
        result = {
            'line_coverage': 0.0,
            'branch_coverage': 0.0,
            'function_coverage': 0.0,
            'files': []
        }
        
        if not coverage_output:
            return result
        
        try:
            lines = coverage_output.split('\n')
            total_lines = 0
            covered_lines = 0
            
            for line in lines:
                if 'Lines executed:' in line:
                    match = re.search(r"Lines executed:(\d+\.\d+)% of (\d+)", line)
                    if match:
                        percent = float(match.group(1))
                        count = int(match.group(2))
                        
                        total_lines += count
                        covered_lines += int(count * percent / 100)
            
            if total_lines > 0:
                result['line_coverage'] = (covered_lines / total_lines) * 100
            
        except Exception as e:
            print(f"Error parsing coverage data: {e}")
        
        return result 