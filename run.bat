@echo off

call .venv/Scripts/activate
python -m fazbot
call .venv/Scripts/deactivate

pause
