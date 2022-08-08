# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Dataset for fractal governance data analysis"""

from enum import Enum, auto
from typing import Dict, List

import attrs
import numpy as np
import pandas as pd
import uncertainties

import fractal_governance.math
import fractal_governance.statistics
import fractal_governance.util
from fractal_governance.util import (
    ACCUMULATED_LEVEL_COLUMN_NAME,
    ACCUMULATED_RESPECT_COLUMN_NAME,
    ACCUMULATED_RESPECT_NEW_MEMBER_COLUMN_NAME,
    ACCUMULATED_RESPECT_RETURNING_MEMBER_COLUMN_NAME,
    ATTENDANCE_COUNT_COLUMN_NAME,
    LEVEL_COLUMN_NAME,
    MEAN_COLUMN_NAME,
    MEETING_DATE_COLUMN_NAME,
    MEETING_ID_COLUMN_NAME,
    MEMBER_ID_COLUMN_NAME,
    MEMBER_NAME_COLUMN_NAME,
    NEW_MEMBER_COUNT_COLUMN_NAME,
    RESPECT_COLUMN_NAME,
    RETURNING_MEMBER_COUNT_COLUMN_NAME,
    STANDARD_DEVIATION_COLUMN_NAME,
    TEAM_NAME_COLUMN_NAME,
    WEIGHTED_MEAN_LEVEL_COLUMN_NAME,
    WEIGHTED_MEAN_RESPECT_COLUMN_NAME,
)


class WeightedMeanLevelAlgorithm(Enum):
    """The various algorithms for calculating a weighted rolling mean `Level`"""

    RollingMean = auto()
    WeightedRollingMean = auto()
    WeightedRollingMeanWithHysteresis = auto()


@attrs.frozen(kw_only=True)
class Statistics:
    """The mean and standard deviation for a measurement"""

    mean: float = attrs.field(repr=lambda value: f"{value:.2f}")
    standard_deviation: float = attrs.field(repr=lambda value: f"{value:.2f}")


