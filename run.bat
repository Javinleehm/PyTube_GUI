@echo off

set "VENV_DIR=./venv"
set "REQUIREMENTS=requirements.txt"
set "MAIN_SCRIPT=main.py"

if not exist %VENV_DIR% (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

echo Activating virtual environment...
call %VENV_DIR%\Scripts\activate.bat

echo Installing required packages...
pip install -r %REQUIREMENTS%
cls
echo Running %MAIN_SCRIPT%...
python %MAIN_SCRIPT%

echo Deactivating virtual environment...
deactivate

echo Done.