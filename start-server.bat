@echo off
REM ============================================================
REM Script para configurar e iniciar o SERVIDOR RPC (Windows)
REM Execute este script no PC que vai hospedar o servidor
REM ============================================================

echo.
echo ========================================
echo   CONFIGURANDO SERVIDOR RPC
echo ========================================
echo.

REM Detectar IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do set SERVER_IP=%%a
set SERVER_IP=%SERVER_IP:~1%

echo IP detectado: %SERVER_IP%
echo.
echo IMPORTANTE: Compartilhe este IP com quem for rodar o cliente!
echo             O cliente precisara configurar: RPC_SERVER_HOST=%SERVER_IP%
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

REM Configurar firewall Windows
echo Configurando firewall Windows...
netsh advfirewall firewall add rule name="RPC Server" dir=in action=allow protocol=TCP localport=8000 >nul 2>&1
netsh advfirewall firewall add rule name="RPC Monitor" dir=in action=allow protocol=TCP localport=5000 >nul 2>&1
echo Firewall configurado
echo.

REM Build e start
echo Buildando e iniciando containers...
docker-compose -f docker-compose-server.yml up -d --build

echo.
echo ========================================
echo   SERVIDOR INICIADO COM SUCESSO!
echo ========================================
echo.
echo URLs de acesso:
echo   - Servidor RPC: http://%SERVER_IP%:8000
echo   - Monitor Web:  http://%SERVER_IP%:5000
echo.
echo Verificar status:
echo   docker ps
echo.
echo Ver logs:
echo   docker logs rpc_server --follow
echo   docker logs rpc_monitor --follow
echo.
echo Parar servidor:
echo   docker-compose -f docker-compose-server.yml down
echo.
pause
