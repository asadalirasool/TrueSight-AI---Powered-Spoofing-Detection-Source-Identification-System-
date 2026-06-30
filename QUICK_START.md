# 🚀 TrueSight Quick Start Guide

## ⚡ One-Command Setup

```bash
# Complete setup with everything (recommended for first time)
python setup_complete.py --all

# Quick setup (no training, no tests)
python setup_complete.py --quick

# Setup with model training
python setup_complete.py --train

# Setup with end-to-end testing
python setup_complete.py --test
```

---

## 📦 Individual Scripts

All automation scripts are in the `scripts/` directory:

### 1. Download Test Datasets (~3GB, 10 minutes)
```bash
python scripts/download_quick_datasets.py
```

**Downloads:**
- DFDC Sample (~500MB) - Requires Kaggle account
- FakeParts Mini (~300MB)
- AI Video Samples (~200MB)
- Sample Videos (from test_videos/)

---

### 2. Verify System Components
```bash
# Full verification
python scripts/verify_system.py

# Quick verification
python scripts/verify_system.py --quick

# Verbose output
python scripts/verify_system.py --verbose
```

**Checks:**
- ✅ All 9 modules
- ✅ Python dependencies
- ✅ Model files
- ✅ Configurations
- ✅ Datasets

---

### 3. System Health Check
```bash
# Single check
python scripts/health_check.py

# Continuous monitoring (refresh every 10 seconds)
python scripts/health_check.py --watch

# Custom refresh interval
python scripts/health_check.py --watch --interval 5
```

**Monitors:**
- CPU/Memory/Disk usage
- GPU availability
- Backend/Frontend servers
- Model files
- Database

---

### 4. End-to-End Testing
```bash
# Test with default videos
python scripts/test_end_to_end.py

# Test with custom directory
python scripts/test_end_to_end.py --test-dir data/quick_test

# Test remote server
python scripts/test_end_to_end.py --base-url http://your-server:8000
```

**Tests:**
- AI Percentage Analysis
- Deepfake Detection
- API endpoints
- Video uploads

---

## 🎯 Common Workflows

### 🟢 First Time Setup (15 minutes)
```bash
# Step 1: Download datasets
python scripts/download_quick_datasets.py

# Step 2: Verify system
python scripts/verify_system.py

# Step 3: Train AI percentage model (10 epochs for quick test)
python backend/train_ai_percentage.py --epochs 10

# Step 4: Start backend server
cd backend
uvicorn app.main:app --reload

# Step 5: In new terminal, test the system
python scripts/test_end_to_end.py
```

---

### 🟡 Quick Demo (5 minutes)
```bash
# Use existing test_videos (no download needed)
python scripts/verify_system.py --quick

# Start server
cd backend
uvicorn app.main:app --reload

# Test with curl
curl -X POST http://localhost:8000/api/v1/analyze/ai-percentage \
  -F "file=@test_videos/test_video.mp4"
```

---

### 🔴 Full Training & Testing (1-2 hours)
```bash
# Step 1: Setup everything
python setup_complete.py --all

# Step 2: Train all models
python backend/train_ai_percentage.py --epochs 30

# Step 3: Test models
python backend/test_ai_percentage.py

# Step 4: Start servers
cd backend
uvicorn app.main:app --reload

# Step 5: Monitor health
python scripts/health_check.py --watch
```

---

## 📊 Understanding Reports

### Verification Report (`verification_report.json`)
```json
{
  "modules": {
    "Module 1: Stream Processor": "PASS",
    "Module 2: Video Detection": "PASS"
  },
  "dependencies": {
    "torch": "2.0.0",
    "fastapi": "0.104.1"
  },
  "models": {
    "AI Percentage Model": "PASS (150.5MB)"
  }
}
```

### Health Check Output
```
🏥 TRUE SIGHT SYSTEM - HEALTH CHECK
==============================================================

✅ Python: Version 3.10.12
✅ Dependencies: All critical dependencies installed
✅ CPU: 45.2% (8 cores)
✅ Memory: 62.3% used (12.5GB available)
✅ Disk: 55% used (250.3GB free)
✅ GPU: 1x NVIDIA RTX 3080 (2048MB allocated)
✅ Backend Server: Running on port 8000
⚠️ Frontend Server: Not running
✅ Models: 2/3 models found
✅ Database: Database file exists

✅ OVERALL STATUS: HEALTHY
```

### E2E Test Report (`e2e_test_report.json`)
```json
[
  {
    "status": "PASS",
    "video": "test_videos/test_video.mp4",
    "result": {
      "ai_percentage": 23.5,
      "verdict": "LIKELY-REAL",
      "confidence": 0.87
    }
  }
]
```

---

## 🛠️ Troubleshooting

### Issue: "Cannot connect to server"
**Solution:**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### Issue: "Model not found"
**Solution:**
```bash
# Train the model first
python backend/train_ai_percentage.py --epochs 20

# Or download pre-trained model (if available)
python scripts/download_models.py
```

---

### Issue: "Dependencies missing"
**Solution:**
```bash
# Install all dependencies
pip install -r backend/requirements.txt

# Or install specific package
pip install torch transformers fastapi
```

---

### Issue: "Kaggle credentials not found"
**Solution:**
1. Create account at https://www.kaggle.com
2. Go to Account → Create API Token
3. Save `kaggle.json` to `~/.kaggle/kaggle.json`
4. Run: `chmod 600 ~/.kaggle/kaggle.json`

---

## 📁 File Structure

```
true-sight/
├── setup_complete.py              # Master setup wizard
├── scripts/
│   ├── download_quick_datasets.py # Dataset downloader
│   ├── verify_system.py           # System verifier
│   ├── health_check.py            # Health monitor
│   └── test_end_to_end.py         # E2E tester
├── backend/
│   ├── train_ai_percentage.py     # Model training
│   ├── test_ai_percentage.py      # Model testing
│   └── app/
│       └── main.py                # FastAPI server
├── frontend/
│   └── src/
│       └── components/
│           └── Dashboard.js       # React UI
└── test_videos/                   # Sample videos for testing
```

---

## 🎯 Success Criteria

Your system is ready when:

- ✅ `verify_system.py` shows 7/9+ modules PASS
- ✅ `health_check.py` shows HEALTHY status
- ✅ `test_end_to_end.py` shows ALL TESTS PASSED
- ✅ Backend server responds at http://localhost:8000/health
- ✅ Frontend loads at http://localhost:3000

---

## 📞 Need Help?

Check these resources:
- **AI Percentage Feature**: `AI_PERCENTAGE_README.md`
- **Deployment Guide**: `DEPLOYMENT_GUIDE.md`
- **System Architecture**: `MICROSERVICES_ARCHITECTURE.md`
- **Implementation Summary**: `AI_PERCENTAGE_IMPLEMENTATION_COMPLETE.md`

---

**🎉 You're all set! Happy detecting!**
