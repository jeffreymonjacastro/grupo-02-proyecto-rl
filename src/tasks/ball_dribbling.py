"""Conducción mediante micro-pateos y carreras cortas."""

import numpy as np

from tasks.common import (
    GOAL_X,
    advance,
    angle_zone,
    distance,
    outside_field,
    relative_angle,
    zone,
)


class BallDribblingEnv:
    """Modelo reducido: balón y jugador se desplazan sin física de inercia."""

    action_names = ("KICK 25", "DASH 80", "TURN +35", "TURN -35")
    n_actions = len(action_names)
    state_shape = (3, 4, 4, 4)

    def __init__(self, seed=42, max_steps=80):
        self.rng = np.random.default_rng(seed)
        self.max_steps = max_steps
        self.goal = (GOAL_X, 0.0)
        self.reset()

    def observation(self):
        ball_distance = distance(self.player, self.ball)
        ball_angle = relative_angle(self.player, self.ball, self.heading)
        goal_distance = distance(self.player, self.goal)
        goal_angle = relative_angle(self.player, self.goal, self.heading)
        return ball_distance, ball_angle, goal_distance, goal_angle

    def state(self):
        ball_distance, ball_angle, goal_distance, goal_angle = self.observation()
        return (
            zone(ball_distance, (0.8, 1.2)),
            angle_zone(ball_angle),
            zone(goal_distance, (20.0, 40.0, 60.0)),
            angle_zone(goal_angle),
        )

    def reset(self):
        self.player = (-30.0, self.rng.uniform(-5, 5))
        self.ball = (self.player[0] + 0.45, self.player[1])
        self.heading = self.rng.uniform(-20, 20)
        self.start_ball_x = self.ball[0]
        self.steps = 0
        self.trajectory = [self.player]
        self.ball_trajectory = [self.ball]
        return self.state()

    def step(self, action):
        if action not in range(self.n_actions):
            raise ValueError(f"Acción inválida: {action}")
        old_goal_distance = distance(self.ball, self.goal)
        self.steps += 1
        invalid_kick = action == 0 and distance(self.player, self.ball) > 1.2
        if action == 0 and not invalid_kick:
            self.ball = advance(self.ball, self.heading, 1.2)
        elif action == 1:
            self.player = advance(self.player, self.heading, 0.8)
        elif action in (2, 3):
            self.heading += 35.0 if action == 2 else -35.0
            self.heading = (self.heading + 180.0) % 360.0 - 180.0

        self.trajectory.append(self.player)
        self.ball_trajectory.append(self.ball)
        possession = distance(self.player, self.ball) <= 2.0
        progress = self.ball[0] - self.start_ball_x
        out = outside_field(self.player) or outside_field(self.ball)
        success = progress > 30.0 and possession and not out
        done = success or not possession or out or self.steps >= self.max_steps
        reward = 2.0 * (old_goal_distance - distance(self.ball, self.goal)) - 0.1
        if invalid_kick:
            reward -= 2.0
        if success:
            reward += 100.0
        elif not possession or out:
            reward -= 30.0
        return (
            self.state(),
            reward,
            done,
            {"success": success, "possession": possession, "progress_m": progress},
        )
