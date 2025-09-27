Este sistema es una aplicación en Python que funciona como un motor de reglas lógicas para encontrar la mejor ruta de transporte público entre dos puntos, no solo la más corta.

Componente	Qué Hace	Valor Inteligente
Modelado de la Red	Utiliza la librería NetworkX para representar el sistema de transporte como un grafo (nodos = estaciones; aristas = tramos/líneas).	Permite aplicar algoritmos de búsqueda eficientes.
Interacción con el Usuario	Pregunta al usuario el punto A, el punto B, y una preferencia de viaje (ej., si requiere accesibilidad).	Las preferencias del usuario se convierten en las reglas activas.
Motor de Reglas Lógicas	Aplica penalizaciones a los tramos de la ruta basándose en la Base de Conocimiento y las preferencias del usuario.	Convierte preferencias subjetivas en costos matemáticos.
Algoritmo de Búsqueda	Ejecuta el algoritmo Dijkstra utilizando un costo ponderado dinámicamente por el motor de reglas.	Encuentra la ruta con el menor costo ajustado (la mejor ruta según las reglas).
