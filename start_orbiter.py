import os
import sys
import time
import subprocess
import signal
import socket

# Find absolute paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
REDIS_EXE = os.path.join(BASE_DIR, "redis", "redis-server.exe")
REDIS_CONF = os.path.join(BASE_DIR, "redis", "redis.windows.conf")
BACKEND_DIR = BASE_DIR
FRONTEND_DIR = os.path.join(BASE_DIR, "dashboard")

processes = []

def signal_handler(sig, frame):
    print("\nShutting down all Orbiter background services...")
    cleanup()
    sys.exit(0)

def cleanup():
    for name, proc in processes:
        if proc.poll() is None:
            print(f"Terminating {name}...")
            try:
                proc.terminate()
                proc.wait(timeout=3)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass
    print("All services stopped.")

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def check_redis_available():
    # Wait up to 5 seconds for Redis to start accepting connections
    for _ in range(5):
        try:
            import redis
            r = redis.Redis(host='127.0.0.1', port=6379, socket_connect_timeout=1)
            r.ping()
            return True
        except Exception:
            time.sleep(1)
    return False

def flush_redis_queues():
    try:
        import redis
        r = redis.Redis(host='127.0.0.1', port=6379)
        r.flushall()
        print("Redis flushed successfully (cleared old pending background tasks).")
    except Exception as e:
        print(f"Warning: Could not flush Redis: {e}")

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("====================================================")
    print("       Orbiter Mission Control Launcher")
    print("====================================================")
    print(f"Project root: {BASE_DIR}")
    print("Starting background services natively on Windows...\n")

    # 1. Start Redis
    if os.path.exists(REDIS_EXE):
        print("[1/5] Launching native Redis server...")
        try:
            redis_proc = subprocess.Popen(
                [REDIS_EXE, REDIS_CONF],
                cwd=BASE_DIR,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            processes.append(("Redis Server", redis_proc))
        except Exception as e:
            print(f"ERROR starting Redis: {e}")
            sys.exit(1)
    else:
        print("WARNING: Local redis-server.exe not found. Expecting an external Redis server on port 6379.")

    if not check_redis_available():
        print("ERROR: Redis is not running on port 6379. Please start Redis.")
        cleanup()
        sys.exit(1)
        
    print("Redis Server is active.")
    flush_redis_queues()

    # Set up environment variables
    env = os.environ.copy()
    env["PYTHONPATH"] = BASE_DIR

    # 2. Start FastAPI Backend
    print("[2/5] Launching FastAPI Backend...")
    try:
        backend_proc = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
            cwd=BASE_DIR,
            env=env
        )
        processes.append(("FastAPI Backend", backend_proc))
    except Exception as e:
        print(f"ERROR starting Backend: {e}")
        cleanup()
        sys.exit(1)

    # 3. Start Celery Worker
    print("[3/5] Launching Celery Worker (thread-pooled)...")
    try:
        # Use pool=threads for Windows compatibility
        celery_proc = subprocess.Popen(
            [sys.executable, "-m", "celery", "-A", "backend.tasks.celery_app", "worker", "--loglevel=info", "--pool=threads"],
            cwd=BASE_DIR,
            env=env
        )
        processes.append(("Celery Worker", celery_proc))
    except Exception as e:
        print(f"ERROR starting Celery Worker: {e}")
        cleanup()
        sys.exit(1)

    # 4. Start Celery Beat
    print("[4/5] Launching Celery Beat Scheduler...")
    try:
        beat_proc = subprocess.Popen(
            [sys.executable, "-m", "celery", "-A", "backend.tasks.celery_app", "beat", "--loglevel=info"],
            cwd=BASE_DIR,
            env=env
        )
        processes.append(("Celery Beat", beat_proc))
    except Exception as e:
        print(f"ERROR starting Celery Beat: {e}")
        cleanup()
        sys.exit(1)

    # 5. Start Frontend Vite Server
    print("[5/5] Launching Vite React Dashboard...")
    try:
        npm_cmd = "npm.cmd" if os.name == 'nt' else "npm"
        frontend_proc = subprocess.Popen(
            [npm_cmd, "run", "dev"],
            cwd=FRONTEND_DIR
        )
        processes.append(("Vite React Dashboard", frontend_proc))
    except Exception as e:
        print(f"ERROR starting Vite Frontend: {e}")
        cleanup()
        sys.exit(1)

    print("\n====================================================")
    print("  ALL SERVICES RUNNING NATIVELY ON WINDOWS!")
    print("  - Backend API:   http://localhost:8000")
    print("  - Dashboard UI:  http://localhost:5173")
    print("====================================================")
    print("Press Ctrl+C to shut down all processes cleanly.\n")

    # Monitor processes
    try:
        while True:
            for name, proc in processes:
                status = proc.poll()
                if status is not None:
                    print(f"\nCRITICAL: {name} terminated with exit code {status}.")
                    cleanup()
                    sys.exit(1)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down all Orbiter background services...")
        cleanup()

if __name__ == "__main__":
    main()
