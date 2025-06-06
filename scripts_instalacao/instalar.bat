@echo off
setlocal enabledelayedexpansion

echo ===================================
echo Instalador do Sistema SIGEPE
echo ===================================
echo.

REM Verifica versão do Python
for /f "tokens=2" %%I in ('python --version 2^>^&1') do set PYTHON_VERSION=%%I
if errorlevel 1 (
    echo Python nao encontrado! Por favor, instale o Python 3.9 ou superior.
    echo Voce pode baixar em: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Verifica se a versão do Python é adequada
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)
if %PYTHON_MAJOR% LSS 3 (
    echo Versao do Python muito antiga. Necessario Python 3.9 ou superior.
    pause
    exit /b 1
)
if %PYTHON_MAJOR%==3 if %PYTHON_MINOR% LSS 9 (
    echo Versao do Python muito antiga. Necessario Python 3.9 ou superior.
    pause
    exit /b 1
)

echo.
echo Iniciando instalacao do sistema...

REM Backup do ambiente virtual existente
if exist venv (
    echo Fazendo backup do ambiente virtual existente...
    ren venv venv_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
)

echo Criando ambiente virtual...
python -m venv venv
if errorlevel 1 (
    echo Falha ao criar ambiente virtual.
    pause
    exit /b 1
)

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Falha ao ativar ambiente virtual.
    pause
    exit /b 1
)

echo Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Falha ao instalar dependencias.
    echo Verifique o arquivo requirements.txt e tente novamente.
    pause
    exit /b 1
)

echo Aplicando migracoes do banco de dados...
python manage.py migrate
if errorlevel 1 (
    echo Falha ao aplicar migracoes.
    pause
    exit /b 1
)

echo.
echo ===================================
echo Instalacao concluida com sucesso!
echo.
echo Para iniciar o sistema, execute: iniciar.bat
echo ===================================

echo Deseja criar um superusuario admin agora? (S/N)
choice /C SN /M ""
if errorlevel 2 goto end

echo.
echo Criando superusuario...
python manage.py createsuperuser

:end
pause
