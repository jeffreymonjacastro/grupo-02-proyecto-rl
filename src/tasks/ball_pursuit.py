"""Persecución del balón en un modelo cinemático acotado."""

import numpy as np

from tasks.common import (
    advance,
    angle_zone,
    distance,
    outside_field,
    relative_angle,
    zone,
)


class BallPursuitEnv:
    """El jugador gira o avanza hasta quedar a 0,8 m del balón."""

    action_names = ("DASH 100", "DASH 50", "TURN +35", "TURN -35")
    n_actions = len(action_names)
    state_shape = (4, 4)

    def __init__(self, seed=42, max_steps=40):
        self.rng = np.random.default_rng(seed)
        self.max_steps = max_steps
        self.reset()

    @staticmethod
    def discretize(ball_distance, ball_angle):
        return zone(ball_distance, (0.8, 3.0, 8.0)), angle_zone(ball_angle)

    def observation(self):
        return distance(self.player, self.ball), relative_angle(
            self.player, self.ball, self.heading
        )

    def state(self):
        return self.discretize(*self.observation())

    def reset(self):
        self.player = (-15.0 + self.rng.uniform(-2, 2), self.rng.uniform(-4, 4))
        while True:
            candidate = advance(
                self.player, self.rng.uniform(-180, 180), self.rng.uniform(5, 40)
            )
            if not outside_field(candidate):
                self.ball = candidate
                break
        self.heading = self.rng.uniform(-180, 180)
        self.steps = 0
        self.trajectory = [self.player]
        self.ball_trajectory = [self.ball]
        return self.state()

    def step(self, action):
        if action not in range(self.n_actions):
            raise ValueError(f"Acción inválida: {action}")
        previous_distance, _ = self.observation()
        self.steps += 1
        if action in (0, 1):
            self.player = advance(
                self.player, self.heading, 1.5 if action == 0 else 0.75
            )
        else:
            self.heading += 35.0 if action == 2 else -35.0
            self.heading = (self.heading + 180.0) % 360.0 - 180.0

        self.trajectory.append(self.player)
        self.ball_trajectory.append(self.ball)
        current_distance, angle = self.observation()
        captured = current_distance <= 0.8
        failed = outside_field(self.player)
        success = captured and not failed and self.steps < 40
        done = captured or failed or self.steps >= self.max_steps
        reward = previous_distance - current_distance - 0.2
        if captured and not failed:
            reward += 100.0
        elif failed:
            reward -= 20.0
        return (
            self.state(),
            reward,
            done,
            {"success": success, "distance": current_distance, "angle": angle},
        )
