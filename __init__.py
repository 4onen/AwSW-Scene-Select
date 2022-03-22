from modloader.modclass import Mod, loadable_mod
from modloader.modinfo import has_mod
import jz_magmalink as ml

import four_scene_select as fss

import renpy
from renpy import store

def block_replay_over_mod_chapter_boundaries():
    fss.end_replay_at_ml_node(ml.find_label('_mod_fixjmp'))

def link_minigames():
    fss.register_scene_select_cateogry("Minigames")

    def link_sebastian_cards():
        fss.register_scene_select("Minigames", "Sebastian cards", 'gamestart')
        fss.end_replay_at_ml_node(ml.find_label('sebastianskip'))
    link_sebastian_cards()

    def link_bryce_drinking_game():
        startpoint =( ml.find_label('_call_skiptut_8')
            .search_say("(Considering they don't even have cars, at least I won't have to worry about drinking and driving.)")
        )

        startpoint.link_behind_from('four_scene_select_minigame_bryce1_drinking_start')

        context = fss.extend_scope(brycemood=1)

        fss.register_scene_select("Minigames", "Bryce drinking game", 'four_scene_select_minigame_bryce1_drinking',replay_scope=context, locked=False)
        fss.end_replay_at_ml_node(startpoint.search_menu("[[Give up.]").branch().search_python('nodrinks = True'))
        fss.end_replay_at_ml_node(startpoint.search_menu("I know when I've had enough, and it's now.", depth=400).search_show('bryce normal').search_with())
    link_bryce_drinking_game()


def link_endings():
    # Endings are too complicated for the replay system I've setup here to handle. Toy with this at your own risk.
    fss.register_scene_select_cateogry("Endings")

    fss.register_scene_select("Endings", "Bryce Friends Bad", 'bryce5', replay_scope=fss.extend_scope(brycestatus='neutral',sebastiansaved=False, brycegoodending=False), locked=lambda: not store.persistent.brycebadending )
    fss.register_scene_select("Endings", "Bryce Friends Good", 'bryce5', replay_scope=fss.extend_scope(brycestatus='neutral',sebastiansaved=False, brycegoodending=True), locked=lambda: not store.persistent.brycegoodending )
    fss.register_scene_select("Endings", "Bryce Romance Bad", 'bryce5', replay_scope=fss.extend_scope(brycestatus='good',sebastiansaved=False, brycegoodending=False), locked=lambda: not (store.persistent.brycebadending and renpy.exports.seen_image('brycerom')))
    fss.register_scene_select("Endings", "Bryce Romance Good", 'bryce5', replay_scope=fss.extend_scope(brycestatus='good',sebastiansaved=False, brycegoodending=True), locked=lambda: not (store.persistent.brycegoodending and renpy.exports.seen_image('brycerom')))


def link_eck_minigames():
    if has_mod('Savior'):# or has_mod('A Solitary Mind'):# or has_mod('Not-so-Tragic Hero'):
        fss.register_scene_select_cateogry("ECK Minigames")

    if has_mod('Savior'):
        # Bryce Build-A-Ship
        fss.register_scene_select("ECK Minigames", "Savior Shipbuilding", 'four_scene_select_minigame_eck_savior_brycebuildaship', locked=lambda: not renpy.exports.seen_label('eck_bryce_buildashipsetup'))
        fss.end_replay_at_ml_node(ml.find_label('eck_bryce_buildashipaftermath').search_say("No complaints here."))

    # Too many variables in the ECK display. Tired of it.
    # if has_mod('A Solitary Mind'):
    #     # Naomi Biolab
    #     fss.register_scene_select("ECK Minigames", "A Solitary Mind Biolab", 'eck_naomi_m3_B9',
    #                                 replay_scope=fss.extend_scope(naomi1mood=10, naomi2mood=10, naomi3mood=1),
    #                                 locked=lambda: not store.persistent.naomi3skip)
    #     fss.end_replay_at_ml_node(ml.find_label('eck_naomi_m3_youdied').search_python('renpy.pause (2.0)'))
    #     fss.end_replay_at_ml_node(ml.find_label('eck_naomi_m3_skip').search_say("Not sure, but it's late, and I better return to my apartment before dark."))


@loadable_mod
class MyAwSWMod(Mod):
    name = "Scene Select"
    version = "v0.2"
    author = "4onen"
    dependencies = ["MagmaLink"]

    @staticmethod
    def mod_load():
        ( ml.Overlay()
            .add(['textbutton "scenes":'\
                 ,'    xalign 0.655'\
                 ,'    yalign 0.7'\
                 ,'    action [Show("gallery", transition=dissolve), SetField(four_scene_select,"_scene_category_selected",None), Show("four_scene_select"), Play("audio", "se/sounds/open.ogg")]'\
                 ,'    hovered Play("audio", "se/sounds/select.ogg")'\
                ])
            .compile_to("main_menu")
        )

        block_replay_over_mod_chapter_boundaries()

        link_minigames()
        # link_endings()
        link_eck_minigames()

    @staticmethod
    def mod_complete():
        pass