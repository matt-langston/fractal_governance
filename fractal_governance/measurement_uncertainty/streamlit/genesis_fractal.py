# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Streamlit app for the Genesis Fractal Measurement Uncertainty Dashboard"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))
import fractal_governance.dataset  # noqa: E402
import fractal_governance.measurement_uncertainty.dataset  # noqa: E402
import fractal_governance.measurement_uncertainty.plots  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402
from fractal_governance.dataset import (  # noqa: E402
    ACCUMULATED_LEVEL_COLUMN_NAME,
    ACCUMULATED_RESPECT_COLUMN_NAME,
    ATTENDANCE_COUNT_COLUMN_NAME,
    MEASUREMENT_UNCERTAINTY_COLUMN_NAME,
)
from fractal_governance.measurement_uncertainty.plots import (  # noqa: E402
    CorrelationType,
    UncertaintyType,
)

import streamlit as st  # noqa: E402


# @st.experimental_memo
def _get_dataset() -> fractal_governance.measurement_uncertainty.dataset.Dataset:
    """Return the Genesis Fractal Measurement Uncertainty Dataset"""
    return fractal_governance.dataset.Dataset.from_csv(
        Path("data/genesis-weekly_measurements.csv")
    )


# @st.experimental_memo
def get_dataset() -> fractal_governance.measurement_uncertainty.dataset.Dataset:
    """Return the Genesis Fractal Measurement Uncertainty Dataset"""
    return fractal_governance.measurement_uncertainty.dataset.Dataset.from_dataset(
        _get_dataset()
    )


# @st.experimental_memo
def get_plots() -> fractal_governance.measurement_uncertainty.plots.Plots:
    """Return the Genesis Fractal Measurement Uncertainty Plots"""
    return fractal_governance.measurement_uncertainty.plots.Plots.from_dataset(
        _get_dataset()
    )


PAGE_TITLE = "An Analysis of Fractally White Paper Addendum 1"
_DATASET = _get_dataset()
DATASET = get_dataset()
PLOTS = get_plots()
LAST_MEETING_DATE = _DATASET.last_meeting_date.strftime("%b %d, %Y")

st.set_page_config(page_title=PAGE_TITLE, page_icon="✅", layout="wide")
st.title(PAGE_TITLE)
f"Data is current up through the meeting held on {LAST_MEETING_DATE}."


st.header("Introduction")
st.markdown(
    """
The purpose of this dashboard is to provide feedback to the fractally team and the
Genesis Fractal on the proposed structural changes to the
Genesis Fractal as described in
[Fractally White Paper Addendum 1](https://hive.blog/fractally/@dan/fractally-white-paper-addendum-1).

The plots in this dashboard support the conclusions in the following brief writeup. A
walk-through of this analysis may be desired by some, and the author would gladly
oblige.
"""  # noqa: E501
)
st.header("Executive Summary")

st.markdown(
    """
The executive summary is that the dataset from the Genesis Fractal does not support the
elimination of the two lowest level contributors from a subsequent second round.
Instead, the data shows that such a reduction in the population may increase the
measurement error even with the addition of the additional measurements provided by a
subsequent second round.

The *Fractally White Paper Addendum 1* proposal is an all-or-nothing up-or-down vote by
the Level 6 contributors from an upcoming Genesis weekly consensus meeting[1]. A nay
vote is supported given the results of the analysis presented in this dashboard.

The data shows that the measurement error inherent in the Genesis Fractal's weekly
consensus meetings is dominated by systematic error and not statistical error, and
therefore cannot be reduced by the proposed changes. The data shows that the Genesis
Fractal should instead improve its measurement technique in order to improve the
quality of its measurements instead of simply adding additional "low quality"
measurements through the addition of a second consensus round with a reduced population.

One possible solution is to simply add additional rounds that are open to all members
that participated in the first round. This would broaden the exposure of all members to
one another and improve the likelihood that members with poorer measurement technique
are grouped with, and therefore trained by, members with higher quality measurement
technique. This solution would only improve the systematic error (i.e. lower it over
time). With this solution there is also no need to limit the number of additional
rounds to only two.

[1] [Interim Group Consensus Process](https://hive.blog/fractally/@dan/genesis-fractal-branding-and-interim-group-consensus-process)
"""  # noqa: E501
)

