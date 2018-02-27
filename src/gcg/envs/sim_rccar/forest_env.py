import os, random

from gcg.envs.sim_rccar.room_cluttered_env import RoomClutteredEnv

class ForestEnv(RoomClutteredEnv):
    @property
    def _model_path(self): 
        return os.path.join(self._base_dir, 'outdoors.egg')

    def _setup_object_paths(self):
        obj_paths = ['rock4.egg', 'rock5.egg', 'tree8.egg', 'tree9.egg']
        self._obj_paths = [os.path.join(self._base_dir, x) for x in obj_paths]

    def _setup_map(self):
        # TODO maybe stagger
        index = 0
        max_len = len(self._obj_paths)
        oris = [0., 90., 180., 270.]
        for i in range(2, 27, 5):
            for j in range(2, 27, 5):
                if (i != 2 and i != 22) or (j!=2 and j!=22):
                    pos = (i - 12., j - 12., 0.1)
                    # path = random.choice(self._obj_paths)
                    path = self._obj_paths[index % max_len]
                    angle = oris[(index // max_len) % 4]
                    hpr = (angle, 0.0, 0.0)
                    scale = 1 if 'tree' in path else 0.4
                    self._setup_collision_object(path, pos, hpr, scale=scale, is_obstacle=True)
                    index += 1
        self._setup_collision_object(self._model_path)

    def _default_pos(self):
        return (11.0, -11., 0.3)

    def _default_restart_pos(self):
        return [
                [  11., -11., 0.3,  30.0, 0.0, 0.0], [  11., -11., 0.3,  45.0, 0.0, 0.0], [  11., -11., 0.3,  60.0, 0.0, 0.0],
                [  11.,  11., 0.3, 120.0, 0.0, 0.0], [  11.,  11., 0.3, 135.0, 0.0, 0.0], [  11.,  11., 0.3, 150.0, 0.0, 0.0],
                [ -11.,  11., 0.3, 210.0, 0.0, 0.0], [ -11.,  11., 0.3, 225.0, 0.0, 0.0], [ -11.,  11., 0.3, 240.0, 0.0, 0.0],
                [ -11., -11., 0.3, 300.0, 0.0, 0.0], [ -11., -11., 0.3, 315.0, 0.0, 0.0], [ -11., -11., 0.3, 330.0, 0.0, 0.0],
            ]

    @property
    def horizon(self):
        return 45

if __name__ == '__main__':
    params = {'visualize': True, 'run_as_task': True, 'do_back_up': True, 'hfov': 120}
    env = ForestEnv(params)
