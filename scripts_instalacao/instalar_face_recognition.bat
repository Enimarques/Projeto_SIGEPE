@echo off
setlocal enabledelayedexpansion

echo ================================================
echo Instalador do Sistema de Reconhecimento Facial
echo ================================================
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

REM Verifica Visual Studio Build Tools
where cl.exe > nul 2>&1
if errorlevel 1 (
    echo Visual Studio Build Tools nao encontrado!
    echo Por favor, instale o Visual Studio Build Tools 2022 com suporte C++
    echo Voce pode baixar em: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo.
    echo IMPORTANTE: Na instalacao, selecione:
    echo - Desenvolvimento para desktop com C++
    echo.
    choice /C SN /M "Deseja abrir o site para download agora? (S/N)"
    if errorlevel 2 goto :continue_install
    start https://visualstudio.microsoft.com/visual-cpp-build-tools/
    exit /b 1
)

:continue_install
REM Verifica e instala CMake se necessário
cmake --version > nul 2>&1
if errorlevel 1 (
    echo CMake nao encontrado! Instalando via pip...
    pip install cmake
    if errorlevel 1 (
        echo Falha ao instalar CMake. Tente instalar manualmente.
        pause
        exit /b 1
    )
)

REM Backup do ambiente atual
if exist venv (
    echo Fazendo backup do ambiente virtual existente...
    ren venv venv_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
)

echo Criando novo ambiente virtual...
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

echo Instalando dependencias do reconhecimento facial...
python -m pip install --upgrade pip setuptools wheel

echo Instalando pacotes na ordem correta...
echo 1/5 Instalando cmake...

if errorlevel 1 goto :error

echo 2/5 Instalando dlib...
pip install dlib==19.24.6
if errorlevel 1 goto :error

echo 3/5 Instalando face_recognition...
pip install face_recognition
if errorlevel 1 goto :error

echo 4/5 Instalando OpenCV...
pip install opencv-python==4.9.0.80
if errorlevel 1 goto :error

echo 5/5 Reinstalando face_recognition_models...
pip install --force-reinstall face_recognition_models
if errorlevel 1 goto :error

echo.
echo ================================================
echo Instalacao do sistema de reconhecimento facial concluida!
echo.
echo VERIFICACAO FINAL:
echo 1. Testando importacao das bibliotecas...
python -c "import dlib; import face_recognition; import cv2" 2>nul
if errorlevel 1 (
    echo ATENCAO: Algumas bibliotecas podem nao estar funcionando corretamente.
    echo Por favor, execute o sistema e reporte qualquer erro.
) else (
    echo Todas as bibliotecas foram instaladas com sucesso!
)
echo ================================================
pause
exit /b 0

:error
echo.
echo ================================================
echo ERRO: Falha na instalacao!
echo Se o erro persistir, tente:
echo 1. Verificar se o Visual Studio Build Tools esta instalado corretamente
echo 2. Reiniciar o computador e tentar novamente
echo 3. Instalar as dependencias manualmente na ordem:
echo    - cmake
echo    - dlib
echo    - face_recognition
echo    - opencv-python
echo ================================================
pause
exit /b 1
