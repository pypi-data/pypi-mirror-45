import numpy as np
from .info_reader import InfoReader


class FrameStream:

    def __init__(self, data_path, info_path):
        self.measurement_info = InfoReader.read_info_from_file(info_path)
        self.data_path = data_path
        self.file_stream = open(data_path)
        self.number_of_lines = 0
        self._nr_of_bytes_before_each_line = [0]
        self._initalise_class_variables()
        self.time = self._read_time()
        self.x_pixels = self.measurement_info['imageWidth']
        self.y_pixels = self.measurement_info['imageHeight']

    def get_frame_at_time(self):
        line_nr = self._find_index_of_nearest(self.time, time)
        intensity = self._FrameStream.get_intensity_from_line(line_nr)
        return np.reshape(intensity, (self.x_Pixels, self.y_Pixels))

    def _get_line_nr(self, nr):
        offset_in_bytes = self._nr_of_bytes_before_each_line[nr]
        self.file_stream.seek(offset_in_bytes)
        return self.file_stream.readline()

    def _read_time(self):
        self._reset_file_stream()
        time = []
        for line_nr, line in enumerate(self.file_stream):
            t = FrameStream._extract_time_from_line(line)
            time.append(t)
        return np.array(time)

    def _initalise_class_variables(self):
        byte_count = 0
        for line_nr, line in enumerate(self.file_stream):
            byte_count += bytes(line, encoding='utf-8').__sizeof__() - 33
            self._nr_of_bytes_before_each_line.append(byte_count)
            self.number_of_lines = line_nr + 2

    def _reset_file_stream(self):
        self.file_stream.seek(0)

    @staticmethod
    def _extract_time_from_line(line):
        return float(line.split(',')[0])

    @staticmethod
    def _find_index_of_nearest(array, value):
        return (np.abs(np.array(array) - value)).argmin()

    def get_intensity_from_line(self, line_nr):
        line = self._get_line_nr(line_nr)
        return FrameStream._extract_intensity_from_line(line)

    @staticmethod
    def _extract_intensity_from_line(line):
        intensity_string = line.split(',')[1].split(';')[:-1]
        return np.array([float(i) for i in intensity_string])

    @staticmethod
    def _find_index_of_nearest(array, value):
        return (np.abs(np.array(array) - value)).argmin()
