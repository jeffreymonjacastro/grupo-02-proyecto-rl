# Tareas acotadas de P1

Estos cuatro informes describen el MDP y la implementación reducida de cada tarea:

1. [Persecución del balón](ball_pursuit.md)
2. [Conducción y drible](ball_dribbling.md)
3. [Tiro a puerta](goal_shooting.md)
4. [Pase y posesión 2v1](passing_possession.md)

Cada módulo en `src/tasks/` es un **modelo cinemático local** que permite experimentar con Q-Learning tabular y comparar exploración. Sus transiciones no reproducen la física, el ruido sensorial ni las reglas completas de `rcssserver`. El cliente UDP y el trainer permiten comprobar por separado la conexión con RoboCup cuando Docker esté listo. Los resultados del modelo local se deben identificar como simulados.

En cada modelo, un estado físico continuo $x_t$ evoluciona por una regla $f$ y se resume mediante una discretización $\phi$. La transición tabular que se intenta aprender es

$$
P(s'\mid s,a)=\Pr\!\left(\phi(f(x_t,a,\xi_t))=s'\mid\phi(x_t)=s\right),
$$

donde $\xi_t$ representa la aleatoriedad del escenario o del defensor. Como un mismo bin puede contener posiciones físicas diferentes, esta transición es una **aproximación de MDP**; el estado discreto puede perder información. Las tablas Q aprenden de episodios observados y no requieren escribir cada probabilidad $P$ a mano.

El [enunciado](../Enunciado%20proyecto.pdf) fija las tareas y sus criterios. La formulación siguiente explica las decisiones concretas del código; los umbrales de discretización y las simplificaciones son propuestas del grupo que deben justificarse y revisarse con los resultados.
