from random import randrange, random
from time import time
import logging
from TwisterTempoGUI import TwisterTempoGUI


class TwoFeetTempoMove(object):

    COLORS_ALPHA = {0: 'RED', 1: 'BLUE', 2: 'YELLOW', 3: 'GREEN'}
    COLORS_RGB = {0: (255, 0, 0), 1: (0, 0, 255), 2: (255, 255, 0), 3: (0, 255, 0)}

    FOOT_CHANGE_PERC = 0.3
    FOOT_ON_AIR_PERC = 0.08
    FEET_ON_SAME_CIRCLE_PERC = 0.05

    def __init__(self, min_delay=0, max_delay=100):
        assert min_delay >= 0
        assert max_delay > 0
        self.min_delay = min_delay
        self.max_delay = max_delay
        self._last_beat_millis = 0
        self._left_color = randrange(0, len(TwoFeetTempoMove.COLORS_ALPHA))
        self._right_color = randrange(0, len(TwoFeetTempoMove.COLORS_ALPHA))
        self._left_direction = "FW"
        self._right_direction = "FW"
        self._next_foot = 'RIGHT'
        logging.info("Starting with LEFT: %s, RIGHT: %s" %
                     (TwoFeetTempoMove.COLORS_ALPHA[self._left_color],
                      TwoFeetTempoMove.COLORS_ALPHA[self._right_color]))
        self.tt_gui = TwisterTempoGUI()
        self.tt_gui.set_left_color(TwoFeetTempoMove.COLORS_ALPHA[self._left_color])
        self.tt_gui.set_right_color(TwoFeetTempoMove.COLORS_ALPHA[self._right_color])

        self._starting_millis = time() * 1000

    def get_colors_alpha(self):
        return {'RIGHT': TwoFeetTempoMove.COLORS_ALPHA[self._right_color],
                'LEFT': TwoFeetTempoMove.COLORS_ALPHA[self._left_color]}

    def get_colors_rgb(self):
        return {'RIGHT': TwoFeetTempoMove.COLORS_RGB[self._right_color],
                'LEFT': TwoFeetTempoMove.COLORS_RGB[self._left_color]}

    def increase_speed(self):
        self.min_delay = self.min_delay - 10

    def decrease_speed(self):
        self.min_delay = self.min_delay + 10

    def tempo_found_callback(self, seconds, millis, confidence):
        act_delay = millis - self._last_beat_millis + randrange(0, self.max_delay)
        if act_delay >= self.min_delay:
            self._last_beat_millis = millis
            self.beat_found()

    def beat_found(self):
        millis = self._last_beat_millis
        logging.debug("Randomized beat found at: %d:%d.%d" %
                      (millis / 60000, millis / 1000, millis % 1000))
        act_millis = time() * 1000 - self._starting_millis
        logging.debug("\tActual: %d:%d.%d" %
                      (act_millis / 60000, act_millis / 1000, act_millis % 1000))

        # special moves
        if random() < TwoFeetTempoMove.FOOT_ON_AIR_PERC:  # randomized next foot on air move
            if self._next_foot == 'RIGHT':
                self.tt_gui.set_right_color(TwoFeetTempoMove.COLORS_ALPHA[self._right_color], on_air=True)
            else:
                self.tt_gui.set_left_color(TwoFeetTempoMove.COLORS_ALPHA[self._left_color], on_air=True)
            logging.debug("\tmove next foot On Air")

        elif random() < TwoFeetTempoMove.FEET_ON_SAME_CIRCLE_PERC:  # randomized both feet on same circle
            if self._next_foot == 'RIGHT':
                self._right_color = self._left_color
                self.tt_gui.set_large_color(TwoFeetTempoMove.COLORS_ALPHA[self._right_color])
            else:
                self._left_color = self._right_color
                self.tt_gui.set_large_color(TwoFeetTempoMove.COLORS_ALPHA[self._left_color])
            logging.debug("\tmove both feet on same circle")

        # end special moves
        else:
            if random() < TwoFeetTempoMove.FOOT_CHANGE_PERC:  # randomize at 30% the switch on foot
                if self._next_foot == 'RIGHT':
                    self._next_foot = 'LEFT'
                else:
                    self._next_foot = 'RIGHT'

            if self._next_foot == 'RIGHT':
                if self._right_direction == "FW":
                    if self._right_color == len(TwoFeetTempoMove.COLORS_ALPHA) - 1:
                        self._right_color = self._right_color - 1
                        self._right_direction = "BW"
                    else:
                        self._right_color = self._right_color + 1
                else:
                    if self._right_color == 0:
                        self._right_color = self._right_color + 1
                        self._right_direction = "FW"
                    else:
                        self._right_color = self._right_color - 1
                self.tt_gui.set_right_color(TwoFeetTempoMove.COLORS_ALPHA[self._right_color])
                logging.debug("\tmove RIGHT foot to " + TwoFeetTempoMove.COLORS_ALPHA[self._right_color])
                self._next_foot = 'LEFT'
            else:
                if self._left_direction == "FW":
                    if self._left_color == len(TwoFeetTempoMove.COLORS_ALPHA) - 1:
                        self._left_color = self._left_color - 1
                        self._left_direction = "BW"
                    else:
                        self._left_color = self._left_color + 1
                else:
                    if self._left_color == 0:
                        self._left_color = self._left_color + 1
                        self._left_direction = "FW"
                    else:
                        self._left_color = self._left_color - 1
                self.tt_gui.set_left_color(TwoFeetTempoMove.COLORS_ALPHA[self._left_color])
                logging.debug("\tmove LEFT foot to " + TwoFeetTempoMove.COLORS_ALPHA[self._left_color])
                self._next_foot = 'RIGHT'

