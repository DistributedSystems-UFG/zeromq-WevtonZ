import zmq, time, pickle, sys, random
from constPipe import PRODUCER_ADDR, PIPE_PORT1, PIPE_PORT2


def classify(temp):
    """Classifica a temperatura em faixas de alerta."""
    if temp < 30.0:
        return "NORMAL"
    elif temp < 40.0:
        return "WARNING"
    else:
        return "CRITICAL"


ICONS = {"NORMAL": "✅", "WARNING": "⚠️", "CRITICAL": "🔴"}

def worker(worker_id):
    context = zmq.Context()

    # Socket PULL — consome dados do Producer
    receiver = context.socket(zmq.PULL)
    receiver.connect(f"tcp://{PRODUCER_ADDR}:{PIPE_PORT1}")

    # Socket PUSH — produz dados para o Sink
    sender = context.socket(zmq.PUSH)
    sender.bind(f"tcp://*:{PIPE_PORT2}")

    print(f"[Worker {worker_id:03d}] Online — "
          f"PULL de {PRODUCER_ADDR}:{PIPE_PORT1} | PUSH na porta {PIPE_PORT2}\n")

    processed = 0
    try:
        while True:
            reading = pickle.loads(receiver.recv())
            processed += 1

            classification = classify(reading["temperature"])
            result = {
                **reading,
                "classification": classification,
                "processed_by":   worker_id,
                "processed_at":   time.strftime("%H:%M:%S"),
            }

            icon = ICONS[classification]
            print(f"[Worker {worker_id:03d}] #{reading['id']:03d}  "
                  f"{reading['sensor']}  {reading['temperature']:5.1f}°C "
                  f"→ {icon} {classification}")

            sender.send(pickle.dumps(result))
    except KeyboardInterrupt:
        print(f"\n[Worker {worker_id:03d}] Encerrado após {processed} itens processados.")
    finally:
        receiver.close()
        sender.close()
        context.term()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        meu_id = int(sys.argv[1])
    else:
        meu_id = random.randint(1, 999)
    worker(meu_id)