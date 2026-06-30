#!/usr/bin/env python3
"""
Simple TrueSight System Test
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_system_components():
    """Test that all system components can be imported"""
    print("🧪 Testing TrueSight System Components")
    print("=" * 50)
    
    components = [
        ("Video Detector", "src.modules.video_detector.detector", "EnhancedVideoDetector"),
        ("Audio Detector", "src.modules.audio_detector.detector", "EnhancedAudioDetector"),
        ("Urdu Detector", "src.modules.multilingual_detector.language_detector", "UrduMultilingualDetector"),
        ("Forensic Analyzer", "src.modules.forensics.analyzer", "ForensicAnalyzer"),
        ("Security Service", "src.modules.security.auth_service", "AuthService"),
        ("Blockchain Logger", "src.modules.blockchain.evidence_logger", "BlockchainEvidenceLogger"),
        ("Watermark Engine", "src.modules.watermarking.watermark_engine", "WatermarkEngine"),
        ("Stream Processor", "src.modules.stream_processor.processor", "StreamProcessor")
    ]
    
    passed = 0
    total = len(components)
    
    for name, module_path, class_name in components:
        try:
            module = __import__(module_path, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✅ {name}: PASS")
            passed += 1
        except Exception as e:
            print(f"❌ {name}: FAIL - {str(e)[:50]}...")
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} components working")
    print(f"📈 Success Rate: {passed/total*100:.1f}%")
    
    return passed == total

def test_api_availability():
    """Test if API can be imported"""
    print("\n🌐 Testing API Availability")
    print("=" * 30)
    
    try:
        from src.api.main import app
        print("✅ FastAPI application imported successfully")
        print("✅ API routes loaded")
        return True
    except Exception as e:
        print(f"❌ API import failed: {e}")
        return False

def main():
    print("🚀 TRUESEEK SYSTEM HEALTH CHECK")
    print("=" * 50)
    
    # Test components
    components_ok = test_system_components()
    
    # Test API
    api_ok = test_api_availability()
    
    print("\n" + "=" * 50)
    print("📋 FINAL SYSTEM STATUS")
    print("=" * 30)
    
    if components_ok and api_ok:
        print("🟢 SYSTEM IS FULLY OPERATIONAL")
        print("✅ All components loaded successfully")
        print("✅ API is ready for requests")
        print("\n🚀 You can now:")
        print("   - Start the full system with: python launch_full_system.py")
        print("   - Run the API server with: python run_api.py")
        print("   - Access the web interface at: http://localhost:3000")
        print("   - View API docs at: http://localhost:8000/docs")
    else:
        print("🟡 SYSTEM HAS SOME ISSUES")
        if not components_ok:
            print("❌ Some core components failed to load")
        if not api_ok:
            print("❌ API server has import issues")
        print("\n🔧 Troubleshooting steps:")
        print("   1. Check that all dependencies are installed")
        print("   2. Verify Python version compatibility")
        print("   3. Run validation script: python validate_system.py")

if __name__ == "__main__":
    main()