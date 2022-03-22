from collections import namedtuple

from renpy import error, store
from renpy.character import DynamicCharacter

default_replay_scope = {
    'c': DynamicCharacter("persistent.player_name", color='#fff'),
    'player_name': store.persistent.player_name,
    '_game_menu_screen': "four_replay_navigation",
}

def extend_scope(**kwargs):
    return dict(default_replay_scope, **kwargs)

class Scene(object):
    def __init__(self, name, label, replay_scope = default_replay_scope, locked=None):
        self.name = name
        self.label = label
        self.replay_scope = replay_scope
        self._locked = locked

    def __repr__(self):
        return "<Scene {}>".format(self.name)

    def __str__(self):
        return self.name

    def get_replay(self):
        return store.Replay(self.label, self.replay_scope, locked=self.get_locked())

    def get_locked(self):
        if callable(self._locked):
            return self._locked()
        else:
            return self._locked

_scene_select_db = dict()
_nsfw_categories = set()

def register_scene_select_cateogry(category, nsfw=False):
    if category not in _scene_select_db:
        _scene_select_db[category] = []
    if nsfw:
        _nsfw_categories.add(category)

def register_scene_select_scene(category, scene):
    if category not in _scene_select_db:
        error("Scene select category '{}' not registered. Make sure 'Scene Select' is a dependency of your mod!".format(category))
    _scene_select_db[category].append(scene)

def register_scene_select(category, name, label, replay_scope = default_replay_scope, locked=None):
    register_scene_select_scene(category, Scene(name, label, replay_scope, locked))

hooknum = 0

def end_replay_at_node(node):
    global hooknum
    from renpy.exports import end_replay
    from modloader import modast
    modast.hook_opcode(node, lambda hook: end_replay(), 'SceneSelectEndReplay%u'%hooknum)
    hooknum = hooknum + 1

def end_replay_at_ml_node(mlnode):
    end_replay_at_node(mlnode.node)