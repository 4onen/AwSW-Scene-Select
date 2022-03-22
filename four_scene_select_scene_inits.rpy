label four_scene_select_minigame_bryce1_drinking:
    scene black with None
    $ renpy.pause (0.5)
    play sound "fx/2glasses.wav"
    $ renpy.pause(0.5)

    scene bare with dissolveslow

    jump four_scene_select_minigame_bryce1_drinking_start
