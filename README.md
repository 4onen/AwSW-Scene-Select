# AwSW-Scene-Select

This mod adds a scene selection menu to Angels with Scaly Wings.

As adding a scene to the menu takes a reasonable amount of modding effort, currently only supports:

+ Bastion Breach with Sebastian
+ Drinking with Bryce
+ ECK Savior: Shipbuilding with Bryce

On top of directly adding scene selection to the game, this mod offers a modding interface to allow other mods to register their own scenes for the menu. See the free functions in [`modules/four_scene_select\__init__.py`](modules/four_scene_select/__init__.py) for more information on the interface.

## Changelog

### v0.3

* Added a checkbox to enable access to all scenes. (As scenes may rely on persistent data, this is not enabled by default and is labeled "Crash Risky.")
* Added a multi-column layout for mods with more than 9 scenes to look prettier.
* Added a pagination system to handle mods/categories with more than 21 scenes going off the screen.
* Added scene registration interface documentation.

## Licensing

This game mod is licensed under the GPLv3, per the license requirements of depending on MagmaLink. If you intend to depend on this mod, and your mod will be distributed, you must do so under licensing terms compatible with GPLv3. See the [LICENSE](LICENSE) file for more information.