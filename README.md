# Starter Kit - Proyecto de Aprendizaje por Refuerzo (DS5345)

**Curso:** DS5345 · Aprendizaje por Refuerzo (2026-II)  
**Institución:** UTEC - Universidad de Ingeniería y Tecnología  
**Docente:** Percy W. Lovon Ramos  
**Dominio:** Fútbol Autónomo Multi-Agente en Simulación 2D (RoboCup 2D Soccer Simulation League)

---

## 1. Contenido de este Starter Kit

Este paquete contiene todo lo necesario para comenzar a trabajar de inmediato en un entorno reproducible y aislado de tu sistema operativo:

```text
rl-robocup2d/
├── docker
│   ├── docker-compose.yml              # orquestador del simulador (rcssserver) y el agente (rl-agent)
│   └── dockerfile                      # configuración de la imagen del agente (python 3.10 + pytorch)
│
├── notebooks/                          # carpeta montada en el contenedor (aquí programas)
│   ├── tutorial_primer_paso.ipynb      # cuaderno tutorial: lectura de observaciones y acciones
│   └── agente_cero_mc_control_persecucion.ipynb  # baseline completo de monte carlo control
│
├── report                              # informe
│   ├── build                           # archivos temporales de build
│   │   └── main.pdf                    # informe compilado
│   ├── figures                         # figuras / images
│   ├── sections                        # secciones del informe
│   ├── tables                          # tablas en .tex
│   ├── template                        # template
│   ├── main.tex                        # main .tex
│   └── references.bib                  # referencias en bib
│
├── src
│   ├── robocup_client.py               # cliente udp oficial para comunicar python con rcssserver
│   └── test_random_agent.py            # script de humo (smoke test) para validar la conexión
│
│── enunciado proyecto.pdf              # documento oficial completo con rúbricas y requerimientos
├── requirements.txt                    # dependencias de python instaladas
└── readme.md                           # esta guía paso a paso
```

---

## 2. Guía de Inicio Rápido

### Requisito Previo

Tener instalado y abierto **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** (funciona en macOS Apple Silicon / Intel, Linux y Windows con WSL2).

### Paso 1: Abrir la terminal en esta carpeta

```bash
cd grupo-02-proyecto-rl
```

### Paso 2: Iniciar los contenedores

Ejecuta el siguiente comando para levantar el simulador y el agente:

```bash
docker compose -f docker/docker-compose.yml up -d
```

> **Nota:** La primera ejecución descargará las imágenes y construirá el entorno. En ejecuciones posteriores iniciará en menos de 5 segundos.

### Paso 3: Abrir Jupyter Lab en tu navegador

