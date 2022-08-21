# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Weighted Means for *Fractally White Paper Addendum 1*

See
[Fractally White Paper Addendum 1](https://hive.blog/fractally/@dan/fractally-white-paper-addendum-1)  # noqa: E501
and
[Refinement of Token Distribution Math](https://hive.blog/fractally/@dan/refinement-of-token-distribution-math).  # noqa: E501
"""

import functools
from enum import Enum, auto
from typing import Dict

import attrs
import fractal_governance.dataset
import fractal_governance.math
import fractal_governance.util
import numpy as np
import pandas as pd
import uncertainties
from fractal_governance.constants import (
    LEVEL_COLUMN_NAME,
    MEETING_ID_COLUMN_NAME,
    MEETING_ID_WHEN_HIVE_SIGNATURE_REQUIRED,
    MEMBER_ID_COLUMN_NAME,
    SIGNATURE_ON_FILE_COLUMN_NAME,
    TEAM_ID_COLUMN_NAME,
    TEAM_NAME_COLUMN_NAME,
    WEIGHTED_MEAN_LEVEL_COLUMN_NAME,
    WEIGHTED_MEAN_RESPECT_COLUMN_NAME,
    WEIGHTED_MEAN_RESPECT_INDIVIDUAL_FRACTION_PER_MEETING_COLUMN_NAME,
    WEIGHTED_MEAN_RESPECT_INDIVIDUAL_PER_MEETING_COLUMN_NAME,
    WEIGHTED_MEAN_RESPECT_TEAM_FRACTION_PER_MEETING_COLUMN_NAME,
    WEIGHTED_MEAN_RESPECT_TEAM_PER_MEETING_COLUMN_NAME,
)


class WeightedMeanLevelAlgorithm(Enum):
    """The various algorithms for calculating a weighted rolling mean `Level`"""

    RollingMean = auto()
    WeightedRollingMean = auto()
    WeightedRollingMeanWithHysteresis = auto()


@attrs.frozen
class WeightedMeanParameters:
    """A wrapper around the parameters for the weighted mean value calculations from
    Fractally White Paper Addendum 1

    Team fractally uses the default attribute values of this class to:

    1. Calculate the *weighted mean Level*
    2. Calculate the *weighted mean Respect* using an approximation to the continuous
       Fibonacci function
    3. Artificially clamp *weighted mean Respect* to zero when the *weighted mean Level*
       is zero.
    4. Artificially clamp *weighted mean Respect* to zero when a user has not signed
       the Fractal Contributor Agreement after a Fractal-defined meeting date.
    """

    window_size: int = 6

    meeting_attendance_requirement_for_members: int = 12

    weighted_mean_level_algorithm: WeightedMeanLevelAlgorithm = (
        WeightedMeanLevelAlgorithm.WeightedRollingMeanWithHysteresis
    )

    respect_fibonacci_bias: float = 0

    respect_fibonacci_include_second_term: bool = False

    clamp_mean_respect_to_zero_when_mean_level_is_zero: bool = True

    clamp_mean_respect_to_zero_when_fractal_contributor_agreement_not_signed: bool = (
        True
    )


@attrs.frozen
class WeightedMeans:
    """A wrapper around weighted mean values from *Fractally White Paper Addendum 1*

    Team fractally uses the default attribute values of this class which calculates
    *weighted mean Respect* using an approximation to the continuous Fibonacci
    function as well as artificially clamping *weighted mean Respect* to zero when the
    *weighted mean Level* is zero.
    """

    dataset: fractal_governance.dataset.Dataset = attrs.field(repr=False)

    parameters: WeightedMeanParameters = WeightedMeanParameters()

    df: pd.DataFrame = attrs.field(default=None, init=False)

    df_per_meeting: pd.DataFrame = attrs.field(default=None, init=False)

    def get_pivot_table(
        self,
        value_column_name: str = "Value",
        weighted_mean_column_name: str = WEIGHTED_MEAN_RESPECT_COLUMN_NAME,
    ) -> pd.DataFrame:
        return get_pivot_table(
            self.df.copy(),
            value_column_name=value_column_name,
            weighted_mean_column_name=weighted_mean_column_name,
        )

    def __attrs_post_init__(self) -> None:
        df = get_weighted_mean_levels(
            self.dataset.df,
            window_size=self.parameters.window_size,
            meeting_attendance_requirement_for_members=self.parameters.meeting_attendance_requirement_for_members,  # noqa: E501
            weighted_mean_level_algorithm=self.parameters.weighted_mean_level_algorithm,
        ).set_index(MEMBER_ID_COLUMN_NAME)

        df[WEIGHTED_MEAN_RESPECT_COLUMN_NAME] = df[
            WEIGHTED_MEAN_LEVEL_COLUMN_NAME
        ].apply(
            fractal_governance.math.respect,
            bias=self.parameters.respect_fibonacci_bias,
            include_second_term=self.parameters.respect_fibonacci_include_second_term,
        )

        if self.parameters.clamp_mean_respect_to_zero_when_mean_level_is_zero:
            df.loc[
                df[WEIGHTED_MEAN_LEVEL_COLUMN_NAME] == 0,
                WEIGHTED_MEAN_RESPECT_COLUMN_NAME,
            ] = 0

        df_account_status = (
            self.dataset.df[[MEMBER_ID_COLUMN_NAME, SIGNATURE_ON_FILE_COLUMN_NAME]]
            .drop_duplicates(ignore_index=True)
            .set_index(MEMBER_ID_COLUMN_NAME)
        )
        df = df.join(df_account_status)

        df_team_status = (
            self.dataset.df[
                [
                    MEMBER_ID_COLUMN_NAME,
                    MEETING_ID_COLUMN_NAME,
                    TEAM_ID_COLUMN_NAME,
                    TEAM_NAME_COLUMN_NAME,
                ]
            ]
            .drop_duplicates()
            .set_index([MEMBER_ID_COLUMN_NAME, MEETING_ID_COLUMN_NAME])
        )
        df = df.set_index(MEETING_ID_COLUMN_NAME, append=True).join(df_team_status)

        df = df.reset_index()

        if (
            self.parameters.clamp_mean_respect_to_zero_when_fractal_contributor_agreement_not_signed  # noqa: E501
        ):
            df.loc[
                ~df[SIGNATURE_ON_FILE_COLUMN_NAME]
                & (
                    df[MEETING_ID_COLUMN_NAME]
                    >= MEETING_ID_WHEN_HIVE_SIGNATURE_REQUIRED
                ),
                [WEIGHTED_MEAN_RESPECT_COLUMN_NAME],
            ] = 0

        df = df.sort_values(
            by=[MEMBER_ID_COLUMN_NAME, MEETING_ID_COLUMN_NAME],
            key=_sort_by_member_id_lower_case,
        )

        def individual_respect_per_meeting(df: pd.DataFrame) -> pd.DataFrame:
            return df[WEIGHTED_MEAN_RESPECT_COLUMN_NAME].sum()

        df_weighted_mean_respect_individual_per_meeting = pd.DataFrame(
            {
                WEIGHTED_MEAN_RESPECT_INDIVIDUAL_PER_MEETING_COLUMN_NAME: df.groupby(
                    MEETING_ID_COLUMN_NAME
                ).apply(individual_respect_per_meeting)
            }
        )

        def individual_respect_fraction_per_meeting(df: pd.DataFrame) -> pd.DataFrame:
            return (
                df[WEIGHTED_MEAN_RESPECT_COLUMN_NAME]
                / df[WEIGHTED_MEAN_RESPECT_COLUMN_NAME].sum()
            )

        df[WEIGHTED_MEAN_RESPECT_INDIVIDUAL_FRACTION_PER_MEETING_COLUMN_NAME] = (
            df.groupby(MEETING_ID_COLUMN_NAME)
            .apply(individual_respect_fraction_per_meeting)
            .reset_index(MEETING_ID_COLUMN_NAME)[WEIGHTED_MEAN_RESPECT_COLUMN_NAME]
        )

        def team_respect_per_meeting(df: pd.DataFrame) -> pd.DataFrame:
            df = df[df[TEAM_ID_COLUMN_NAME].notna()]
            return df[WEIGHTED_MEAN_RESPECT_COLUMN_NAME].sum()

        df_weighted_mean_respect_team_per_meeting = pd.DataFrame(
            {
                WEIGHTED_MEAN_RESPECT_TEAM_PER_MEETING_COLUMN_NAME: df.groupby(
                    MEETING_ID_COLUMN_NAME
                ).apply(team_respect_per_meeting)
            }
        )

        def team_respect_fraction_per_meeting(df: pd.DataFrame) -> pd.DataFrame:
            df = df[df[TEAM_ID_COLUMN_NAME].notna()]
            return (
                df[WEIGHTED_MEAN_RESPECT_COLUMN_NAME]
                / df[WEIGHTED_MEAN_RESPECT_COLUMN_NAME].sum()
            )

        df[WEIGHTED_MEAN_RESPECT_TEAM_FRACTION_PER_MEETING_COLUMN_NAME] = (
            df.groupby(MEETING_ID_COLUMN_NAME)
            .apply(team_respect_fraction_per_meeting)
            .reset_index(MEETING_ID_COLUMN_NAME)[WEIGHTED_MEAN_RESPECT_COLUMN_NAME]
        )

        df_weighted_mean_respect_individual_fraction_per_meeting = (
            df_weighted_mean_respect_individual_per_meeting
            / (
                df_weighted_mean_respect_individual_per_meeting.values
                + df_weighted_mean_respect_team_per_meeting.values
            )
        )
        df_weighted_mean_respect_individual_fraction_per_meeting.rename(
            columns={
                WEIGHTED_MEAN_RESPECT_INDIVIDUAL_PER_MEETING_COLUMN_NAME: WEIGHTED_MEAN_RESPECT_INDIVIDUAL_FRACTION_PER_MEETING_COLUMN_NAME  # noqa: E501
            },
            inplace=True,
        )

        df_weighted_mean_respect_team_fraction_per_meeting = (
            df_weighted_mean_respect_team_per_meeting
            / (
                df_weighted_mean_respect_individual_per_meeting.values
                + df_weighted_mean_respect_team_per_meeting.values
            )
        )
        df_weighted_mean_respect_team_fraction_per_meeting.rename(
            columns={
                WEIGHTED_MEAN_RESPECT_TEAM_PER_MEETING_COLUMN_NAME: WEIGHTED_MEAN_RESPECT_TEAM_FRACTION_PER_MEETING_COLUMN_NAME  # noqa: E501
            },
            inplace=True,
        )

        df_per_meeting = (
            df_weighted_mean_respect_individual_per_meeting.join(
                df_weighted_mean_respect_team_per_meeting
            )
            .join(df_weighted_mean_respect_individual_fraction_per_meeting)
            .join(df_weighted_mean_respect_team_fraction_per_meeting)
        )

        object.__setattr__(self, "df", df)
        object.__setattr__(
            self,
            "df_per_meeting",
            df_per_meeting,
        )


def _get_mean_levels(*, levels: pd.Series, window_size: int) -> pd.Series:
    """Return a rolling mean of size `window_size` for the given `levels`"""
    mean_levels = levels.rolling(window_size).mean()
    mean_levels = mean_levels.dropna()

    standard_deviation_levels = levels.rolling(window_size).std()
    standard_deviation_levels = standard_deviation_levels.dropna()

    mean_levels = pd.Series(
        [
            uncertainties.ufloat(mean, standard_deviation)
            for mean, standard_deviation in zip(mean_levels, standard_deviation_levels)
        ]
    )
    mean_levels.index += window_size

    return mean_levels[1:]


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
            for mean, standard_deviation in zip(mean_levels, standard_deviation_levels)
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


def _get_weighted_mean_levels_fractally(
    *,
    levels: pd.Series,
    window_size: int,
    meeting_attendance_requirement_for_members: int,
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

    for meeting_id in np.arange(window_size, len(weighted_mean_levels)) + 1:
        previous, current = weighted_mean_levels.loc[meeting_id - 1 : meeting_id]
        mean_level = (lookback_window_size * previous + current) / window_size
        weighted_mean_levels.loc[meeting_id] = mean_level
        meeting_id_min = meeting_id - meeting_attendance_requirement_for_members + 1
        if meeting_id_min >= 0 and not levels.loc[meeting_id_min:meeting_id].sum() > 0:
            # Reset a member's `Level` history if they have not been in attendance for
            # the previous required number of meetings, thus making them new members.
            weighted_mean_levels.loc[meeting_id] = uncertainties.ufloat(0, 0)

    return weighted_mean_levels[window_size:]


def get_weighted_mean_levels(
    df: pd.DataFrame,
    *,
    window_size: int,
    meeting_attendance_requirement_for_members: int,
    weighted_mean_level_algorithm: WeightedMeanLevelAlgorithm,
) -> pd.DataFrame:
    """Return a DataFrame of weighted mean levels

    See section "Initial Average" in the article
    [Refinement of Token Distribution Math]
    (https://hive.blog/fractally/@dan/refinement-of-token-distribution-math)
    """

    if weighted_mean_level_algorithm == WeightedMeanLevelAlgorithm.RollingMean:
        _weighted_mean_level_algorithm = _get_mean_levels
    elif (
        weighted_mean_level_algorithm == WeightedMeanLevelAlgorithm.WeightedRollingMean
    ):
        _weighted_mean_level_algorithm = _get_weighted_mean_levels
    elif (
        weighted_mean_level_algorithm
        == WeightedMeanLevelAlgorithm.WeightedRollingMeanWithHysteresis
    ):
        _weighted_mean_level_algorithm = functools.partial(
            _get_weighted_mean_levels_fractally,
            meeting_attendance_requirement_for_members=meeting_attendance_requirement_for_members,  # noqa: E501
        )
    else:
        raise ValueError(
            f"Unsupported weighted_mean_level_algorithm {weighted_mean_level_algorithm.name}"  # noqa: E501
        )

    # Create a Series of levels with value 0, one for each meeting.
    zero_level_list = pd.Series(np.zeros(df[MEETING_ID_COLUMN_NAME].max()))
    zero_level_list.index += 1

    # The (MEETING_DATE_COLUMN_NAME, MEMBER_ID_COLUMN_NAME) tuple is degenerate
    # after the addition of multiple rounds, which is the reason for the `notna` on
    # LEVEL_COLUMN_NAME.
    df = df[df[LEVEL_COLUMN_NAME].notna()]
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

        # Team fractally uses a progressive mean for the first `window_size` levels so
        # that there is a *weighted_mean_level* value for for every meeting_id.
        _levels = pd.Series(
            [uncertainties.ufloat(level, 0) for level in levels[:window_size]]
        )
        _levels.index = levels.index[:window_size]
        _levels = _levels.cumsum() / window_size
        _levels
        weighted_mean_levels = pd.concat([_levels, weighted_mean_levels])

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

    return df_weighted_mean_levels.sort_values(
        by=[MEMBER_ID_COLUMN_NAME, MEETING_ID_COLUMN_NAME],
        key=_sort_by_member_id_lower_case,
    )


def _sort_by_member_id_lower_case(series: pd.Series) -> pd.Series:
    if pd.api.types.infer_dtype(series) == "string":
        return series.str.lower()
    return series


def get_pivot_table(
    df: pd.DataFrame,
    value_column_name: str = "Value",
    weighted_mean_column_name: str = WEIGHTED_MEAN_LEVEL_COLUMN_NAME,
) -> pd.DataFrame:
    column_names = [value_column_name, MEMBER_ID_COLUMN_NAME, MEETING_ID_COLUMN_NAME]
    df[value_column_name] = df[weighted_mean_column_name].apply(
        lambda series: uncertainties.unumpy.nominal_values(series)
    )
    pivot_table = pd.pivot_table(
        df[column_names],
        values=value_column_name,
        index=MEMBER_ID_COLUMN_NAME,
        columns=MEETING_ID_COLUMN_NAME,
        sort=False,
    )
    return pivot_table
