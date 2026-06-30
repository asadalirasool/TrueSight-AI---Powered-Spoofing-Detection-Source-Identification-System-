@echo off
echo ================================================================
echo TRUE SIGHT - COMPLETE MODEL SETUP
echo ================================================================
echo.

cd backend

echo [1/3] Downloading models...
echo.
python download_models.py
if errorlevel 1 (
    echo Warning: Some downloads failed, continuing...
)
echo.

echo [2/3] Training AI Percentage model (10 epochs)...
echo.
python train_ai_percentage.py --epochs 10
if errorlevel 1 (
    echo Warning: Training failed, you may need to prepare datasets first
)
echo.

echo [3/3] Verifying models...
echo.
python benchmark_models.py
echo.

echo ================================================================
echo SETUP COMPLETE!
echo ================================================================
echo.
echo To start the server:
echo   cd backend
echo   uvicorn app.main:app --reload
echo.
echo Then visit: http://localhost:8000/docs
echo.
pause
