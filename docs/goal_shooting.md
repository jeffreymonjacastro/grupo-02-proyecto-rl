# Definición y tiro a puerta

## Problema y MDP

El delantero dispone de un único disparo por episodio. Se estudian dos escenarios: arco abierto y portero activo. El MDP es $\langle S,A,P,R,\gamma\rangle$.

| Componente | Definición implementada |
|---|---|
| $S$ | Distancia al arco, ángulos relativos a ambos postes y zona vertical del portero; el valor 0 indica que no hay portero. |
| $A$ | 15 combinaciones de potencia $\{40,70,100\}$ y dirección $\{-20,-10,0,10,20\}$ grados de `KICK`. |
| $P$ | Un rayo sale del balón con el ángulo elegido y alcance $0{,}2\times\text{potencia}$ metros. Se comprueba cruce con la línea de gol y posible bloqueo. |
| $R$ | $+100$ por gol, $-30$ por fallo, $-50$ por bloqueo. |
| $\gamma$ | 0,99 en el experimento, aunque no altera un retorno de un solo paso. |

La distancia al arco se divide por 12 y 16 m; cada ángulo por $-15$, 0 y 15 grados; la posición del portero tiene cuatro valores (ausente, abajo, centro, arriba). Por tanto, $|S|=3\times4\times4\times4=192$ y $|A|=15$, con $2880$ entradas posibles. La tabla se llena solo en estados visitados.

Los cortes de distancia se relacionan con el alcance de las tres potencias: aproximadamente 8, 14 y 20 m. Los cortes angulares separan tiros centrados de los dirigidos a un lateral. La zona del portero reduce el espacio tabular, pero es más gruesa que su radio de bloqueo de 1,5 m; por eso una tasa de conversión obtenida en este modelo no debe interpretarse como precisión física del servidor.

Para un disparo que llega a $x_g$, su coordenada vertical estimada es

$$
y_{\mathrm{impacto}}=y_b+(x_g-x_b)\tan(\theta_{\mathrm{cuerpo}}+\theta_{\mathrm{acción}}).
$$

El disparo es gol si $|y_{\mathrm{impacto}}|\leq7$ m y el portero no se encuentra a $1{,}5$ m o menos de ese punto. El objetivo del enunciado es convertir más del 75 % con arco abierto y más del 50 % con portero activo. El notebook `03_goal_shooting.ipynb` entrena y muestra ambos escenarios por separado; los porcentajes reales quedan pendientes de ejecución.

## Alcance del modelo

Este cálculo geométrico omite velocidad real del balón, física del portero y ruido. `robocup_client.py` todavía no extrae la posición del portero ni los postes individuales. El entrenamiento actual demuestra el MDP simplificado; una evaluación dentro de `rcssserver` requerirá ampliar esa percepción y controlar el escenario con el trainer.