Una vez iniciado, abre en tu navegador:
**[http://localhost:8888](http://localhost:8888)**

No requiere contraseña. En la barra lateral verás la carpeta `workspace/` con todos los archivos de trabajo.

---

## 3. Verificación de la Conexión

Para verificar que el contenedor del agente se comunica correctamente con el servidor de RoboCup:

### Opción A: Desde Jupyter Lab (Recomendada)

1. Abre el cuaderno `notebooks/tutorial_primer_paso.ipynb`.
2. Ejecuta las celdas secuencialmente (`Shift + Enter`).
3. Observarás el mensaje `Conectado exitosamente a rcssserver` y una gráfica de trayectoria.

### Opción B: Desde la terminal

```bash
docker compose -f docker/docker-compose.yml exec rl-agent python /workspace/src/test_random_agent.py
```

---

## 4. Hoja de Ruta del Proyecto

El proyecto se desarrolla en dos fases acumulativas:

| Fase   | Entrega       | Ponderación | Contenido Principal                                                                                                                                                                                                                                                                                                                                              |
| :----- | :------------ | :---------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **P1** | **Semana 7**  |   **10%**   | **Baseline Tabular en Tarea Restringida:** Modelado MDP formal ($\mathcal{S}, \mathcal{A}, \mathcal{R}, \gamma$), discretización justificada analíticamente, implementación de Monte Carlo Control / Q-Learning / SARSA, comparación de políticas de exploración ($\varepsilon$ fijo vs. decreciente) e informe técnico de 5 páginas.                            |
| **P2** | **Semana 15** |   **20%**   | **Deep RL y Desafío de Integración:** Redes neuronales continuas (DQN, PPO, DDPG), reward shaping para evitar _reward hacking_, y elección entre: <br>• **Vía A:** Partido competitivo MARL contra campeones RoboCup (HELIOS, CYRUS). <br>• **Vía B:** Transferencia de políticas (_Transfer Learning_) a robótica móvil, búsqueda y rescate, o AGVs logísticos. |

---

## 5. Comandos Útiles de Docker

- **Ver el estado de los contenedores:**
  ```bash
  docker compose -f docker/docker-compose.yml ps
  ```
- **Ver los logs de la simulación o el agente:**
  ```bash
  docker compose -f docker/docker-compose.yml logs -f rcssserver
  docker compose -f docker/docker-compose.yml logs -f rl-agent
  ```
- **Reiniciar el simulador:**
  ```bash
  docker compose -f docker/docker-compose.yml restart rcssserver
  ```
- **Detener los servicios:**
  ```bash
  docker compose -f docker/docker-compose.yml down
  ```

---

## 6. Formato de Entrega del Grupo

Cada equipo (hasta 3 estudiantes) deberá entregar:

1. **Repositorio privado de GitHub / GitLab** (acceso otorgado al docente) con la siguiente estructura:
   ```text
   grupo-XX-proyecto-rl/
   ├── docker/              # Archivos Docker para reproducibilidad
   ├── src/                 # Código modular Python (agente, discretizador, cliente)
   ├── notebooks/           # Cuadernos Jupyter con curvas de entrenamiento
   ├── informe_p1.pdf       # Informe compilado desde la plantilla LaTeX
   └── README.md            # Instrucciones claras para reproducir los experimentos
   ```
2. **Informe Técnico en PDF:** Compilado desde la plantilla provista en `plantilla_informe_latex/` y entregado a través de la plataforma Canvas.

---

> ¡Muchos éxitos en el desarrollo del proyecto! Para dudas o soporte técnico, consulta con el docente o a través de los canales oficiales del curso.

---

## 7. Integración con VS Code y Sincronización Automática

Si prefieres utilizar **Visual Studio Code** en lugar de Jupyter Lab en el navegador, sigue estos pasos para conectarlo directamente al contenedor y sincronizar los cambios de tus scripts en tiempo real.

### A. Sincronización Automática en Notebooks (`autoreload`)

Para que tu Notebook reconozca inmediatamente cualquier cambio que hagas en los archivos `.py` (como `robocup_client.py` o tus agentes) sin necesidad de reiniciar el kernel, asegúrate de que la **primera celda** de todos tus Notebooks contenga esto:

```python
%load_ext autoreload
%autoreload 2

import sys
import os
# Asegura que el Notebook siempre encuentre la carpeta src sin importar desde dónde se abra
sys.path.append("/workspace/src")
```

### B. Usar el Kernel del Docker dentro de VS Code

Puedes programar en tus Notebooks directamente dentro de VS Code aprovechando todo el entorno preconfigurado de Docker:

1. Abre tu archivo `.ipynb` en VS Code.
2. Arriba a la derecha (o presionando `Ctrl+Shift+P` y buscando _Notebook: Select Notebook Kernel_), haz clic en **Seleccionar Kernel** (Select Kernel).
3. Selecciona **Existing Jupyter Server** (Servidor Jupyter existente).
4. Pega la URL del servidor local: `http://localhost:8888` y presiona Enter.
5. ¡Listo! Todo el código que ejecutes en el Notebook dentro de VS Code se estará procesando internamente en el contenedor Docker.
