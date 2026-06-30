# AI-Generated Video Percentage Detection Feature

## Overview

This feature allows users to upload ANY video and receive a **percentage score (0-100%)** indicating how much of the video appears to be AI-generated, including:

- Pure AI videos from Sora, RunwayML, Pika, Kling, Stable Video Diffusion
- Deepfake videos (FaceForensics++, DFDC)
- Partially AI-enhanced content

## Quick Start

### 1. Backend Setup

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Train the model (optional - will use base model if not trained)
python train_ai_percentage.py --epochs 20 --batch_size 8 --lr 1e-4

# Start the server
cd ..
uvicorn backend.app.main:app --reload --port 8000
```

### 2. Test the API

```bash
# Upload a video for analysis
curl -X POST http://localhost:8000/api/v1/analyze/ai-percentage \
  -F "file=@test_video.mp4"

# Check service health
curl http://localhost:8000/api/v1/analyze/health
```

### 3. Run Demo

```bash
# Test on a specific video
python demo_ai_percentage.py --video test_video.mp4

# Test all videos in test_videos directory
python demo_ai_percentage.py --all
```

### 4. Frontend Usage

The frontend components are already integrated into the Dashboard. Simply:

1. Start the React frontend:
```bash
cd frontend
npm install
npm start
```

2. Upload a video through the UI
3. View the AI percentage analysis in the new "AI Generation Analysis" tab

## API Documentation

### Endpoint: `POST /api/v1/analyze/ai-percentage`

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `file` (video file)

**Response:**
```json
{
  "status": "success",
  "request_id": "uuid",
  "timestamp": "2024-01-01T00:00:00",
  "file_info": {
    "filename": "test.mp4",
    "file_extension": ".mp4"
  },
  "analysis_result": {
    "ai_percentage": 78.2,
    "confidence": 0.85,
    "breakdown": {
      "gan_artifacts": 45.1,
      "temporal_anomalies": 18.3,
      "frequency_artifacts": 22.0,
      "texture_anomalies": 12.0,
      "lighting_issues": 2.6
    },
    "per_frame_scores": [65, 72, 78, 82, ...],
    "likely_tool": "RunwayML",
    "tool_confidence": 0.72,
    "frames_analyzed": 40,
    "processing_time_ms": 1240,
    "verdict": "AI-GENERATED"
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `ai_percentage` | float | Overall AI generation percentage (0-100%) |
| `confidence` | float | Model confidence in prediction (0-1) |
| `breakdown` | object | Per-artifact scores (GAN, temporal, frequency, texture, lighting) |
| `per_frame_scores` | array | AI percentage for each analyzed frame |
| `likely_tool` | string | Most likely AI generation tool used |
| `tool_confidence` | float | Confidence in tool identification (0-1) |
| `verdict` | string | Overall verdict (AI-GENERATED, SUSPICIOUS, LIKELY-REAL) |

## Model Architecture

### Vision Transformer Backbone
- **Base Model**: Facebook DeiT (Data-efficient Image Transformer)
- **Input**: 40 frames per video (224x224 pixels)
- **Features**: Pre-trained on ImageNet, fine-tuned for AI detection

### Multi-Head Architecture
1. **Percentage Regression Head**: Predicts overall AI percentage (0-100%)
2. **Artifact Breakdown Head**: Multi-label regression for 5 artifact types
3. **Tool Classification Head**: Identifies likely AI generation tool

### Artifact Types Detected
- **GAN Artifacts**: Generator-discriminator patterns
- **Temporal Anomalies**: Frame-to-frame inconsistencies
- **Frequency Artifacts**: Unusual frequency domain patterns
- **Texture Anomalies**: Unnatural texture synthesis
- **Lighting Issues**: Inconsistent lighting and shadows

## Training the Model

### Dataset Structure
```
data/
  real/                    # Authentic videos (500+)
  ai_generated/
    sora/                  # Sora-generated videos (200+)
    runwayml/              # RunwayML videos (200+)
    pika/                  # Pika videos (200+)
    kling/                 # Kling videos (200+)
    stable_video/          # Stable Video Diffusion (200+)
  deepfake/                # Deepfake videos (200+)
```

### Training Command
```bash
python backend/train_ai_percentage.py \
  --data_dir data \
  --epochs 20 \
  --batch_size 8 \
  --lr 1e-4 \
  --num_workers 4
```

### Training Features
- **Data Augmentation**: Flip, rotation, color jitter
- **Early Stopping**: Stops if validation MAE < 0.15
- **Learning Rate Scheduling**: Reduces LR on plateau
- **Model Checkpointing**: Saves best model automatically
- **Training History**: Logged to `models/training_history.json`

## Frontend Components

### 1. AIPercentageGauge
Circular gauge showing overall AI percentage with color-coded verdict.

### 2. AIBreakdownChart
Horizontal bar chart showing artifact breakdown.

### 3. FrameHeatmap
Timeline visualization showing per-frame AI scores with hover tooltips.

## Success Criteria

- ✅ Model trains without errors
- ✅ Validation MAE < 15% (predicted percentage off by less than 15)
- ✅ Real videos get < 30% AI score
- ✅ AI videos get > 70% AI score
- ✅ API endpoint returns correct JSON
- ✅ Frontend displays all components correctly
- ✅ End-to-end test: upload video → see percentage

## File Structure

```
backend/
  app/
    services/
      ai_percentage.py          # Main detection service
    api/v1/endpoints/
      ai_percentage.py          # API endpoint
  train_ai_percentage.py        # Training script

frontend/src/components/
  AIPercentageGauge.jsx         # Gauge component
  AIPercentageGauge.css
  AIBreakdownChart.jsx          # Breakdown chart
  AIBreakdownChart.css
  FrameHeatmap.jsx              # Frame heatmap
  FrameHeatmap.css

demo_ai_percentage.py           # Demo script
```

## Troubleshooting

### Model Not Found
If you see "No trained model found" warning, the system will use the base DeiT model. To improve accuracy, train with your own dataset.

### Out of Memory
Reduce batch size in training:
```bash
python backend/train_ai_percentage.py --batch_size 4
```

### Slow Inference
- Enable GPU: Set `use_gpu=True` in `AIPercentageDetector`
- Reduce frames: Change `target_frames` from 40 to 20

## Dependencies

Additional dependencies added:
- `scikit-learn` - For metrics
- `timm` - For model backbones
- `Pillow` - For image processing

## License

Part of the TrueSight AI-Powered Deepfake Detection System
