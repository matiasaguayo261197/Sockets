import socket
import threading

# Variable global para que todos los hilos sepan quiénes están conectados
lista_de_conexiones_activas = []

def manejar_comunicacion_del_cliente(socket_del_cliente, direccion_ip_del_cliente):
    """Este hilo se dedica exclusivamente a escuchar a un solo cliente en un bucle infinito."""
    print(f"Nueva conexión de {direccion_ip_del_cliente[0]}:{direccion_ip_del_cliente[1]}")
    lista_de_conexiones_activas.append(socket_del_cliente)

    try:
        while True:
            # Se queda esperando el mensaje de este cliente específico
            mensaje_recibido = socket_del_cliente.recv(1024)
            
            # Si recv() devuelve 0 bytes, el cliente cerró su terminal
            if not mensaje_recibido:
                print(f"Conexión cerrada por {direccion_ip_del_cliente}")
                break
            
            print(f"Mensaje recibido de {direccion_ip_del_cliente}")
            
            # Implementá broadcast: si un cliente habla, todos escuchan [cite: 44]
            repartir_mensaje_a_todos(mensaje_recibido, socket_del_cliente)
            
    except Exception as error_de_red:
        # Manejá desconexiones inesperadas con elegancia [cite: 49]
        print(f"Error con el cliente {direccion_ip_del_cliente}: {error_de_red}")
    finally:
        # Mantené una lista activa de conexiones. Si alguien se va, borralo con dignidad [cite: 45]
        if socket_del_cliente in lista_de_conexiones_activas:
            lista_de_conexiones_activas.remove(socket_del_cliente)
        socket_del_cliente.close()

def repartir_mensaje_a_todos(mensaje_recibido, socket_emisor):
    """Envía el mensaje a todos los clientes excepto al que lo mandó."""
    clientes_desconectados = []
    
    for socket_destino in lista_de_conexiones_activas:
        if socket_destino != socket_emisor:
            try:
                socket_destino.send(mensaje_recibido)
            except Exception:
                # Detectá cuando un socket está muerto y sacalo de la lista [cite: 50]
                clientes_desconectados.append(socket_destino)
    
    for socket_roto in clientes_desconectados:
        if socket_roto in lista_de_conexiones_activas:
            lista_de_conexiones_activas.remove(socket_roto)
        socket_roto.close()

def iniciar_servidor_de_chat():
    ip_del_servidor = "127.0.0.1"
    puerto_del_servidor = 8000

    socket_principal_del_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_principal_del_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_principal_del_servidor.bind((ip_del_servidor, puerto_del_servidor))
    socket_principal_del_servidor.listen()

    print(f"Servidor escuchando en {ip_del_servidor}:{puerto_del_servidor} (Modo: Multi-hilos)")

    try:
        while True:
            # El hilo principal se bloquea aquí esperando que alguien llame a la puerta
            nuevo_socket_de_cliente, direccion_ip_del_cliente = socket_principal_del_servidor.accept()
            
            # Por cada cliente que entra, creamos un hilo independiente para que lo atienda
            hilo_del_cliente = threading.Thread(
                target=manejar_comunicacion_del_cliente, 
                args=(nuevo_socket_de_cliente, direccion_ip_del_cliente)
            )
            # Daemon True asegura que si apagamos el servidor, los hilos secundarios mueran también
            hilo_del_cliente.daemon = True
            hilo_del_cliente.start()
            
    except KeyboardInterrupt:
        print("\nApagando el servidor...")
    finally:
        socket_principal_del_servidor.close()

if __name__ == "__main__":
    iniciar_servidor_de_chat()