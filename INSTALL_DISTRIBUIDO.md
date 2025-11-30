# 🌐 Sistema RPC Distribuído - Guia de Instalação

Este guia explica como executar o sistema RPC de forma **distribuída entre dois computadores**, simulando um cenário real de Sistemas Distribuídos.

## 📋 Pré-requisitos

Ambos os PCs precisam ter:
- Docker instalado
- Docker Compose instalado
- Conexão na mesma rede (LAN ou VPN)
- Firewall configurado para permitir as portas necessárias

---

## 🖥️ **PC 1: SERVIDOR** (hospeda o servidor RPC + monitor)

### Passo 1️⃣: Descubra o IP do PC servidor

**Windows:**
```bash
ipconfig
```
Procure por "IPv4 Address" na interface de rede ativa (ex: `192.168.1.100`)

**Linux/Mac:**
```bash
hostname -I
# ou
ip addr show
```

**Anote esse IP!** Você vai precisar passar para o colega.

### Passo 2️⃣: Configure o Firewall

**Windows:**
```powershell
# Permitir porta 8000 (servidor RPC)
netsh advfirewall firewall add rule name="RPC Server" dir=in action=allow protocol=TCP localport=8000

# Permitir porta 5000 (monitor web)
netsh advfirewall firewall add rule name="RPC Monitor" dir=in action=allow protocol=TCP localport=5000
```

**Linux (ufw):**
```bash
sudo ufw allow 8000/tcp
sudo ufw allow 5000/tcp
```

### Passo 3️⃣: Inicie o servidor

```bash
cd sd
docker-compose -f docker-compose-server.yml up -d --build
```

### Passo 4️⃣: Verifique se está funcionando

```bash
# Verificar containers rodando
docker ps

# Testar se o servidor está acessível
curl http://localhost:8000
```

### Passo 5️⃣: Acesse o monitor

Abra no navegador: `http://localhost:5000`

O monitor também estará acessível na rede em: `http://<SEU_IP>:5000`

---

## 💻 **PC 2: CLIENTE** (executa o cliente RPC)

### Passo 1️⃣: Configure o IP do servidor

**Opção A - Criar arquivo `.env`:**

Crie um arquivo `.env` na pasta `sd/`:
```bash
RPC_SERVER_HOST=192.168.1.100
RPC_SERVER_PORT=8000
```
(Substitua `192.168.1.100` pelo IP real do PC servidor)

**Opção B - Exportar variável de ambiente:**

**Windows (PowerShell):**
```powershell
$env:RPC_SERVER_HOST="192.168.1.100"
```

**Linux/Mac (Bash):**
```bash
export RPC_SERVER_HOST="192.168.1.100"
```

### Passo 2️⃣: Teste a conectividade

Antes de rodar o cliente, confirme que consegue alcançar o servidor:

```bash
# Windows
Test-NetConnection -ComputerName 192.168.1.100 -Port 8000

# Linux/Mac
nc -zv 192.168.1.100 8000
# ou
telnet 192.168.1.100 8000
```

Se não conectar, verifique:
- Firewall do PC servidor
- Se ambos estão na mesma rede
- Se o IP está correto

### Passo 3️⃣: Inicie o cliente

**Com arquivo `.env`:**
```bash
cd sd
docker-compose -f docker-compose-client.yml up -d --build
```

**Passando variável direto:**
```bash
cd sd
RPC_SERVER_HOST=192.168.1.100 docker-compose -f docker-compose-client.yml up -d --build
```

### Passo 4️⃣: Conecte ao cliente interativo

```bash
docker attach rpc_client
```

Agora você verá o menu da calculadora! 🎉

### Passo 5️⃣: Use a calculadora

```
====== CLIENTE RPC - CALCULADORA DISTRIBUÍDA ======
Selecione a operação:
1 - Somar
2 - Subtrair
3 - Multiplicar
4 - Dividir
0 - Sair
===================================================
Opção: 1
```

Para sair do cliente **sem parar o container**, pressione: `Ctrl+P` seguido de `Ctrl+Q`

Para parar o cliente completamente: escolha opção `0` no menu.

---

## 🔍 Monitoramento em Tempo Real

Ambos os PCs podem acessar o monitor web do servidor:

```
http://<IP_DO_SERVIDOR>:5000
```

Exemplo: `http://192.168.1.100:5000`

O monitor mostrará **todas as operações RPC** que acontecem entre cliente e servidor em tempo real!

---

## 🛠️ Comandos Úteis

### Ver logs do servidor (PC 1)
```bash
docker logs rpc_server --follow
```

### Ver logs do cliente (PC 2)
```bash
docker logs rpc_client --follow
```

