@echo off
setlocal enabledelayedexpansion

echo ===================================
echo Verificador de Requisitos SIGEPE
echo ===================================
echo.

set REQUISITOS_OK=true

REM Verifica Python e versão
echo Verificando Python...
for /f "tokens=2" %%I in ('python --version 2^>^&1') do set PYTHON_VERSION=%%I
if errorlevel 1 (
    echo [X] Python nao encontrado!
    echo     Instale Python 3.9 ou superior: https://www.python.org/downloads/
    set REQUISITOS_OK=false
) else (
    echo [✓] Python %PYTHON_VERSION% encontrado
)

REM Verifica Visual Studio Build Tools
echo.
echo Verificando Visual Studio Build Tools...
where cl.exe > nul 2>&1
if errorlevel 1 (
    echo [X] Visual Studio Build Tools nao encontrado!
    echo     Instale VS Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    set REQUISITOS_OK=false
) else (
    echo [✓] Visual Studio Build Tools encontrado
)

REM Verifica CMake
echo.
echo Verificando CMake...
cmake --version > nul 2>&1
if errorlevel 1 (
    echo [X] CMake nao encontrado!
    echo     Sera instalado automaticamente durante a instalacao
    set REQUISITOS_OK=false
) else (
    echo [✓] CMake encontrado
)

echo.
echo ===================================
if "%REQUISITOS_OK%"=="true" (
    echo [✓] Todos os requisitos atendidos!
    echo     Voce pode prosseguir com a instalacao
    echo     Execute instalar.bat para comecar
) else (
    echo [X] Alguns requisitos nao foram atendidos
    echo     Instale os itens faltantes e tente novamente
)
echo ===================================

pause
