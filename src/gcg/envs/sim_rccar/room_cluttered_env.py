import os
from math import pi
from collections import OrderedDict
import numpy as np

from gcg.envs.sim_rccar.square_env import SquareEnv
from gcg.envs.spaces.box import Box

class RoomClutteredEnv(SquareEnv):
    def __init__(self, params={}):
        #TODO
        self._goal_speed = 2.
        self._goal_heading = 0.
        self._obstacles = []
        self._setup_object_paths()
        SquareEnv.__init__(self, params=params)
    
    @property
    def _model_path(self): 
        return os.path.join(self._base_dir, 'room.egg')
    
    def _setup_object_paths(self):
        obj_paths = ['bookcase.egg', 'chair.egg', 'coffee_table.egg', 'desk.egg', 'stool.egg', 'table.egg']
        self._obj_paths = [os.path.join(self._base_dir, x) for x in obj_paths]

    def _setup_spec(self):
        SquareEnv._setup_spec(self)
        self.goal_spec['speed'] = Box(low=-4.0, high=4.0)
        self.goal_spec['heading'] = Box(low=0, high=2 * 3.14)

    def _default_pos(self):
        return (20.0, -20., 0.3)

    def _setup_collision_object(self, path, pos=(0.0, 0.0, 0.0), hpr=(0.0, 0.0, 0.0), scale=1, is_obstacle=False):
        SquareEnv._setup_collision_object(self, path, pos, hpr, scale)
        if is_obstacle:
            self._obstacles.append((path, pos, hpr))
    
    def _setup_map(self):
        index = 0
        max_len = len(self._obj_paths)
        oris = [0., 90., 180., 270.]
        for i in range(5, 45, 5):
            for j in range(5, 45, 5):
                pos = (i - 22.5, j - 22.5, 0.3)
                path = self._obj_paths[index % max_len]
                angle = oris[(index // max_len) % 4]
                hpr = (angle, 0.0, 0.0)
                self._setup_collision_object(path, pos, hpr, is_obstacle=True)
                index += 1
        self._setup_collision_object(self._model_path)

    def _get_goal(self):
        goal = np.array([self._goal_speed, self._goal_heading])
        return goal

    def _get_reward(self):
        if self._collision_reward_only:
            if self._collision:
                reward = -1.0
            else:
                reward = 0.0
        else:
            if self._collision:
                reward = self._collision_reward
            else:
                heading_reward = np.cos(self._goal_heading - self._get_heading())
                speed_reward = - (((self._goal_speed - self._get_speed()) / self._goal_speed) ** 2)
                reward = heading_reward + speed_reward
        assert(reward <= self.max_reward)
        return reward

    def _default_restart_pos(self):
        return [
                [  21., -21., 0.3,  30.0, 0.0, 0.0], [  21., -21., 0.3,  45.0, 0.0, 0.0], [  21., -21., 0.3,  60.0, 0.0, 0.0],
                [  21.,  21., 0.3, 120.0, 0.0, 0.0], [  21.,  21., 0.3, 135.0, 0.0, 0.0], [  21.,  21., 0.3, 150.0, 0.0, 0.0],
                [ -21.,  21., 0.3, 210.0, 0.0, 0.0], [ -21.,  21., 0.3, 225.0, 0.0, 0.0], [ -21.,  21., 0.3, 240.0, 0.0, 0.0],
                [ -21., -21., 0.3, 300.0, 0.0, 0.0], [ -21., -21., 0.3, 315.0, 0.0, 0.0], [ -21., -21., 0.3, 330.0, 0.0, 0.0],
            ]

    def _default_restart_goal(self):
        goals = []
        for pos in self._default_restart_pos():
            goal = pos[3] * pi / 180.0
            goals.append(goal)
        return goals

    def _next_restart_pos_hpr_goal(self):
        num = len(self._restart_pos)
        if num == 0:
            return None, None
        else:
            pos_hpr = self._restart_pos[self._restart_index]
            goal = self._default_restart_goal()[self._restart_index]
            self._restart_index = (self._restart_index + 1) % num
            return pos_hpr[:3], pos_hpr[3:], goal

    @property
    def horizon(self):
        return 100

    @property
    def max_reward(self):
        return 1.0

    def reset(self):
        if self._do_back_up:
            if self._collision:
                self._back_up()
        else:
            pos, hpr, goal = self._next_restart_pos_hpr_goal()
            self._place_vehicle(pos=pos, hpr=hpr)
            self._goal_heading = goal
        self._collision = False
        return self._get_observation(), self._get_goal()

    def _get_info(self):
        info = SquareEnv._get_info(self)
        info['goal_h'] =  self._goal_heading
        info['goal_s'] = self._goal_speed
        info['obstacles'] = self._obstacles
        return info

if __name__ == '__main__':
    params = {'visualize': True, 'run_as_task': True, 'do_back_up': True, 'hfov': 120}
    env = RoomClutteredEnv(params)
