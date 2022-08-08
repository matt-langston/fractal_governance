# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Token Supply functionality for Fractal Governance data analysis"""

import math

import attrs
import numpy as np


@attrs.frozen(kw_only=True)
class TokenSupply:
    """The token supply of a Fractal"""

    time: float = attrs.field(default=1)

    token_inflation_rate: float = attrs.field(default=10**6)

    half_life: float = attrs.field(default=52.0)

    constant_inflation_rate: float = attrs.field(default=1.05)

    transition_to_constant_inflation: float = attrs.field(
        init=False, repr=lambda value: f"{value:,.10f}"
    )

    token_supply_at_transition_to_constant_inflation: float = attrs.field(
        init=False, repr=lambda value: f"{value:,.10f}"
    )

    integral_start: float = attrs.field(init=False, repr=lambda value: f"{value:,.10f}")

    integral_end: float = attrs.field(init=False, repr=lambda value: f"{value:,.10f}")

    integral: float = attrs.field(init=False, repr=lambda value: f"{value:,.10f}")

    token_integral: float = attrs.field(init=False, repr=lambda value: f"{value:,.0f}")

    token_supply_before_transition_to_constant_inflation: float = attrs.field(
        init=False, repr=lambda value: f"{value:,.2f}"
    )

    token_supply_after_transition_to_constant_inflation: float = attrs.field(
        init=False, repr=lambda value: f"{value:,.2f}"
    )

    token_supply: float = attrs.field(init=False, repr=lambda value: f"{value:,.2f}")

    def _integral_start(self, *, time: float) -> float:
        if time < 1:
            raise RuntimeError(f"LOGIC ERROR: unexpected time={time}")
        integral_start = np.power(2, -(time - 1) / self.half_life)
        integral_start *= -self.half_life / np.log(2)
        return integral_start  # type: ignore

    def _integral_end(self, *, time: float) -> float:
        if time < 1:
            raise RuntimeError(f"LOGIC ERROR: unexpected time={time}")
        return self._integral_start(time=(time + 1))

    def __attrs_post_init__(self) -> None:
        if self.time < 1:
            raise RuntimeError(f"LOGIC ERROR: unexpected time={self.time}")

        INTEGRAL_START = self._integral_start(time=self.time)

        INTEGRAL_END = self._integral_end(time=self.time)

        INTEGRAL = INTEGRAL_END - INTEGRAL_START

        INTEGRAL_START_WEEK_1 = self._integral_start(time=1)

        # TODO(mlangston) I think Team fractlly may have the time wrong for when the
        # transition to constant 5% inflation occurs because the time when the
        # exponential decay reaches 5% is -log2(0.05) ~= 4.32193.
        #
        # For some reason Team fractlly transitions to constant 5% inflation at time
        # -log2(x / (1 + x)) ~= 3.92664 where x == log2(1.05). I simplified their value
        # for x by using the logarithmic identity log2(1.05) == ln(1.05) / ln(2). This
        # corresponds to abruptly transitioning from ~6.6% to 5%.
        TRANSITION_TO_CONSTANT_INFLATION = -np.log2(
            np.log2(self.constant_inflation_rate)
            / (1 + np.log2(self.constant_inflation_rate))
        )

        T0 = (self.time - 1) / self.half_life

        T1 = (self.time - 0) / self.half_life

        T0_DELTA = T0 - TRANSITION_TO_CONSTANT_INFLATION

        T1_DELTA = T1 - TRANSITION_TO_CONSTANT_INFLATION

        print(f"MDL: {self.time} T0:       {T0}")
        print(f"MDL: {self.time} T1:       {T1}")
        print(f"MDL: {self.time} T0_DELTA: {T0_DELTA}")
        print(f"MDL: {self.time} T1_DELTA: {T1_DELTA}")

        TIME_AT_TRANSITION_TO_CONSTANT_INFLATION = (
            TRANSITION_TO_CONSTANT_INFLATION * self.half_life
        )

        TIME_BEFORE_TRANSITION_TO_CONSTANT_INFLATION = math.floor(
            TIME_AT_TRANSITION_TO_CONSTANT_INFLATION
        )

        TIME_AFTER_TRANSITION_TO_CONSTANT_INFLATION = math.ceil(
            TIME_AT_TRANSITION_TO_CONSTANT_INFLATION
        )

        TOKEN_SUPPLY_BEFORE_TRANSITION_TO_CONSTANT_INFLATION = (
            INTEGRAL_END - INTEGRAL_START_WEEK_1
        ) * self.token_inflation_rate

        TOKEN_SUPPLY_AT_TRANSITION_TO_CONSTANT_INFLATION = (
            self.token_inflation_rate * self.half_life / np.log(2)
        ) * (1 - 2**-TRANSITION_TO_CONSTANT_INFLATION)

        TOKEN_SUPPLY_AFTER_TRANSITION_TO_CONSTANT_INFLATION = (
            TOKEN_SUPPLY_AT_TRANSITION_TO_CONSTANT_INFLATION
            * self.constant_inflation_rate**T1_DELTA
        )

        # Team fractally changes their spreadsheet formula in column J (with column
        # label "Combined Cont. Supply") between weeks 205 and 206 (see rows 217 and
        # 218). I think this may be a bug and that the formula should instead be
        # identical to the previous rows (i.e. weeks 1 through 205 are correct). The
        # following was copied from the spreadsheet on 2022.08.14 and the issue is with
        # week 206 where the division should instead be multiplication as it is for
        # weeks 1 through 205.
        #
        # week 1  : =if(C217<$R$210*52, (E217-$D$13)*$E$4,I217)
        # week 205: =if(C217<$R$210*52, (E217-$D$13)*$E$4,I217)
        # week 206: =if(C218<$R$210/52, (E218-$D$13)*$E$4,I218)
        #
        # I defined the two constants `TIME_BEFORE_TRANSITION_TO_CONSTANT_INFLATION` and
        # `TIME_AFTER_TRANSITION_TO_CONSTANT_INFLATION` to make this clear in the
        # following calculations for `token_integral` and `token_supply`.

        if self.time < TIME_BEFORE_TRANSITION_TO_CONSTANT_INFLATION:
            token_integral = INTEGRAL * self.token_inflation_rate
            token_supply = TOKEN_SUPPLY_BEFORE_TRANSITION_TO_CONSTANT_INFLATION
        elif (
            TIME_BEFORE_TRANSITION_TO_CONSTANT_INFLATION
            <= self.time
            < TIME_AFTER_TRANSITION_TO_CONSTANT_INFLATION
        ):
            token_integral = (
                TOKEN_SUPPLY_AT_TRANSITION_TO_CONSTANT_INFLATION
                * self.constant_inflation_rate**T1_DELTA
                - (INTEGRAL_START - INTEGRAL_START_WEEK_1) * self.token_inflation_rate
            )
            # TODO(mlangston) I think the following value for token_supply is
            # incorrect because the exact token supply is the sum of the
            # exponential decay value before the transition to constant
            # inflation and the value of constant inflation after the
            # transition.
            #
            # I am using TOKEN_SUPPLY_BEFORE_TRANSITION_TO_CONSTANT_INFLATION
            # for now since that is what Team fractally is advertising publicly.
            token_supply = TOKEN_SUPPLY_BEFORE_TRANSITION_TO_CONSTANT_INFLATION
        elif self.time >= TIME_AFTER_TRANSITION_TO_CONSTANT_INFLATION:
            token_integral = TOKEN_SUPPLY_AT_TRANSITION_TO_CONSTANT_INFLATION * (
                self.constant_inflation_rate**T1_DELTA
                - self.constant_inflation_rate**T0_DELTA
            )
            token_supply = TOKEN_SUPPLY_AFTER_TRANSITION_TO_CONSTANT_INFLATION
        else:
            raise RuntimeError(f"LOGIC ERROR: unexpected time={self.time}")

        object.__setattr__(
            self,
            "transition_to_constant_inflation",
            TRANSITION_TO_CONSTANT_INFLATION,
        )
        object.__setattr__(
            self,
            "token_supply_at_transition_to_constant_inflation",
            TOKEN_SUPPLY_AT_TRANSITION_TO_CONSTANT_INFLATION,
        )
        object.__setattr__(self, "integral_start", INTEGRAL_START)
        object.__setattr__(self, "integral_end", INTEGRAL_END)
        object.__setattr__(self, "integral", INTEGRAL)
        object.__setattr__(self, "token_integral", token_integral)
        object.__setattr__(
            self,
            "token_supply_before_transition_to_constant_inflation",
            TOKEN_SUPPLY_BEFORE_TRANSITION_TO_CONSTANT_INFLATION,
        )
        object.__setattr__(
            self,
            "token_supply_after_transition_to_constant_inflation",
            TOKEN_SUPPLY_AFTER_TRANSITION_TO_CONSTANT_INFLATION,
        )
        object.__setattr__(
            self,
            "token_supply",
            token_supply,
        )
