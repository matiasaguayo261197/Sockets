import socket
import threading
import sys
import time

def escuchar_al_servidor(socket_del_cliente):
    """Hilo secundario dedicado únicamente a imprimir en pantalla lo que llega del servidor."""
    while True:
        try:
            mensaje_recibido = socket_del_cliente.recv(1024)
            
            if not mensaje_recibido:
                print("\n[!] El servidor cerró la conexión.")
                break
                
            texto_decodificado = mensaje_recibido.decode('utf-8')
            print(f"\n[Chat]: {texto_decodificado}")
            print("> Escribí tu mensaje: ", end="", flush=True)
            
        except Exception as error_de_lectura:
            print(f"\n[!] Desconexión abrupta: {error_de_lectura}")
            break
            
    socket_del_cliente.close()

def iniciar_cliente_chat():
    ip_del_servidor = "127.0.0.1"
    puerto_del_servidor = 8000

    # Bucle principal para implementar reintentos si algo falla [cite: 50]
    while True:
        socket_del_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[*] Intentando conectar a {ip_del_servidor}:{puerto_del_servidor}...")
        
        try:
            socket_del_cliente.connect((ip_del_servidor, puerto_del_servidor))
            print("[*] Conectado exitosamente. El chat está vivo.")
        except Exception:
            print(f"[!] Fallo al conectar. Reintentando en 3 segundos...")
            time.sleep(3)
            continue

        # Inicia un hilo daemon para escuchar sin bloquear la entrada del usuario 
        hilo_receptor_de_mensajes = threading.Thread(
            target=escuchar_al_servidor, 
            args=(socket_del_cliente,)
        )
        hilo_receptor_de_mensajes.daemon = True 
        hilo_receptor_de_mensajes.start()

        try:
            while True:
                # El hilo principal se queda aquí, esperando que el usuario escriba
                texto_del_usuario = input("> Escribí tu mensaje: ")
                
                if texto_del_usuario.lower() == 'salir':
                    print("Saliendo del chat...")
                    sys.exit(0)
                    
                if socket_del_cliente.fileno() == -1:
                    break
                    
                mensaje_codificado = texto_del_usuario.encode("utf-8")[:1024]
                socket_del_cliente.send(mensaje_codificado)
                
        except KeyboardInterrupt:
            print("\nCerrando terminal de chat...")
            sys.exit(0)
        except Exception as error_de_red:
            print(f"[!] Error de red: {error_de_red}")
        finally:
            socket_del_cliente.close()
            print("[*] Conexión perdida. Reiniciando ciclo...")
            time.sleep(2)

if __name__ == "__main__":
    iniciar_cliente_chat()