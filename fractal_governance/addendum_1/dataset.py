# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Dataset for Fractally White Paper Addendum 1"""

from enum import Enum, auto
from typing import List

import attrs
import fractal_governance.dataset
import pandas as pd
import uncertainties
from fractal_governance.constants import (
    GROUP_COLUMN_NAME,
    INTEGRAL_COLUMN_NAME,
    INTEGRAL_END_COLUMN_NAME,
    INTEGRAL_START_COLUMN_NAME,
    LEVEL_COLUMN_NAME,
    MEETING_ID_COLUMN_NAME,
    MEETING_ID_WHEN_ADDENDUM_1_GOES_INTO_EFFECT,
    MEMBER_ID_COLUMN_NAME,
    RESPECT_COLUMN_NAME,
    RESPECT_PRO_RATA_COLUMN_NAME,
    TEAM_ID_COLUMN_NAME,
    TOKEN_INTEGRAL_COLUMN_NAME,
    TOKEN_SUPPLY_AFTER_TRANSITION_TO_CONSTANT_INFLATION_COLUMN_NAME,
    TOKEN_SUPPLY_BEFORE_TRANSITION_TO_CONSTANT_INFLATION_COLUMN_NAME,
    TOKEN_SUPPLY_COLUMN_NAME,
    TOKENS_INDIVIDUAL,
    TOKENS_TEAM,
    WEIGHTED_MEAN_RESPECT_COLUMN_NAME,
)

from .constants import Addendum1Constants
from .token_supply import TokenSupply
from .weighted_means import WeightedMeans


