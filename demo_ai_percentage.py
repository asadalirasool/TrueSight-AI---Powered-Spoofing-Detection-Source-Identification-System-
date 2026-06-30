#!/usr/bin/env python3
"""
Demo Script for AI Percentage Detection
========================================

Tests the AI percentage detection model on sample videos.

Usage:
    python demo_ai_percentage.py --video test_video.mp4
"""

import asyncio
import argparse
import json
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.ai_percentage import AIPercentageDetector


async def demo_ai_percentage(video_path: str):
    """Run AI percentage detection on a video"""
    
    if not os.path.exists(video_path):
        print(f"❌ Error: Video file not found: {video_path}")
        return
    
    print(f"\n{'='*60}")
    print(f"🚀 AI-GENERATED VIDEO PERCENTAGE DETECTION")
    print(f"{'='*60}\n")
    
    print(f"📹 Analyzing: {video_path}")
    print(f"⏳ Processing...\n")
    
    try:
        # Initialize detector
        detector = AIPercentageDetector()
        
        # Run prediction
        result = await detector.predict_percentage(video_path)
        
        # Display results
        print(f"{'='*60}")
        print(f"📊 ANALYSIS RESULTS")
        print(f"{'='*60}\n")
        
        # Main percentage
        ai_percentage = result['ai_percentage']
        verdict = result['verdict']
        
        # Color code based on percentage
        if ai_percentage >= 70:
            emoji = "🔴"
            color = "HIGH"
        elif ai_percentage >= 40:
            emoji = "🟡"
            color = "MODERATE"
        else:
            emoji = "🟢"
            color = "LOW"
        
        print(f"{emoji} AI Generation Percentage: {ai_percentage}% ({color})")
        print(f"🎯 Verdict: {verdict}")
        print(f"📈 Confidence: {result['confidence']*100:.1f}%\n")
        
        # Artifact breakdown
        print(f"📋 Artifact Breakdown:")
        print(f"{'-'*60}")
        breakdown = result['breakdown']
        for artifact, score in breakdown.items():
            # Format artifact name
            artifact_name = artifact.replace('_', ' ').title()
            bar_length = int(score / 2)
            bar = "█" * bar_length + "░" * (50 - bar_length)
            print(f"  {artifact_name:25} {bar} {score:.1f}%")
        
        print(f"\n🤖 Likely AI Tool: {result['likely_tool']}")
        print(f"📊 Tool Confidence: {result['tool_confidence']*100:.1f}%")
        
        # Frame analysis
        print(f"\n🎬 Frame-by-Frame Analysis:")
        print(f"{'-'*60}")
        per_frame = result['per_frame_scores']
        print(f"  Frames analyzed: {len(per_frame)}")
        print(f"  Min AI%: {min(per_frame):.1f}%")
        print(f"  Max AI%: {max(per_frame):.1f}%")
        print(f"  Avg AI%: {sum(per_frame)/len(per_frame):.1f}%")
        
        # Show timeline
        print(f"\n  Timeline (each █ = 2%):")
        for i, score in enumerate(per_frame[::4]):  # Show every 4th frame
            bar = "█" * int(score/2)
            print(f"    Frame {i*4:3d}: {bar} {score:.1f}%")
        
        print(f"\n⏱️  Processing Time: {result['processing_time_ms']:.0f}ms")
        print(f"{'='*60}\n")
        
        # Save detailed results
        output_file = "ai_percentage_results.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"💾 Detailed results saved to: {output_file}\n")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()


async def demo_with_test_videos():
    """Run demo on multiple test videos"""
    
    test_videos_dir = "test_videos"
    
    if not os.path.exists(test_videos_dir):
        print(f"❌ Test videos directory not found: {test_videos_dir}")
        print("Please add test videos to the directory")
        return
    
    # Find all video files
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    test_videos = []
    
    for root, dirs, files in os.walk(test_videos_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in video_extensions):
                test_videos.append(os.path.join(root, file))
    
    if not test_videos:
        print(f"❌ No test videos found in {test_videos_dir}")
        return
    
    print(f"\n🎬 Found {len(test_videos)} test videos\n")
    
    # Test each video
    for video_path in test_videos:
        await demo_ai_percentage(video_path)
        print("\n" + "="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Demo AI Percentage Detection")
    parser.add_argument('--video', type=str, help='Path to video file to analyze')
    parser.add_argument('--all', action='store_true', help='Test all videos in test_videos directory')
    
    args = parser.parse_args()
    
    if args.video:
        # Test specific video
        asyncio.run(demo_ai_percentage(args.video))
    elif args.all:
        # Test all videos
        asyncio.run(demo_with_test_videos())
    else:
        # Default: show help
        parser.print_help()
        print("\nExample usage:")
        print("  python demo_ai_percentage.py --video test_video.mp4")
        print("  python demo_ai_percentage.py --all")


if __name__ == "__main__":
    main()
