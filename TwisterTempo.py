import pyglet
from pyglet.window import key

from TempoFinder import TempoFinder
from TwoFeetTempoMove import TwoFeetTempoMove

if __name__ == '__main__':
    # record_sink(sys.argv[1])
    # print_tempo()
    tf = TempoFinder(samplerate=8000)
    tf.start()
    tftm = TwoFeetTempoMove(800, 100)
    tf.set_tempo_found_callback(tftm.tempo_found_callback)
    pyglet.clock.schedule_interval(tf.record_hop, .01)

    @tftm.tt_gui.window.event
    def on_draw():
        tftm.tt_gui.draw()

    @tftm.tt_gui.window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.UP:  # increase sensibility
            tf.increase_sensibility()
            print("increased sensibility")
        elif symbol == key.DOWN:  # decrease sensibility
            tf.decrease_sensibility()
            print("decreased sensibility")
        elif symbol == key.RIGHT:  # increase speed
            tftm.increase_speed()
            print("increased speed")
        elif symbol == key.LEFT:  # decrease speed
            tftm.decrease_speed()
            print("decreased speed")
        elif symbol == key.SPACE:  # toggle pause on beat recognition
            tf.on_pause = not tf.on_pause
            tftm.tt_gui.show_pause = tf.on_pause
            print("pause toggle")
        elif symbol == key.ESCAPE:  # exit
            pyglet.app.exit()
        elif symbol == key.L:  # exit
            tftm.tt_gui.set_large_color("GREEN")

    tf.on_pause = False
    tftm.tt_gui.show_pause = False

    pyglet.app.run()

    tf.end()

    print("BPM: %f" % tf.get_bpms())

# TODO: comandi da tastiera: flag di muovere il piede di più posizioni
# TODO: spostare di più di una posizione con impostazione da tastiera
# TODO: splashscreen con pausa, istruzioni con credits e comandi
# TODO: input da loopback --> sembra impossibile sotto Mac OS
# TODO: aggiungere i nomi L e R sotto i cerchi e una + quando sono insieme
# TODO: trovare bel nome (TwisterRhythm?)
# TODO: scrivere su un log invece che a schermo
