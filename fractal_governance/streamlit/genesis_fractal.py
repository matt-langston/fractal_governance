# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Streamlit app for the Genesis Fractal Dashboard"""

# builtins
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

# 3rd party dependencies

# pylint: disable=C0413

import pandas as pd
import seaborn as sns
import streamlit as st

# 2nd party dependencies
import fractal_governance.dataset
import fractal_governance.plots

from fractal_governance.dataset import ACCUMULATED_RANK_COLUMN_NAME
from fractal_governance.dataset import ACCUMULATED_RESPECT_COLUMN_NAME
from fractal_governance.dataset import ATTENDANCE_COUNT_COLUMN_NAME

# pylint: enable=C0413


# @st.experimental_memo
def get_dataset() -> fractal_governance.dataset.Dataset:
    """Return the Genesis Fractal Dataset"""
    return fractal_governance.dataset.Dataset.from_csv(
        'data/genesis-weekly_rank.csv')


# @st.experimental_memo
def get_plots() -> fractal_governance.plots.Plots:
    """Return the Genesis Fractal Dataset"""
    return fractal_governance.plots.Plots.from_dataset(get_dataset())


PAGE_TITLE = 'Genesis Fractal Dashboard'
DATASET = get_dataset()
PLOTS = get_plots()
LAST_MEETING_DATE = DATASET.last_meeting_date.strftime('%b %d, %Y')
ATTENDANCE_STATS = DATASET.attendance_stats
ATTENDANCE_CONSISTENCY_STATS = DATASET.attendance_consistency_stats

st.set_page_config(page_title=PAGE_TITLE, page_icon='✅', layout='wide')
st.title(PAGE_TITLE)
f"Data is current up through the meeting held on {LAST_MEETING_DATE}."  # pylint: disable=W0104

column1, column2 = st.columns(2)

with column1:
    st.subheader('Summary Statistics')
    # pylint: disable=C0301,W1401
    st.markdown(f"""
    |Description|Measurement|
    |:---|---:|
    |Total Respect tokens earned from all sources|{DATASET.total_respect:,}|
    |Total Respect tokens earned by members|{DATASET.total_member_respect:,}|
    |Respect tokens earned by teams|{DATASET.total_team_respect:,}|
    |Total number of unique members|{DATASET.total_unique_members:,}|
    |Average number of attendees per meeting|{ATTENDANCE_STATS.mean:.0f} $\pm$ {ATTENDANCE_STATS.standard_deviation:.0f}|
    |Average number of meetings attended by a unique member|{ATTENDANCE_CONSISTENCY_STATS.mean:.0f} $\pm$ {ATTENDANCE_CONSISTENCY_STATS.standard_deviation:.0f}|
    |Average team representation per meeting*|{DATASET.team_representation_stats.mean:.2f} $\pm$ {DATASET.team_representation_stats.standard_deviation:.2f}|
    """)

    st.caption(
        '\* The "average team representation" is the number of members in attendance that are members of a team divided by the total number of members in attendance.'
    )
    # pylint: enable=C0301,W1401

with column2:
    st.pyplot(PLOTS.accumulated_member_respect_vs_time)

CMAP = sns.light_palette("#34A853", as_cmap=True)

st.subheader('Member Leaderboard')
'The table is sorted first by rank (descending), then by attendance (descending) and then by member ID (ascending).'  #pylint: disable=C0301,W0105
df_member_leader_board = DATASET.df_member_leader_board.style.background_gradient(
    cmap=CMAP,
    subset=pd.IndexSlice[:, [
        ACCUMULATED_RANK_COLUMN_NAME, ACCUMULATED_RESPECT_COLUMN_NAME,
        ATTENDANCE_COUNT_COLUMN_NAME
    ]])
st.dataframe(df_member_leader_board)

st.subheader('Attendance')

column1, column2 = st.columns(2)

with column1:
    st.pyplot(PLOTS.attendance_vs_time)

with column2:
    st.pyplot(PLOTS.attendance_consistency_histogram)

st.header('Team Statistics')

