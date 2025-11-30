@echo off
REM ============================================================
REM Script para configurar e iniciar o CLIENTE RPC (Windows)
REM Execute este script no PC que vai rodar o cliente
REM ============================================================

echo.
echo ========================================
echo   CONFIGURANDO CLIENTE RPC
echo ========================================
echo.

REM Solicitar IP do servidor se não estiver definido
if "%RPC_SERVER_HOST%"=="" (
    set /p SERVER_IP="Digite o IP do PC que esta rodando o SERVIDOR (ex: 192.168.1.100): "
    if "!SERVER_IP!"=="" (
        echo ERRO: IP nao pode ser vazio!
        pause
        exit /b 1
    )
    set RPC_SERVER_HOST=!SERVER_IP!
) else (
    echo Usando servidor: %RPC_SERVER_HOST% (da variavel de ambiente^)
)

echo.
echo Testando conectividade com o servidor...

REM Testar ping
ping -n 1 -w 2000 %RPC_SERVER_HOST% >nul 2>&1
if errorlevel 1 (
    echo Aviso: Nao foi possivel fazer ping no servidor
    echo        (pode ser normal se ICMP estiver bloqueado^)
) else (
    echo Ping OK - servidor alcancavel
)

REM Testar porta com PowerShell
powershell -Command "Test-NetConnection -ComputerName %RPC_SERVER_HOST% -Port 8000 -InformationLevel Quiet" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERRO: Porta 8000 nao esta acessivel!
    echo.
    echo Verifique se:
    echo   1. O servidor esta rodando no outro PC
    echo   2. O firewall esta permitindo porta 8000
    echo   3. Ambos estao na mesma rede
    echo.
    pause
    exit /b 1
) else (
    echo Porta 8000 acessivel - servidor RPC esta pronto!
)

echo.

REM Verificar Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Docker nao encontrado! Instale o Docker Desktop primeiro.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Docker Compose nao encontrado! Instale o Docker Compose primeiro.
    pause
    exit /b 1
)

echo Docker encontrado
echo.

REM Build e start
echo Buildando e iniciando cliente...
docker-compose -f docker-compose-client.yml up -d --build

echo.
echo ========================================
echo   CLIENTE INICIADO COM SUCESSO!
echo ========================================
echo.
echo Para usar a calculadora, execute:
echo   docker attach rpc_client
echo.
echo Dicas:
echo   - Para sair sem parar: Ctrl+P depois Ctrl+Q
echo   - Para ver logs: docker logs rpc_client --follow
echo   - Para parar: docker-compose -f docker-compose-client.yml down
echo.
echo Acesse o monitor do servidor em:
echo   http://%RPC_SERVER_HOST%:5000
echo.
pause
