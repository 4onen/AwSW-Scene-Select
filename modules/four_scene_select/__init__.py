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

def extend_scope_by_dict(d):
    return dict(default_replay_scope, **d)

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

    def get_locked(self):
        if callable(self._locked):
            return self._locked()
        elif self._locked is None:
            return False
        else:
            return self._locked

_scene_select_db = dict()
_nsfw_categories = set()

def register_scene_select_cateogry(category, nsfw=False):
    """
    This function registers a new "category" at the top of the scene select menu.

    You must call this function to add a category before adding any scenes to that category.

    Parameters
    ----------
    category : str
        The category name to register. This will be the exact text the user will see in the menu.
    nsfw : bool
        If True, the scene will be registered to the nsfw categories. These categories only appear if NSFW scenes are allowed in the modtools global config.
    """
    if category not in _scene_select_db:
        _scene_select_db[category] = []
    if nsfw:
        _nsfw_categories.add(category)

def register_scene_select_scene_instance(category, scene):
    """
    This function registers a scene class instance to the scene select menu.

    Unless you know what you're doing and have subclassed the Scene class to implement what you need, use `register_scene_select` instead.

    Parameters
    ----------
    category : str
        The category name to register this scene under. This category must have been registered with `register_scene_select_cateogry`.
    scene : Scene
        The scene class instance to register.
    """
    if category not in _scene_select_db:
        error("Scene select category '{}' not registered. Make sure 'Scene Select' is a dependency of your mod!".format(category))
    _scene_select_db[category].append(scene)

def register_scene_select(category, name, label, replay_scope = default_replay_scope, locked=None):
    """
    This function registers a scene to the scene select menu.

    Parameters
    ----------
    category : str
        The category name to register this scene under. This category must have been registered with `register_scene_select_cateogry`.
    name : str
        The scene name to register. This will be the exact text the user will see in the menu.
    label : str
        The Ren'Py label to begin replaying the scene. If it is a mod you control, it is recommended to set up a black screen and give the user a bit of context to help bring them into the moment, before setting up the correct background.
    replay_scope: dict
        The variables to configure in the replay environemnt. Defaults to this module's `default_replay_scope`. If you need to set additional variables than those set in `default_replay_scope`, it is recommended to use the `extend_scope` function rather than to make your own dict, as this allows your mod to get any future improvements in the default scoping.
    locked : NoneType | bool | Callable[[],bool]
        If truthy, or if a callable that returns a true value, the scene will not be clickable in the scene select menu. Use this to allow scenes to unlock only for particular player progress, e.g. when they reach that scene in the story themselves. This is overridden by the "Enable All" checkbox in the scene select menu. The callable form may read variables from the environment, but should not perform any side-effects.
    """
    register_scene_select_scene_instance(category, Scene(name, label, replay_scope, locked))

hooknum = 0

def end_replay_at_node(node):
    """
    This function registers a mod hook following a node to end a Ren'Py replay. That is, given a Ren'Py AST node, the replay will end immediately following that node. If not in replay mode, nothing will happen and the hook will be passed silently.

    Parameters
    ----------
    node : renpy.ast.Node
    """
    global hooknum
    from renpy.exports import end_replay
    from modloader import modast
    modast.hook_opcode(node, lambda hook: end_replay(), 'SceneSelectEndReplay%u'%hooknum)
    hooknum = hooknum + 1

def end_replay_at_ml_node(mlnode):
    """
    This function registers a mod hook following a MagmaLink node reference to end a Ren'Py replay. That is, given the result of a MagmaLink `search_*` or `find_*`, the replay will end immediately following that point. If not in replay mode, nothing will happen and the hook will be passed silently.

    Parameters
    ----------
    node : ml.ast_link.base.Node
    """
    end_replay_at_node(mlnode.node)