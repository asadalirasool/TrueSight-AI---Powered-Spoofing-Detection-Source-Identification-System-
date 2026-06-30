"""
Minimal TrueSight API Server
Simple FastAPI server demonstrating core detection capabilities
"""

import os
import sys
from pathlib import Path
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import torch
import asyncio

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import core modules
from modules.video_detector.detector import EnhancedVideoDetector
from modules.audio_detector.detector import EnhancedAudioDetector
from modules.multilingual_detector.language_detector import UrduMultilingualDetector

app = FastAPI(
    title="TrueSight Minimal API",
    description="Simplified TrueSight API for demonstration",
    version="1.0.0"
)

# Initialize detectors
print("🚀 Initializing TrueSight detectors...")
video_detector = EnhancedVideoDetector()
audio_detector = EnhancedAudioDetector()
ml_detector = UrduMultilingualDetector()
print("✅ Detectors initialized successfully!")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "TrueSight Minimal API",
        "version": "1.0.0",
        "status": "running",
        "detectors": {
            "video": str(video_detector.device),
            "audio": str(audio_detector.device), 
            "multilingual": str(ml_detector.device)
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "gpu_available": torch.cuda.is_available(),
        "detectors": {
            "video": "online",
            "audio": "online", 
            "multilingual": "online"
        }
    }

@app.post("/detect/video")
async def detect_video(file: UploadFile = File(...)):
    """Video deepfake detection"""
    try:
        # In a real implementation, you'd save the file and process it
        # For demo, return simulated results
        result = await video_detector.analyze_video_stream("demo_video_path")
        
        return {
            "status": "success",
            "is_deepfake": result.get("is_deepfake", False),
            "confidence": result.get("confidence", 0.0),
            "artifacts_found": result.get("artifacts_found", 0),
            "processing_time": result.get("processing_time", 0),
            "device": str(video_detector.device)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Video detection failed: {str(e)}"}
        )

@app.post("/detect/audio")
async def detect_audio(file: UploadFile = File(...)):
    """Audio deepfake detection"""
    try:
        # Simulated audio detection
        result = await audio_detector.analyze_audio_stream("demo_audio_path")
        
        return {
            "status": "success", 
            "is_deepfake": result.get("is_deepfake", False),
            "confidence": result.get("confidence", 0.0),
            "anomalies_found": result.get("anomalies_found", 0),
            "processing_time": result.get("processing_time", 0),
            "device": str(audio_detector.device)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Audio detection failed: {str(e)}"}
        )

@app.post("/detect/multilingual")
async def detect_multilingual(
    audio_file: UploadFile = File(...),
    text_transcript: str = Form(None)
):
    """Multilingual deepfake detection"""
    try:
        # Simulated multilingual detection
        result = await ml_detector.detect_multilingual_anomalies(
            "demo_audio_path", 
            text_transcript=text_transcript
        )
        
        return {
            "status": "success",
            "is_deepfake": result.get("is_deepfake", False),
            "authenticity_score": result.get("authenticity_score", 0.0),
            "languages_detected": result.get("language_analysis", {}).get("languages_detected", {}),
            "roman_urdu_detected": result.get("roman_urdu_analysis", {}).get("roman_urdu_detected", False),
            "processing_time": result.get("processing_time_ms", 0),
            "device": str(ml_detector.device)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Multilingual detection failed: {str(e)}"}
        )

@app.get("/capabilities")
async def get_capabilities():
    """Get system capabilities"""
    return {
        "video_detection": {
            "methods": [
                "Visual Artifact Detection",
                "Temporal Consistency Analysis", 
                "Facial Landmark Tracking",
                "Compression Artifact Analysis",
                "Motion Pattern Recognition"
            ],
            "device": str(video_detector.device)
        },
        "audio_detection": {
            "methods": [
                "Spectral Domain Analysis",
                "Voice Characteristic Analysis",
                "Temporal Pattern Recognition", 
                "Audio Artifact Detection",
                "Compression Analysis"
            ],
            "device": str(audio_detector.device)
        },
        "multilingual_detection": {
            "features": [
                "40+ Urdu Phonemes with IPA",
                "Roman Urdu Detection & Normalization",
                "Advanced Code-Switching Classification",
                "10+ Language Support",
                "Automatic Model Switching"
            ],
            "phonemes_loaded": len(ml_detector.urdu_phonemes),
            "device": str(ml_detector.device)
        }
    }

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 STARTING TRUESIGHT MINIMAL API SERVER")
    print("=" * 60)
    print(f"📍 Server URL: http://localhost:8000")
    print(f"📚 API Docs: http://localhost:8000/docs")
    print(f"🏥 Health Check: http://localhost:8000/health")
    print(f"⚡ Capabilities: http://localhost:8000/capabilities")
    print("=" * 60)
    
    uvicorn.run(
        "minimal_api:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=1
    )