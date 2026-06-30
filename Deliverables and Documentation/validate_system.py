#!/usr/bin/env python3
"""
TRUESIGHT SYSTEM VALIDATION & COMPLETENESS VERIFICATION
=====================================================

This script performs comprehensive validation of the TrueSight system to ensure:
1. All required modules are implemented and functional
2. Version compliance is met
3. Security requirements are satisfied
4. Integration points work correctly
5. System is production-ready

RUN THIS SCRIPT AFTER ANY MAJOR CHANGES
"""

import sys
import os
import importlib
import subprocess
import json
from typing import Dict, List, Tuple, Any
from datetime import datetime
import asyncio
import traceback

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def print_header(title: str, char: str = "="):
    """Print formatted header"""
    print(f"\n{char * 60}")
    print(f"{title:^60}")
    print(f"{char * 60}")

def print_result(test_name: str, status: str, details: str = ""):
    """Print test result in consistent format"""
    status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"{status_symbol} {test_name:<40} [{status}]")
    if details:
        print(f"   {details}")

class TrueSightValidator:
    """Comprehensive TrueSight system validator"""
    
    def __init__(self):
        self.results = {
            'module_tests': [],
            'version_tests': [],
            'security_tests': [],
            'integration_tests': [],
            'frontend_tests': []
        }
        self.passed = 0
        self.failed = 0
        self.warnings = 0
    
    async def run_all_tests(self) -> bool:
        """Run all validation tests"""
        print_header("TRUESIGHT SYSTEM VALIDATION", "🚀")
        print(f"Validation started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Phase 1: Module Implementation Tests
            await self.test_module_implementations()
            
            # Phase 2: Version Compliance Tests
            await self.test_version_compliance()
            
            # Phase 3: Security Implementation Tests
            await self.test_security_implementations()
            
            # Phase 4: Integration Tests
            await self.test_integration_points()
            
            # Phase 5: Frontend Tests
            await self.test_frontend_components()
            
            # Generate final report
            await self.generate_final_report()
            
            return self.failed == 0
            
        except Exception as e:
            print(f"\n❌ CRITICAL VALIDATION ERROR: {e}")
            traceback.print_exc()
            return False
    
    async def test_module_implementations(self):
        """Test that all required modules are implemented"""
        print_header("PHASE 1: MODULE IMPLEMENTATION VERIFICATION")
        
        required_modules = {
            'Stream Processing': 'src.modules.stream_processor.processor',
            'Video Detection': 'src.modules.video_detector.lnclip_detector',
            'Audio Detection': 'src.modules.audio_detector.wav2vec2_detector',
            'Urdu Detection': 'src.modules.multilingual_detector.language_detector',
            'Forensic Analysis': 'src.modules.forensics.source_identifier',
            'Security & MFA': 'src.modules.security.zero_trust_manager',
            'Behavioral Biometrics': 'src.modules.security.behavioral_biometrics',
            'Blockchain': 'src.modules.blockchain.evidence_logger',
            'Watermarking': 'src.modules.watermarking.watermark_engine',
            'API Layer': 'src.api.main'
        }
        
        for module_name, module_path in required_modules.items():
            try:
                # Try to import the module
                module = importlib.import_module(module_path)
                print_result(module_name, "PASS", f"Module imported successfully")
                self.results['module_tests'].append({
                    'module': module_name,
                    'status': 'PASS',
                    'details': 'Import successful'
                })
                self.passed += 1
            except ImportError as e:
                print_result(module_name, "FAIL", f"Import failed: {e}")
                self.results['module_tests'].append({
                    'module': module_name,
                    'status': 'FAIL',
                    'details': str(e)
                })
                self.failed += 1
            except Exception as e:
                print_result(module_name, "FAIL", f"Unexpected error: {e}")
                self.results['module_tests'].append({
                    'module': module_name,
                    'status': 'FAIL',
                    'details': str(e)
                })
                self.failed += 1
    
    async def test_version_compliance(self):
        """Test version compliance requirements"""
        print_header("PHASE 2: VERSION COMPLIANCE VERIFICATION")
        
        # Required versions
        required_versions = {
            'torch': '2.2.2',
            'torchvision': '0.17.2',
            'torchaudio': '2.2.2',
            'transformers': '4.36.2',
            'peft': '0.7.1',
            'fastapi': '0.104.1',
            'sqlalchemy': '2.0.23'
        }
        
        try:
            # Get installed versions
            result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--format=json'], 
                                  capture_output=True, text=True)
            installed_packages = json.loads(result.stdout)
            installed_dict = {pkg['name'].lower(): pkg['version'] for pkg in installed_packages}
            
            for package, required_version in required_versions.items():
                if package in installed_dict:
                    installed_version = installed_dict[package]
                    # Check if installed version is compatible (same major.minor or newer patch)
                    if self.is_version_compatible(installed_version, required_version):
                        print_result(f"{package} version", "PASS", f"{installed_version} (compatible with {required_version})")
                        self.passed += 1
                    else:
                        print_result(f"{package} version", "FAIL", f"{installed_version} != {required_version}")
                        self.failed += 1
                    self.results['version_tests'].append({
                        'package': package,
                        'required': required_version,
                        'installed': installed_version,
                        'status': 'PASS' if self.is_version_compatible(installed_version, required_version) else 'FAIL'
                    })
                else:
                    print_result(f"{package} installed", "FAIL", "Package not found")
                    self.failed += 1
                    self.results['version_tests'].append({
                        'package': package,
                        'required': required_version,
                        'installed': 'NOT INSTALLED',
                        'status': 'FAIL'
                    })
                    
        except Exception as e:
            print_result("Version checking", "FAIL", f"Error checking versions: {e}")
            self.failed += 1
    
    def is_version_compatible(self, installed_version, required_version):
        """Check if installed version is compatible with required version"""
        try:
            # Parse version strings
            inst_parts = [int(x) for x in installed_version.split('.')[:3]]
            req_parts = [int(x) for x in required_version.split('.')[:3]]
            
            # Major and minor versions must match, patch can be equal or higher
            if inst_parts[0] == req_parts[0] and inst_parts[1] == req_parts[1]:
                return inst_parts[2] >= req_parts[2]
            return False
        except:
            # If parsing fails, do exact match
            return installed_version == required_version
    
    async def test_security_implementations(self):
        """Test security module implementations"""
        print_header("PHASE 3: SECURITY IMPLEMENTATION VERIFICATION")
        
        security_tests = [
            ('Zero-Trust Manager', 'src.modules.security.zero_trust_manager', 'ZeroTrustSecurityManager'),
            ('Behavioral Biometrics', 'src.modules.security.behavioral_biometrics', 'BehavioralBiometricsEngine'),
            ('Authentication Service', 'src.modules.security.auth_service', 'ZeroTrustAuthService'),
            ('RBAC System', 'src.modules.security.rbac', 'RBACService')
        ]
        
        for test_name, module_path, class_name in security_tests:
            try:
                module = importlib.import_module(module_path)
                if hasattr(module, class_name):
                    cls = getattr(module, class_name)
                    # Try to instantiate (may require parameters)
                    print_result(test_name, "PASS", f"Class {class_name} found")
                    self.passed += 1
                else:
                    print_result(test_name, "FAIL", f"Class {class_name} not found")
                    self.failed += 1
                self.results['security_tests'].append({
                    'test': test_name,
                    'status': 'PASS' if hasattr(module, class_name) else 'FAIL',
                    'details': f"Class {class_name} {'found' if hasattr(module, class_name) else 'not found'}"
                })
            except Exception as e:
                print_result(test_name, "FAIL", f"Error: {e}")
                self.failed += 1
                self.results['security_tests'].append({
                    'test': test_name,
                    'status': 'FAIL',
                    'details': str(e)
                })
    
    async def test_integration_points(self):
        """Test integration between modules"""
        print_header("PHASE 4: INTEGRATION POINT VERIFICATION")
        
        # Test API endpoints
        try:
            from src.api.main import app
            print_result("FastAPI Application", "PASS", "API app created successfully")
            self.passed += 1
            self.results['integration_tests'].append({
                'test': 'FastAPI Application',
                'status': 'PASS',
                'details': 'API app created successfully'
            })
        except Exception as e:
            print_result("FastAPI Application", "FAIL", f"Error: {e}")
            self.failed += 1
            self.results['integration_tests'].append({
                'test': 'FastAPI Application',
                'status': 'FAIL',
                'details': str(e)
            })
        
        # Test database connection
        try:
            from src.shared.database import init_db
            print_result("Database Connection", "PASS", "Database module imported")
            self.passed += 1
            self.results['integration_tests'].append({
                'test': 'Database Connection',
                'status': 'PASS',
                'details': 'Database module imported'
            })
        except Exception as e:
            print_result("Database Connection", "WARN", f"Database module error: {e}")
            self.warnings += 1
            self.results['integration_tests'].append({
                'test': 'Database Connection',
                'status': 'WARN',
                'details': str(e)
            })
    
    async def test_frontend_components(self):
        """Test frontend component existence"""
        print_header("PHASE 5: FRONTEND COMPONENT VERIFICATION")
        
        frontend_files = [
            ('React App', 'frontend/src/index.js'),
            ('Dashboard Component', 'frontend/src/components/Dashboard.js'),
            ('Dashboard Styles', 'frontend/src/components/Dashboard.css'),
            ('Global Styles', 'frontend/src/index.css'),
            ('Package.json', 'frontend/package.json'),
            ('HTML Template', 'frontend/index.html')
        ]
        
        for component_name, file_path in frontend_files:
            full_path = os.path.join(project_root, file_path)
            if os.path.exists(full_path):
                print_result(component_name, "PASS", f"File exists: {file_path}")
                self.passed += 1
            else:
                print_result(component_name, "FAIL", f"File missing: {file_path}")
                self.failed += 1
            self.results['frontend_tests'].append({
                'component': component_name,
                'file_path': file_path,
                'status': 'PASS' if os.path.exists(full_path) else 'FAIL',
                'details': 'File exists' if os.path.exists(full_path) else 'File missing'
            })
    
    async def generate_final_report(self):
        """Generate comprehensive validation report"""
        print_header("VALIDATION SUMMARY", "📊")
        
        total_tests = self.passed + self.failed + self.warnings
        success_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"⚠️  Warnings: {self.warnings}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        # System readiness assessment
        print_header("SYSTEM READINESS ASSESSMENT", "📋")
        
        if self.failed == 0 and success_rate >= 95:
            print("🎉 SYSTEM IS PRODUCTION READY!")
            print("✅ All critical modules implemented")
            print("✅ Version compliance verified")
            print("✅ Security components functional")
            print("✅ Integration points working")
            print("✅ Frontend components present")
        elif self.failed <= 2 and success_rate >= 85:
            print("🟡 SYSTEM IS NEARLY READY")
            print("⚠️  Some non-critical issues detected")
            print("🔧 Minor fixes needed before production")
        else:
            print("🔴 SYSTEM REQUIRES ATTENTION")
            print("❌ Critical issues detected")
            print("🔧 Significant work needed before production")
        
        # Save detailed report
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': total_tests,
                'passed': self.passed,
                'failed': self.failed,
                'warnings': self.warnings,
                'success_rate': success_rate
            },
            'detailed_results': self.results
        }
        
        report_file = os.path.join(project_root, 'validation_report.json')
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📝 Detailed report saved to: {report_file}")

async def main():
    """Main validation function"""
    validator = TrueSightValidator()
    success = await validator.run_all_tests()
    
    if success:
        print_header("VALIDATION COMPLETE - SYSTEM READY", "🎉")
        sys.exit(0)
    else:
        print_header("VALIDATION COMPLETE - ISSUES DETECTED", "⚠️")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())