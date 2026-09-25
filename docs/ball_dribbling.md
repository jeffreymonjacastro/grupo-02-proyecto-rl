# Conducción y drible del balón

## Problema y MDP

El agente debe transportar el balón hacia la portería rival durante más de 30 m sin perder el control. Se modela mediante $\langle S,A,P,R,\gamma\rangle$.

| Componente | Definición implementada |
|---|---|
| $S$ | Tupla $(d_b,\theta_b,d_g,\theta_g)$: balón y arco en coordenadas relativas al jugador. |
| $A$ | `KICK 25`, `DASH 80`, `TURN +35`, `TURN -35`. |
| $P$ | KICK desplaza el balón 1,2 m si está a no más de 1,2 m del jugador; DASH mueve al jugador 0,8 m; TURN modifica la orientación. |
| $R$ | Avance hacia la meta, coste por paso y penalizaciones por pérdida de posesión, salida de campo o pateo inválido. |
| $\gamma$ | 0,99 en el notebook. |

La distancia al balón usa tres zonas con fronteras $0{,}8$ y $1{,}2$ m. La distancia a meta usa cuatro con fronteras $20$, $40$ y $60$ m. Ambos ángulos usan los cuatro sectores definidos en [persecución](ball_pursuit.md). Por ello, $|S|=3\times4\times4\times4=192$, $|A|=4$ y una tabla completa tendría $768$ entradas. Q se almacena dispersamente.

Los dos umbrales cercanos del balón distinguen control inmediato, posibilidad de micro-pateo y necesidad de alcanzarlo. La meta admite zonas más amplias porque su distancia cambia lentamente por acción. Los sectores angulares distinguen avance alineado y corrección de rumbo. El límite es que dos distancias dentro de una misma zona pueden requerir secuencias diferentes de KICK y DASH.

Con $d_g$ medido desde el **balón** hasta el centro de la portería para calcular avance, la recompensa es

$$
r_{t+1}=2(d_{g,t}-d_{g,t+1})-0{,}1+100\,\mathbf{1}\{\text{éxito}\}-30\,\mathbf{1}\{\text{pérdida o salida}\}-2\,\mathbf{1}\{\text{pateo inválido}\}.
$$

La posesión se conserva mientras la separación jugador-balón sea $\leq2$ m. El episodio acaba al superar 30 m de avance, perder posesión, salir del campo o completar 80 pasos. La meta del enunciado exige mantener el balón en más del 80 % de los episodios; la tasa se calcula a partir de `success` cuando se ejecute el notebook.

## Alcance del modelo

El micro-pateo no reproduce rozamiento, rebotes ni ciclos de `rcssserver`. La observación `goal_opp` del cliente real permite aproximar orientación a meta, pero el entrenamiento documentado en `02_ball_dribbling.ipynb` usa esta física local. Se deberán contrastar sus decisiones en el simulador oficial antes de atribuirle rendimiento real.
