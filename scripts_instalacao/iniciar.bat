@echo off
setlocal enabledelayedexpansion

echo ===================================
echo Iniciando Sistema SIGEPE
echo ===================================
echo.

REM Verifica se o ambiente virtual existe
if not exist venv (
    echo Ambiente virtual nao encontrado!
    echo Execute primeiro o arquivo instalar.bat
    pause
    exit /b 1
)

REM Ativa o ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Falha ao ativar ambiente virtual.
    pause
    exit /b 1
)

REM Verifica se o banco de dados está atualizado
echo Verificando banco de dados...
python manage.py migrate --check
if errorlevel 1 (
    echo Ha migracoes pendentes. Aplicando...
    python manage.py migrate
    if errorlevel 1 (
        echo Falha ao aplicar migracoes.
        pause
        exit /b 1
    )
)

REM Inicia o servidor
echo Iniciando servidor...
echo.
echo Para acessar o sistema, abra seu navegador e acesse:
echo http://127.0.0.1:8000/
echo.
echo Para acessar o admin, use:
echo http://127.0.0.1:8000/admin/
echo.
echo Para parar o servidor, pressione CTRL+C
echo.
python manage.py runserver

pause
