#!/usr/bin/env python3
"""
TrueSight Complete Setup & Automation Wizard

One-command setup that:
1. Downloads small test datasets
2. Verifies system components
3. Trains models (optional)
4. Runs health checks
5. Executes end-to-end tests

Usage:
    python setup_complete.py [--quick] [--train] [--test] [--all]
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from loguru import logger

# Configure logger
logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>")


class SetupWizard:
    """Complete setup wizard for TrueSight"""
    
    def __init__(self, quick_mode: bool = False, train_models: bool = False, run_tests: bool = False):
        self.quick_mode = quick_mode
        self.train_models = train_models
        self.run_tests = run_tests
        self.steps_completed = []
        self.steps_failed = []
        
    def run_step(self, step_name: str, command: str, required: bool = True) -> bool:
        """Run a setup step"""
        logger.info(f"\n{'='*80}")
        logger.info(f"📍 STEP: {step_name}")
        logger.info(f"{'='*80}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=False,
                text=True
            )
            
            logger.info(f"✅ {step_name} completed successfully")
            self.steps_completed.append(step_name)
            return True
            
        except subprocess.CalledProcessError as e:
            if required:
                logger.error(f"❌ {step_name} failed")
                self.steps_failed.append(step_name)
                return False
            else:
                logger.warning(f"⚠️ {step_name} failed (non-critical)")
                self.steps_completed.append(f"{step_name} (partial)")
                return True
    
    def step_welcome(self):
        """Welcome message"""
        logger.info("\n" + "="*80)
        logger.info("🚀 TRUE SIGHT - COMPLETE SETUP WIZARD")
        logger.info("="*80)
        logger.info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Mode: {'Quick' if self.quick_mode else 'Full'}")
        logger.info(f"Training: {'Yes' if self.train_models else 'No'}")
        logger.info(f"Testing: {'Yes' if self.run_tests else 'No'}")
        logger.info("="*80)
        
    def step_check_python(self) -> bool:
        """Check Python installation"""
        logger.info("\n🔍 Checking Python Installation")
        
        version = sys.version_info
        logger.info(f"Python version: {version.major}.{version.minor}.{version.micro}")
        
        if version.major == 3 and version.minor >= 9:
            logger.info("✅ Python version OK")
            return True
        else:
            logger.error("❌ Python 3.9+ required")
            return False
    
    def step_install_dependencies(self) -> bool:
        """Install Python dependencies"""
        return self.run_step(
            "Install Dependencies",
            "pip install -r backend/requirements.txt",
            required=True
        )
    
    def step_verify_system(self) -> bool:
        """Run system verification"""
        return self.run_step(
            "System Verification",
            "python scripts/verify_system.py",
            required=True
        )
    
    def step_download_datasets(self) -> bool:
        """Download test datasets"""
        return self.run_step(
            "Download Test Datasets",
            "python scripts/download_quick_datasets.py",
            required=False
        )
    
    def step_train_models(self) -> bool:
        """Train all models"""
        if not self.train_models:
            logger.info("⏭️ Skipping model training (use --train to enable)")
            return True
        
        models_to_train = [
            ("AI Percentage Model", "python backend/train_ai_percentage.py --epochs 10"),
        ]
        
        all_success = True
        for name, cmd in models_to_train:
            success = self.run_step(f"Train {name}", cmd, required=False)
            if not success:
                all_success = False
        
        return all_success
    
    def step_health_check(self) -> bool:
        """Run health check"""
        return self.run_step(
            "Health Check",
            "python scripts/health_check.py",
            required=False
        )
    
    def step_run_tests(self) -> bool:
        """Run end-to-end tests"""
        if not self.run_tests:
            logger.info("⏭️ Skipping tests (use --test to enable)")
            return True
        
        return self.run_step(
            "End-to-End Tests",
            "python scripts/test_end_to_end.py",
            required=False
        )
    
    def step_start_server(self):
        """Instructions to start server"""
        logger.info("\n" + "="*80)
        logger.info("🎉 SETUP COMPLETE!")
        logger.info("="*80)
        
        logger.info("\n📋 NEXT STEPS:")
        logger.info("\n1️⃣  Start Backend Server:")
        logger.info("   cd backend")
        logger.info("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        
        logger.info("\n2️⃣  Start Frontend (in new terminal):")
        logger.info("   cd frontend")
        logger.info("   npm install")
        logger.info("   npm start")
        
        logger.info("\n3️⃣  Access Application:")
        logger.info("   Frontend: http://localhost:3000")
        logger.info("   API Docs: http://localhost:8000/docs")
        
        logger.info("\n4️⃣  Test AI Percentage Feature:")
        logger.info("   curl -X POST http://localhost:8000/api/v1/analyze/ai-percentage \\")
        logger.info('     -F "file=@test_videos/test_video.mp4"')
        
        logger.info("\n5️⃣  Monitor Health:")
        logger.info("   python scripts/health_check.py --watch")
        
        logger.info("\n" + "="*80)
    
    def generate_report(self):
        """Generate setup report"""
        logger.info("\n" + "="*80)
        logger.info("📊 SETUP REPORT")
        logger.info("="*80)
        
        logger.info(f"\n✅ Completed: {len(self.steps_completed)} steps")
        for step in self.steps_completed:
            logger.info(f"   • {step}")
        
        if self.steps_failed:
            logger.info(f"\n❌ Failed: {len(self.steps_failed)} steps")
            for step in self.steps_failed:
                logger.info(f"   • {step}")
        
        logger.info("\n" + "="*80)
        
        if not self.steps_failed:
            logger.info("✅ ALL CRITICAL STEPS COMPLETED SUCCESSFULLY!")
        else:
            logger.warning("⚠️ Some steps failed. Review report above.")
        
        logger.info("="*80)
    
    def run_all(self):
        """Run complete setup"""
        self.step_welcome()
        
        # Critical steps (must succeed)
        if not self.step_check_python():
            logger.error("❌ Python check failed. Aborting.")
            sys.exit(1)
        
        # Run all steps
        self.step_install_dependencies()
        self.step_verify_system()
        self.step_download_datasets()
        self.step_train_models()
        self.step_health_check()
        self.step_run_tests()
        
        # Generate report
        self.generate_report()
        self.step_start_server()


def main():
    parser = argparse.ArgumentParser(
        description="TrueSight Complete Setup Wizard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick setup (no training, no tests)
  python setup_complete.py --quick
  
  # Full setup with training
  python setup_complete.py --train
  
  # Full setup with testing
  python setup_complete.py --test
  
  # Complete automation (everything)
  python setup_complete.py --all
        """
    )
    
    parser.add_argument("--quick", action="store_true", help="Quick setup mode")
    parser.add_argument("--train", action="store_true", help="Train models after setup")
    parser.add_argument("--test", action="store_true", help="Run tests after setup")
    parser.add_argument("--all", action="store_true", help="Run everything (train + test)")
    
    args = parser.parse_args()
    
    # If --all, enable both train and test
    if args.all:
        args.train = True
        args.test = True
    
    wizard = SetupWizard(
        quick_mode=args.quick,
        train_models=args.train,
        run_tests=args.test
    )
    
    wizard.run_all()


if __name__ == "__main__":
    main()
