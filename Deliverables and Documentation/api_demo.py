"""
TrueSight API Demo Script
Demonstrates the running TrueSight system capabilities
"""

import requests
import json
from datetime import datetime

def demo_truesight_api():
    """Demonstrate TrueSight API capabilities"""
    
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("🚀 TRUESEEK SYSTEM DEMONSTRATION")
    print("=" * 60)
    print(f"🕒 Demo Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test 1: Root endpoint
    print("📋 1. SYSTEM INFORMATION")
    print("-" * 30)
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ System Name: {data['name']}")
            print(f"✅ Version: {data['version']}")
            print(f"✅ Status: {data['status']}")
            print(f"✅ Video Detector: {data['detectors']['video']}")
            print(f"✅ Audio Detector: {data['detectors']['audio']}")
            print(f"✅ Multilingual Detector: {data['detectors']['multilingual']}")
        else:
            print(f"❌ Failed to get system info: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test 2: Health check
    print("🏥 2. SYSTEM HEALTH")
    print("-" * 30)
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Overall Status: {data['status']}")
            print(f"✅ GPU Available: {data['gpu_available']}")
            print(f"✅ Video Detector: {data['detectors']['video']}")
            print(f"✅ Audio Detector: {data['detectors']['audio']}")
            print(f"✅ Multilingual Detector: {data['detectors']['multilingual']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test 3: Capabilities
    print("⚡ 3. SYSTEM CAPABILITIES")
    print("-" * 30)
    try:
        response = requests.get(f"{base_url}/capabilities")
        if response.status_code == 200:
            data = response.json()
            
            print("🎥 VIDEO DETECTION METHODS:")
            for method in data['video_detection']['methods']:
                print(f"   • {method}")
            print(f"   Device: {data['video_detection']['device']}")
            
            print("\n🎵 AUDIO DETECTION METHODS:")
            for method in data['audio_detection']['methods']:
                print(f"   • {method}")
            print(f"   Device: {data['audio_detection']['device']}")
            
            print("\n🌍 MULTILINGUAL DETECTION FEATURES:")
            for feature in data['multilingual_detection']['features']:
                print(f"   • {feature}")
            print(f"   Phonemes Loaded: {data['multilingual_detection']['phonemes_loaded']}")
            print(f"   Device: {data['multilingual_detection']['device']}")
            
        else:
            print(f"❌ Capabilities check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test 4: Simulated detection (showing the API structure)
    print("🔍 4. DETECTION API STRUCTURE")
    print("-" * 30)
    print("Available Detection Endpoints:")
    print("   POST /detect/video     - Video deepfake detection")
    print("   POST /detect/audio     - Audio deepfake detection")
    print("   POST /detect/multilingual - Multilingual analysis")
    print()
    print("Example Request Format:")
    print("   curl -X POST http://localhost:8000/detect/video \\")
    print("        -F \"file=@video.mp4\"")
    print()
    print("Example Response Format:")
    print("   {")
    print("     \"status\": \"success\",")
    print("     \"is_deepfake\": false,")
    print("     \"confidence\": 0.95,")
    print("     \"artifacts_found\": 2,")
    print("     \"processing_time\": 1.23,")
    print("     \"device\": \"cpu\"")
    print("   }")
    
    print()
    print("=" * 60)
    print("🎉 DEMONSTRATION COMPLETE!")
    print("=" * 60)
    print("🌐 Access the interactive API documentation at:")
    print(f"   {base_url}/docs")
    print()
    print("📱 System is ready for detection requests!")
    print("=" * 60)

if __name__ == "__main__":
    demo_truesight_api()