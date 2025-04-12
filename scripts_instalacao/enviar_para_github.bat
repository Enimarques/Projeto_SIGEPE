@echo off
echo ===================================
echo Enviando Scripts para GitHub
echo ===================================
echo.

REM Verifica se o Git está instalado
git --version > nul 2>&1
if errorlevel 1 (
    echo Git nao encontrado! Por favor, instale o Git primeiro:
    echo https://git-scm.com/download/win
    echo.
    echo Apos instalar o Git:
    echo 1. Feche este terminal
    echo 2. Abra um novo terminal
    echo 3. Execute este script novamente
    pause
    exit /b 1
)

cd ..
echo Inicializando repositorio Git...
git init

echo Criando e mudando para o branch main...
git checkout -b main

echo Adicionando arquivos...
git add scripts_instalacao/* instalar.bat iniciar.bat

echo Criando commit...
git commit -m "Adicionando scripts de instalacao do Urutal"

echo Configurando repositorio remoto...
git remote add origin https://github.com/TersanPlay/Urutal.git

echo Enviando para o GitHub...
git push -u origin main

echo.
echo ===================================
echo Se nao houver erros, os arquivos foram enviados com sucesso!
echo Verifique em: https://github.com/TersanPlay/Urutal
echo ===================================
pause
