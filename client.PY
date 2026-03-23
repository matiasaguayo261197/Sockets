import socket
import threading
import sys
import time

def escuchar_servidor(client_socket):
    while True:
        try:
            # Recibe los mensajes en tiempo real [cite: 48]
            mensaje = client_socket.recv(1024)
            
            # Si el servidor cae, recv devuelve 0 bytes
            if not mensaje:
                print("\n[!] El servidor cerró la conexión.")
                break
                
            print(f"\n[Chat]: {mensaje.decode('utf-8')}")
            print("> Escribí tu mensaje: ", end="", flush=True)
            
        except Exception as e:
            # Manejo de error si el socket muere abruptamente 
            break
            
    # Cierra el socket de este lado para que el hilo principal se entere
    client_socket.close()

def run_client():
    server_ip = "127.0.0.1"
    server_port = 8000

    # Bucle principal para implementar reintentos 
    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[*] Intentando conectar a {server_ip}:{server_port}...")
        
        try:
            client_socket.connect((server_ip, server_port))
            print("[*] Conectado exitosamente. El chat está vivo.")
        except Exception as e:
            print(f"[!] Fallo al conectar. Reintentando en 3 segundos... ")
            time.sleep(3)
            continue

        # Inicia un hilo daemon para escuchar sin bloquear el input del usuario 
        hilo_escucha = threading.Thread(target=escuchar_servidor, args=(client_socket,))
        hilo_escucha.daemon = True 
        hilo_escucha.start()

        try:
            while True:
                # El input bloquea este hilo, pero el hilo_escucha sigue activo 
                msg = input("> Escribí tu mensaje: ")
                
                if msg.lower() == 'salir':
                    print("Saliendo del chat...")
                    sys.exit(0)
                    
                # Si el socket se cerró en el otro hilo, salimos para reconectar
                if client_socket.fileno() == -1:
                    break
                    
                client_socket.send(msg.encode("utf-8")[:1024])
                
        except Exception as e:
            print(f"[!] Error de red: {e}")
        finally:
            client_socket.close()
            print("[*] Conexión perdida. Reiniciando ciclo... ")
            time.sleep(2)

if __name__ == "__main__":
    run_client()