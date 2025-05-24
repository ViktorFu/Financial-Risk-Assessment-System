#!/usr/bin/env python3
"""
Professional startup script for Financial Risk Assessment System
Handles environment setup, dependency checks, and application launch
"""
import os
import sys
import subprocess
import platform
import argparse
import time
from pathlib import Path
from typing import List, Dict, Any

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Try to import enhanced dependencies, fall back to basics
try:
    from config.settings import current_config
except ImportError as e:
    print(f"Warning: Could not import config: {e}")
    current_config = None

try:
    from Client.utils.logger import get_logger, logger_manager
except ImportError as e:
    print(f"Warning: Could not import logger: {e}")
    logger_manager = None
    get_logger = None


class SystemChecker:
    """System requirements and dependency checker"""
    
    REQUIRED_PYTHON_VERSION = (3, 8)
    REQUIRED_PACKAGES = [
        'PyQt5',
        'sqlite3'  # Essential packages only
    ]
    
    OPTIONAL_PACKAGES = [
        'psycopg2',
        'pandas',
        'numpy',
        'bcrypt',
        'cryptography',
        'loguru'
    ]
    
    def __init__(self):
        self.issues = []
        self.warnings = []
    
    def check_python_version(self) -> bool:
        """Check if Python version meets requirements"""
        current_version = sys.version_info[:2]
        if current_version < self.REQUIRED_PYTHON_VERSION:
            self.issues.append(
                f"Python {'.'.join(map(str, self.REQUIRED_PYTHON_VERSION))}+ required, "
                f"but {'.'.join(map(str, current_version))} found"
            )
            return False
        return True
    
    def check_dependencies(self) -> bool:
        """Check if required packages are installed"""
        missing_required = []
        missing_optional = []
        
        # Check required packages
        for package in self.REQUIRED_PACKAGES:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing_required.append(package)
        
        # Check optional packages
        for package in self.OPTIONAL_PACKAGES:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing_optional.append(package)
        
        if missing_required:
            self.issues.append(f"Missing required packages: {', '.join(missing_required)}")
            return False
        
        if missing_optional:
            self.warnings.append(f"Missing optional packages (enhanced features unavailable): {', '.join(missing_optional)}")
        
        return True
    
    def check_database_file(self) -> bool:
        """Check if database file exists and is accessible"""
        if current_config and hasattr(current_config, 'DB_TYPE') and current_config.DB_TYPE == 'sqlite':
            db_path = Path(project_root) / 'Client' / current_config.DB_NAME
            if not db_path.exists():
                self.warnings.append(f"Database file {db_path} not found - will be created")
            elif not os.access(db_path, os.R_OK | os.W_OK):
                self.issues.append(f"Database file {db_path} is not accessible")
                return False
        
        return True
    
    def check_display(self) -> bool:
        """Check if display is available (for GUI applications)"""
        if platform.system() == 'Linux':
            if not os.environ.get('DISPLAY'):
                self.warnings.append("No DISPLAY environment variable set")
                return False
        return True
    
    def check_all(self) -> bool:
        """Run all system checks"""
        checks = [
            self.check_python_version,
            self.check_dependencies,
            self.check_database_file,
            self.check_display
        ]
        
        all_passed = True
        for check in checks:
            try:
                if not check():
                    all_passed = False
            except Exception as e:
                self.warnings.append(f"Check failed: {e}")
        
        return all_passed


