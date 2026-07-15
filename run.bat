@echo off
echo Creando entorno virtual e instalando dependencias...
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo Dependencias instaladas.
echo Iniciando programa...
python main.py
pause
