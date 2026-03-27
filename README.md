# 🌐 Protocolo Cero: Chat en Tiempo Real con Sockets

Un sistema de comunicación de terminal a terminal construido desde cero, utilizando puramente la biblioteca estándar de Python (`socket`, `threading`, `select`). Sin frameworks mágicos ni dependencias externas. 

Este proyecto demuestra la capacidad de gestionar concurrencia, implementar lógica de broadcast y sobrevivir a desconexiones abruptas en un entorno de red inestable.

---

## 📜 Entregables: Respuestas al Challenge

### [cite_start]¿Quién sos después de este reto? [cite: 78]
Un desarrollador full-stack junior que ahora entiende que la red no es magia negra, sino un entorno hostil donde las conexiones pueden fallar en cualquier milisegundo. Antes daba por sentado que los mensajes de una web app simplemente llegaban a su destino gracias a los frameworks de alto nivel; ahora entiendo el trabajo sucio que ocurre por debajo: mantener los puertos abiertos, gestionar los bloqueos de I/O y limpiar la memoria a mano cuando los nodos desaparecen.

### [cite_start]¿Cómo sobrevivió tu aplicación? [cite: 79]
Sobrevivió gracias a una arquitectura estrictamente defensiva y a la separación de responsabilidades:
* **En el Servidor:** La aplicación nunca confía ciegamente en que un envío de datos (`send`) será exitoso. Todo intento de comunicación está envuelto en bloques `try/except`. Si un cliente colapsa, el servidor captura el error, aísla el socket roto en una lista temporal y lo purga de las conexiones activas sin detener el ciclo de multiplexación que atiende a los demás.
* **En el Cliente:** El programa sobrevive separando la lectura y la escritura. Un hilo demonio (`daemon thread`) se encarga de escuchar los mensajes del servidor en segundo plano, evitando que la función bloqueante `input()` congele la recepción de datos. Además, implementa un bucle infinito que reintenta la conexión automáticamente si el servidor principal se cae.

### [cite_start]¿Qué aprendiste cuando todo se rompió? [cite: 79]
Aprendí tres lecciones fundamentales sobre el caos en la red:
1.  **La concurrencia es obligatoria:** Enviar y recibir datos en un solo hilo bloquea la terminal. Si no delegas la escucha a procesos paralelos o selectores, tu chat se convierte en un sistema por turnos.
2.  **Nunca iterar y eliminar al mismo tiempo:** Intentar borrar un socket desconectado de la misma lista que el servidor está recorriendo para hacer un broadcast desincroniza los índices y corrompe el programa. 
3.  **Los cierres limpios son un mito:** Rara vez un cliente avisa que se va a desconectar. El servidor debe estar preparado para interpretar un paquete de `0 bytes` o un error `Broken Pipe` como una señal de salida, manejándolo con elegancia para que el sistema siga operando.

---

## 🛠️ Ejecución

1. Levantar el servidor en una terminal: `python server.py`
2. Conectar N cantidad de clientes en terminales separadas: `python client.py`