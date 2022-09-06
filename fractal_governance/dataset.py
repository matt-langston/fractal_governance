# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Dataset for fractal governance data analysis"""

from typing import List

import attrs
import pandas as pd

import fractal_governance.math
import fractal_governance.statistics
import fractal_governance.util

from .constants import (
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
)


@attrs.frozen(kw_only=True)
class Statistics:
    """The mean and standard deviation for a measurement"""

    mean: float = attrs.field(repr=lambda value: f"{value:.2f}")
    standard_deviation: float = attrs.field(repr=lambda value: f"{value:.2f}")


@attrs.frozen
class Dataset:
    """A wrapper around the fractal governance dataset

    The only required argument to the constructor is `df`.
    """

    df: pd.DataFrame

    df_member_summary_stats_by_member_id: pd.DataFrame = attrs.field(
        default=None, init=False
    )
    df_member_level_by_attendance_count: pd.DataFrame = attrs.field(
        default=None, init=False
    )
    df_member_respect_new_and_returning_by_meeting: pd.DataFrame = attrs.field(
        default=None, init=False
    )
    df_member_attendance_new_and_returning_by_meeting: pd.DataFrame = attrs.field(
        default=None, init=False
    )
    df_member_leader_board: pd.DataFrame = attrs.field(default=None, init=False)
    df_team_respect_by_meeting_date: pd.DataFrame = attrs.field(
        default=None, init=False
    )
    df_team_representation_by_date: pd.DataFrame = attrs.field(default=None, init=False)
    df_team_leader_board: pd.DataFrame = attrs.field(default=None, init=False)

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

    @classmethod
    def from_csv(
        cls,
        fractal_dataset_csv_paths: fractal_governance.util.FractalDatasetCSVPaths = fractal_governance.util.FractalDatasetCSVPaths(),  # noqa: E501
    ) -> "Dataset":
        """Return a Dataset for the given Fractal's .csv file paths"""
        return cls(df=fractal_governance.util.read_csv(fractal_dataset_csv_paths))

    def __attrs_post_init__(self) -> None:
        df = self.df
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
                ACCUMULATED_RESPECT_COLUMN_NAME,
                ATTENDANCE_COUNT_COLUMN_NAME,
                MEMBER_ID_COLUMN_NAME,
            ],
            ascending=[False, False, True],
        )
        column_names = [
            MEMBER_NAME_COLUMN_NAME,
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

        object.__setattr__(self, "df", df)
        object.__setattr__(
            self,
            "df_member_summary_stats_by_member_id",
            df_member_summary_stats_by_member_id,
        )
        object.__setattr__(
            self,
            "df_member_level_by_attendance_count",
            df_member_level_by_attendance_count,
        )
        object.__setattr__(
            self,
            "df_member_respect_new_and_returning_by_meeting",
            _create_df_member_respect_new_and_returning_by_meeting(df),
        )
        object.__setattr__(
            self,
            "df_member_attendance_new_and_returning_by_meeting",
            _create_df_member_attendance_new_and_returning_by_meeting(df),
        )
        object.__setattr__(self, "df_member_leader_board", df_member_leader_board)
        object.__setattr__(
            self, "df_team_respect_by_meeting_date", df_team_respect_by_meeting_date
        )
        object.__setattr__(
            self, "df_team_representation_by_date", df_team_representation_by_date
        )
        object.__setattr__(self, "df_team_leader_board", df_team_leader_board)


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
