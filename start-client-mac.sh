#!/bin/bash
# ============================================================
# Script para configurar e testar o CLIENTE no Mac
# ============================================================

echo "============================================"
echo "   CONFIGURANDO CLIENTE RPC NO MAC"
echo "============================================"
echo ""

# IP do servidor Windows (configurado automaticamente)
SERVER_IP="192.168.1.160"
echo "Servidor Windows configurado para: $SERVER_IP"
echo ""

# Testar conectividade básica
echo "Testando conectividade básica..."
if ping -c 2 -W 2000 $SERVER_IP > /dev/null 2>&1; then
    echo "✅ Ping OK - Windows é alcançável"
else
    echo "❌ Ping falhou - verificar conexão de rede"
fi

# Testar porta do servidor
echo "Testando porta 8000 (Servidor RPC)..."
if nc -z -v $SERVER_IP 8000 2>/dev/null; then
    echo "✅ Porta 8000 acessível - Servidor RPC está rodando"
else
    echo "❌ Porta 8000 inacessível - Servidor pode não estar rodando"
fi

# Testar porta do monitor
echo "Testando porta 5000 (Monitor Web)..."
if nc -z -v $SERVER_IP 5000 2>/dev/null; then
    echo "✅ Porta 5000 acessível - Monitor Web está rodando"
else
    echo "❌ Porta 5000 inacessível - Monitor pode não estar rodando"
fi

echo ""
echo "============================================"
echo "   INICIANDO CLIENTE"
echo "============================================"

# Configurar variáveis de ambiente
export RPC_SERVER_HOST=$SERVER_IP
export RPC_SERVER_PORT=8000
export RPC_MONITOR_URL="http://$SERVER_IP:5000/control/clear"

echo "Variáveis configuradas:"
echo "  RPC_SERVER_HOST=$RPC_SERVER_HOST"
echo "  RPC_SERVER_PORT=$RPC_SERVER_PORT"
echo "  RPC_MONITOR_URL=$RPC_MONITOR_URL"
echo ""

# Verificar se Docker está disponível
if command -v docker > /dev/null 2>&1; then
    echo "Iniciando cliente com Docker..."
    docker-compose -f docker-compose-client.yml up --build
else
    echo "Docker não encontrado. Iniciando com Python..."
    cd client
    if command -v python3 > /dev/null 2>&1; then
        python3 client.py
    elif command -v python > /dev/null 2>&1; then
        python client.py
    else
        echo "❌ Python não encontrado! Instale Python 3 ou Docker."
        exit 1
    fi
fi