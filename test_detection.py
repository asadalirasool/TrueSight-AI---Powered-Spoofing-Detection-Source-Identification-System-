#!/usr/bin/env python3
"""
Simple test script to verify the updated TrueSight detection system
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Add backend to path
backend_path = project_root / "backend"
sys.path.insert(0, str(backend_path))

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from app.services.video_detection import VideoDetectionService
        print("✅ VideoDetectionService imported successfully")
    except Exception as e:
        print(f"❌ Failed to import VideoDetectionService: {e}")
        return False
    
    try:
        from app.services.audio_detection import AudioDetectionService
        print("✅ AudioDetectionService imported successfully")
    except Exception as e:
        print(f"❌ Failed to import AudioDetectionService: {e}")
        return False
    
    try:
        from app.services.temporal_analyzer import TemporalAnalyzer
        print("✅ TemporalAnalyzer imported successfully")
    except Exception as e:
        print(f"❌ Failed to import TemporalAnalyzer: {e}")
        return False
    
    try:
        from app.services.lip_sync import LipSyncAnalyzer
        print("✅ LipSyncAnalyzer imported successfully")
    except Exception as e:
        print(f"❌ Failed to import LipSyncAnalyzer: {e}")
        return False
    
    return True

def test_model_loading():
    """Test that models can be loaded"""
    print("\n🔍 Testing model loading...")
    
    try:
        from app.services.video_detection import VideoDetectionService
        video_detector = VideoDetectionService()
        print("✅ Video detection service initialized")
    except Exception as e:
        print(f"❌ Failed to initialize video detection service: {e}")
        return False
    
    try:
        from app.services.audio_detection import AudioDetectionService
        audio_detector = AudioDetectionService()
        print("✅ Audio detection service initialized")
    except Exception as e:
        print(f"❌ Failed to initialize audio detection service: {e}")
        return False
    
    try:
        from app.services.temporal_analyzer import TemporalAnalyzer
        temporal_analyzer = TemporalAnalyzer()
        print("✅ Temporal analyzer initialized")
    except Exception as e:
        print(f"❌ Failed to initialize temporal analyzer: {e}")
        return False
    
    try:
        from app.services.lip_sync import LipSyncAnalyzer
        lip_sync_analyzer = LipSyncAnalyzer()
        print("✅ Lip sync analyzer initialized")
    except Exception as e:
        print(f"❌ Failed to initialize lip sync analyzer: {e}")
        return False
    
    return True

def test_detection_logic():
    """Test the detection logic with sample data"""
    print("\n🔍 Testing detection logic...")
    
    # Test ensemble scoring logic
    test_cases = [
        (0.7, "FAKE"),
        (0.65, "FAKE"), 
        (0.6, "SUSPICIOUS"),
        (0.5, "SUSPICIOUS"),
        (0.4, "SUSPICIOUS"),
        (0.35, "REAL"),
        (0.2, "REAL")
    ]
    
    from app.api.v1.endpoints.detection import get_verdict
    
    all_passed = True
    for conf, expected_verdict in test_cases:
        actual_verdict = get_verdict(conf)
        if actual_verdict == expected_verdict:
            print(f"  ✅ Confidence {conf} -> '{actual_verdict}'")
        else:
            print(f"  ❌ Confidence {conf} -> '{actual_verdict}', expected '{expected_verdict}'")
            all_passed = False
    
    if all_passed:
        print("✅ All ensemble scoring tests passed")
        return True
    else:
        print("❌ Some ensemble scoring tests failed")
        return False

def main():
    """Run all tests"""
    print("🚀 Running TrueSight Detection System Tests")
    print("=" * 50)
    
    # Run tests
    tests = [
        ("Import Tests", test_imports),
        ("Model Loading Tests", test_model_loading),
        ("Detection Logic Tests", test_detection_logic)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The updated TrueSight system is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please review the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)