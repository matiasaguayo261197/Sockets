import socket
import select

def run_server():
    server_ip = "127.0.0.1"
    port = 8000

    # Creación del socket del servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reusar el puerto inmediatamente si el servidor se reinicia
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((server_ip, port))
    server_socket.listen()

    # Mantené una lista activa de conexiones 
    # Se inicializa con el socket del servidor para escuchar nuevas conexiones
    sockets_list = [server_socket]

    print(f"Servidor escuchando en {server_ip}:{port}")

    try:
        while True:
            # select() bloquea hasta que al menos un socket esté listo para lectura
            read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

            for notified_socket in read_sockets:
                # Si el socket notificado es el servidor, hay una nueva conexión entrante
                if notified_socket == server_socket:
                    client_socket, client_address = server_socket.accept()
                    sockets_list.append(client_socket)
                    print(f"Nueva conexión de {client_address[0]}:{client_address[1]}")
                
                # Si es un socket de cliente, está enviando un mensaje
                else:
                    try:
                        message = notified_socket.recv(1024)
                        
                        # Si recv() devuelve 0 bytes, el cliente se desconectó
                        if not message:
                            print(f"Conexión cerrada por {notified_socket.getpeername()}")
                            sockets_list.remove(notified_socket) # Si alguien se va, borralo 
                            notified_socket.close()
                            continue
                        
                        print(f"Mensaje recibido de {notified_socket.getpeername()}")
                        
                        # Implementá broadcast: si un cliente habla, todos escuchan 
                        dead_clients=[]
                        for client in sockets_list:
                            # Enviar a todos excepto al servidor y al emisor original
                            if client != server_socket and client != notified_socket:
                                try:
                                    client.send(message)
                                except Exception:
                                    # Detectá cuando un socket está muerto y sacalo de la lista
                                    
                                    dead_clients.append(client)
                        for clietn in dead_clients:
                            sockets_list.remove(clietn)
                            client.close()
                                    
                    except Exception as e:
                        # Manejá desconexiones inesperadas con elegancia [cite: 50]
                        print(f"Error recibiendo mensaje: {e}")
                        sockets_list.remove(notified_socket)
                        notified_socket.close()

            # Manejo de sockets con excepciones
            for notified_socket in exception_sockets:
                sockets_list.remove(notified_socket)
                notified_socket.close()

    except KeyboardInterrupt:
        print("\nApagando el servidor...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    run_server()