@attrs.frozen
class Dataset:
    """A wrapper around the fractal governance dataset"""

    df: pd.DataFrame
    df_member_summary_stats_by_member_id: pd.DataFrame
    df_member_level_by_attendance_count: pd.DataFrame
    df_member_respect_new_and_returning_by_meeting: pd.DataFrame
    df_member_attendance_new_and_returning_by_meeting: pd.DataFrame
    df_member_leader_board: pd.DataFrame
    df_team_respect_by_meeting_date: pd.DataFrame
    df_team_representation_by_date: pd.DataFrame
    df_team_leader_board: pd.DataFrame

    @property
    def total_respect(self) -> int:
        """Return the total respect earned from all sources"""
        return self.total_member_respect + self.total_team_respect

    @property
    def total_member_respect(self) -> int:
        """Return the total respect earned by individual members"""
        return self.df[RESPECT_COLUMN_NAME].sum()  # type: ignore

    @property
    def total_team_respect(self) -> int:
        """Return the total respect earned by teams"""
        return self.df_team_respect_by_meeting_date[  # type: ignore
            ACCUMULATED_RESPECT_COLUMN_NAME
        ].sum()

    @property
    def total_unique_members(self) -> int:
        """Return the total number of unique members"""
        return self.df_member_leader_board[MEMBER_ID_COLUMN_NAME].size  # type: ignore

    @property
    def total_meetings(self) -> int:
        """Return the total number weekly consensus meetings"""
        return len(self.df.groupby(MEETING_ID_COLUMN_NAME))

    @property
    def last_meeting_date(self) -> pd.Timestamp:
        """Return the last meeting date for this dataset"""
        return self.df.sort_values(by=MEETING_DATE_COLUMN_NAME, ascending=True).iloc[
            -1
        ][MEETING_DATE_COLUMN_NAME]

    @property
    def attendance_stats(self) -> Statistics:
        """Return the mean and standard deviation for attendance from this dataset"""
        # The (MEETING_DATE_COLUMN_NAME, MEMBER_ID_COLUMN_NAME) tuple is degenerate
        # after the addition of multiple rounds, which is the reason for the `notna` on
        # LEVEL_COLUMN_NAME.
        df = self.df[self.df[LEVEL_COLUMN_NAME].notna()]
        groupby = df.groupby(MEETING_DATE_COLUMN_NAME).size()
        return Statistics(mean=groupby.mean(), standard_deviation=groupby.std())

    @property
    def attendance_consistency_stats(self) -> Statistics:
        """Return the mean and standard deviation for attendance consistency from this
        dataset"""
        attendance_consistency = self.df_member_leader_board[
            ATTENDANCE_COUNT_COLUMN_NAME
        ]
        return Statistics(
            mean=attendance_consistency.mean(),
            standard_deviation=attendance_consistency.std(),
        )

    @property
    def team_representation_stats(self) -> Statistics:
        """Return the mean and standard deviation for team representation from this
        dataset"""
        return Statistics(
            mean=self.df_team_representation_by_date.mean(),
            standard_deviation=self.df_team_representation_by_date.std(),
        )

    def get_new_member_dataframe_for_meeting_id(self, meeting_id: int) -> pd.DataFrame:
        """Return a DataFrame of new members for the given meeting ID."""
        df_current, _, boolean_filter = self._get_new_member_filter_for_meeting_id(
            meeting_id
        )
        return df_current[~boolean_filter]

    def get_returning_member_dataframe_for_meeting_id(
        self, meeting_id: int
    ) -> pd.DataFrame:
        """Return a DataFrame of veteran members for the given meeting ID."""
        df_current, _, boolean_filter = self._get_new_member_filter_for_meeting_id(
            meeting_id
        )
        return df_current[boolean_filter]

    def _get_new_member_filter_for_meeting_id(self, meeting_id: int) -> pd.DataFrame:
        """Internal helper method for selecting new members for the given meeting ID."""
        meeting_id_min, meeting_id_max = (
            self.df[MEETING_ID_COLUMN_NAME].min(),
            self.df[MEETING_ID_COLUMN_NAME].max(),
        )
        if not meeting_id_min <= meeting_id <= meeting_id_max:
            raise ValueError(
                f"meeting_id={meeting_id} must be in range [{meeting_id_min}, {meeting_id_max}]"  # noqa: E501
            )
        df_current = self.df[self.df[MEETING_ID_COLUMN_NAME] == meeting_id]
        df_previous = self.df[self.df[MEETING_ID_COLUMN_NAME] < meeting_id]
        boolean_filter = df_current[MEMBER_ID_COLUMN_NAME].isin(
            df_previous[MEMBER_ID_COLUMN_NAME]
        )
        return df_current, df_previous, boolean_filter

    @staticmethod
    def _get_mean_levels(*, levels: pd.Series, window_size: int) -> pd.Series:
        """Return a rolling mean of size `window_size` for the given `levels`"""
        mean_levels = levels.rolling(window_size).mean()
        mean_levels = mean_levels.dropna()

        standard_deviation_levels = levels.rolling(window_size).std()
        standard_deviation_levels = standard_deviation_levels.dropna()

        mean_levels = pd.Series(
            [
                uncertainties.ufloat(mean, standard_deviation)
                for mean, standard_deviation in zip(
                    mean_levels, standard_deviation_levels
                )
            ]
        )
        mean_levels.index += window_size

        return mean_levels[1:]

    @staticmethod
    def _get_partial_weighted_mean_levels(
        *, levels: pd.Series, window_size: int
    ) -> pd.Series:
        """Return the *ramp up average* initial values

        These are the initial `window_size` values in Team fractally's spreadsheet."""
        return levels[:window_size].cumsum() / window_size

    @staticmethod
    def _get_weighted_mean_levels(*, levels: pd.Series, window_size: int) -> pd.Series:
        """Return a weighted rolling mean of size `window_size` for the given `levels`

        The is similar to the result returned by `_get_weighted_mean_levels_fractally`
        but without the hysteresis."""
        lookback_window_size = window_size - 1

        mean_levels = levels.rolling(window_size).mean()
        mean_levels = mean_levels.dropna()

        standard_deviation_levels = levels.rolling(window_size).std()
        standard_deviation_levels = standard_deviation_levels.dropna()

        mean_levels = pd.Series(
            [
                uncertainties.ufloat(mean, standard_deviation)
                for mean, standard_deviation in zip(
                    mean_levels, standard_deviation_levels
                )
            ]
        )
        mean_levels.index += window_size

        # Create a temporary copy of `mean_levels` only to align the index with
        # `levels`.
        tmp_mean_levels = mean_levels[:-1]
        tmp_mean_levels.index += 1

        weighted_mean_levels = (
            lookback_window_size * tmp_mean_levels + levels.iloc[window_size:]
        ) / window_size

        return weighted_mean_levels

    @staticmethod
    def _get_weighted_mean_levels_fractally(
        *, levels: pd.Series, window_size: int
    ) -> pd.Series:
        """Return Team fractally's so-called *5xn6* value for the given `levels`

        The formula that Team fractally chose is a *weighted rolling average of `Level`
        over time* with the design goal of optimizing the storage of this average to a
        single value through hysteresis. This is accomplished as follows:

        1. Initialize the first *5xn6* value with the mean of the first `window_size`
        values of `levels`.

        2. Calculate the next value by taking the previous value as calculated in step
        #1 and multiplying it by `window_size - 1`, adding this result to the current
        value of `level` and then dividing this result by `window_size`.
        """
        lookback_window_size = window_size - 1

        mean_level = levels[:window_size].mean()
        standard_deviation_level = np.mean(levels[:window_size]).mean()

        weighted_mean_levels = pd.Series(levels, dtype=object)
        weighted_mean_levels.loc[window_size] = uncertainties.ufloat(
            mean_level, standard_deviation_level
        )

        for i in np.arange(window_size, len(weighted_mean_levels)) + 1:
            previous, current = weighted_mean_levels.loc[i - 1 : i]
            mean_level = (lookback_window_size * previous + current) / window_size
            weighted_mean_levels.loc[i] = mean_level

        return weighted_mean_levels[window_size:]

    def get_weighted_mean_levels(  # type: ignore
        self,
        *,
        window_size: int = 6,
        weighted_mean_level_algorithm: WeightedMeanLevelAlgorithm = WeightedMeanLevelAlgorithm.WeightedRollingMeanWithHysteresis,  # noqa: E501
        **kwargs,
    ) -> pd.DataFrame:
        """Return a DataFrame of various weighted mean levels

        See section "Initial Average" in the article
        [Refinement of Token Distribution Math]
        (https://hive.blog/fractally/@dan/refinement-of-token-distribution-math)
        """

        if weighted_mean_level_algorithm == WeightedMeanLevelAlgorithm.RollingMean:
            _weighted_mean_level_algorithm = self._get_mean_levels
        elif (
            weighted_mean_level_algorithm
            == WeightedMeanLevelAlgorithm.WeightedRollingMean
        ):
            _weighted_mean_level_algorithm = self._get_weighted_mean_levels
        elif (
            weighted_mean_level_algorithm
            == WeightedMeanLevelAlgorithm.WeightedRollingMeanWithHysteresis
        ):
            _weighted_mean_level_algorithm = self._get_weighted_mean_levels_fractally
        else:
            raise ValueError(
                f"Unsupported weighted_mean_level_algorithm {weighted_mean_level_algorithm.name}"  # noqa: E501
            )

        # Create a Series of levels with value 0, one for each meeting.
        zero_level_list = pd.Series(np.zeros(self.df[MEETING_ID_COLUMN_NAME].max()))
        zero_level_list.index += 1

        # The (MEETING_DATE_COLUMN_NAME, MEMBER_ID_COLUMN_NAME) tuple is degenerate
        # after the addition of multiple rounds, which is the reason for the `notna` on
        # LEVEL_COLUMN_NAME.
        df = self.df[self.df[LEVEL_COLUMN_NAME].notna()]
        weighted_mean_levels_by_member_id: Dict[str, pd.Series] = dict()
        for member_id, dfx in df.groupby(MEMBER_ID_COLUMN_NAME):
            # Insert a level of 0 for each meeting for which they were not in
            # attendance.
            levels = (
                dfx.groupby(MEETING_ID_COLUMN_NAME)[LEVEL_COLUMN_NAME].sum()
                + zero_level_list
            )
            levels = levels.fillna(0)

            weighted_mean_levels = _weighted_mean_level_algorithm(
                levels=levels, window_size=window_size
            )

            weighted_mean_levels_by_member_id[member_id] = weighted_mean_levels

        s_weighted_mean_levels = pd.DataFrame.from_dict(
            weighted_mean_levels_by_member_id, orient="index"
        ).unstack()
        s_weighted_mean_levels.index.names = [
            MEETING_ID_COLUMN_NAME,
            MEMBER_ID_COLUMN_NAME,
        ]

        df_weighted_mean_levels = pd.DataFrame(
            s_weighted_mean_levels, columns=[WEIGHTED_MEAN_LEVEL_COLUMN_NAME]
        ).reset_index()
        df_weighted_mean_levels = df_weighted_mean_levels[
            [
                MEMBER_ID_COLUMN_NAME,
                MEETING_ID_COLUMN_NAME,
                WEIGHTED_MEAN_LEVEL_COLUMN_NAME,
            ]
        ]

        df_weighted_mean_levels[
            WEIGHTED_MEAN_RESPECT_COLUMN_NAME
        ] = fractal_governance.math.respect(
            df_weighted_mean_levels[WEIGHTED_MEAN_LEVEL_COLUMN_NAME], **kwargs
        )

        return df_weighted_mean_levels

    @classmethod
    def from_csv(
        cls,
        fractal_dataset_csv_paths: fractal_governance.util.FractalDatasetCSVPaths = fractal_governance.util.FractalDatasetCSVPaths(),  # noqa: E501
    ) -> "Dataset":
        """Return a Dataset for the given Fractal's .csv file paths"""
        df = fractal_governance.util.read_csv(fractal_dataset_csv_paths)

        df_member_summary_stats_by_member_id = df.groupby(MEMBER_ID_COLUMN_NAME).agg(
            AttendanceCount=pd.NamedAgg(column=LEVEL_COLUMN_NAME, aggfunc="count"),
            AccumulatedLevel=pd.NamedAgg(column=LEVEL_COLUMN_NAME, aggfunc="sum"),
            AccumulatedRespect=pd.NamedAgg(column=RESPECT_COLUMN_NAME, aggfunc="sum"),
            Mean=pd.NamedAgg(column=LEVEL_COLUMN_NAME, aggfunc="mean"),
            StandardDeviation=pd.NamedAgg(column=LEVEL_COLUMN_NAME, aggfunc="std"),
        )

        df_member_level_by_attendance_count = (
            df_member_summary_stats_by_member_id.groupby(ATTENDANCE_COUNT_COLUMN_NAME)
            .apply(combined_statistics)
            .reset_index()
        )

        df_member_leader_board = df_member_summary_stats_by_member_id.join(
            df.groupby(MEMBER_ID_COLUMN_NAME).first()[[MEMBER_NAME_COLUMN_NAME]]
        ).sort_values(
            by=[
                ACCUMULATED_LEVEL_COLUMN_NAME,
                ATTENDANCE_COUNT_COLUMN_NAME,
                MEMBER_ID_COLUMN_NAME,
            ],
            ascending=[False, False, True],
        )
        column_names = [
            MEMBER_NAME_COLUMN_NAME,
            ACCUMULATED_LEVEL_COLUMN_NAME,
            ACCUMULATED_RESPECT_COLUMN_NAME,
            ATTENDANCE_COUNT_COLUMN_NAME,
        ]
        df_member_leader_board = df_member_leader_board[column_names].reset_index()
        df_member_leader_board.index += 1

        df_team_respect_by_meeting_date = (
            df[df[TEAM_NAME_COLUMN_NAME].notna()]
            .groupby([TEAM_NAME_COLUMN_NAME, MEETING_DATE_COLUMN_NAME])
            .agg(
                AccumulatedRespect=pd.NamedAgg(
                    column=RESPECT_COLUMN_NAME, aggfunc="sum"
                )
            )
            .reset_index()
        )

        # The (MEETING_DATE_COLUMN_NAME, MEMBER_ID_COLUMN_NAME) tuple is degenerate
        # after the addition of multiple rounds, which is the reason for the `notna` on
        # LEVEL_COLUMN_NAME.
        _df = df[df[LEVEL_COLUMN_NAME].notna()]
        df_team_representation_by_date = (
            _df[_df[TEAM_NAME_COLUMN_NAME].notna()]
            .groupby(MEETING_DATE_COLUMN_NAME)
            .size()
            / _df.groupby(MEETING_DATE_COLUMN_NAME).size()
        )

        df_team_leader_board = (
            df_team_respect_by_meeting_date.groupby(TEAM_NAME_COLUMN_NAME)
            .agg(
                AccumulatedRespect=pd.NamedAgg(
                    column=ACCUMULATED_RESPECT_COLUMN_NAME, aggfunc="sum"
                )
            )
            .sort_values(by=ACCUMULATED_RESPECT_COLUMN_NAME, ascending=False)
        )

        return cls(
            df=df,
            df_member_summary_stats_by_member_id=df_member_summary_stats_by_member_id,
            df_member_level_by_attendance_count=df_member_level_by_attendance_count,
            df_member_respect_new_and_returning_by_meeting=_create_df_member_respect_new_and_returning_by_meeting(  # noqa: E501
                df
            ),
            df_member_attendance_new_and_returning_by_meeting=_create_df_member_attendance_new_and_returning_by_meeting(  # noqa: E501
                df
            ),
            df_member_leader_board=df_member_leader_board,
            df_team_respect_by_meeting_date=df_team_respect_by_meeting_date,
            df_team_representation_by_date=df_team_representation_by_date,
            df_team_leader_board=df_team_leader_board,
        )


