import numpy as np
import matplotlib.pyplot as plt
from .frame_stream import FrameStream
import ipywidgets as widgets
from ipywidgets import interact


class FART:

    def __init__(self, filename, gridfs=None, recording_software='fart'):
        self._FrameStream = FrameStream(filename)

    @property
    def measurement_info(self):
        return self._FrameStream.measurement_info

    @property
    def time(self):
        return self._FrameStream.time

    @property
    def frames(self):
        for time in self.time:
            yield self._FrameStream.get_frame_at_time(time)
        return

    def get_frame_at_time(self, time):
        return self._FrameStream.get_frame_at_time(time)

    def plot_frame_at_time(self, time):
        frame = self.get_frame_at_time(time)
        plt.imshow(frame)

    def plot_all_frames(self, figsize=(6, 8)):
        plt.style.use({'figure.figsize': figsize})
        interact(self.plot_frame_at_time, time=widgets.SelectionSlider(
            options=self.time,
            value=self.time[0],
            description='Time:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True
        ))

    @staticmethod
    def _find_index_of_nearest(array, value):
        return (np.abs(np.array(array) - value)).argmin()
