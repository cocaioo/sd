# Calculadora RPC (guia rápido)

Projeto didático: uma calculadora distribuída por XML-RPC, empacotada com Docker.

Contém três componentes principais:

- `server`: servidor XML-RPC (operações: somar, subtrair, multiplicar, dividir).
- `client`: cliente em modo texto (menu interativo) que chama o `server`.
- `monitor`: frontend web (Flask) que mostra eventos do `client` e do `server`.

O `docker-compose.yml` sobe os três serviços e cria um volume compartilhado (`rpc_shared`) para troca de eventos.

## 🌐 Deployment Distribuído - Simulação Real de SD

Este projeto pode rodar em **dois PCs diferentes** para simular um cenário real de Sistemas Distribuídos!

### 📡 Cenários Suportados

**✅ Mesma rede Wi-Fi** (mais comum)
- Ambos os PCs conectados no mesmo Wi-Fi
- Exemplo: você e seu colega na mesma casa/laboratório

**✅ Mesma rede cabeada (LAN)**
- PCs conectados via cabo Ethernet no mesmo switch/roteador

**✅ Redes diferentes via VPN**
- Use VPN como Hamachi, ZeroTier ou Tailscale
- Simula conexão pela internet de forma segura

**✅ Internet pública (com port forwarding)**
- Configure port forwarding no roteador
- Servidor acessível pela internet (não recomendado para produção sem segurança)

---

### 🚀 Passo a Passo Completo

#### **PC 1: Configurar como SERVIDOR**

1. **Inicie o Docker Desktop** (aguarde até aparecer "Docker is running")

2. **Abra o terminal na pasta do projeto** (`sd/`)

3. **Execute o script de servidor:**
   
   **Git Bash / Linux / Mac:**
   ```bash
   bash start-server.sh
   ```
   
   **PowerShell / CMD (Windows):**
   ```cmd
   start-server.bat
   ```
   
   **Ou manualmente:**
   ```bash
   docker-compose -f docker-compose-server.yml up -d --build
   ```

4. **Descubra seu IP:**
   
   **Windows (PowerShell/CMD):**
   ```cmd
   ipconfig
   ```
   Procure por "IPv4 Address" na sua conexão ativa (Wi-Fi ou Ethernet)
   
   **Linux/Mac:**
   ```bash
   hostname -I
   # ou
   ifconfig
   ```
   
   **Exemplo de IP:** `192.168.15.8`

5. **Anote esse IP!** Você vai passar para quem rodar o cliente.

6. **Acesse o monitor no navegador:**
   ```
   http://localhost:5000
   ```
   Ou pela rede:
   ```
   http://192.168.15.8:5000
   ```
   (substitua pelo seu IP real)

7. **Verifique se está tudo rodando:**
   ```bash
   docker ps
   ```
   Você deve ver `rpc_server` e `rpc_monitor` com status `Up`

---

#### **PC 2: Configurar como CLIENTE**

1. **Clone o repositório ou copie a pasta** `sd/` para o segundo PC

2. **Inicie o Docker Desktop**

3. **Abra o terminal na pasta do projeto** (`sd/`)

4. **Execute o script de cliente:**
   
   **Git Bash / Linux / Mac:**
   ```bash
   bash start-client.sh
   ```
   
   **PowerShell / CMD (Windows):**
   ```cmd
   start-client.bat
   ```

5. **Quando pedir, digite o IP do servidor** (ex: `192.168.15.8`)

6. **Aguarde o build e início do cliente**

7. **Conecte ao cliente interativo:**
   ```bash
   docker attach rpc_client
   ```

8. **Use a calculadora!** 🎉
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

9. **Para sair sem parar o container:**
   - Pressione `Ctrl+P` seguido de `Ctrl+Q`

10. **Acesse o monitor do servidor:**
    ```
    http://192.168.15.8:5000
    ```
    (use o IP do PC servidor)

---

### 🔧 Configuração Manual (alternativa)

Se preferir configurar manualmente sem os scripts:

**No PC Cliente, crie um arquivo `.env`:**
```bash
cp .env.example .env
```

**Edite o `.env` e configure:**
```env
RPC_SERVER_HOST=192.168.15.8
RPC_SERVER_PORT=8000
```

**Depois execute:**
```bash
docker-compose -f docker-compose-client.yml up -d --build
docker attach rpc_client
```

---

### 📊 Monitoramento em Tempo Real

**Ambos os PCs podem acessar o monitor** abrindo no navegador:
```
http://IP_DO_SERVIDOR:5000
```

O monitor mostra:
- ✅ Todas as requisições RPC (request)
- ✅ Todas as respostas (response)
- ✅ Erros (error)
- ✅ Timestamp de cada operação
- ✅ Parâmetros e resultados

**Teste:** Faça uma operação no cliente e veja aparecer instantaneamente no monitor! 🚀

---

### 🐛 Resolução de Problemas

**❌ "Connection refused" no cliente**

1. Verifique se o servidor está rodando:
   ```bash
   docker ps
   ```

2. Teste conectividade do cliente para o servidor:
   
   **Windows:**
   ```powershell
   Test-NetConnection -ComputerName 192.168.15.8 -Port 8000
   ```
   
   **Linux/Mac:**
   ```bash
   nc -zv 192.168.15.8 8000
   # ou
   telnet 192.168.15.8 8000
   ```

3. Verifique o firewall do Windows no PC servidor:
   ```powershell
   # Permitir porta 8000
   netsh advfirewall firewall add rule name="RPC Server" dir=in action=allow protocol=TCP localport=8000
   
   # Permitir porta 5000
   netsh advfirewall firewall add rule name="RPC Monitor" dir=in action=allow protocol=TCP localport=5000
   ```

