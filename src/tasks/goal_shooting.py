"""Disparos de penal con portería abierta o portero simplificado."""

import math

import numpy as np

from tasks.common import (
    GOAL_HALF_WIDTH,
    GOAL_X,
    advance,
    distance,
    relative_angle,
    zone,
)


class GoalShootingEnv:
    """Cada episodio contiene un disparo; el portero bloquea por cercanía vertical."""

    shot_powers = (40, 70, 100)
    shot_directions = (-20, -10, 0, 10, 20)
    action_names = tuple(
        f"KICK {power}/{direction:+}"
        for power in (40, 70, 100)
        for direction in (-20, -10, 0, 10, 20)
    )
    n_actions = len(action_names)
    state_shape = (3, 4, 4, 4)

    def __init__(self, seed=42, goalie_active=False):
        self.rng = np.random.default_rng(seed)
        self.goalie_active = goalie_active
        self.max_steps = 1
        self.goal = (GOAL_X, 0.0)
        self.reset()

    def state(self):
        left_post = (GOAL_X, GOAL_HALF_WIDTH)
        right_post = (GOAL_X, -GOAL_HALF_WIDTH)
        left_angle = relative_angle(self.player, left_post, self.heading)
        right_angle = relative_angle(self.player, right_post, self.heading)
        goalie_zone = (
            0 if self.goalie is None else 1 + zone(self.goalie[1], (-2.0, 2.0))
        )
        return (
            zone(distance(self.player, self.goal), (12.0, 16.0)),
            zone(left_angle, (-15.0, 0.0, 15.0)),
            zone(right_angle, (-15.0, 0.0, 15.0)),
            goalie_zone,
        )

    def reset(self):
        self.player = (self.rng.uniform(36, 43), self.rng.uniform(-6, 6))
        self.ball = (self.player[0] + 0.3, self.player[1])
        self.heading = self.rng.uniform(-10, 10)
        self.goalie = (51.0, self.rng.uniform(-5, 5)) if self.goalie_active else None
        self.steps = 0
        self.trajectory = [self.player]
        self.ball_trajectory = [self.ball]
        return self.state()

    def step(self, action):
        if action not in range(self.n_actions):
            raise ValueError(f"Acción inválida: {action}")
        self.steps = 1
        power = self.shot_powers[action // len(self.shot_directions)]
        direction = self.shot_directions[action % len(self.shot_directions)]
        shot_angle = math.radians(self.heading + direction)
        reach = 0.2 * power
        dx = GOAL_X - self.ball[0]
        reaches_goal = math.cos(shot_angle) > 0 and reach * math.cos(shot_angle) >= dx
        impact_y = self.ball[1] + dx * math.tan(shot_angle) if reaches_goal else None
        on_target = impact_y is not None and abs(impact_y) <= GOAL_HALF_WIDTH
        blocked = (
            on_target
            and self.goalie is not None
            and abs(impact_y - self.goalie[1]) <= 1.5
        )
        success = on_target and not blocked
        outcome = "gol" if success else "bloqueo" if blocked else "fallo"
        reward = 100.0 if success else -50.0 if blocked else -30.0
        self.ball = (
            (GOAL_X, impact_y)
            if reaches_goal
            else advance(self.ball, self.heading + direction, reach)
        )
        self.ball_trajectory.append(self.ball)
        return (
            self.state(),
            reward,
            True,
            {"success": success, "outcome": outcome, "impact_y": impact_y},
        )