class DependencyInstaller:
    """Automatic dependency installer"""
    
    def __init__(self):
        self.pip_command = self._get_pip_command()
    
    def _get_pip_command(self) -> List[str]:
        """Get the appropriate pip command for the current system"""
        python_exe = sys.executable
        return [python_exe, '-m', 'pip']
    
    def install_requirements(self, requirements_file: str = 'requirements.txt') -> bool:
        """Install packages from requirements file"""
        requirements_path = project_root.parent / requirements_file
        
        if not requirements_path.exists():
            print(f"Requirements file {requirements_path} not found")
            return False
        
        print(f"Installing dependencies from {requirements_file}...")
        try:
            cmd = self.pip_command + ['install', '-r', str(requirements_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install dependencies: {e}")
            print(f"Error output: {e.stderr}")
            return False
    
    def install_package(self, package: str) -> bool:
        """Install a specific package"""
        print(f"Installing {package}...")
        try:
            cmd = self.pip_command + ['install', package]
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"{package} installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}: {e}")
            return False


class ApplicationLauncher:
    """Application launcher with various modes"""
    
    def __init__(self):
        self.logger = None
        if current_config and get_logger:
            try:
                self.logger = get_logger(__name__)
            except Exception:
                pass
    
    def _log(self, message: str, level: str = 'info'):
        """Log message if logger is available"""
        if self.logger:
            try:
                getattr(self.logger, level)(message)
            except:
                print(f"[{level.upper()}] {message}")
        else:
            print(f"[{level.upper()}] {message}")
    
    def run_gui_mode(self) -> int:
        """Launch the GUI application"""
        self._log("Starting Financial Risk Assessment System (GUI Mode)")
        
        try:
            # Import and run the main application
            from main import App
            
            app = App(sys.argv)
            return app.exec_()
            
        except ImportError as e:
            self._log(f"Failed to import main application: {e}", 'error')
            return 1
        except Exception as e:
            self._log(f"Application error: {e}", 'error')
            return 1
    
    def run_api_mode(self) -> int:
        """Launch the API server (if implemented)"""
        self._log("Starting Financial Risk Assessment System (API Mode)")
        
        try:
            # TODO: Implement API server launch
            self._log("API mode not yet implemented", 'warning')
            return 1
        except Exception as e:
            self._log(f"API server error: {e}", 'error')
            return 1
    
    def run_cli_mode(self, command: str) -> int:
        """Run CLI commands"""
        self._log(f"Running CLI command: {command}")
        
        if command == 'test':
            return self._run_tests()
        elif command == 'migrate':
            return self._run_migrations()
        elif command == 'backup':
            return self._create_backup()
        else:
            self._log(f"Unknown CLI command: {command}", 'error')
            return 1
    
    def _run_tests(self) -> int:
        """Run the test suite"""
        try:
            import pytest
            test_dir = project_root.parent / 'tests'
            if test_dir.exists():
                return pytest.main([str(test_dir), '-v'])
            else:
                self._log("Test directory not found", 'warning')
                return 1
        except ImportError:
            self._log("pytest not installed", 'error')
            return 1
    
    def _run_migrations(self) -> int:
        """Run database migrations"""
        try:
            from Client.models.database import init_database
            init_database('./CSV')
            self._log("Database migrations completed successfully")
            return 0
        except Exception as e:
            self._log(f"Migration failed: {e}", 'error')
            return 1
    
    def _create_backup(self) -> int:
        """Create system backup"""
        try:
            # TODO: Implement backup functionality
            self._log("Backup functionality not yet implemented", 'warning')
            return 1
        except Exception as e:
            self._log(f"Backup failed: {e}", 'error')
            return 1


def print_banner():
    """Print application banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║              Financial Risk Assessment System                 ║
    ║                      Professional Edition                     ║
    ║                         Version 2.0.0                        ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main startup function"""
    parser = argparse.ArgumentParser(
        description='Financial Risk Assessment System Launcher',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                    # Launch GUI application
  python run.py --mode api         # Launch API server
  python run.py --mode cli test    # Run tests
  python run.py --check-only       # Check system requirements only
  python run.py --install-deps     # Install missing dependencies
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['gui', 'api', 'cli'],
        default='gui',
        help='Application mode (default: gui)'
    )
    
    parser.add_argument(
        '--command',
        help='CLI command to run (for cli mode)'
    )
    
    parser.add_argument(
        '--check-only',
        action='store_true',
        help='Only check system requirements'
    )
    
    parser.add_argument(
        '--install-deps',
        action='store_true',
        help='Install missing dependencies'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )
    
    parser.add_argument(
        '--no-banner',
        action='store_true',
        help='Skip banner display'
    )
    
    args = parser.parse_args()
    
    # Print banner unless suppressed
    if not args.no_banner:
        print_banner()
    
    # System checks
    print("Checking system requirements...")
    checker = SystemChecker()
    system_ok = checker.check_all()
    
    # Report issues and warnings
    if checker.issues:
        print("\n❌ System Issues Found:")
        for issue in checker.issues:
            print(f"  • {issue}")
    
    if checker.warnings:
        print("\n⚠️  Warnings:")
        for warning in checker.warnings:
            print(f"  • {warning}")
    
    if system_ok:
        print("✅ System checks passed")
    else:
        print("❌ System checks failed")
        
        if args.install_deps:
            print("\nAttempting to install missing dependencies...")
            installer = DependencyInstaller()
            if installer.install_requirements():
                print("Dependencies installed. Please restart the application.")
                return 0
            else:
                print("Failed to install dependencies.")
                return 1
        else:
            print("Use --install-deps to automatically install missing dependencies")
            return 1
    
    # Exit if only checking
    if args.check_only:
        return 0
    
    # Launch application
    launcher = ApplicationLauncher()
    
    print(f"\nStarting application in {args.mode} mode...")
    
    if args.mode == 'gui':
        return launcher.run_gui_mode()
    elif args.mode == 'api':
        return launcher.run_api_mode()
    elif args.mode == 'cli':
        if not args.command:
            print("CLI mode requires --command argument")
            return 1
        return launcher.run_cli_mode(args.command)
    
    return 0


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        if '--verbose' in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1) 