#!/usr/bin/env python3
"""
Bug Hunter v2.0 Installation Test
=================================
Validates that Bug Hunter v2.0 is properly installed and configured.
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple


class InstallationTester:
    """Test suite for Bug Hunter v2.0 installation validation."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.home_dir = Path.home()
        self.test_results = []
        
        # Colors for output
        self.colors = {
            'GREEN': '\033[92m',
            'YELLOW': '\033[93m',
            'RED': '\033[91m',
            'BLUE': '\033[94m',
            'BOLD': '\033[1m',
            'END': '\033[0m'
        }
    
    def _print_colored(self, message: str, color: str = 'END'):
        """Print colored output."""
        print(f"{self.colors.get(color, '')}{message}{self.colors['END']}")
    
    def _print_header(self, title: str):
        """Print a section header."""
        print(f"\n{self.colors['BOLD']}{self.colors['BLUE']}{'='*60}{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['BLUE']} {title} {self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['BLUE']}{'='*60}{self.colors['END']}\n")
    
    def _test_result(self, test_name: str, passed: bool, message: str = ""):
        """Record and display test result."""
        icon = "✅" if passed else "❌"
        color = 'GREEN' if passed else 'RED'
        
        self._print_colored(f"{icon} {test_name}", color)
        if message:
            print(f"   {message}")
        
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'message': message
        })
    
    def test_python_version(self) -> bool:
        """Test Python version compatibility."""
        try:
            version = sys.version_info
            if version >= (3, 8):
                self._test_result(
                    "Python Version", 
                    True, 
                    f"Python {version.major}.{version.minor}.{version.micro}"
                )
                return True
            else:
                self._test_result(
                    "Python Version", 
                    False, 
                    f"Python 3.8+ required, found {version.major}.{version.minor}"
                )
                return False
        except Exception as e:
            self._test_result("Python Version", False, str(e))
            return False
    
    def test_package_imports(self) -> bool:
        """Test if Bug Hunter package can be imported."""
        try:
            # Test core imports
            from src.bug_hunter.config.settings import get_settings
            from src.bug_hunter.models.bug_report import BugReport
            from src.bug_hunter.core.similarity_engine import SimilarityEngine
            
            self._test_result("Package Imports", True, "All core modules imported successfully")
            return True
        except ImportError as e:
            self._test_result("Package Imports", False, f"Import error: {e}")
            return False
        except Exception as e:
            self._test_result("Package Imports", False, f"Unexpected error: {e}")
            return False
    
    def test_configuration_loading(self) -> bool:
        """Test configuration loading."""
        try:
            from src.bug_hunter.config.settings import get_settings
            settings = get_settings()
            
            self._test_result(
                "Configuration Loading", 
                True, 
                f"Loaded Bug Hunter v{settings.version}"
            )
            return True
        except Exception as e:
            self._test_result("Configuration Loading", False, str(e))
            return False
    
    def test_environment_file(self) -> bool:
        """Test if .env file exists and has required variables."""
        env_file = self.project_root / ".env"
        
        if not env_file.exists():
            self._test_result("Environment File", False, ".env file not found")
            return False
        
        try:
            content = env_file.read_text()
            required_vars = [
                "JIRA_BASE_URL",
                "JIRA_USERNAME", 
                "JIRA_API_TOKEN",
                "JIRA_PROJECT_KEY"
            ]
            
            missing_vars = []
            for var in required_vars:
                if f"{var}=" not in content or f"{var}=your-" in content:
                    missing_vars.append(var)
            
            if missing_vars:
                self._test_result(
                    "Environment File", 
                    False, 
                    f"Missing or unconfigured: {', '.join(missing_vars)}"
                )
                return False
            else:
                self._test_result("Environment File", True, "All required variables configured")
                return True
                
        except Exception as e:
            self._test_result("Environment File", False, str(e))
            return False
    
    def test_server_script(self) -> bool:
        """Test if optimized server script exists."""
        server_script = self.project_root / "optimized_bug_hunter_server.py"
        
        if server_script.exists() and server_script.is_file():
            self._test_result("Server Script", True, "optimized_bug_hunter_server.py found")
            return True
        else:
            self._test_result("Server Script", False, "optimized_bug_hunter_server.py not found")
            return False
    
    def test_directories(self) -> bool:
        """Test if required directories exist."""
        directories = [
            self.home_dir / ".bug-hunter" / "logs",
            self.home_dir / ".bug-hunter" / "cache",
            self.home_dir / ".bug-hunter" / "config"
        ]
        
        all_exist = True
        for directory in directories:
            if not directory.exists():
                self._test_result("Directories", False, f"Missing: {directory}")
                all_exist = False
        
        if all_exist:
            self._test_result("Directories", True, "All required directories exist")
        
        return all_exist
    
    def test_similarity_engine(self) -> bool:
        """Test similarity engine performance."""
        try:
            from src.bug_hunter.core.similarity_engine import SimilarityEngine
            from src.bug_hunter.config.settings import get_settings
            
            settings = get_settings()
            engine = SimilarityEngine(settings.similarity_settings)
            
            # Test basic similarity calculation
            start_time = time.time()
            score = engine.calculate_similarity(
                "Application error in user authentication module",
                "Authentication service throwing errors for user login"
            )
            end_time = time.time()
            
            duration_ms = (end_time - start_time) * 1000
            
            if score > 0.5 and duration_ms < 500:  # Should be fast and find similarity
                self._test_result(
                    "Similarity Engine", 
                    True, 
                    f"Score: {score:.2f}, Time: {duration_ms:.1f}ms"
                )
                return True
            else:
                self._test_result(
                    "Similarity Engine", 
                    False, 
                    f"Score: {score:.2f}, Time: {duration_ms:.1f}ms (may be slow)"
                )
                return False
                
        except Exception as e:
            self._test_result("Similarity Engine", False, str(e))
            return False
    
    def test_mcp_configuration(self) -> bool:
        """Test MCP configuration file."""
        # Check platform-specific MCP config location
        if sys.platform == "darwin":  # macOS
            config_path = self.home_dir / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        elif sys.platform == "win32":  # Windows
            config_path = Path(os.environ.get("APPDATA", "")) / "Claude" / "claude_desktop_config.json"
        else:  # Linux
            config_path = self.home_dir / ".config" / "Claude" / "claude_desktop_config.json"
        
        if not config_path.exists():
            self._test_result("MCP Configuration", False, f"Config not found at: {config_path}")
            return False
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            if "mcpServers" in config and "bug-hunter-optimized" in config["mcpServers"]:
                self._test_result("MCP Configuration", True, "Bug Hunter MCP server configured")
                return True
            else:
                self._test_result("MCP Configuration", False, "Bug Hunter server not found in MCP config")
                return False
                
        except Exception as e:
            self._test_result("MCP Configuration", False, str(e))
            return False
    
    def test_performance_optimization(self) -> bool:
        """Test if performance optimizations are enabled."""
        try:
            from src.bug_hunter.config.settings import get_settings
            settings = get_settings()
            
            optimizations = []
            if settings.performance_settings.enable_similarity_cache:
                optimizations.append("Similarity Cache")
            if settings.performance_settings.enable_async_processing:
                optimizations.append("Async Processing")
            if settings.performance_settings.enable_batch_processing:
                optimizations.append("Batch Processing")
            
            if len(optimizations) >= 2:
                self._test_result(
                    "Performance Optimization", 
                    True, 
                    f"Enabled: {', '.join(optimizations)}"
                )
                return True
            else:
                self._test_result(
                    "Performance Optimization", 
                    False, 
                    "Not enough optimizations enabled"
                )
                return False
                
        except Exception as e:
            self._test_result("Performance Optimization", False, str(e))
            return False
    
    def run_all_tests(self) -> Dict:
        """Run all installation tests."""
        self._print_header("🧪 Bug Hunter v2.0 Installation Test Suite")
        
        tests = [
            ("Python Version", self.test_python_version),
            ("Package Imports", self.test_package_imports),
            ("Configuration Loading", self.test_configuration_loading),
            ("Environment File", self.test_environment_file),
            ("Server Script", self.test_server_script),
            ("Directory Structure", self.test_directories),
            ("Similarity Engine", self.test_similarity_engine),
            ("MCP Configuration", self.test_mcp_configuration),
            ("Performance Optimization", self.test_performance_optimization)
        ]
        
        print("Running installation validation tests...\n")
        
        for test_name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                self._test_result(test_name, False, f"Test error: {e}")
        
        # Summary
        passed_tests = sum(1 for result in self.test_results if result['passed'])
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests) * 100
        
        self._print_header("📊 Test Results Summary")
        
        if success_rate == 100:
            self._print_colored(f"🎉 All tests passed! ({passed_tests}/{total_tests})", 'GREEN')
            self._print_colored("✅ Bug Hunter v2.0 is properly installed and ready to use!", 'GREEN')
        elif success_rate >= 80:
            self._print_colored(f"⚠️  Most tests passed ({passed_tests}/{total_tests} - {success_rate:.1f}%)", 'YELLOW')
            self._print_colored("🔧 Some configuration may be needed", 'YELLOW')
        else:
            self._print_colored(f"❌ Installation issues detected ({passed_tests}/{total_tests} - {success_rate:.1f}%)", 'RED')
            self._print_colored("🛠️  Please review the failed tests and run the installer again", 'RED')
        
        # Show next steps
        if success_rate >= 80:
            print(f"\n{self.colors['BOLD']}🚀 Next Steps:{self.colors['END']}")
            print("1. Start the server: python optimized_bug_hunter_server.py")
            print("2. Restart Cursor to load MCP integration")
            print("3. Test with: @bug-hunter get_system_status_optimized")
        
        return {
            'passed': passed_tests,
            'total': total_tests,
            'success_rate': success_rate,
            'results': self.test_results
        }


def main():
    """Main test runner."""
    tester = InstallationTester()
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    if results['success_rate'] == 100:
        sys.exit(0)
    elif results['success_rate'] >= 80:
        sys.exit(1)  # Some issues but mostly working
    else:
        sys.exit(2)  # Major issues


if __name__ == "__main__":
    main() 