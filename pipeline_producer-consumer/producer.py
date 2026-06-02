import zmq, time, pickle, random
from constPipe import PIPE_PORT1

SENSORS = ["S01", "S02", "S03", "S04", "S05"]

def producer():
    context = zmq.Context()
    socket  = context.socket(zmq.PUSH)
    socket.bind(f"tcp://*:{PIPE_PORT1}")
    print(f"[Producer] Bind na porta {PIPE_PORT1} — aguardando workers...\n")

    time.sleep(1)

    task_id = 0
    try:
        while True:
            task_id += 1
            reading = {
                "id":          task_id,
                "sensor":      random.choice(SENSORS),
                "temperature": round(random.uniform(20.0, 50.0), 1),
                "timestamp":   time.strftime("%H:%M:%S"),
            }
            socket.send(pickle.dumps(reading))
            print(f"[Producer] #{task_id:03d}  sensor={reading['sensor']}  "
                  f"temp={reading['temperature']:5.1f}°C  ({reading['timestamp']})")
            time.sleep(random.uniform(0.5, 1.5))
    except KeyboardInterrupt:
        print(f"\n[Producer] Encerrado após {task_id} leituras.")
    finally:
        socket.close()
        context.term()

if __name__ == "__main__":
    producer()