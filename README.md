# Projeto RPC - Calculadora Distribuída

Este repositório contém uma versão didática de uma calculadora distribuída usando XML-RPC em Python.
O projeto inclui:

- Um serviço `server` (XML-RPC) que implementa operações de cálculo (somar, subtrair, multiplicar, dividir).
- Um `client` de terminal que usa `xmlrpc.client` e fornece uma interface em modo texto.
- Um `monitor` web simples (Flask) que exibe eventos gerados pelo `server` e pelo `client` em tempo real.
- Um `docker-compose.yml` que empacota os três serviços e compartilha um volume `rpc_shared` para eventos.

Este README documenta passo-a-passo como usar, debugar e estender o sistema.

---

## Estrutura do projeto

Principais arquivos e diretórios:

- `docker-compose.yml` : define os serviços `server`, `client` e `monitor`, e o volume `rpc_shared`.
- `server/` : código do servidor RPC (`server.py`) e `Dockerfile`.
- `client/` : cliente interativo (`client.py`) e `Dockerfile`.
- `monitor/` : frontend Flask que lê `/shared/events.log` e mostra no navegador.
- `README.md` : este arquivo.

---

## Pré-requisitos

- Docker e Docker Compose instalados e funcionando no sistema.
- (Opcional) Python 3.11+ se quiser executar componentes localmente sem Docker.

---

## Como subir tudo (modo recomendado: Docker)

1. Na raiz do projeto (onde está `docker-compose.yml`) execute:

```bash
docker-compose up --build -d
```

Esse comando reconstrói as imagens (caso necessário) e sobe os três serviços em background.

2. Verifique status dos containers:

```bash
docker-compose ps
# ou
docker ps -a
```

Você deve ver os containers `rpc_server`, `rpc_client` e `rpc_monitor` com STATUS `Up`.

---

## Acessando o Monitor Web

- Abra o navegador em: `http://localhost:5000`.
- O monitor mostra os eventos recentes escritos em `/shared/events.log` por ambos `server` e `client`.
- A UI atual é leitura (histórico + atualização automática a cada ~1.5s). Ela não substitui a calculadora interativa do `client` (que roda no terminal).

---

## Usando a calculadora (cliente interativo)

O cliente é um app de terminal dentro do container `rpc_client`. Existem 3 maneiras de usá-lo:

1) Anexar ao processo principal do container (rápido):

```bash
docker attach rpc_client
```

- Observação: `docker attach` conecta ao stdin/stdout do processo principal do container.
- Se a tela abrir em branco, pressione `ENTER` — o menu textual aparecerá.
- Para desconectar do attach sem parar o container, use `Ctrl-p` `Ctrl-q`.

2) Abrir um shell dentro do container e rodar o cliente (recomendado para desenvolvimento):

```bash
docker exec -it rpc_client /bin/sh
# dentro do container:
python -u client.py
```

Essa abordagem cria um TTY novo e evita alguns problemas de attach.

3) Rodar o cliente localmente (sem Docker) — útil apenas para depuração:

```bash
# a partir da raiz do projeto
python client/client.py
```

Certifique-se que o `server` esteja acessível como `http://server:8000/RPC2` quando dentro do Docker, ou `http://localhost:8000/RPC2` se rodando tudo localmente.

---

## Teste rápido via script (do host)

Se quiser testar o servidor sem abrir o cliente interativo, execute no host:

```bash
python - <<'PY'
import xmlrpc.client
s = xmlrpc.client.ServerProxy("http://localhost:8000/RPC2")
print('somar(2,3) ->', s.somar(2,3))
PY
```

---

## Logs e monitoramento

- Logs do Flask Monitor:
```bash
docker logs -f rpc_monitor
```
- Logs do servidor e cliente:
```bash
docker logs -f rpc_server
docker logs -f rpc_client
```
- O arquivo compartilhado de eventos fica em `/shared/events.log` dentro dos containers; para inspecioná-lo diretamente:

```bash
docker exec -it rpc_monitor /bin/sh -c "tail -n 200 /shared/events.log || true"
```

O `events.log` contém um JSON por linha com formato:

```json
{"ts": "2025-11-26T..Z", "source": "client|server", "type": "request|response|error", "payload": {...}}
```

---

## Parar e remover os containers

```bash
docker-compose down
```

Esse comando para e remove os containers (mas mantém o volume `rpc_shared` por padrão). Para remover também volumes use:

```bash
docker-compose down -v
```

---

## Problemas comuns e soluções

- Monitor não sobe / erro `flask_cors` import error:
  - Verifique se a imagem do `monitor` foi reconstruída após adicionar dependências:
    ```bash
    docker-compose build monitor
    docker-compose up -d monitor
    ```

- `docker attach` mostra tela em branco:
  - Pressione `ENTER` para forçar reimpressão do prompt.
  - Recomendo `docker exec -it rpc_client /bin/sh` + `python -u client.py` para desenvolvimento interativo.

- `events.log` vazio ou sem atualizações:
  - Confirme que o volume `rpc_shared` está montado em todos os containers (`docker inspect rpc_monitor` e verificar `Mounts`).
  - Verifique permissões: dentro do `rpc_monitor`, rode `ls -la /shared`.

- Container com ExitCode != 0:
  - Veja `docker logs <container>` para stacktrace.

---

## Desenvolvimento e extensão

- Adicionar frontend interativo no `monitor`:
  - A UI atual já pode ser expandida para enviar chamadas XML-RPC diretamente ao servidor. Posso implementar essa funcionalidade se quiser.

- Melhorias possíveis:
  - Filtros por método/cliente/servidor, contadores em tempo real, thumbnails, histórico persistente em base leve.
  - Substituir desenvolvimento Flask server por WSGI (gunicorn) para produção.

---

## Arquivo `docker-compose.yml` importante (resumo)

- Serviços: `server` (porta 8000), `client`, `monitor` (porta 5000).
- Volume compartilhado: `rpc_shared` → montado em `/shared` nos 3 containers.

---

Se preferir, eu posso gerar um `README_pt_BR.md` com capturas de tela e exemplos de uso passo-a-passo (prints). Também posso implementar o frontend web interativo (botões + formulário) no `monitor` agora — diga qual próximo passo prefere.

Obrigado — se algo falhar ao rodar os comandos acima cole aqui a saída que eu te ajudo a corrigir.
