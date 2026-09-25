"""Q-Learning tabular y evaluación de las tareas acotadas."""

from collections import defaultdict

import numpy as np


def train_q_learning(
    env,
    episodes=1500,
    alpha=0.2,
    gamma=0.99,
    epsilon_mode="constant",
    epsilon_start=0.2,
    epsilon_min=0.05,
    epsilon_decay=0.995,
    seed=42,
):
    """Entrena una tabla Q y registra G0 descontado por episodio."""
    if epsilon_mode not in {"constant", "decay"}:
        raise ValueError("epsilon_mode debe ser 'constant' o 'decay'")
    rng = np.random.default_rng(seed)
    q = defaultdict(lambda: np.zeros(env.n_actions, dtype=float))
    history = {"g0": [], "reward_sum": [], "success": [], "steps": [], "epsilon": []}

    for episode in range(episodes):
        epsilon = (
            epsilon_start
            if epsilon_mode == "constant"
            else max(epsilon_min, epsilon_start * epsilon_decay**episode)
        )
        state = env.reset()
        discounted_return = 0.0
        reward_sum = 0.0
        for step in range(env.max_steps):
            if rng.random() < epsilon:
                action = int(rng.integers(env.n_actions))
            else:
                best = np.flatnonzero(q[state] == q[state].max())
                action = int(rng.choice(best))
            next_state, reward, done, info = env.step(action)
            target = reward if done else reward + gamma * q[next_state].max()
            q[state][action] += alpha * (target - q[state][action])
            discounted_return += gamma**step * reward
            reward_sum += reward
            state = next_state
            if done:
                break
        history["g0"].append(discounted_return)
        history["reward_sum"].append(reward_sum)
        history["success"].append(int(info["success"]))
        history["steps"].append(step + 1)
        history["epsilon"].append(epsilon)
    return dict(q), history


def greedy_episode(env, q):
    """Ejecuta una política aprendida sin actualizar Q."""
    state = env.reset()
    total_reward = 0.0
    for step in range(env.max_steps):
        values = q.get(state)
        action = int(np.argmax(values)) if values is not None else 0
        state, reward, done, info = env.step(action)
        total_reward += reward
        if done:
            return {**info, "steps": step + 1, "reward_sum": total_reward}
    raise RuntimeError("El entorno no terminó al alcanzar max_steps")