column1, column2 = st.columns(2)
with column1:
    st.subheader('Team Leaderboard')
    df_team_leader_board = DATASET.df_team_leader_board.style.background_gradient(
        cmap=CMAP,
        subset=pd.IndexSlice[:, [
            ACCUMULATED_RESPECT_COLUMN_NAME,
        ]])
    st.dataframe(df_team_leader_board)

with column2:
    st.pyplot(PLOTS.accumulated_team_respect_vs_time)

column1, column2 = st.columns(2)

with column1:
    st.subheader('Team Representation')
    # pylint: disable=W1401
    st.markdown(f"""
    The average team representation per meeting: {DATASET.team_representation_stats.mean:.2f} $\pm$ {DATASET.team_representation_stats.standard_deviation:.2f}.

    The "average team representation" is the number of members in attendance that are members of a team divided by the total number of members in attendance.
    """)
    # pylint: enable=W1401

with column2:
    st.pyplot(PLOTS.team_representation_vs_time)

st.header('Description')

st.markdown('''
The goal of Fractal Governance is lofty: incentivize people to collaborate in the production of public goods and services that eliminates corruption and graft in the process.

The principles of Fractal Governance are described in the book [More Equal Animals](https://moreequalanimals.com) by Daniel Larimer, and the technical specifications for how to implement Fractal Governance at scale is defined in the [fractally White Paper](https://fractally.com).

This is a live dashboard that follows the first group of people to govern themselves according to these principles and technical specifications.

The word *fractal* is used throughput this dashboard and is capitalized as *Fractal* depending on the context to distinguish between the usual mathematical meaning and its specific use in governance.

The first governing body based on the specifications and principles of Fractal Governance is called [Genesis](https://gofractally.com/groups/7064857/feed). The Genesis members meet weekly to mine the inherent value of their collaboration to produce public goods and services and return that mined value, tokenized in units called *Respect*, directly back to its members through a governance process that naturally prevents corruption and graft. This incorruptibility is the defining feature of Fractal Governance.

Fractal Governance directly and consistently rewards individuals for their recent past contributions towards the creation of public goods and services that also avoids the formation of Pareto distributions due to corruption and graft found in all other known forms of governance. Gone are the days of rewarding collusion with illicit gains (such as currency) from dishonest behavior or other questionable means.

Analogous to Bitcoin's *Proof of Work* consensus algorithm which rewards people for transforming stored energy, in the form of electricity, into an incorruptible public ledger of account, a collaboration of people governed in a Fractal nature also uses a *Proof of Work* consensus algorithm to reward people for transforming stored energy, in the form of human collaboration, into public goods and services.

The fundamental difference between the two consensus algorithms is in how rewards are allocated. The Bitcoin model allocates rewards called BTC tokens to those who consume the most electricity most consistently. The Fractal model, on the other hand, allocates rewards called Respect tokens to those who contribute the most value most consistently, as judged by their peers.

The Bitcoin consensus algorithm is prone to corruption and graft because it rewards those that obtain the most consistent source of electricity by any means whatsoever, illicit or otherwise. The Fractal Governance consensus algorithm, on the other hand, prevents corruption and graft by eliminating opportunities for collusion.

The nature of how the rewards from the Bitcoin and Fractal Governance systems are recorded is similar in  that both systems use a blockchain for their public ledger of account.

This dashboard will automatically update when new changes are pushed to its [Github repository](https://github.com/matt-langston/fractal_governance).
''')

st.header('Resources')

st.markdown('''
Resources to learn more about fractal governance:

- [fractally White Paper](https://fractally.com)
- [More Equal Animals](https://moreequalanimals.com) by Daniel Larimer
- [First Results from the Fractal Governance Experiments](https://hive.blog/fractally/@mattlangston/first-results-from-the-fractal-governance-experiments)
- [GitHub Repository for this Streamlit Dashboard](https://github.com/matt-langston/fractal_governance)
- [Modeling and Simulation](https://gofractally.com/groups/7064857/topics/7623063) topic on [gofractally.com](https://gofractally.com)
''')