@attrs.frozen
class Addendum1Dataset:
    """A wrapper around `fractal_governance.dataset.Dataset` with the *Fractally White
    Paper Addendum 1* changes.

    The only required argument to the constructor is `dataset`.
    """

    dataset: fractal_governance.dataset.Dataset = attrs.field(repr=False)

    weighted_means: WeightedMeans = attrs.field(repr=False, default=None)

    addendum_1_constants: Addendum1Constants = attrs.field(default=None)

    dataset_with_addendum_1_respect: fractal_governance.dataset.Dataset = attrs.field(
        repr=False, default=None, init=False
    )

    df: pd.DataFrame = attrs.field(default=None, init=False)

    df_weighted_means: pd.DataFrame = attrs.field(default=None, init=False)

    df_token_distribution_per_meeting: pd.DataFrame = attrs.field(
        default=None, init=False
    )

    df_token_supply: pd.DataFrame = attrs.field(default=None, init=False)

    def __attrs_post_init__(self) -> None:
        #
        # Make copies of the original required DataFrame because it will be augmented
        # with columns that could be different if this class is instantiated with
        # different initial state.
        #
        df = self.dataset.df.copy()

        #
        # Create a DataFrame for the token supply that spans the meeting dates from the
        # given dataset.
        #
        meeting_id_list: List[float] = []
        integral_start_list: List[float] = []
        integral_end_list: List[float] = []
        integral_list: List[float] = []
        token_integral_list: List[float] = []
        token_supply_before_transition_to_constant_inflation_list: List[float] = []
        token_supply_after_transition_to_constant_inflation_list: List[float] = []
        token_supply_list: List[float] = []
        for meeting_id in range(1, df[MEETING_ID_COLUMN_NAME].max() + 1):
            token_supply = TokenSupply(time=meeting_id)
            assert meeting_id == token_supply.time
            meeting_id_list.append(meeting_id)
            integral_start_list.append(token_supply.integral_start)
            integral_end_list.append(token_supply.integral_end)
            integral_list.append(token_supply.integral)
            token_integral_list.append(token_supply.token_integral)
            token_supply_before_transition_to_constant_inflation_list.append(
                token_supply.token_supply_before_transition_to_constant_inflation
            )
            token_supply_after_transition_to_constant_inflation_list.append(
                token_supply.token_supply_after_transition_to_constant_inflation
            )
            token_supply_list.append(token_supply.token_supply)
        df_token_supply = pd.DataFrame(
            {
                MEETING_ID_COLUMN_NAME: meeting_id_list,
                INTEGRAL_START_COLUMN_NAME: integral_start_list,
                INTEGRAL_END_COLUMN_NAME: integral_end_list,
                INTEGRAL_COLUMN_NAME: integral_list,
                TOKEN_INTEGRAL_COLUMN_NAME: token_integral_list,
                TOKEN_SUPPLY_BEFORE_TRANSITION_TO_CONSTANT_INFLATION_COLUMN_NAME: token_supply_before_transition_to_constant_inflation_list,  # noqa: E501
                TOKEN_SUPPLY_AFTER_TRANSITION_TO_CONSTANT_INFLATION_COLUMN_NAME: token_supply_after_transition_to_constant_inflation_list,  # noqa: E501
                TOKEN_SUPPLY_COLUMN_NAME: token_supply_list,
            }
        )
        df_token_supply.set_index(MEETING_ID_COLUMN_NAME, inplace=True)
        object.__setattr__(self, "df_token_supply", df_token_supply)

        #
        # Add pro-rata Respect tokens for both individuals and teams. These are Respect
        # tokens earned before the meeting when Addendum 1 went into effect, but
        # adjusted for the Addendum 1 token supply that went into effect at the time of
        # the first meeting.
        #
        addendum_1_constants = self.addendum_1_constants
        if not addendum_1_constants:
            addendum_1_constants = Addendum1Constants(dataset=self.dataset)
            object.__setattr__(self, "addendum_1_constants", addendum_1_constants)

        df[RESPECT_PRO_RATA_COLUMN_NAME] = (
            df[RESPECT_COLUMN_NAME] * addendum_1_constants.pro_rata_respect
        )
        # Pro-rata Respect is only non-zero for meetings before Addendum 1 went into
        # effect.
        df.loc[
            df[MEETING_ID_COLUMN_NAME] >= MEETING_ID_WHEN_ADDENDUM_1_GOES_INTO_EFFECT,
            RESPECT_PRO_RATA_COLUMN_NAME,
        ] = 0
        # Move the new column from the back to the front.
        columns = list(df.columns)
        columns = columns[-1:] + columns[:-1]
        df = df[columns]
        object.__setattr__(self, "df", df)

        #
        # Respect tokens earned after Addendum 1 went into effect.
        #
        weighted_means = self.weighted_means
        if not weighted_means:
            weighted_means = WeightedMeans(dataset=self.dataset)
            object.__setattr__(self, "weighted_means", weighted_means)

        #
        # Make copies of the original required DataFrame because it will be augmented
        # with columns that could be different if this class is instantiated with
        # different initial state.
        #
        df_weighted_means = self.weighted_means.df.copy()

        class WeightedMeanRespectFraction(Enum):
            """The various weighted mean Respect fractions"""

            Individual = auto()
            Team = auto()

        def calculate_tokens(
            df: pd.DataFrame,
            weighted_mean_respect_fraction: WeightedMeanRespectFraction,
        ) -> pd.Series:
            meeting_id = df.iloc[0][MEETING_ID_COLUMN_NAME]
            token_integral = df_token_supply.loc[meeting_id, TOKEN_INTEGRAL_COLUMN_NAME]

            weighted_mean_respect_individual = df[WEIGHTED_MEAN_RESPECT_COLUMN_NAME]
            weighted_mean_respect_team = df[df[TEAM_ID_COLUMN_NAME].notna()][
                WEIGHTED_MEAN_RESPECT_COLUMN_NAME
            ]
            weighted_mean_respect_total = (
                weighted_mean_respect_individual.sum()
                + weighted_mean_respect_team.sum()
            )

            if weighted_mean_respect_fraction == WeightedMeanRespectFraction.Individual:
                fraction = (
                    weighted_mean_respect_individual / weighted_mean_respect_total
                )
            elif weighted_mean_respect_fraction == WeightedMeanRespectFraction.Team:
                fraction = weighted_mean_respect_team / weighted_mean_respect_total
            else:
                raise ValueError(
                    f"Unsupported weighted_mean_respect_fraction {weighted_mean_respect_fraction.name}"  # noqa: E501
                )

            return token_integral * fraction

        tokens_individual = df_weighted_means.groupby(MEETING_ID_COLUMN_NAME).apply(
            calculate_tokens, WeightedMeanRespectFraction.Individual
        )
        df_weighted_means[TOKENS_INDIVIDUAL] = tokens_individual.reset_index(level=0)[
            WEIGHTED_MEAN_RESPECT_COLUMN_NAME
        ]

        tokens_team = df_weighted_means.groupby(MEETING_ID_COLUMN_NAME).apply(
            calculate_tokens, WeightedMeanRespectFraction.Team
        )
        df_weighted_means[TOKENS_TEAM] = tokens_team.reset_index(level=0)[
            WEIGHTED_MEAN_RESPECT_COLUMN_NAME
        ]

        # Move the two new columns from the back to the front.
        columns = list(df_weighted_means.columns)
        columns = columns[-2:] + columns[:-2]
        df_weighted_means = df_weighted_means[columns]
        object.__setattr__(self, "df_weighted_means", df_weighted_means)

        #
        # Create a `fractal_governance.dataset.Dataset` that replaces the values in the
        # *Respect* token column with the values using the Addendum 1 calculations.
        #
        df_addendum_1 = df.copy()

        #
        # Replace the *Respect* values before the date when Addendum 1 went into effect
        # with the pro-rata *Respect* values.
        #
        df_addendum_1[RESPECT_COLUMN_NAME] = df_addendum_1[RESPECT_PRO_RATA_COLUMN_NAME]
        df_addendum_1 = df_addendum_1.drop(RESPECT_PRO_RATA_COLUMN_NAME, axis=1)

        #
        # Replace the *Respect* values after the date when Addendum 1 went into effect
        # with the weighted mean *Respect* values.
        #
        df_weighted_means = df_weighted_means[
            df_weighted_means[MEETING_ID_COLUMN_NAME]
            >= MEETING_ID_WHEN_ADDENDUM_1_GOES_INTO_EFFECT
        ]
        df_weighted_means = df_weighted_means[
            [
                MEETING_ID_COLUMN_NAME,
                MEMBER_ID_COLUMN_NAME,
                TOKENS_INDIVIDUAL,
                TOKENS_TEAM,
            ]
        ]
        df_weighted_means[[TOKENS_INDIVIDUAL, TOKENS_TEAM]] = df_weighted_means[
            [TOKENS_INDIVIDUAL, TOKENS_TEAM]
        ].apply(lambda series: uncertainties.unumpy.nominal_values(series))

        df_addendum_1 = (
            df_addendum_1.set_index([MEETING_ID_COLUMN_NAME, MEMBER_ID_COLUMN_NAME])
            .join(
                df_weighted_means.set_index(
                    [MEETING_ID_COLUMN_NAME, MEMBER_ID_COLUMN_NAME]
                ),
                how="outer",
            )
            .reset_index()
        )
        rows = (
            df_addendum_1[LEVEL_COLUMN_NAME].notna()
            | df_addendum_1[GROUP_COLUMN_NAME].isna()
        ) & df_addendum_1[TOKENS_INDIVIDUAL].notna()
        df_addendum_1.loc[rows, RESPECT_COLUMN_NAME] = df_addendum_1.loc[
            rows, TOKENS_INDIVIDUAL
        ]
        df_addendum_1 = df_addendum_1.drop(TOKENS_INDIVIDUAL, axis=1)
        dataset_with_addendum_1_respect = fractal_governance.dataset.Dataset(
            df=df_addendum_1
        )
        object.__setattr__(
            self, "dataset_with_addendum_1_respect", dataset_with_addendum_1_respect
        )

        #
        # Create a DataFrame for the aggregate weekly token distributions for both
        # individuals and teams.
        #
        df_token_distribution_per_meeting = df_weighted_means.groupby(
            MEETING_ID_COLUMN_NAME
        ).sum()
        object.__setattr__(
            self, "df_token_distribution_per_meeting", df_token_distribution_per_meeting
        )
