"""Gráficas de aprendizaje, política y trayectorias para los notebooks."""

from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

from metrics import moving_average
from tasks.common import FIELD_X, FIELD_Y, GOAL_HALF_WIDTH, GOAL_X


def plot_training_comparison(histories, window=50):
    """Compara exploración fija y decreciente sobre tres métricas."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    metrics = (
        ("g0", "Retorno descontado G₀", 1),
        ("success", "Tasa de éxito (%)", 100),
        ("steps", "Pasos por episodio", 1),
    )
    for name, history in histories.items():
        for ax, (key, title, factor) in zip(axes, metrics):
            ax.plot(moving_average(history[key], window) * factor, label=name)
            ax.set(title=title, xlabel="Episodio")
            ax.grid(alpha=0.25)
    axes[0].set_ylabel("Retorno")
    axes[1].set_ylabel("Porcentaje")
    axes[2].set_ylabel("Pasos")
    axes[0].legend()
    fig.tight_layout()
    return fig


def plot_value_policy(q, state_shape, action_names):
    """Muestra un corte 2D del valor y la política greedy de estados visitados."""
    if not q:
        raise ValueError("La tabla Q está vacía")
    suffix = Counter(state[2:] for state in q).most_common(1)[0][0]
    values = np.full(state_shape[:2], np.nan)
    policy = np.full(state_shape[:2], np.nan)
    for state, action_values in q.items():
        if state[2:] == suffix:
            values[state[:2]] = np.max(action_values)
            policy[state[:2]] = np.argmax(action_values)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for index, (ax, data, title, cmap) in enumerate(
        (
            (axes[0], values, "V estimado = max Q", "viridis"),
            (axes[1], policy, "Política greedy estimada", "tab20"),
        )
    ):
        image = ax.imshow(
            np.ma.masked_invalid(data), origin="lower", cmap=cmap, aspect="auto"
        )
        ax.set(title=title, xlabel="Índice del estado 2", ylabel="Índice del estado 1")
        colorbar = fig.colorbar(image, ax=ax)
        if index == 1:
            colorbar.set_ticks(range(len(action_names)))
            if len(action_names) <= 6:
                colorbar.set_ticklabels(action_names)
            else:
                colorbar.set_label("Índice de acción (ver action_names)")
    fig.suptitle(
        f"Corte con dimensiones restantes = {suffix}; blanco = no visitado", fontsize=10
    )
    fig.tight_layout()
    return fig


def plot_trajectory(env):
    """Dibuja el episodio evaluado sobre la cancha simplificada."""
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.set(
        xlim=(-FIELD_X - 3, FIELD_X + 3),
        ylim=(-FIELD_Y - 3, FIELD_Y + 3),
        xlabel="X (m)",
        ylabel="Y (m)",
        title="Trayectoria del episodio",
    )
    ax.plot(
        [-FIELD_X, FIELD_X, FIELD_X, -FIELD_X, -FIELD_X],
        [-FIELD_Y, -FIELD_Y, FIELD_Y, FIELD_Y, -FIELD_Y],
        color="gray",
    )
    ax.plot([0, 0], [-FIELD_Y, FIELD_Y], color="lightgray")
    ax.plot(
        [GOAL_X, GOAL_X],
        [-GOAL_HALF_WIDTH, GOAL_HALF_WIDTH],
        color="green",
        linewidth=5,
        label="Arco rival",
    )
    for index, path in enumerate(getattr(env, "attacker_trajectories", [])):
        x, y = zip(*path)
        color = "tab:blue" if index == 0 else "tab:cyan"
        ax.plot(
            x, y, marker="o", markersize=2, color=color, label=f"Atacante {index + 1}"
        )
        ax.scatter(x[0], y[0], color=color, marker="s", s=45)
    for attribute, label, color in (
        ("trajectory", "Jugador", "tab:blue"),
        ("ball_trajectory", "Balón", "tab:orange"),
        ("defender_trajectory", "Defensor", "tab:red"),
    ):
        points = getattr(env, attribute, None)
        if points:
            x, y = zip(*points)
            ax.plot(x, y, marker="o", markersize=2, color=color, label=label)
            ax.scatter(x[0], y[0], color=color, marker="s", s=45)
    if getattr(env, "goalie", None) is not None:
        ax.scatter(*env.goalie, color="tab:purple", marker="X", s=80, label="Portero")
    ax.set_aspect("equal", adjustable="box")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    return fig
