#!/usr/bin/env python3
"""
TrueSight Enhanced System Demonstration
Showcases the enhanced capabilities of the upgraded TrueSight system
"""

import asyncio
import time
from datetime import datetime
import sys
import os
import torch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modules.video_detector.detector import EnhancedVideoDetector
from modules.audio_detector.detector import EnhancedAudioDetector
from shared.monitoring_enhanced import EnhancedMonitoringSystem

async def demonstrate_video_detection():
    """Demonstrate enhanced video detection capabilities"""
    print("🎬 ENHANCED VIDEO DETECTION DEMO")
    print("=" * 50)
    
    # Initialize enhanced detector
    detector = EnhancedVideoDetector()
    
    # Show detector capabilities
    print("🔍 Enhanced Video Detector Initialized")
    print(f"   Device: {detector.device}")
    print(f"   GPU Available: {torch.cuda.is_available()}")
    print(f"   Models Loaded: {len(detector.models) if hasattr(detector, 'models') else 'Default models'}")
    
    # Show what analysis methods are available
    print("\n🔬 Available Analysis Methods:")
    print("   • Visual Artifact Detection")
    print("   • Temporal Consistency Analysis") 
    print("   • Facial Landmark Tracking")
    print("   • Compression Artifact Analysis")
    print("   • Motion Pattern Recognition")
    
    return {"status": "initialized", "detector": detector}

async def demonstrate_audio_detection():
    """Demonstrate enhanced audio detection capabilities"""
    print("\n🔊 ENHANCED AUDIO DETECTION DEMO")
    print("=" * 50)
    
    # Initialize enhanced detector
    detector = EnhancedAudioDetector()
    
    # Show detector capabilities
    print("🎵 Enhanced Audio Detector Initialized")
    print(f"   Sample Rate: 16000 Hz (default)")
    print(f"   Device: {detector.device}")
    print(f"   GPU Available: {torch.cuda.is_available()}")
    
    # Show what analysis methods are available
    print("\n🔬 Available Analysis Methods:")
    print("   • Spectral Domain Analysis")
    print("   • Voice Characteristic Analysis")
    print("   • Temporal Pattern Recognition")
    print("   • Audio Artifact Detection")
    print("   • Compression Analysis")
    
    return {"status": "initialized", "detector": detector}

def demonstrate_monitoring():
    """Demonstrate enhanced monitoring capabilities"""
    print("\n📊 ENHANCED SYSTEM MONITORING")
    print("=" * 50)
    
    monitor = EnhancedMonitoringSystem()
    
    # Simulate some system activity
    print("📈 Recording system metrics...")
    
    # Record some sample metrics
    monitor.record_http_request(
        endpoint="/api/v1/detection/video",
        method="POST",
        status_code=200,
        response_time=0.150,
        user_agent="DemoClient/1.0"
    )
    
    monitor.record_detection_processing(
        detector_type="video",
        processing_time=0.120,
        confidence_score=0.85,
        artifacts_found=3
    )
    
    # Get system health
    health = monitor.get_system_health()
    print(f"✅ System Health Status: {health.status}")
    print(f"   CPU Usage: {health.cpu_percent:.1f}%")
    print(f"   Memory Usage: {health.memory_percent:.1f}%")
    print(f"   Active Connections: {health.active_connections}")
    
    # Get performance summary
    summary = monitor.get_performance_summary(minutes=5)
    print(f"\n📈 Performance Summary (Last 5 minutes):")
    print(f"   Total Requests: {summary.total_requests}")
    print(f"   Avg Response Time: {summary.avg_response_time:.3f}s")
    print(f"   Error Rate: {summary.error_rate:.2f}%")
    print(f"   Detection Throughput: {summary.detection_throughput:.1f}/min")

async def main():
    """Main demonstration function"""
    print("🚀 TRUESEEK ENHANCED SYSTEM DEMONSTRATION")
    print("=" * 60)
    print(f"🕒 Demo Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Run demonstrations
        video_result = await demonstrate_video_detection()
        audio_result = await demonstrate_audio_detection()
        demonstrate_monitoring()
        
        print("\n🎉 DEMONSTRATION COMPLETE!")
        print("=" * 60)
        print("Enhanced TrueSight system is running with:")
        print("✅ Advanced computer vision detection")
        print("✅ Sophisticated audio analysis")
        print("✅ Real-time performance monitoring")
        print("✅ Comprehensive system health tracking")
        print("\n🌐 Access the web interface at: http://localhost:8000")
        print("📚 API Documentation: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())