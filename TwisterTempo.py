import pyglet
from pyglet.window import key
import logging

from TempoFinder import TempoFinder
from TwoFeetTempoMove import TwoFeetTempoMove

if __name__ == '__main__':
    logging.basicConfig(filename='TwisterTempo.log', level=logging.INFO,
                        filemode='w')

    # a sample rate of 8000 is somehow enough
    tf = TempoFinder(samplerate=8000)
    tf.start()

    # starting values for the random move detector
    tftm = TwoFeetTempoMove(500, 1)
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
            logging.info("increased sensibility")
        elif symbol == key.DOWN:  # decrease sensibility
            tf.decrease_sensibility()
            print("decreased sensibility")
            logging.info("decreased sensibility")
        elif symbol == key.RIGHT:  # increase speed
            tftm.increase_speed()
            print("increased speed")
            logging.info("increased speed")
        elif symbol == key.LEFT:  # decrease speed
            tftm.decrease_speed()
            print("decreased speed")
            logging.info("decreased speed")
        elif symbol == key.SPACE:  # toggle pause on beat recognition
            tf.on_pause = not tf.on_pause
            tftm.tt_gui.show_pause = tf.on_pause
            logging.info("pause toggle")
        elif symbol == key.ESCAPE:  # exit
            pyglet.app.exit()
            logging.info("exiting")
        elif symbol == key.L:  # exit
            tftm.tt_gui.set_large_color("GREEN")

    tf.on_pause = False
    tftm.tt_gui.show_pause = False

    print("Starting...")
    logging.info("Starting...")
    pyglet.app.run()

    tf.end()

    logging.info("BPM: %f" % tf.get_bpms())
    logging.info("Ending...")
    print("Ending...")

# TODO: move the foot more than a single position (configurable by keyboard)
# TODO: splashscreen with pause, instructions and credits
