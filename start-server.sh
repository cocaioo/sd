#!/bin/bash

# ============================================================
# Script para configurar e iniciar o SERVIDOR RPC
# Execute este script no PC que vai hospedar o servidor
# ============================================================

set -e

echo "🚀 Configurando PC como SERVIDOR RPC..."
echo ""

# Detectar IP automaticamente
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    SERVER_IP=$(hostname -I | awk '{print $1}')
elif [[ "$OSTYPE" == "darwin"* ]]; then
    SERVER_IP=$(ipconfig getifaddr en0 || ipconfig getifaddr en1)
else
    echo "⚠️  Sistema não suportado para detecção automática de IP"
    SERVER_IP="<detectar manualmente>"
fi

echo "📡 IP detectado: $SERVER_IP"
echo ""
echo "⚠️  IMPORTANTE: Compartilhe este IP com quem for rodar o cliente!"
echo "   O cliente precisará configurar: RPC_SERVER_HOST=$SERVER_IP"
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

# Configurar firewall (Linux com ufw)
if command -v ufw &> /dev/null; then
    echo "🔥 Configurando firewall..."
    sudo ufw allow 8000/tcp comment 'RPC Server'
    sudo ufw allow 5000/tcp comment 'RPC Monitor'
    echo "✅ Firewall configurado"
    echo ""
fi

# Build e start
echo "🏗️  Buildando e iniciando containers..."
docker-compose -f docker-compose-server.yml up -d --build

echo ""
echo "✅ Servidor RPC iniciado com sucesso!"
echo ""
echo "📊 URLs de acesso:"
echo "   - Servidor RPC: http://$SERVER_IP:8000"
echo "   - Monitor Web:  http://$SERVER_IP:5000"
echo ""
echo "🔍 Verificar status:"
echo "   docker ps"
echo ""
echo "📜 Ver logs:"
echo "   docker logs rpc_server --follow"
echo "   docker logs rpc_monitor --follow"
echo ""
echo "🛑 Parar servidor:"
echo "   docker-compose -f docker-compose-server.yml down"
echo ""