def _create_df_member_respect_new_and_returning_by_meeting(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Return a DataFrame containing aggregate member attendance and respect for each
    meeting"""
    meeting_dates: List[pd.Timestamp] = []
    meeting_ids: List[int] = []
    accumulated_respect_total: List[int] = []
    accumulated_respect_new_member: List[int] = []
    accumulated_respect_returning_member: List[int] = []
    # The (MEETING_DATE_COLUMN_NAME, MEMBER_ID_COLUMN_NAME) tuple is degenerate after
    # the addition of multiple rounds, which is the reason for the `notna` on
    # LEVEL_COLUMN_NAME.
    df = df[df[LEVEL_COLUMN_NAME].notna()]
    for ((meeting_date, meeting_id), dfx) in df.groupby(
        [MEETING_DATE_COLUMN_NAME, MEETING_ID_COLUMN_NAME]
    ):
        total_respect = dfx[RESPECT_COLUMN_NAME].sum()
        accumulated_respect_total.append(total_respect)
        df_previous = df[df[MEETING_DATE_COLUMN_NAME] < meeting_date]
        df_filter = dfx[MEMBER_ID_COLUMN_NAME].isin(df_previous[MEMBER_ID_COLUMN_NAME])
        df_new_member = dfx[~df_filter]
        df_returning_member = dfx[df_filter]
        new_member_respect = df_new_member[RESPECT_COLUMN_NAME].sum()
        returning_member_respect = df_returning_member[RESPECT_COLUMN_NAME].sum()
        meeting_dates.append(meeting_date)
        meeting_ids.append(meeting_id)
        accumulated_respect_new_member.append(new_member_respect)
        accumulated_respect_returning_member.append(returning_member_respect)
    return pd.DataFrame(
        {
            MEETING_DATE_COLUMN_NAME: meeting_dates,
            MEETING_ID_COLUMN_NAME: meeting_ids,
            ACCUMULATED_RESPECT_COLUMN_NAME: accumulated_respect_total,
            ACCUMULATED_RESPECT_NEW_MEMBER_COLUMN_NAME: accumulated_respect_new_member,
            ACCUMULATED_RESPECT_RETURNING_MEMBER_COLUMN_NAME: accumulated_respect_returning_member,  # noqa: E501
        }
    ).sort_index()


def _create_df_member_attendance_new_and_returning_by_meeting(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Return a DataFrame containing aggregate member attendance for each meeting"""
    meeting_dates = []
    meeting_ids = []
    new_member_counts = []
    returning_member_counts = []
    # The (MEETING_DATE_COLUMN_NAME, MEMBER_ID_COLUMN_NAME) tuple is degenerate after
    # the addition of multiple rounds, which is the reason for the `notna` on
    # LEVEL_COLUMN_NAME.
    df = df[df[LEVEL_COLUMN_NAME].notna()]
    for ((meeting_date, meeting_id), dfx) in df.groupby(
        [MEETING_DATE_COLUMN_NAME, MEETING_ID_COLUMN_NAME]
    ):
        df_previous = df[df[MEETING_DATE_COLUMN_NAME] < meeting_date]
        df_filter = dfx[MEMBER_ID_COLUMN_NAME].isin(df_previous[MEMBER_ID_COLUMN_NAME])
        df_new_member = dfx[~df_filter]
        df_returning_member = dfx[df_filter]
        meeting_dates.append(meeting_date)
        meeting_ids.append(meeting_id)
        new_member_counts.append(len(df_new_member))
        returning_member_counts.append(len(df_returning_member))
    return pd.DataFrame(
        {
            MEETING_DATE_COLUMN_NAME: meeting_dates,
            MEETING_ID_COLUMN_NAME: meeting_ids,
            NEW_MEMBER_COUNT_COLUMN_NAME: new_member_counts,
            RETURNING_MEMBER_COUNT_COLUMN_NAME: returning_member_counts,
        }
    )


def combined_statistics(df: pd.DataFrame) -> pd.Series:
    """Return the 'mean of means' and the 'mean of standard deviations' for the given
    DataFame"""
    mean = fractal_governance.statistics.combined_mean(
        df,
        count_column_name=ATTENDANCE_COUNT_COLUMN_NAME,
        mean_column_name=MEAN_COLUMN_NAME,
    )
    standard_deviation = fractal_governance.statistics.combined_standard_deviation(
        df,
        count_column_name=ATTENDANCE_COUNT_COLUMN_NAME,
        mean_column_name=MEAN_COLUMN_NAME,
        standard_deviation_column_name=STANDARD_DEVIATION_COLUMN_NAME,
    )
    return pd.Series(
        {
            MEAN_COLUMN_NAME: mean,
            STANDARD_DEVIATION_COLUMN_NAME: standard_deviation,
        }
    )
