import os
from math import pi
import numpy as np

from gcg.envs.sim_rccar.room_cluttered_env import RoomClutteredEnv

class SimpleRoomBackupEnv(RoomClutteredEnv):
    @property
    def _model_path(self):
        return os.path.join(self._base_dir, 'backup_room.egg')
   
    def _setup_map(self):
        self._setup_collision_object(self._model_path)

    def _default_pos(self):
        return (0.0, 0.0, 0.3)

    def _next_restart_pos_hpr_goal(self):
        pos = (0.0, 0.0, 0.3)
        goal = pi
        hpr = (0.0, 0.0, 0.0)
        return pos, hpr, goal

    @property
    def horizon(self):
        return 45

    def step(self, action):
        # TODO hack
        new_action = [action[0]]
        if action[1] >= 0.0:
            new_action.append(2.0)
        else:
            new_action.append(-2.0)
        new_action = np.array(new_action)
        return RoomClutteredEnv.step(self, new_action)


    def _get_reward(self):
        if self._collision:
            reward = self._collision_reward
        else:
            lb, ub = self.action_space.bounds
            reward = np.cos(self._goal_heading - self._get_heading()) * np.maximum(self._get_speed() / ub[1], 0.)
        assert(reward <= self.max_reward)
        return reward

if __name__ == '__main__':
    params = {'visualize': True, 'run_as_task': False, 'do_back_up': True, 'hfov': 120}
    env = SimpleRoomBackupEnv(params)
    env.step(np.array([0.0, 0.0]))
    env.reset()