4. Confirme que ambos estão na mesma rede:
   ```bash
   ping 192.168.15.8
   ```

**❌ IP errado configurado**

Reconfigure o IP:
```bash
docker-compose -f docker-compose-client.yml down
RPC_SERVER_HOST=192.168.15.8 docker-compose -f docker-compose-client.yml up -d
```

**❌ Monitor não mostra eventos**

É normal em cenário distribuído - o monitor mostra apenas eventos do servidor (onde ele está hospedado).

---

### 🎯 Exemplo Completo de Uso

**Cenário:** Você (PC 1) e seu colega (PC 2) na mesma rede Wi-Fi

**PC 1 - Seu computador (192.168.15.8):**
```bash
# 1. Iniciar servidor
bash start-server.sh

# 2. Descobrir IP
ipconfig.exe | grep "IPv4"
# Resultado: 192.168.15.8

# 3. Abrir monitor
# http://localhost:5000
```

**PC 2 - Computador do colega:**
```bash
# 1. Iniciar cliente
bash start-client.sh
# Digite quando pedir: 192.168.15.8

# 2. Conectar ao cliente
docker attach rpc_client

# 3. Fazer uma operação
# Escolha: 1 (Somar)
# Digite: 10 e 20
# Resultado: 30

# 4. Ver no monitor (navegador)
# http://192.168.15.8:5000
```

**Resultado:** Vocês verão a operação acontecendo em tempo real! O cliente está no PC 2, mas o cálculo acontece no PC 1. 🎉

---

👉 **Documentação completa:** [INSTALL_DISTRIBUIDO.md](INSTALL_DISTRIBUIDO.md)  
👉 **Guia rápido:** [QUICKSTART.md](QUICKSTART.md)

---

## Estrutura do projeto

- `docker-compose.yml`  — define os serviços e volume compartilhado.
# Calculadora RPC (guia rápido)

Projeto didático: uma calculadora distribuída por XML-RPC, empacotada com Docker.

Contém três componentes principais:

- `server`: servidor XML-RPC (operações: somar, subtrair, multiplicar, dividir).
- `client`: cliente em modo texto (menu interativo) que chama o `server`.
- `monitor`: frontend web (Flask) que mostra eventos do `client` e `server`.

O `docker-compose.yml` sobe os três serviços e cria um volume compartilhado (`rpc_shared`) para troca de eventos.
---

## Estrutura do projeto

- `docker-compose.yml`  — define os serviços e volume compartilhado.
- `server/`             — código do servidor (`server.py`).
- `client/`             — código do cliente (`client.py`).
- `monitor/`            — app Flask e templates do monitor.
- `README.md`           — este guia.
---

## Pré-requisitos

- Docker e Docker Compose instalados.
- Navegador para acessar o monitor (http://localhost:5000).
---

## Como subir (Docker)

1) Na pasta do projeto, rode:

```bash
docker-compose up --build -d
```

2) Verifique os containers:

```bash
docker-compose ps
```

Procure por `rpc_server`, `rpc_client` e `rpc_monitor` com status `Up`.
---

## Monitor (web)

- Abra: `http://localhost:5000`.
- O monitor mostra eventos recentes (requisições, respostas e erros) gerados pelo `client` e `server`.

Observação: o monitor é um painel de observação; a calculadora interativa continua sendo o cliente em terminal.
---

## Usar a calculadora (cliente)

Opções principais:

- Anexar ao processo já em execução:

```bash
docker attach rpc_client
```

Se a tela aparecer vazia, pressione `ENTER`. Para sair do attach sem parar o container: `Ctrl-p` `Ctrl-q`.

- Abrir um shell no container e rodar o cliente (recomendado):

```bash
docker exec -it rpc_client /bin/sh
python -u client.py
```

- Rodar localmente (sem Docker): execute `python client/client.py` a partir da raiz do projeto.

Dentro do Docker, o `server` está disponível pelo endereço `http://server:8000/RPC2`.
---

## Teste rápido (do host)

Para testar o servidor diretamente:

```bash
python - <<'PY'
import xmlrpc.client
s = xmlrpc.client.ServerProxy("http://localhost:8000/RPC2")
print('somar(2,3) ->', s.somar(2,3))
PY
```
---

## Logs e arquivo de eventos

- Ver logs do monitor (Flask):

```bash
docker logs -f rpc_monitor
```

- Ver logs do servidor/cliente:

```bash
docker logs -f rpc_server
docker logs -f rpc_client
```

- Inspecionar o arquivo de eventos (compartilhado):

```bash
docker exec -it rpc_monitor /bin/sh -c "tail -n 200 /shared/events.log || true"
```

O arquivo `events.log` contém um JSON por linha com entradas do tipo `request`, `response` ou `error`.
---

## Parar e remover

Parar e remover containers (não remove volumes):

```bash
docker-compose down
```

Para também remover volumes:

```bash
docker-compose down -v
```
---

## Problemas comuns

- Erro `flask_cors` ao iniciar o monitor: reconstrua a imagem do monitor:

```bash
docker-compose build monitor
docker-compose up -d monitor
```

- `docker attach` sem saída visível: pressione `ENTER` ou use `docker exec -it rpc_client /bin/sh`.

- `events.log` sem conteúdo: verifique se o volume `rpc_shared` está montado em todos os containers e as permissões em `/shared`.

- Container com erro: consulte `docker logs <container>` para a mensagem completa.
---

## Próximos passos (opcionais)

- Adicionar ao `monitor` um formulário para chamar o `server` diretamente e exibir resultados na web.
- Melhorias: filtros, métricas por método e histórico em banco leve.
---

## Resumo rápido

- Subir tudo: `docker-compose up --build -d`
- Abrir monitor: `http://localhost:5000`
- Usar cliente: `docker attach rpc_client`
