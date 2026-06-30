@echo off
echo ============================================================
echo TRUE SIGHT - DOWNLOAD & TRAIN MODELS
echo ============================================================
echo.

cd backend

echo Step 1: Downloading Pre-trained Models...
echo.
python -c "from app.services.model_loader import ModelLoader; ModelLoader().download_all_models()"
echo.

echo Step 2: Training AI Percentage Model (10 epochs)...
echo.
python train_ai_percentage.py --epochs 10
echo.

echo ============================================================
echo COMPLETE!
echo ============================================================
echo.
echo Next steps:
echo 1. Start server: cd backend ^&^& uvicorn app.main:app --reload
echo 2. Access API: http://localhost:8000/docs
echo 3. Test: curl -X POST http://localhost:8000/api/v1/analyze/ai-percentage -F "file=@test_videos/test_video.mp4"
pause
