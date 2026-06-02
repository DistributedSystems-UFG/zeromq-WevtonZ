[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wa7oHGos)
# ZeroMQ-Examples

Exemplos de comunicação distribuída com ZeroMQ, baseados em Tanenbaum & van Steen (2025). Os processos foram adaptados para execução em **máquinas distintas na AWS**.

## Pré-requisitos

- Python 3
- pyzmq (`pip install pyzmq`)

---

## 1. Client-Server (Request-Reply)

O cliente envia uma mensagem ao servidor, que responde com a mensagem acrescida de `*`.

```
Cliente (REQ)  ──────►  Servidor (REP)
               ◄──────
```

| Arquivo | Papel | Onde rodar |
|---|---|---|
| `client-server/server.py` | Servidor — escuta na porta `5679` | Máquina A |
| `client-server/client.py` | Cliente — conecta ao IP do servidor | Máquina B |

### Configuração

Em `client.py`, altere o IP na linha `socket.connect(...)` para o IP da máquina que roda o servidor.

### Execução

```bash
# Máquina A (servidor) — iniciar primeiro
python3 server.py

# Máquina B (cliente)
python3 client.py
```

---

## 2. Pub-Sub (Publish-Subscribe)

O servidor publica a hora atual a cada 5 segundos. Clientes assinam o tópico `TIME` e recebem as mensagens.

```
Publisher (PUB)  ──────►  Subscriber 1 (SUB)
                 ──────►  Subscriber 2 (SUB)
                 ──────►  ...
```

| Arquivo | Papel | Onde rodar |
|---|---|---|
| `pub-sub/server.py` | Publisher — publica na porta `5679` | Máquina A |
| `pub-sub/client.py` | Subscriber — conecta ao IP do publisher | Máquina B |

### Configuração

Em `client.py`, altere o IP na linha `socket.connect(...)` para o IP da máquina que roda o servidor.

### Execução

```bash
# Máquina A (publisher) — iniciar primeiro
python3 server.py

# Máquina B (subscriber)
python3 client.py
```

O subscriber recebe 5 mensagens e encerra automaticamente.

---

## 3. Pipeline Producer-Consumer (3 estágios)

Pipeline de 3 processos que simula uma rede de sensores de temperatura:

```
Producer (PUSH) ──► Worker (PULL/PUSH) ──► Sink (PULL)
  Gera leituras       Classifica temp.      Agrega estatísticas
  (Máquina A)         (Máquina B)           (Máquina C)
```

- **Producer**: gera leituras aleatórias de 5 sensores (temperatura entre 20°C e 50°C)
- **Worker**: recebe as leituras, classifica em `NORMAL` (<30°C), `WARNING` (30-40°C) ou `CRITICAL` (>40°C), e encaminha
- **Sink**: agrega os dados e exibe estatísticas em tempo real (média, contadores por classificação)

| Arquivo | Papel | Socket ZMQ | Onde rodar |
|---|---|---|---|
| `pipeline_producer-consumer/producer.py` | Estágio 1 — Gera dados | `PUSH` (bind porta 5678) | Máquina A |
| `pipeline_producer-consumer/worker.py`   | Estágio 2 — Classifica (consumer/producer) | `PULL` + `PUSH` (bind porta 5679) | Máquina B |
| `pipeline_producer-consumer/sink.py`     | Estágio 3 — Agrega resultados | `PULL` | Máquina C |
| `pipeline_producer-consumer/constPipe.py`| Configuração de IPs e portas | — | Todas |

### Configuração

Em `constPipe.py`, atualize os IPs das suas instâncias AWS:

```python
PRODUCER_ADDR = "<IP da Máquina A>"   # IP da máquina que roda producer.py
WORKER_ADDR   = "<IP da Máquina B>"   # IP da máquina que roda worker.py
```

### Execução

```bash
# Máquina B (worker) — iniciar primeiro
python3 worker.py 1

# Máquina C (sink)
python3 sink.py

# Máquina A (producer) — iniciar por último
python3 producer.py
```

Encerre qualquer processo com `Ctrl+C`. O Sink exibe um relatório final ao ser encerrado.
