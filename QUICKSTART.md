# 🚀 Quick Start - Sistema Distribuído

## Cenário 1: Tudo em um PC (desenvolvimento/testes)

```bash
docker-compose up -d --build
docker attach rpc_client
```

Acesse monitor: http://localhost:5000

---

## Cenário 2: Dois PCs (produção/simulação real)

### 📍 PC 1 - SERVIDOR

**Windows:**
```cmd
start-server.bat
```

**Linux/Mac:**
```bash
./start-server.sh
```

✅ **Anote o IP que aparecer** (ex: 192.168.1.100)

---

### 📍 PC 2 - CLIENTE

**Windows:**
```cmd
start-client.bat
```
_(vai pedir o IP do servidor)_

**Linux/Mac:**
```bash
./start-client.sh
```
_(vai pedir o IP do servidor)_

**Ou configure via .env:**
```bash
cp .env.example .env
# Edite .env e configure RPC_SERVER_HOST=192.168.1.100
./start-client.sh
```

---

## 🎮 Usar o cliente

```bash
docker attach rpc_client
```

**Sair sem parar:** `Ctrl+P` + `Ctrl+Q`  
**Parar:** Opção `0` no menu

---

## 📊 Monitor

**No PC servidor:**  
http://localhost:5000

**De qualquer PC na rede:**  
http://IP_DO_SERVIDOR:5000

Exemplo: http://192.168.1.100:5000

---

## 🛑 Parar tudo

**PC Servidor:**
```bash
docker-compose -f docker-compose-server.yml down
```

**PC Cliente:**
```bash
docker-compose -f docker-compose-client.yml down
```

---

## 🐛 Problemas?

**"Connection refused"**
1. Servidor está rodando? `docker ps`
2. Firewall permite porta 8000?
3. IPs corretos?

**Testar conectividade:**
```bash
# Windows
Test-NetConnection -ComputerName 192.168.1.100 -Port 8000

# Linux/Mac
nc -zv 192.168.1.100 8000
```

**Ver logs:**
```bash
docker logs rpc_server --follow
docker logs rpc_client --follow
```

---

## 📚 Documentação Completa

Veja [INSTALL_DISTRIBUIDO.md](INSTALL_DISTRIBUIDO.md) para:
- Configuração de firewall detalhada
- Troubleshooting avançado
- Cenários com VPN/Internet
- Conceitos de SD explicados
