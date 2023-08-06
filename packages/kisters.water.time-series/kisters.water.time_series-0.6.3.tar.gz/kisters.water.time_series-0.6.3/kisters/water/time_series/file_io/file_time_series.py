# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, KISTERS AG, Germany.
# All rights reserved.
# Modification, redistribution and use in source and binary
# forms, with or without modification, are not permitted
# without prior written approval by the copyright holder.
#
# Created on Tue Aug 29 16:29:26 2017
# @author: rs

from datetime import datetime
import logging

from pandas.errors import EmptyDataError
from typing import Any, Mapping, TYPE_CHECKING, Union

import pandas as pd
import pytz
from pytz import UnknownTimeZoneError

from kisters.water.time_series.core.time_series import TimeSeries
from kisters.water.time_series.core.time_series_attributes_mixin import TimeSeriesAttributesMixin
from kisters.water.time_series.core.time_series_cut_range_mixin import TimeSeriesCutRangeMixin
from kisters.water.time_series.core.time_series_item_mixin import TimeSeriesItemMixin
if TYPE_CHECKING:
    from kisters.water.time_series.file_io.time_series_format import TimeSeriesFormat

logger = logging.getLogger(__name__)


class FileTimeSeries(TimeSeriesItemMixin, TimeSeriesAttributesMixin, TimeSeriesCutRangeMixin, TimeSeries):
    def __init__(self, fmt: 'TimeSeriesFormat', meta: Mapping[str, Any]=None):
        super().__init__()
        self.__meta = meta
        self.__fmt = fmt
        self.__meta.setdefault('dataCoverageFrom', None)
        self.__meta.setdefault('dataCoverageUntil', None)
        timezone = self.metadata.get('timezone', None)
        if timezone is None:
            timezone = self.__format_metadata().get('timezone', 'UTC')
        if 'UTC+' in timezone or 'GMT+' in timezone:
            timezone = 'Etc/GMT-' + timezone.split('+')[-1].split(')')[0].split(':')[0]
        elif 'UTC-' in timezone or 'GMT-' in timezone:
            timezone = 'Etc/GMT+' + timezone.split('-')[-1].split(')')[0].split(':')[0]
        try:
            self._tz = pytz.timezone(timezone)
        except UnknownTimeZoneError:
            self._tz = pytz.timezone('UTC')

    def __refresh_coverage(self):
        try:
            df = self._load_data_frame()
            self.__meta['dataCoverageFrom'] = df.index[0]
            self.__meta['dataCoverageUntil'] = df.index[-1]
            self.__fmt.writer.update_metadata(
                self.path, self.__format_metadata()['file'], self.metadata)
        except (EmptyDataError, IndexError):
            self.__meta['dataCoverageFrom'] = None
            self.__meta['dataCoverageUntil'] = None

    @property
    def coverage_from(self) -> Union[datetime, None]:
        if self.__meta['dataCoverageFrom'] is None:
            self.__refresh_coverage()
            if self.__meta['dataCoverageFrom'] is None:
                return None
        return pd.to_datetime(self.__meta['dataCoverageFrom'], utc=True).tz_convert(self._tz)

    @property
    def coverage_until(self) -> Union[datetime, None]:
        if self.__meta['dataCoverageUntil'] is None:
            self.__refresh_coverage()
            if self.__meta['dataCoverageUntil'] is None:
                return None
        return pd.to_datetime(self.__meta['dataCoverageUntil'], utc=True).tz_convert(self._tz)

    def _raw_metadata(self) -> Mapping[str, str]:
        return self.__meta

    def __format_metadata(self) -> Mapping[str, Any]:
        return self.__meta.get(list(self.__fmt.extensions)[0].upper(), {})

    def __file_path(self) -> str:
        pre_path = ''
        if self.__fmt.root_dir != '':
            pre_path = self.__fmt.root_dir + '/'
        return pre_path + self.path + '.' + self.__format_metadata()['file'].rsplit('.', 1)[-1]

    def _load_data_frame(self, start: datetime=None, end: datetime=None,
                         params: Mapping[str, str]=None) -> pd.DataFrame:
        try:
            df = self.__fmt.reader.load_data_frame(
                columns=self.__meta.get('columns'), **self.__format_metadata())
        except (EmptyDataError, ValueError, FileNotFoundError):
            for meta in self.__fmt.reader._extract_metadata(self.__file_path()):
                if meta.get('tsPath', '') == self.path:
                    self.__meta = meta
                    self.__meta.setdefault('dataCoverageFrom', None)
                    self.__meta.setdefault('dataCoverageUntil', None)
            df = self.__fmt.reader.load_data_frame(
                columns=self.__meta.get('columns'), **self.__format_metadata())

        if start is None and end is None:
            return df
        if start is None:
            mask = df.index <= end
        elif end is None:
            mask = df.index >= start
        else:
            mask = (df.index >= start) & (df.index <= end)
        return df.loc[mask]

    @classmethod
    def write_comments(cls, comments):
        logger.warning("write_comments not implemented. Ignoring {} comments".format(len(comments)))

    @classmethod
    def update_qualities(cls, qualities):
        logger.warning("update_qualities not implemented. Ignoring {} qualities".format(len(qualities)))

    def write_data_frame(self, data_frame: pd.DataFrame, start: datetime=None, end: datetime=None):
        start = start if start is not None else data_frame.index[0]
        end = end if end is not None else data_frame.index[-1]
        try:
            data_inside = self.read_data_frame()
        except EmptyDataError:
            data_inside = pd.DataFrame()
        data = pd.concat([data_inside, data_frame[~data_frame.index.isin(data_inside.index)]], sort=True)
        data.update(data_frame)
        data = data.reindex(data.index.sort_values())
        if data_frame.shape[0] == 0:
            mask = (start <= data.index) | (data.index <= end)
        else:
            mask = (((start <= data.index) & (data.index < data_frame.index[0]))
                    | ((data_frame.index[-1] < data.index) & (data.index <= end)))
        if data.index[mask].shape[0] > 0:
            data = data.drop(data.index[mask])

        self.__fmt.writer.write(self.__file_path(), [data], start, end, [self.metadata])
        for meta in self.__fmt.reader._get_metadata(self.__file_path()):
            if meta.get('tsPath', '') == self.path:
                self.__meta = meta
                self.__meta.setdefault('dataCoverageFrom', None)
                self.__meta.setdefault('dataCoverageUntil', None)
