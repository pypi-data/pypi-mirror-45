import math
import pandas as pd


class BaseSignal(object):
    def __init__(self, data, data_period, start_date, env_period, wrap_index=True):
        self._data_period = data_period
        self._env_period = env_period
        self._start = start_date

        indexes = pd.period_range(start=self._start, periods=len(data), freq='{0}min'.format_map(self._data_period))
        self.data = pd.Series(data, indexes)
        self.data.resample('{0}min'.format_map(self._env_period))

    def __getitem__(self, i):
        return self.data[i % len(self.data)]

    # def __getslice__(self, i, j):
    #     length = i - j
    #     wrapped_i = i % len(self.data)
    #
    #     tile_multiple = math.ceil((start + length) / len(schedule))
    #     tiled_schedule = schedule * tile_multiple
    #     return tiled_schedule[start:start + length]
    #     return self.data[i:j]
