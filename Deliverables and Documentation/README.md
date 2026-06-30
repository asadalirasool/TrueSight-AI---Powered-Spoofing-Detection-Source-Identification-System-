# TrueSight - AI-Powered Deepfake Detection System

## Overview
TrueSight is a comprehensive AI-powered multi-modal deepfake detection and forensic attribution system designed for real-time detection with <100ms latency and >95% accuracy.

## Key Features
- **Multi-modal stream processing** (Video/Audio)
- **Advanced deepfake detection algorithms** (LNCLIP, Wav2Vec2)
- **AI-Generated Video Percentage Detection** - Detect 0-100% AI-generated content with artifact breakdown
- **AI Tool Attribution** - Identify likely AI generation tool (Sora, RunwayML, Pika, Kling, etc.)
- **Frame-by-Frame Heatmap** - Visualize AI scores across video timeline
- **Urdu and multilingual support**
- **Forensic source identification**
- **Zero-trust security architecture**
- **Blockchain-based evidence logging**
- **Legal-grade forensic capabilities**

## System Requirements
- Python 3.9+
- Docker and Docker Compose
- NVIDIA GPU (recommended for ML inference)
- 16GB+ RAM
- 50GB+ storage

## Quick Start
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment: `cp .env.example .env`
4. Run development server: `python src/api/main.py`

### AI Percentage Detection Feature
Train and test the AI-generated video percentage detection model:
```bash
# Train the model (20 epochs)
python backend/train_ai_percentage.py --epochs 20

# Test the model
python backend/test_ai_percentage.py

# Run demo on test videos
python demo_ai_percentage.py --all
```

Start the backend API server:
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Test the AI percentage endpoint:
```bash
curl -X POST http://localhost:8000/api/v1/analyze/ai-percentage \
  -F "file=@test_videos/test_video.mp4"
```

Access the frontend dashboard at `http://localhost:3000` and navigate to the **AI Analysis** tab.

## Documentation
See `/docs` directory for detailed documentation.

- **AI Percentage Feature**: See `AI_PERCENTAGE_README.md` for complete documentation
- **Deployment**: See `DEPLOYMENT_GUIDE.md`
- **Frontend**: See `FRONTEND_README.md`
- **Microservices**: See `MICROSERVICES_ARCHITECTURE.md`

## License
Proprietary - TrueSight Systems