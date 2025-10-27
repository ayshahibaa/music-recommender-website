@echo off
echo Starting Music Recommendation Backend...
cd backend\dt
python -m venv venv
call venv\Scripts\activate
pip install fastapi uvicorn pymongo pandas tensorflow scikit-learn
echo Starting FastAPI server on http://localhost:8000
uvicorn main:app --reload --port 8000
pause
