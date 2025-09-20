init:
    python in four_scene_select:
        from four_scene_select import _scene_select_db, _nsfw_categories
        from four_scene_select.replay import call_replay

        _scene_category_selected = None

        @renpy.pure
        def get_categories():
            if renpy.store.persistent.nsfwtoggle:
                return list(_scene_select_db.keys())
            else:
                return [ k for k in _scene_select_db.keys() if k not in _nsfw_categories]

        @renpy.pure
        class Replay(renpy.store.Replay):
            def __call__(self):
                if self.locked:
                    return

                if renpy.config.enter_replay_transition:
                    renpy.transition(renpy.config.enter_replay_transition)

                call_replay(self.label, self.scope)

                if renpy.config.exit_replay_transition:
                    renpy.transition(renpy.config.exit_replay_transition)

    python:
        style.foursceneselectmenubutton = Style(style.menubutton)
        style.foursceneselectmenubutton_text.insensitive_color = "#FFF7"

        style.foursceneselectmenubutton2 = Style(style.foursceneselectmenubutton)
        style.foursceneselectmenubutton2_text.color = "#FFF7"
        style.foursceneselectmenubutton2_text.hover_color = "#FFFF"
        style.foursceneselectmenubutton2_text.selected_idle_color = "#FFFF"
        style.foursceneselectmenubutton2_text.selected_hover_color = "#FFFF"

    transform four_scene_select_category_button:
        anchor (0.5,0.5)
        on idle:
            linear 0.2 alpha 0.5
        on hover:
            alpha 1.0
        on selected_idle:
            alpha 1.0
        on selected_hover:
            alpha 1.0


    define four_scene_select_hover_sound = Play("audio", "se/sounds/select.ogg")

    style four_scene_select_hover_sound_sty is image_button:
        activate_sound "se/sounds/yes.wav"
        hover_sound "se/sounds/select.ogg"

    python:
        renpy.const('four_scene_select._scene_select_db')
        renpy.const('four_scene_select._nsfw_categories')
        renpy.const('four_scene_select_category_button')


    screen four_scene_select():
        tag gallery_page

        hbox:
            xalign 0.2
            yalign 0.02
            spacing 10
            imagebutton:
                idle im.Scale("ui/nsfw_chbox-unchecked.png", 55, 55)
                hover im.Recolor(im.Scale("ui/nsfw_chbox-unchecked.png", 55, 55), 64, 64, 64)
                selected_idle im.Scale("ui/nsfw_chbox-checked.png", 55, 55)
                selected_hover im.Recolor(im.Scale("ui/nsfw_chbox-checked.png", 55, 55), 64, 64, 64)
                action MTSTogglePersistentBool('four_scene_select_unlockall')
                style "four_scene_select_hover_sound_sty"
                focus_mask None
            text _("(Crash Risky) Open All")

        hbox:
            xalign 0.5
            yanchor 0.0
            ypos 0.13
            spacing 40

            for category in four_scene_select.get_categories():
                textbutton "[category]":
                    action [SetField(four_scene_select,'_scene_category_selected',category), Play("audio", "se/sounds/select.ogg")]
                    hovered four_scene_select_hover_sound
                    style "menubutton"
                    at four_scene_select_category_button

        if four_scene_select._scene_category_selected:
            vbox:
                xalign 0.5
                yanchor 0.0
                ypos 0.25
                spacing 10

                for sceneobj in four_scene_select._scene_select_db.get(four_scene_select._scene_category_selected, []):
                    textbutton "[sceneobj]":
                        action [Play("audio","se/sounds/new.ogg"),
                                four_scene_select.Replay(sceneobj.label, sceneobj.replay_scope, locked=sceneobj.get_locked() and not persistent.four_scene_select_unlockall),
                        ]
                        hovered four_scene_select_hover_sound
                        style "foursceneselectmenubutton"
                        at four_scene_select_category_button



    screen four_replay_navigation():
        tag menu
        frame:
            add "image/ui/ingame_menu_bg2.png" at alpha_dissolve
            add "image/ui/navmenu/menu_title.png" at alpha_dissolve
            add "image/ui/ingame_menu_bg_light.png" at ingame_menu_light

            hbox at zoom_fade_in:
                xalign 0.5
                yalign 0.13
                spacing 55

                imagebutton idle "image/ui/back_title.png" hover "image/ui/back_title.png" action [Return(), Play("audio", "se/sounds/close.ogg")] hovered four_scene_select_hover_sound at navmenu_button_mid

                vbox:
                    null height 7
                    imagebutton idle "image/ui/settings_title.png" hover "image/ui/settings_title.png" action [Show('preferences_nav'), Hide('load_nav'), Hide('save_nav'), Hide('videosettings_nav'), Hide('audiosettings_nav'), Hide('textsettings_nav'), Hide('achievements'), Hide('achievement_page'), Hide('status'), Play("audio", "se/sounds/open.ogg")] hovered four_scene_select_hover_sound at navmenu_button_center

                imagebutton idle "image/ui/quit_title.png" hover "image/ui/quit_title.png" action [MainMenu(), Play("audio", "se/sounds/alert.ogg")] hovered four_scene_select_hover_sound at navmenu_button_mid
