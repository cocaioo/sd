#!/bin/bash

# ============================================================
# Script para configurar e iniciar o CLIENTE RPC
# Execute este script no PC que vai rodar o cliente
# ============================================================

set -e

echo "💻 Configurando PC como CLIENTE RPC..."
echo ""

# Solicitar IP do servidor
if [ -z "$RPC_SERVER_HOST" ]; then
    echo "📡 Digite o IP do PC que está rodando o SERVIDOR:"
    read -p "IP do servidor (ex: 192.168.1.100): " SERVER_IP
    
    if [ -z "$SERVER_IP" ]; then
        echo "❌ IP não pode ser vazio!"
        exit 1
    fi
    
    export RPC_SERVER_HOST=$SERVER_IP
else
    echo "📡 Usando servidor: $RPC_SERVER_HOST (da variável de ambiente)"
fi

echo ""
echo "🔍 Testando conectividade com o servidor..."

# Testar ping
if ping -c 1 -W 2 $RPC_SERVER_HOST &> /dev/null; then
    echo "✅ Ping OK - servidor alcançável"
else
    echo "⚠️  Aviso: Não foi possível fazer ping no servidor"
    echo "   (pode ser normal se ICMP estiver bloqueado)"
fi

# Testar porta 8000
if command -v nc &> /dev/null; then
    if nc -zv -w 2 $RPC_SERVER_HOST 8000 &> /dev/null; then
        echo "✅ Porta 8000 acessível - servidor RPC está pronto!"
    else
        echo "❌ ERRO: Porta 8000 não está acessível!"
        echo "   Verifique se:"
        echo "   1. O servidor está rodando no outro PC"
        echo "   2. O firewall está permitindo porta 8000"
        echo "   3. Ambos estão na mesma rede"
        exit 1
    fi
fi

echo ""

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado! Instale o Docker primeiro."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não encontrado! Instale o Docker Compose primeiro."
    exit 1
fi

echo "✅ Docker encontrado"
echo ""

# Build e start
echo "🏗️  Buildando e iniciando cliente..."
docker-compose -f docker-compose-client.yml up -d --build

echo ""
echo "✅ Cliente RPC iniciado com sucesso!"
echo ""
echo "🎮 Para usar a calculadora, execute:"
echo "   docker attach rpc_client"
echo ""
echo "💡 Dicas:"
echo "   - Para sair sem parar: Ctrl+P depois Ctrl+Q"
echo "   - Para ver logs: docker logs rpc_client --follow"
echo "   - Para parar: docker-compose -f docker-compose-client.yml down"
echo ""
echo "📊 Acesse o monitor do servidor em:"
echo "   http://$RPC_SERVER_HOST:5000"
echo ""
