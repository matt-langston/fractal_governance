# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Constants for *Fractally White Paper Addendum 1*

See
[Fractally White Paper Addendum 1](https://hive.blog/fractally/@dan/fractally-white-paper-addendum-1)  # noqa: E501
and
[Refinement of Token Distribution Math](https://hive.blog/fractally/@dan/refinement-of-token-distribution-math).  # noqa: E501
"""


import attrs
import fractal_governance.dataset
import fractal_governance.math
import fractal_governance.util
from fractal_governance.addendum_1.token_supply import TokenSupply
from fractal_governance.constants import (
    ACCUMULATED_RESPECT_COLUMN_NAME,
    MEETING_DATE_COLUMN_NAME,
    MEETING_ID_WHEN_ADDENDUM_1_GOES_INTO_EFFECT,
)


@attrs.frozen
class Addendum1Constants:
    """Constants for *Fractally White Paper Addendum 1* calculations

    The only required argument to the constructor is `dataset`.

    The arguments `total_respect_before_addendum_1_individual` and
    `total_respect_before_addendum_1_team` are useful for highlighting issues in Team
    fractally's spreadsheet.
    """

    dataset: fractal_governance.dataset.Dataset = attrs.field(repr=False)

    total_respect_before_addendum_1_individual: float = attrs.field(default=None)

    total_respect_before_addendum_1_team: float = attrs.field(default=None)

    total_respect_before_addendum_1: float = attrs.field(default=None, init=False)

    token_supply_before_addendum_1_individual: float = attrs.field(
        default=None, init=False
    )
    token_supply_before_addendum_1_team: float = attrs.field(default=None, init=False)

    token_supply_before_addendum_1: float = attrs.field(default=None, init=False)

    pro_rata_respect: float = attrs.field(default=None, init=False)

    def __attrs_post_init__(self) -> None:
        DATE_WHEN_ADDENDUM_1_GOES_INTO_EFFECT = (
            fractal_governance.util.meeting_id_to_timestamp(
                MEETING_ID_WHEN_ADDENDUM_1_GOES_INTO_EFFECT
            )
        )

        df_member_respect_over_time = (
            self.dataset.df_member_respect_new_and_returning_by_meeting[
                [MEETING_DATE_COLUMN_NAME, ACCUMULATED_RESPECT_COLUMN_NAME]
            ].set_index(MEETING_DATE_COLUMN_NAME)
        )

        df_team_respect_over_time = (
            self.dataset.df_team_respect_by_meeting_date[
                [MEETING_DATE_COLUMN_NAME, ACCUMULATED_RESPECT_COLUMN_NAME]
            ]
            .groupby(MEETING_DATE_COLUMN_NAME)
            .sum()
        )

        total_respect_before_addendum_1_individual = (
            self.total_respect_before_addendum_1_individual
        )
        if not total_respect_before_addendum_1_individual:
            total_respect_before_addendum_1_individual = (
                df_member_respect_over_time[
                    df_member_respect_over_time.index
                    < DATE_WHEN_ADDENDUM_1_GOES_INTO_EFFECT
                ]
                .sum()
                .iloc[0]
            )
            object.__setattr__(
                self,
                "total_respect_before_addendum_1_individual",
                total_respect_before_addendum_1_individual,
            )

        total_respect_before_addendum_1_team = self.total_respect_before_addendum_1_team
        if not total_respect_before_addendum_1_team:
            total_respect_before_addendum_1_team = (
                df_team_respect_over_time[
                    df_team_respect_over_time.index
                    < DATE_WHEN_ADDENDUM_1_GOES_INTO_EFFECT
                ]
                .sum()
                .iloc[0]
            )
            object.__setattr__(
                self,
                "total_respect_before_addendum_1_team",
                total_respect_before_addendum_1_team,
            )

        total_respect_before_addendum_1 = (
            total_respect_before_addendum_1_individual
            + total_respect_before_addendum_1_team
        )
        object.__setattr__(
            self,
            "total_respect_before_addendum_1",
            total_respect_before_addendum_1,
        )

        token_supply_before_addendum_1 = TokenSupply(
            time=(MEETING_ID_WHEN_ADDENDUM_1_GOES_INTO_EFFECT - 1)
        ).token_supply
        object.__setattr__(
            self,
            "token_supply_before_addendum_1",
            token_supply_before_addendum_1,
        )

        token_supply_before_addendum_1_individual = (
            total_respect_before_addendum_1_individual / total_respect_before_addendum_1
        ) * token_supply_before_addendum_1
        object.__setattr__(
            self,
            "token_supply_before_addendum_1_individual",
            token_supply_before_addendum_1_individual,
        )

        token_supply_before_addendum_1_team = (
            total_respect_before_addendum_1_team / total_respect_before_addendum_1
        ) * token_supply_before_addendum_1
        object.__setattr__(
            self,
            "token_supply_before_addendum_1_team",
            token_supply_before_addendum_1_team,
        )

        pro_rata_respect = (
            token_supply_before_addendum_1 / total_respect_before_addendum_1
        )
        object.__setattr__(
            self,
            "pro_rata_respect",
            pro_rata_respect,
        )
