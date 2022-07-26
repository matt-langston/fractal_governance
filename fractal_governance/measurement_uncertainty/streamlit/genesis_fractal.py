# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Streamlit app for the Genesis Uncertainty Observatory"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))
import fractal_governance.dataset  # noqa: E402
import fractal_governance.measurement_uncertainty.dataset  # noqa: E402
import fractal_governance.measurement_uncertainty.plots  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402
from fractal_governance.dataset import (  # noqa: E402
    ACCUMULATED_LEVEL_COLUMN_NAME,
    ATTENDANCE_COUNT_COLUMN_NAME,
    MEMBER_ID_COLUMN_NAME,
)
from fractal_governance.measurement_uncertainty.dataset import (  # noqa: E402
    ACCURACY_COLUMN_NAME,
    PRECISION_COLUMN_NAME,
)
from fractal_governance.measurement_uncertainty.plots import (  # noqa: E402
    CorrelationType,
    UncertaintyType,
)

import streamlit as st  # noqa: E402


# @st.experimental_memo
def _get_dataset() -> fractal_governance.measurement_uncertainty.dataset.Dataset:
    """Return the Genesis Fractal Measurement Uncertainty Dataset"""
    return fractal_governance.dataset.Dataset.from_csv()


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


PAGE_TITLE = "Genesis Uncertainty Observatory"
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
This Genesis Uncertainty Observatory is a surveillance tool to track the *accuracy*
and *precision* of the Genesis Fractal's consensus algorithm over time.

This accompanying article motivates the creation of this dashboard:
[A Model-Independent Method to Measure Uncertainties in Fractal Governance Consensus Algorithms](https://hive.blog/fractally/@mattlangston/a-model-independent-method-to-measure-uncertainties-in-fractal-governance-consensus-algorithms)

"""  # noqa: E501
)

CMAP = sns.light_palette("#34A853", as_cmap=True)

st.subheader("Member Leaderboard")
"""
This member leaderboard highlights Genesis members who contribute the highest quality
measurements to the Genesis Fractal's consensus algorithm.

The table is sorted first by Accuracy and Precision in ascending order (smaller values
are better and the order is selected in the sidebar), then by Level (descending), then
by Attendance (descending) and finally by member ID (ascending)."""

with st.sidebar:
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

    sort_column = st.radio(
        "Sort By",
        (UncertaintyType.NominalValue, UncertaintyType.StdDev),
        index=1,
        format_func=lambda uncertainty_type: ACCURACY_COLUMN_NAME
        if uncertainty_type == UncertaintyType.NominalValue
        else PRECISION_COLUMN_NAME,
    )

sort_columns = [ACCURACY_COLUMN_NAME, PRECISION_COLUMN_NAME]
if sort_column == UncertaintyType.StdDev:
    sort_columns.reverse()

sort_columns += [
    ACCUMULATED_LEVEL_COLUMN_NAME,
    ATTENDANCE_COUNT_COLUMN_NAME,
    MEMBER_ID_COLUMN_NAME,
]

df_member_leader_board = df_member_leader_board.sort_values(
    by=sort_columns,
    key=lambda series: abs(series)
    if np.issubdtype(series.dtype, np.number)
    else series,
    ascending=[True, True, False, False, True],
)

df_member_leader_board = df_member_leader_board.style.background_gradient(
    cmap=CMAP,
    subset=pd.IndexSlice[
        :,
        [
            ACCURACY_COLUMN_NAME,
            PRECISION_COLUMN_NAME,
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
        PLOTS.measurement_uncertainty_correlation(
            UncertaintyType.NominalValue, correlation_type
        )
    )

with column2:
    st.pyplot(
        PLOTS.measurement_uncertainty_correlation(
            UncertaintyType.StdDev, correlation_type
        )
    )

column1, column2 = st.columns(2)
correlation_type = CorrelationType.AttendanceCount

with column1:
    st.pyplot(
        PLOTS.measurement_uncertainty_correlation(
            UncertaintyType.NominalValue, correlation_type
        )
    )

with column2:
    st.pyplot(
        PLOTS.measurement_uncertainty_correlation(
            UncertaintyType.StdDev, correlation_type
        )
    )

st.pyplot(PLOTS.measurement_uncertainty)

st.header("Resources")

st.markdown(
    """
- [A Model-Independent Method to Measure Uncertainties in Fractal Governance Consensus Algorithms](https://hive.blog/fractally/@mattlangston/a-model-independent-method-to-measure-uncertainties-in-fractal-governance-consensus-algorithms)
- [fractally White Paper](https://fractally.com)
- [Fractally White Paper Addendum 1](https://hive.blog/fractally/@dan/fractally-white-paper-addendum-1)
- [Genesis Fractal Dashboard](https://share.streamlit.io/matt-langston/fractal_governance/main/fractal_governance/streamlit/genesis_fractal.py)
- [GitHub Repository](https://github.com/matt-langston/fractal_governance) with the Genesis Fractal Dataset and this Streamlit app
- [First Results from the Fractal Governance Experiments](https://hive.blog/fractally/@mattlangston/first-results-from-the-fractal-governance-experiments)
- [On Simulating Fractal Governance](https://hive.blog/fractally/@mattlangston/on-simulating-fractal-governance)
- [Modeling and Simulation](https://gofractally.com/groups/7064857/topics/7623063) topic on gofractally.com

"""  # noqa: E501
)