### Parar tudo (em cada PC)
```bash
# PC 1 (servidor)
docker-compose -f docker-compose-server.yml down

# PC 2 (cliente)
docker-compose -f docker-compose-client.yml down
```

### Limpar volumes e recomeçar
```bash
# PC 1
docker-compose -f docker-compose-server.yml down -v

# PC 2
docker-compose -f docker-compose-client.yml down -v
```

### Re-anexar ao cliente
```bash
docker attach rpc_client
```

---

## 🐛 Troubleshooting

### ❌ "Connection refused" no cliente

**Causas comuns:**
1. Firewall bloqueando porta 8000 no servidor
2. IP errado configurado
3. Servidor não está rodando

**Solução:**
```bash
# No PC servidor, verifique se está rodando:
docker ps | grep rpc_server

# Teste conectividade do PC cliente:
ping <IP_DO_SERVIDOR>
telnet <IP_DO_SERVIDOR> 8000
```

### ❌ Cliente não consegue resolver hostname "server"

**Causa:** Variável `RPC_SERVER_HOST` não foi configurada.

**Solução:** Configure o `.env` ou exporte a variável antes de rodar o docker-compose.

### ❌ Monitor não mostra eventos

**Causa:** Cliente e servidor podem estar usando volumes diferentes.

**Solução no cenário distribuído:** O monitor só mostra eventos do servidor (que é onde está hospedado). Isso é normal em cenários distribuídos reais.

### ❌ Não consigo sair do cliente

Pressione: `Ctrl+P` depois `Ctrl+Q` (detach sem parar)

Ou escolha opção `0` no menu (encerra o cliente)

---

## 🎯 Cenários de Teste

### Cenário 1: Rede Local (mesma WiFi/Ethernet)
- PC 1 e PC 2 conectados na mesma rede
- Use IP local (192.168.x.x)
- Ideal para testes em casa/laboratório

### Cenário 2: Internet (via VPN ou IP público)
- Configure VPN (Hamachi, ZeroTier, Tailscale)
- Ou use port forwarding no roteador
- Use IP da VPN ou IP público

### Cenário 3: Máquinas Virtuais
- Rode duas VMs na mesma máquina
- Configure rede em modo Bridge
- Simula ambiente distribuído

---

## 📊 Arquitetura Distribuída

```
┌─────────────────────┐         Rede Local/Internet        ┌─────────────────────┐
│    PC 1 (Servidor)  │◄────────────────────────────────►│    PC 2 (Cliente)   │
├─────────────────────┤          Porta 8000 (RPC)         ├─────────────────────┤
│                     │          Porta 5000 (Monitor)     │                     │
│  ┌───────────────┐  │                                   │  ┌───────────────┐  │
│  │  RPC Server   │  │                                   │  │  RPC Client   │  │
│  │  (port 8000)  │  │                                   │  │   (stub)      │  │
│  └───────────────┘  │                                   │  └───────────────┘  │
│                     │                                   │                     │
│  ┌───────────────┐  │                                   │                     │
│  │   Monitor     │  │                                   │                     │
│  │  (port 5000)  │  │                                   │                     │
│  └───────────────┘  │                                   │                     │
└─────────────────────┘                                   └─────────────────────┘
         │                                                          │
         └──────────────── HTTP (eventos RPC) ─────────────────────┘
```

---

## 🎓 Conceitos de SD Demonstrados

✅ **Comunicação Cliente-Servidor:** Cliente e servidor em máquinas diferentes  
✅ **Transparência de Localização:** Cliente não precisa saber onde servidor está  
✅ **Middleware RPC:** XML-RPC abstrai comunicação em rede  
✅ **Serialização/Deserialização:** Parâmetros convertidos para XML e transmitidos  
✅ **Stub/Skeleton:** Cliente usa stub local, servidor processa via skeleton  
✅ **Monitoramento Distribuído:** Monitor centralizado observa todas interações  

---

## 📝 Notas Importantes

- O cliente pode rodar em **vários PCs simultaneamente**, todos conectando ao mesmo servidor
- O monitor mostra eventos de **todos os clientes** conectados
- Em produção, use HTTPS e autenticação (este é um exemplo didático)
- Latência de rede será visível (observe os delays nas operações)

---

## 🚀 Próximos Passos

Experimente:
1. Rodar múltiplos clientes simultaneamente
2. Simular falhas de rede (desconectar WiFi temporariamente)
3. Medir latência das operações
4. Implementar timeout e retry no cliente
5. Adicionar autenticação/segurança

---

**Dúvidas?** Verifique os logs com `docker logs <container_name> --follow`
