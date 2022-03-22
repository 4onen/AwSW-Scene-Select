import renpy

def call_replay(label, scope={}):
    renpy.game.log.complete()

    old_log = renpy.game.log
    renpy.game.log = renpy.python.RollbackLog()

    sb = renpy.python.StoreBackup()
    renpy.python.clean_stores()

    context = renpy.execution.Context(True)
    renpy.game.contexts.append(context)

    if renpy.display.interface is not None:
        renpy.display.interface.enter_context()

    for k, v in renpy.config.replay_scope.iteritems():
        setattr(renpy.store, k, v)

    for k, v in scope.iteritems():
        if '.' in k:
            store, name = k.rsplit('.', 1)
            store = 'store.' + store
            setattr(renpy.python.get_store_module(store), name, v)
        else:
            setattr(renpy.store, k, v)

    renpy.store._in_replay = label

    try:

        context.goto_label("_start_replay")
        renpy.execution.run_context(False)

    except renpy.game.EndReplay:
        pass

    finally:

        context.pop_all_dynamic()

        renpy.game.contexts.pop()
        renpy.game.log = old_log
        sb.restore()

        if renpy.game.interface and renpy.game.interface.restart_interaction and renpy.game.contexts:
            renpy.game.contexts[-1].scene_lists.focused = None

        renpy.config.skipping = None

    if renpy.config.after_replay_callback:
        renpy.config.after_replay_callback()