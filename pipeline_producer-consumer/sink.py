import zmq, time, pickle
from constPipe import WORKER_ADDR, PIPE_PORT2


def sink():
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.connect(f"tcp://{WORKER_ADDR}:{PIPE_PORT2}")

    print(f"[Sink] Online — PULL de {WORKER_ADDR}:{PIPE_PORT2}")
    print("[Sink] Aguardando dados classificados...\n")

    stats = {"NORMAL": 0, "WARNING": 0, "CRITICAL": 0}
    total = 0
    temp_sum = 0.0
    icons = {"NORMAL": "✅", "WARNING": "⚠️", "CRITICAL": "🔴"}

    try:
        while True:
            result = pickle.loads(receiver.recv())
            total += 1
            temp_sum += result["temperature"]
            stats[result["classification"]] += 1

            avg = temp_sum / total
            icon = icons[result["classification"]]

            print(f"── Leitura #{result['id']:03d} ──────────────────────────")
            print(f"  Sensor:         {result['sensor']}")
            print(f"  Temperatura:    {result['temperature']:5.1f}°C  {icon} {result['classification']}")
            print(f"  Produzido em:   {result['timestamp']}")
            print(f"  Processado em:  {result['processed_at']}  (worker {result['processed_by']:03d})")
            print(f"  ── Estatísticas (total: {total}) ──")
            print(f"  Média: {avg:5.1f}°C | "
                  f"Normal: {stats['NORMAL']} | "
                  f"Warning: {stats['WARNING']} | "
                  f"Critical: {stats['CRITICAL']}")
            print()
    except KeyboardInterrupt:
        print(f"\n{'='*45}")
        print(f"[Sink] Relatório final — {total} leituras recebidas")
        print(f"  Média geral:  {temp_sum/total:.1f}°C" if total else "  Nenhuma leitura.")
        print(f"  ✅ Normal:    {stats['NORMAL']}")
        print(f"  ⚠️  Warning:  {stats['WARNING']}")
        print(f"  🔴 Critical:  {stats['CRITICAL']}")
        print(f"{'='*45}")
    finally:
        receiver.close()
        context.term()


if __name__ == "__main__":
    sink()
