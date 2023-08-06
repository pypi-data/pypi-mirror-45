# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, KISTERS AG, Germany.
# All rights reserved.
# Modification, redistribution and use in source and binary
# forms, with or without modification, are not permitted
# without prior written approval by the copyright holder.
#
# Created on 13.02.2018
# @author: rs

from abc import ABC, abstractmethod
from datetime import datetime
import pytz
from typing import Mapping, Union

from pandas import DataFrame, to_datetime

from kisters.water.time_series.core import TimeSeries


class TimeSeriesCutRangeMixin(TimeSeries):
    """
    classdocs
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self._tz = pytz.utc

    @abstractmethod
    def _load_data_frame(self, start: datetime=None, end: datetime=None, params: Mapping=None) -> DataFrame:
        """Return the DataFrame containing the TimeSeries data for the interval start:end"""

    def _get_timezone(self) -> pytz.timezone:
        return self._tz

    def _to_zoned_datetime(self, dt: Union[str, datetime]) -> Union[datetime, None]:
        if dt is None:
            return None
        else:
            dt = to_datetime(dt)
            if dt.tz is None:
                return dt.tz_localize(self._get_timezone())
            return dt

    def read_data_frame(self, start: datetime=None, end: datetime=None, params: Mapping=None) -> DataFrame:
        start = start if start is not None else self.coverage_from
        end = end if end is not None else self.coverage_until
        start = self._to_zoned_datetime(start)
        end = self._to_zoned_datetime(end)

        df = self._load_data_frame(start, end, params)
        df.index = df.index.tz_convert(self._get_timezone())
        return df