CMAP = sns.light_palette("#34A853", as_cmap=True)

st.subheader("Member Leaderboard")
"""
This is a member leaderboard that highlights members who produce the highest quality
measurements (i.e. the lowest measurement uncertainty).

The table is sorted first by the quality of the measurement (i.e. the measurement
uncertainty; a smaller value is better), then by level (descending), then by attendance
(descending) and then by member ID (ascending)."""


if st.checkbox("Include Self Measurements", value=True):
    df_member_leader_board = DATASET.get_member_leader_board(
        include_self_measurement=True
    )
else:
    df_member_leader_board = DATASET.get_member_leader_board(
        include_self_measurement=False
    )

if not st.checkbox("Show All"):
    df_member_leader_board = df_member_leader_board.head(10)

df_member_leader_board = df_member_leader_board.style.background_gradient(
    cmap=CMAP,
    subset=pd.IndexSlice[
        :,
        [
            MEASUREMENT_UNCERTAINTY_COLUMN_NAME,
            ACCUMULATED_LEVEL_COLUMN_NAME,
            ACCUMULATED_RESPECT_COLUMN_NAME,
            ATTENDANCE_COUNT_COLUMN_NAME,
        ],
    ],
)

st.table(df_member_leader_board)

st.subheader("Plots")

column1, column2 = st.columns(2)

with column1:
    st.pyplot(PLOTS.measurement_uncertainty_distribution(UncertaintyType.NominalValue))

with column2:
    st.pyplot(PLOTS.measurement_uncertainty_distribution(UncertaintyType.StdDev))


column1, column2 = st.columns(2)
correlation_type = CorrelationType.MeanLevel

with column1:
    st.pyplot(
        PLOTS.measurement_uncertainty_vs_mean_level(
            UncertaintyType.NominalValue, correlation_type
        )
    )

with column2:
    st.pyplot(
        PLOTS.measurement_uncertainty_vs_mean_level(
            UncertaintyType.StdDev, correlation_type
        )
    )

column1, column2 = st.columns(2)
correlation_type = CorrelationType.AttendanceCount

with column1:
    st.pyplot(
        PLOTS.measurement_uncertainty_vs_mean_level(
            UncertaintyType.NominalValue, correlation_type
        )
    )

with column2:
    st.pyplot(
        PLOTS.measurement_uncertainty_vs_mean_level(
            UncertaintyType.StdDev, correlation_type
        )
    )

st.pyplot(PLOTS.measurement_uncertainty)

st.header("Description")

st.markdown(
    """
The purpose of this dashboard is to provide feedback and clarification to the
fractally team and the Genesis Fractal on the following paragraph
from
[Fractally White Paper Addendum 1](https://hive.blog/fractally/@dan/fractally-white-paper-addendum-1):

> We can therefore assume that any given measurement has a wide margin of error and that
> many measurements are required in order to get a more accurate measure of community
> consensus.

This assumption requires clarification since repeated measurements only reduce
statistical error, but there are two types of measurement error that must be
characterized:

1. Statistical Error
2. Systematic Error

All measurement error is a combination of these two types of error and needs to be
characterized and quoted separately in order to judge the merits of a proposed change
to an experiment and its experimental apparatus.

Statistical error can only be reduced by adding additional measurements, while
systematic error is unchanged regardless of the number of measurements - systematic
error is inherent to the experimental apparatus.

Systematic error can only be reduced by improving the experimental apparatus, which is
part of what *Fractally White Paper Addendum 1* is proposing.

This dashboard will automatically update when new changes are pushed to its
[Github repository](https://github.com/matt-langston/fractal_governance).
"""  # noqa: E501
)

st.header("Resources")

st.markdown(
    """
Resources to learn more about fractal governance:

- [fractally White Paper](https://fractally.com)
- [Fractally White Paper Addendum 1](https://hive.blog/fractally/@dan/fractally-white-paper-addendum-1)
- [First Results from the Fractal Governance Experiments](https://hive.blog/fractally/@mattlangston/first-results-from-the-fractal-governance-experiments)
- [GitHub Repository for this Streamlit Dashboard](https://github.com/matt-langston/fractal_governance)
"""  # noqa: E501
)
