# [cite_start]Challenge 4: Reconstrucción de la Comunicación Global [cite: 3, 36]

## [cite_start]¿Quién sos después de este reto? [cite: 21, 54]
[cite_start]Soy Matías, un desarrollador que dejó de depender de bibliotecas de lujo y frameworks mágicos [cite: 5, 38] para entender cómo fluyen realmente los bytes. Ahora comprendo la capa de transporte (TCP), la multiplexación de sockets y cómo gestionar la concurrencia a bajo nivel usando la API del sistema operativo.

## [cite_start]¿Cómo sobrevivió tu aplicación? [cite: 21, 54]
La aplicación se mantuvo estable aplicando tres conceptos clave:
1. [cite_start]**Concurrencia con Selectores en el Servidor:** Utilizando la función `select` [cite: 12, 45][cite_start], el servidor es capaz de monitorear múltiples descriptores de archivo simultáneamente en un solo bucle, evitando el uso excesivo de hilos y sin explotar la CPU[cite: 8, 41].
2. [cite_start]**Eliminación Diferida (Deferred Deletion):** Para evitar bugs de desplazamiento al iterar, el broadcast se realiza sobre la lista de sockets activos y, si ocurre un fallo, los clientes desconectados se agrupan en una lista temporal (`dead_clients`) para ser eliminados de forma segura una vez finalizado el ciclo[cite: 13, 14, 46].
3. **Multihilo en el Cliente:** Se implementó `threading` para separar la lectura del teclado (`stdin`) de la recepción de datos del socket. [cite_start]Esto garantiza que el usuario pueda escribir y ver mensajes en tiempo real, sin lag[cite: 15, 16, 48, 49].

## [cite_start]¿Qué aprendiste cuando todo se rompió? [cite: 22, 55]
[cite_start]Que la red es inestable por naturaleza y hay que programar asumiendo el caos[cite: 10, 43]. Aprendí que:
* [cite_start]Cuando la función `recv()` devuelve 0 bytes, significa que el cliente cerró la conexión abruptamente y el socket está muerto[cite: 18, 51].
* Iterar y modificar una lista al mismo tiempo rompe el flujo del programa.
* [cite_start]Capturar excepciones de red (como `ConnectionResetError`) y limpiar los recursos con elegancia es lo que mantiene vivo al servidor aunque la mitad de los clientes se desconecte[cite: 17, 20, 50, 53].
* [cite_start]Los reintentos de conexión automáticos en el cliente son esenciales para recuperarse de caídas temporales del servidor[cite: 19, 52].