# Cooperación 2v1 y posesión

## Problema y MDP

Dos atacantes comparten el balón frente a un defensor que se aproxima. Deben mantener la posesión durante más de 50 pasos y completar al menos tres pases. El MDP simplificado es $\langle S,A,P,R,\gamma\rangle$.

| Componente | Definición implementada |
|---|---|
| $S$ | Zona $x,y$ del balón, distancia y ángulo al compañero, distancia y ángulo al defensor, pases completados (0 a 3) y pasos de posesión (0 a 51). |
| $A$ | `PASE`, `DRIBLE`, `GIRAR +35`, `DESPEJE`. |
| $P$ | PASE transfiere la posesión si el defensor no corta el segmento; DRIBLE mueve al portador y al balón; el defensor se acerca 0,2 m por paso. |
| $R$ | $+30$ por pase completado, $-30$ por intercepción, $-10$ por salida y pequeña recompensa por conservar el balón. |
| $\gamma$ | 0,99 en el notebook. |

Las zonas tienen tamaños $4\times3$ para posición del balón, $3\times4$ para el vector al compañero y $3\times4$ para el vector al defensor. Se agregan 4 categorías de pases y 52 de tiempo de posesión porque la condición terminal depende de ambos. Así, $|S|=1728\times4\times52=359\,424$, $|A|=4$ y la tabla densa tendría $1\,437\,696$ valores Q. Se usa una tabla dispersa. El pase se intercepta si el defensor está a $\leq1{,}5$ m de su recorrido o por una probabilidad aleatoria de $0{,}05$; el contacto a $\leq1{,}2$ m también pierde la posesión.

Los cortes espaciales separan regiones del campo; las distancias al compañero (5 y 12 m) distinguen pases cortos y largos, y las del defensor (3 y 10 m) reflejan riesgo cercano o remoto. Los contadores se conservan con resolución exacta hasta el criterio de éxito: agrupar los pasos 1 y 49 ocultaría cuándo termina el episodio. El coste es una tabla potencialmente grande; usar solo estados visitados reduce memoria, pero puede exigir muchos episodios para aprender una política estable.

La recompensa implementada es

$$
r_{t+1}=0{,}2+30\,\mathbf{1}\{\text{pase completo}\}+100\,\mathbf{1}\{\text{éxito}\}-30\,\mathbf{1}\{\text{intercepción}\}-10\,\mathbf{1}\{\text{balón fuera}\}.
$$

El episodio acaba por éxito, pérdida del balón, salida del campo o 70 pasos. `04_passing_possession.ipynb` muestra el entrenamiento y los indicadores después de ejecutar sus celdas. El criterio de éxito del enunciado aún debe verificarse empíricamente.

## Alcance del modelo

La cooperación se modela alternando al portador tras un pase. El defensor usa una regla sencilla de persecución; no existe una segunda política aprendida. El cliente UDP actual no parsea compañeros ni rivales, por lo que estas observaciones todavía no están disponibles para ejecutar el agente 2v1 dentro de `rcssserver`.
