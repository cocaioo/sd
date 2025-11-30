# ��� Calculadora RPC Distribuída

Sistema de calculadora distribuída usando XML-RPC com Docker. Demonstra conceitos de Sistemas Distribuídos com cliente-servidor em máquinas diferentes.

## ��� O que faz

- **Servidor RPC**: processa operações (somar, subtrair, multiplicar, dividir)
- **Cliente**: interface interativa que envia requisições ao servidor
- **Monitor Web**: painel em tempo real mostrando todas as operações RPC

---

## ��� Como executar

### Opção 1: Tudo em um PC (desenvolvimento/testes)

```bash
# Subir tudo
docker-compose up -d --build

# Usar o cliente
docker attach rpc_client

# Acessar monitor
# http://localhost:5000
```

**Para sair do cliente sem parar:** `Ctrl+P` + `Ctrl+Q`

**Para parar tudo:**
```bash
docker-compose down
```

---

### Opção 2: Distribuído em 2 PCs (cenário real)

**Requisito:** Ambos na mesma rede Wi-Fi/LAN

#### PC 1 - Servidor

```bash
# Iniciar servidor
bash start-server.sh

# Descobrir IP
ipconfig.exe  # Windows
# ou
hostname -I   # Linux/Mac

# Anote o IP (ex: 192.168.15.8)
```

#### PC 2 - Cliente

```bash
# Iniciar cliente
bash start-client.sh
# Digite o IP do servidor quando pedir

# Conectar
docker attach rpc_client
```

**Ambos podem acessar o monitor:**
```
http://IP_DO_SERVIDOR:5000
```

---

## ��� Como usar

Ao conectar no cliente, você verá:

```
====== CLIENTE RPC - CALCULADORA DISTRIBUÍDA ======
Selecione a operação:
1 - Somar
2 - Subtrair
3 - Multiplicar
4 - Dividir
0 - Sair
===================================================
```

Escolha uma operação, digite os números e veja o resultado!

---

## ��� Estrutura

```
sd/
├── server/              # Servidor RPC (Python)
├── client/              # Cliente interativo (Python)
├── monitor/             # Monitor web (Flask)
├── docker-compose.yml   # Modo local (tudo junto)
├── docker-compose-server.yml  # Só servidor
├── docker-compose-client.yml  # Só cliente
├── start-server.sh      # Script iniciar servidor
└── start-client.sh      # Script iniciar cliente
```

---

## ��� Comandos úteis

```bash
# Ver logs
docker logs rpc_server --follow
docker logs rpc_client --follow
docker logs rpc_monitor --follow

# Ver containers rodando
docker ps

# Parar tudo
docker-compose down

# Parar e limpar volumes
docker-compose down -v

# Reconectar ao cliente
docker attach rpc_client
```

---

## ��� Cenários suportados

✅ Mesma rede Wi-Fi  
✅ Mesma rede cabeada (LAN)  
✅ VPN (ZeroTier, Hamachi, Tailscale)  
✅ Internet (com port forwarding no roteador)  

**Mais fácil:** Mesma rede Wi-Fi/LAN  
**Para casas diferentes:** Use VPN (ZeroTier recomendado)

---

## ��� Problemas comuns

**"Connection refused"**
- Verifique se o servidor está rodando: `docker ps`
- Teste conectividade: `ping IP_DO_SERVIDOR`
- Configure firewall (Windows): permitir portas 8000 e 5000

**Cliente não conecta**
- Confirme que ambos estão na mesma rede
- Verifique o IP do servidor está correto
- Teste: `telnet IP_DO_SERVIDOR 8000`

**Monitor vazio**
- Normal em modo distribuído (mostra apenas eventos do servidor)
- Faça uma operação no cliente para aparecer eventos

---

## ��� Documentação adicional


