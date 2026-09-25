# Persecución e intercepción del balón

## Problema y MDP

El agente parte cerca de $x=-15$ m con orientación variable. El balón aparece a una distancia inicial aleatoria entre 5 y 40 m, dentro de la cancha. Debe acercarse hasta el radio de captura de $0{,}8$ m. El MDP implementado es $\langle S,A,P,R,\gamma\rangle$.

| Componente | Definición implementada |
|---|---|
| $S$ | Distancia relativa $d_b$ y ángulo relativo $\theta_b$, discretizados en 4 zonas cada uno. |
| $A$ | `DASH 100`, `DASH 50`, `TURN +35`, `TURN -35`. |
| $P$ | Los giros cambian la orientación $35^\circ$; DASH desplaza al jugador 1,5 o 0,75 m en su dirección actual. El balón permanece fijo durante el episodio. |
| $R$ | Reducción de distancia, coste temporal y bonificación por captura. |
| $\gamma$ | 0,99 en los experimentos del notebook. |

La observación polar se obtiene de la posición del balón respecto al jugador. El ángulo cero apunta al frente del jugador. Los intervalos de distancia son $[0,0{,}8)$, $[0{,}8,3)$, $[3,8)$ y $[8,\infty)$ m. Los cuatro sectores angulares son frente $[-45,45)$, izquierda $[45,135)$, atrás y derecha $[-135,-45)$ grados. Así, $|S|=4\times4=16$, $|A|=4$ y la tabla densa tendría $64$ valores $Q(s,a)$. El código almacena solo estados visitados.

El primer umbral de distancia coincide con el radio de captura. Los siguientes separan aproximación cercana (unos pocos DASH) de navegación lejana. El sector frontal permite privilegiar avance; los laterales y el posterior indican cuándo girar. Esta compresión mantiene pequeña la tabla, aunque pierde diferencias entre, por ejemplo, 8 y 40 m.

La recompensa al ejecutar $a_t$ es

$$
r_{t+1}=d_{b,t}-d_{b,t+1}-0{,}2+100\,\mathbf{1}\{\text{captura válida}\}-20\,\mathbf{1}\{\text{salida del campo}\}.
$$

El episodio termina por captura, salida de la cancha o al llegar a 40 pasos. Para el indicador de **éxito** se exige captura en *menos de* 40 pasos. El objetivo del enunciado es una tasa de captura superior al 90 % y menos de 40 pasos. Ese umbral debe medirse tras ejecutar el entrenamiento; aquí no se afirma que se haya alcanzado.

## Alcance del modelo

Este entorno reproduce las acciones como desplazamientos ideales por paso. No incorpora inercia, energía, ciclos UDP ni ruido visual. El notebook `01_ball_pursuit.ipynb` compara dos estrategias de exploración, muestra $G_0$, éxito, pasos, una estimación de $V^*$ y $\pi^*$, y una trayectoria 2D. Una celda opcional comprueba los clientes de jugador y trainer en `rcssserver`; no mide allí la política entrenada.
