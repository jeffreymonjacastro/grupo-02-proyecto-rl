"""Posesión cooperativa de dos atacantes frente a un defensor."""

import numpy as np

from tasks.common import (
    advance,
    angle_zone,
    distance,
    outside_field,
    relative_angle,
    segment_distance,
    zone,
)


class PassingPossessionEnv:
    """Modelo 2v1 con pases, conducción, giro y despeje."""

    action_names = ("PASE", "DRIBLE", "GIRAR +35", "DESPEJE")
    n_actions = len(action_names)
    state_shape = (4, 3, 3, 4, 3, 4, 4, 52)

    def __init__(self, seed=42, max_steps=70):
        self.rng = np.random.default_rng(seed)
        self.max_steps = max_steps
        self.reset()

    def state(self):
        player = self.attackers[self.holder]
        teammate = self.attackers[1 - self.holder]
        heading = self.headings[self.holder]
        return (
            zone(self.ball[0], (-20.0, -5.0, 10.0)),
            zone(self.ball[1], (-8.0, 8.0)),
            zone(distance(player, teammate), (5.0, 12.0)),
            angle_zone(relative_angle(player, teammate, heading)),
            zone(distance(player, self.defender), (3.0, 10.0)),
            angle_zone(relative_angle(player, self.defender, heading)),
            min(self.passes, 3),
            min(self.steps, 51),
        )

    def reset(self):
        self.attackers = [(-12.0, -4.0), (-8.0, 4.0)]
        self.headings = [0.0, 0.0]
        self.holder = 0
        self.ball = self.attackers[0]
        self.defender = (self.rng.uniform(-3, 0), self.rng.uniform(-2, 2))
        self.steps = 0
        self.passes = 0
        self.attacker_trajectories = [[self.attackers[0]], [self.attackers[1]]]
        self.ball_trajectory = [self.ball]
        self.defender_trajectory = [self.defender]
        return self.state()

    def step(self, action):
        if action not in range(self.n_actions):
            raise ValueError(f"Acción inválida: {action}")
        self.steps += 1
        player = self.attackers[self.holder]
        teammate = self.attackers[1 - self.holder]
        intercepted = False
        reward = 0.2  # pequeño incentivo por conservar la posesión un paso más

        if action == 0:
            intercepted = (
                segment_distance(self.defender, player, teammate) <= 1.5
                or self.rng.random() < 0.05
            )
            if intercepted:
                self.ball = self.defender
            else:
                self.holder = 1 - self.holder
                self.ball = self.attackers[self.holder]
                self.passes += 1
                reward += 30.0
        elif action == 1:
            new_position = advance(player, self.headings[self.holder], 0.8)
            self.attackers[self.holder] = new_position
            self.ball = new_position
        elif action == 2:
            self.headings[self.holder] = (self.headings[self.holder] + 35.0) % 360.0
        else:
            self.ball = advance(player, self.headings[self.holder], 3.0)
            if distance(self.ball, teammate) <= 1.2:
                self.holder = 1 - self.holder
                self.ball = teammate
            else:
                intercepted = True

        # El defensor se aproxima al balón después de cada acción del equipo.
        if not intercepted:
            dx = self.ball[0] - self.defender[0]
            dy = self.ball[1] - self.defender[1]
            length = np.hypot(dx, dy)
            if length > 0:
                self.defender = (
                    self.defender[0] + 0.2 * dx / length,
                    self.defender[1] + 0.2 * dy / length,
                )
            intercepted = distance(self.defender, self.ball) <= 1.2

        out = outside_field(self.ball)
        success = self.steps > 50 and self.passes >= 3 and not intercepted and not out
        done = success or intercepted or out or self.steps >= self.max_steps
        if success:
            reward += 100.0
        if intercepted:
            reward -= 30.0
        if out:
            reward -= 10.0
        for path, position in zip(self.attacker_trajectories, self.attackers):
            path.append(position)
        self.ball_trajectory.append(self.ball)
        self.defender_trajectory.append(self.defender)
        return (
            self.state(),
            reward,
            done,
            {"success": success, "passes": self.passes, "possession_steps": self.steps},
        )
