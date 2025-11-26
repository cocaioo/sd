# Calculadora RPC (guia rápido)

Projeto didático: uma calculadora distribuída por XML-RPC, empacotada com Docker.

Contém três componentes principais:

- `server`: servidor XML-RPC (operações: somar, subtrair, multiplicar, dividir).
- `client`: cliente em modo texto (menu interativo) que chama o `server`.
- `monitor`: frontend web (Flask) que mostra eventos do `client` e do `server`.

O `docker-compose.yml` sobe os três serviços e cria um volume compartilhado (`rpc_shared`) para troca de eventos.
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
- Usar cliente: `docker exec -it rpc_client /bin/sh` → `python -u client.py`
