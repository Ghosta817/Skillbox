@echo off
git clone git@gitlab.skillbox.ru:ilia_k/python_basic_diploma.git -b master TET
cd TET
START python -m venv venv
COPY Install_Bot\requirements.txt requirements.txt
DEL Ubnt_runBot.sh, .gitignore, readme.md
RMDIR /S /Q Install_Bot
timeout /t 10
CALL venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt