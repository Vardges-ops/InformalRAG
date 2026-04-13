@echo off

echo Starting Docker services...
docker compose up -d

echo Installing dependencies...
python -m pip install -r requirements.txt

echo Pulling Gemma model...
ollama pull gemma:2b

echo Setup complete!
pause