"""
class TempoFinder
"""
from time import time, perf_counter, sleep
import numpy
import sounddevice
from aubio import tempo, pitch, sink

WRITE_WAV = False
WAV_NAME = "out.wav"


class TempoFinder(object):

    MAX_LISTEN_PER_RECORD_MS = 20. * 1000.

    def __init__(self, win_size=512, samplerate=44100):

        # total number of audio frames read
        self._total_frames = 0

        # list of beats, in seconds since start
        self._beats = []

        # recording window and hop size
        self._win_size = win_size
        self._hop_size = win_size // 2  # hop size

        # audio sample rate
        self._samplerate = samplerate

        # tempo finder algorithm instance
        self._tempo_alg = tempo("default", self._win_size, self._hop_size, self._samplerate)
        print("Tempo silence=%d" % self._tempo_alg.get_silence())
        self._tempo_alg.set_silence(-40)

        self.on_pause = False

        # pitch algorithm instance
        # self.pitch_alg = pitch("default", self.win_size, self.hop_size, self.samplerate)

        self._mono_vec = numpy.array([], dtype=numpy.float32)
        self._tempo_found_callback = TempoFinder.default_tempo_found_callback
        self._starting_millis = time() * 1000.

        self._stream = sounddevice.InputStream(
            channels=1, samplerate=float(self._samplerate), dtype='float32',
            latency='low', callback=self.audio_callback)

        if WRITE_WAV:
            self._out_file = sink(samplerate=int(self._samplerate))

    def start(self):
        self._stream.start()

    def end(self):
        if WRITE_WAV:
            self._out_file.close()

    def set_tempo_found_callback(self, tempo_found_callback):
        assert callable(tempo_found_callback)
        self._tempo_found_callback = tempo_found_callback

    @staticmethod
    def default_tempo_found_callback(seconds, millis, confidence):
        print("Beat found at: %d:%d.%d, confidence=%.2f" %
              (seconds // 60, seconds % 60, millis % 1000, confidence))

    def audio_callback(self, indata, frames, timez, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print("Input status: %s. Read %d blocks" % (status, len(indata)))
        # mix down to mono and append data
        # print(str(self._mono_vec))
        # print(str(indata))
        self._mono_vec = numpy.append(self._mono_vec, indata)
        # print("In record_hop after %.2f seconds" % dt)

    def increase_sensibility(self):
        self._tempo_alg.set_silence(self._tempo_alg.get_silence() - 10)

    def decrease_sensibility(self):
        self._tempo_alg.set_silence(self._tempo_alg.get_silence() + 10)

    def record_hop(self, nd):
        # record some audio
        now = perf_counter()
        # print("in record_hop with %d blocks, @ %f" % (len(self._mono_vec), now))
        if len(self._mono_vec) >= self._hop_size:
            # print("after recorded %d hops, delta = %f" % (len(mono_vec), perf_counter() - now))

            # consider as many slices of size hop_size as possible
            # within a boxed timeframe of MAX_LISTEN_PER_RECORD_MS
            rec_start_millis = time()
            while len(self._mono_vec) >= self._hop_size \
                    and time() - rec_start_millis < TempoFinder.MAX_LISTEN_PER_RECORD_MS:
                compute_vec = self._mono_vec[0:self._hop_size]
                self._mono_vec = self._mono_vec[self._hop_size:]
                if WRITE_WAV:
                    self._out_file(compute_vec, len(compute_vec))

                # algorithm found a beat?
                is_beat = self._tempo_alg(compute_vec)
                if is_beat and not self.on_pause:
                    print("Beat found")  # . Latency: %.2f" % self.mic.latency)
                    this_beat_s = self._tempo_alg.get_last_s()
                    this_beat_ms = self._tempo_alg.get_last_ms()
                    this_beat_confidence = self._tempo_alg.get_confidence()
                    act_millis = time() * 1000. - self._starting_millis
                    self._tempo_found_callback(act_millis // 1000, act_millis, this_beat_confidence)
                    self._beats.append(act_millis // 1000)
                self._total_frames = self._total_frames + self._hop_size
        # print("@ %d after while delta = %f" % ((self._total_frames // self._samplerate),
        #                                        (perf_counter() - now)))

    def get_bpms(self):
        return self._tempo_alg.get_bpm()


if __name__ == '__main__':
    # record_sink(sys.argv[1])
    # print_tempo()
    tf = TempoFinder(samplerate=8000)
    tf.start()
    while True:
        tf.record_hop(0)
        sleep(0.1)
