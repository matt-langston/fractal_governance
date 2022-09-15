# Fractal Governance

## Table of Contents
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Introduction](#introduction)
- [What is Fractal Governance?](#what-is-fractal-governance)
- [Getting Started for Data Scientists](#getting-started-for-data-scientists)
  - [Step 1 (one time setup):](#step-1-one-time-setup)
  - [Step 2 (one time setup):](#step-2-one-time-setup)
  - [Step 3 (optional):](#step-3-optional)
  - [Step 4 (optional):](#step-4-optional)
  - [Step 5:](#step-5)
- [Example Analysis of the Genesis Fractal](#example-analysis-of-the-genesis-fractal)
  - [Setup](#setup)
  - [A Dataset of Multiple pandas DataFrames](#a-dataset-of-multiple-pandas-dataframes)
  - [DataFrame of Member Leaderboard](#dataframe-of-member-leaderboard)
  - [A Plots Object of Multiple Visualizations](#a-plots-object-of-multiple-visualizations)
  - [Plot of Attendance vs Time](#plot-of-attendance-vs-time)
  - [DataFrame of New and Returning Member Attendance vs Time](#dataframe-of-new-and-returning-member-attendance-vs-time)
  - [Average Attendees per Meeting](#average-attendees-per-meeting)
  - [Plot of Consistency of Attendance](#plot-of-consistency-of-attendance)
  - [Average Consistency of Attendance](#average-consistency-of-attendance)
  - [DataFrame of New and Returning Member Respect Mined (or Earned) vs Time](#dataframe-of-new-and-returning-member-respect-mined-or-earned-vs-time)
  - [Plot of Accumulated New and Returning Member Respect vs Time](#plot-of-accumulated-new-and-returning-member-respect-vs-time)
  - [Total Accumulated Member Respect](#total-accumulated-member-respect)
  - [Plot of Accumulated Team Respect vs Time](#plot-of-accumulated-team-respect-vs-time)
  - [Total Accumulated Team Respect](#total-accumulated-team-respect)
  - [DataFrame of Team Leaderboard](#dataframe-of-team-leaderboard)
  - [Plot of Team Representation](#plot-of-team-representation)
  - [Average Team Representation per Meeting](#average-team-representation-per-meeting)
  - [DataFrame of Accumulated Level vs Attendance](#dataframe-of-accumulated-level-vs-attendance)
  - [Plot of Attendance Consistency vs Level](#plot-of-attendance-consistency-vs-level)
- [Getting Started for Software Engineers](#getting-started-for-software-engineers)
  - [Step 1 (one time setup):](#step-1-one-time-setup-1)
  - [Step 2 (one time setup):](#step-2-one-time-setup-1)
  - [Step 3 (one time setup):](#step-3-one-time-setup)
  - [Step 4 (one time setup; optional):](#step-4-one-time-setup-optional)
  - [Step 5:](#step-5-1)
  - [Step 6:](#step-6)
- [Notes for Contributors](#notes-for-contributors)
  - [Python Dependencies](#python-dependencies)
  - [Format and Lint Python Source Code](#format-and-lint-python-source-code)
  - [Format and Lint Bazel Source Files](#format-and-lint-bazel-source-files)
  - [Updating README.md](#updating-readmemd)
    - [Step 1 (one time setup):](#step-1-one-time-setup-2)
    - [Step 2:](#step-2)
- [Resources](#resources)
- [License](#license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Introduction

[Datasets](data), [Jupyter notebooks](notebook/README.ipynb) and [Streamlit dashboards](https://share.streamlit.io/matt-langston/fractal_governance/main/fractal_governance/streamlit/genesis_fractal.py) for Fractal Governance

The motivation for this repository is to advance the understanding of Fractal Governance. The [datasets](data) from our [experimental apparatus](https://gofractally.com) will be of particular interest to data scientists, researchers and educators.

## What is Fractal Governance?

The goal of Fractal Governance is lofty: incentivize people to collaborate in the production of public goods and services that also eliminates corruption and graft in the process.

The principles of Fractal Governance are described in the book [More Equal Animals](https://moreequalanimals.com) by Daniel Larimer, and the technical specifications for how to implement Fractal Governance at scale is defined in the [fractally White Paper](https://fractally.com). This article presents an analysis of the initial results of the first group of people to govern themselves according to these principles and technical specifications.

These pioneers call their group [Genesis](https://gofractally.com/groups/7064857/feed) and refer to it as a Fractal. The Genesis members meet weekly to mine the inherent value of their collaboration to produce public goods and services and return that mined value, tokenized in units called *Respect*, directly back to its members through a governance process that naturally prevents corruption and graft. This incorruptibility is the defining feature of Fractal Governance.

Fractal Governance directly and consistently rewards individuals for their recent past contributions towards the creation of public goods and services that also avoids the formation of Pareto distributions due to corruption and graft found in all other known forms of governance. Gone are the days of rewarding collusion with illicit gains (such as currency) from dishonest behavior or other questionable means.

Analogous to Bitcoin's *Proof of Work* consensus algorithm which rewards people for transforming stored energy, in the form of electricity, into an incorruptible public ledger of account, a collaboration of people governed in a Fractal nature also uses a *Proof of Work* consensus algorithm to reward people for transforming stored energy, in the form of human collaboration, into public goods and services.

The fundamental difference between the two consensus algorithms is in how rewards are allocated. The Bitcoin model allocates rewards called BTC tokens to those who consume the most electricity most consistently. The Fractal model, on the other hand, allocates rewards called Respect tokens to those who contribute the most value most consistently, as judged by their peers.

The Bitcoin consensus algorithm is prone to corruption and graft because it rewards those that obtain the most consistent source of electricity by any means whatsoever, illicit or otherwise. The Fractal Governance consensus algorithm, on the other hand, prevents corruption and graft by eliminating opportunities for collusion.

The nature of how the rewards from the Bitcoin and Fractal Governance systems are recorded is similar in  that both systems use a blockchain for their public ledger of account.

You can [immediately explore the Genesis Fractal dataset](https://share.streamlit.io/matt-langston/fractal_governance/main/fractal_governance/streamlit/genesis_fractal.py) before returning here to continue your exploration. The dataset for this dashboard is curated by [Gregory Wexler](https://gofractally.com/members/10362727), [Joshua Seymour](https://gofractally.com/members/10361546) and [Matt Langston](https://gofractally.com/members/10426315).

## Getting Started for Data Scientists

I use my M1 MacBook with [MacPorts](https://www.macports.org) for the steps labeled **one time setup**.

### Step 1 (one time setup):

Install [python 3.9](https://docs.python.org/3.9/) and [pipenv](https://pipenv.pypa.io/en/latest/). I do this using MacPorts.

```bash
sudo port install python39
sudo port select --set python3 python39
sudo port select --set python python39
sudo port install pipenv
```

### Step 2 (one time setup):

Use pipenv to install the python dependencies. Run this command from the top-level directory of this git repository.

```bash
pipenv install --dev
```

### Step 3 (optional):

Run the Streamlit app. This will run the same dashboard as [Genesis Fractal dataset](https://share.streamlit.io/matt-langston/fractal_governance/main/fractal_governance/streamlit/genesis_fractal.py).

```bash
pipenv run streamlit run fractal_governance/streamlit/genesis_fractal.py
open http://localhost:8501
```

### Step 4 (optional):

Explore the Jupyter notebooks:

```bash
pipenv run jupyter lab
```

### Step 5:

Start exploring our datasets, models and simulations. What follows is an example analysis of the Genesis fractal's dataset to inspire your own explorations.

## Example Analysis of the Genesis Fractal

### Setup


```python
# 3rd party dependencies
import matplotlib.pyplot as plt

# 2nd party dependencies
import fractal_governance.addendum_1.dataset
import fractal_governance.dataset
import fractal_governance.plots

from fractal_governance.util import GitHubMarkdownDataFrame
```

### A Dataset of Multiple pandas DataFrames

Read the Genesis fractal's dataset into a `Dataset` object consisting of multiple convenient pandas DataFrames.


```python
dataset = fractal_governance.dataset.Dataset.from_csv()
```

Uodate the *Respect* values using Addendum 1 algorithm changes. See the *Resources* section below for links that describe these changes.


```python
dataset = fractal_governance.addendum_1.dataset.Addendum1Dataset(dataset=dataset).dataset_with_addendum_1_respect
```

List the attributes of this `Dataset` object to see what properties and methods we have to work with.


```python
[attribute for attribute in dir(dataset) if not attribute.startswith('__')]
```




    ['_get_new_member_filter_for_meeting_id',
     'attendance_consistency_stats',
     'attendance_stats',
     'df',
     'df_member_attendance_new_and_returning_by_meeting',
     'df_member_leader_board',
     'df_member_level_by_attendance_count',
     'df_member_respect_new_and_returning_by_meeting',
     'df_member_summary_stats_by_member_id',
     'df_team_leader_board',
     'df_team_representation_by_date',
     'df_team_respect_by_meeting_date',
     'from_csv',
     'get_new_member_dataframe_for_meeting_id',
     'get_returning_member_dataframe_for_meeting_id',
     'last_meeting_date',
     'team_representation_stats',
     'total_meetings',
     'total_member_respect',
     'total_respect',
     'total_team_respect',
     'total_unique_members']



The curated raw data from the Genesis weekly consensus meetings is a pandas DataFrame accessed through the `df` property.

The other properties beginning with the prefix `df_` are derived DataFrames from the raw data in the `df` DataFrame.

All other properties, `total_respect` for example, are interesting values calculated from the various DataFrames.


```python
dataset.total_meetings
```




    28




```python
dataset.total_unique_members
```




    136



### DataFrame of Member Leaderboard

Inspect the first few rows of the member leaderboard DataFrame based on accumulated level.


```python
GitHubMarkdownDataFrame(dataset.df_member_leader_board.head(10))
```




<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>MemberID</th>
      <th>Name</th>
      <th>AccumulatedRespect</th>
      <th>AttendanceCount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>dan</td>
      <td>Daniel Larimer</td>
      <td>984783.848669</td>
      <td>27</td>
    </tr>
    <tr>
      <td>wildwex</td>
      <td>Gregory Wexler</td>
      <td>794631.002385</td>
      <td>27</td>
    </tr>
    <tr>
      <td>dansingjoy</td>
      <td>Dan Singjoy</td>
      <td>635687.752838</td>
      <td>27</td>
    </tr>
    <tr>
      <td>thomashallgren</td>
      <td>Thomas Hallgren</td>
      <td>607544.610526</td>
      <td>21</td>
    </tr>
    <tr>
      <td>fractallymike</td>
      <td>Mike Manfredi</td>
      <td>606909.474106</td>
      <td>21</td>
    </tr>
    <tr>
      <td>jseymour</td>
      <td>Joshua Seymour</td>
      <td>573716.817344</td>
      <td>28</td>
    </tr>
    <tr>
      <td>hachtu</td>
      <td>Mark Scheer</td>
      <td>555661.944079</td>
      <td>24</td>
    </tr>
    <tr>
      <td>dphillippi</td>
      <td>Duane Phillippi</td>
      <td>550704.201048</td>
      <td>27</td>
    </tr>
    <tr>
      <td>val</td>
      <td>Valentine Zavgorodnev</td>
      <td>538247.654919</td>
      <td>22</td>
    </tr>
    <tr>
      <td>mattlangston</td>
      <td>Matt Langston</td>
      <td>523957.806240</td>
      <td>24</td>
    </tr>
  </tbody>
</table>



### A Plots Object of Multiple Visualizations

Create a `Plots` object that contains interesting visualizations used throughput the remainder of our example analysis.


```python
plots = fractal_governance.plots.Plots.from_dataset(dataset)
```

List the attributes of this `Plots` object to see what properties and methods we have to work with.


```python
[attribute for attribute in dir(plots) if not attribute.startswith('__')]
```




    ['accumulated_member_respect_vs_time',
     'accumulated_member_respect_vs_time_stacked',
     'accumulated_team_respect_vs_time',
     'accumulated_team_respect_vs_time_stacked',
     'attendance_consistency_histogram',
     'attendance_count_vs_level',
     'attendance_vs_time',
     'attendance_vs_time_stacked',
     'dataset',
     'from_csv',
     'from_dataset',
     'team_representation_vs_time']



### Plot of Attendance vs Time

Plot the attendance vs time for each weekly consensus meeting.

The plot demonstrates that a relatively steady state has been reached where a core group of dedicated members is mixed with a steady stream of new participants as interest in Fractal Governance grows.


```python
plots.attendance_vs_time_stacked
plt.show()
```


    
![png](README_files/README_27_0.png)
    


### DataFrame of New and Returning Member Attendance vs Time

Inspect the DataFrame of the attendance counts of new members vs returning members for each of the last 12 weekly consensus meeting.


```python
GitHubMarkdownDataFrame(dataset.df_member_attendance_new_and_returning_by_meeting.iloc[::-1].head(12))
```




<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>MeetingDate</th>
      <th>MeetingID</th>
      <th>NewMemberCount</th>
      <th>ReturningMemberCount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2022-09-10</td>
      <td>28</td>
      <td>2</td>
      <td>37</td>
    </tr>
    <tr>
      <td>2022-09-03</td>
      <td>27</td>
      <td>5</td>
      <td>41</td>
    </tr>
    <tr>
      <td>2022-08-27</td>
      <td>26</td>
      <td>5</td>
      <td>38</td>
    </tr>
    <tr>
      <td>2022-08-20</td>
      <td>25</td>
      <td>0</td>
      <td>41</td>
    </tr>
    <tr>
      <td>2022-08-13</td>
      <td>24</td>
      <td>2</td>
      <td>42</td>
    </tr>
    <tr>
      <td>2022-08-06</td>
      <td>23</td>
      <td>2</td>
      <td>42</td>
    </tr>
    <tr>
      <td>2022-07-30</td>
      <td>22</td>
      <td>4</td>
      <td>39</td>
    </tr>
    <tr>
      <td>2022-07-23</td>
      <td>21</td>
      <td>2</td>
      <td>41</td>
    </tr>
    <tr>
      <td>2022-07-16</td>
      <td>20</td>
      <td>1</td>
      <td>35</td>
    </tr>
    <tr>
      <td>2022-07-09</td>
      <td>19</td>
      <td>2</td>
      <td>31</td>
    </tr>
    <tr>
      <td>2022-07-02</td>
      <td>18</td>
      <td>1</td>
      <td>39</td>
    </tr>
    <tr>
      <td>2022-06-25</td>
      <td>17</td>
      <td>1</td>
      <td>35</td>
    </tr>
  </tbody>
</table>



### Average Attendees per Meeting

The average number of attendees per meeting.


```python
dataset.attendance_stats
```




    Statistics(mean=36.79, standard_deviation=7.21)



### Plot of Consistency of Attendance

Plot the consistency of attendance for the weekly consensus meetings. This is the total number of meetings attended by a unique member. The first bin counts the number of people who have only attended one weekly consensus meeting.


```python
plots.attendance_consistency_histogram
plt.show()
```


    
![png](README_files/README_36_0.png)
    


### Average Consistency of Attendance

The average number of meetings attended by a unique member.


```python
dataset.attendance_consistency_stats
```




    Statistics(mean=7.57, standard_deviation=8.64)



### DataFrame of New and Returning Member Respect Mined (or Earned) vs Time

Inspect the DataFrame for the total amount of member Respect mined (or earned) for each of the last 12 weekly consensus meeting.


```python
GitHubMarkdownDataFrame(dataset.df_member_respect_new_and_returning_by_meeting.iloc[::-1].head(12))
```




<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>MeetingDate</th>
      <th>MeetingID</th>
      <th>AccumulatedRespect</th>
      <th>AccumulatedRespectNewMember</th>
      <th>AccumulatedRespectReturningMember</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2022-09-10</td>
      <td>28</td>
      <td>331087.985631</td>
      <td>1297.809655</td>
      <td>329790.175975</td>
    </tr>
    <tr>
      <td>2022-09-03</td>
      <td>27</td>
      <td>351683.032709</td>
      <td>7266.088716</td>
      <td>344416.943994</td>
    </tr>
    <tr>
      <td>2022-08-27</td>
      <td>26</td>
      <td>347607.172179</td>
      <td>6452.137571</td>
      <td>341155.034607</td>
    </tr>
    <tr>
      <td>2022-08-20</td>
      <td>25</td>
      <td>364235.820930</td>
      <td>0.000000</td>
      <td>364235.820930</td>
    </tr>
    <tr>
      <td>2022-08-13</td>
      <td>24</td>
      <td>376071.223308</td>
      <td>3786.062061</td>
      <td>372285.161247</td>
    </tr>
    <tr>
      <td>2022-08-06</td>
      <td>23</td>
      <td>392525.714095</td>
      <td>3977.719665</td>
      <td>388547.994430</td>
    </tr>
    <tr>
      <td>2022-07-30</td>
      <td>22</td>
      <td>761178.037318</td>
      <td>36337.644998</td>
      <td>724840.392320</td>
    </tr>
    <tr>
      <td>2022-07-23</td>
      <td>21</td>
      <td>776478.098369</td>
      <td>13387.553420</td>
      <td>763090.544949</td>
    </tr>
    <tr>
      <td>2022-07-16</td>
      <td>20</td>
      <td>673202.686271</td>
      <td>5737.522894</td>
      <td>667465.163377</td>
    </tr>
    <tr>
      <td>2022-07-09</td>
      <td>19</td>
      <td>575664.797067</td>
      <td>21037.583946</td>
      <td>554627.213121</td>
    </tr>
    <tr>
      <td>2022-07-02</td>
      <td>18</td>
      <td>673202.686271</td>
      <td>0.000000</td>
      <td>673202.686271</td>
    </tr>
    <tr>
      <td>2022-06-25</td>
      <td>17</td>
      <td>592877.365750</td>
      <td>0.000000</td>
      <td>592877.365750</td>
    </tr>
  </tbody>
</table>



### Plot of Accumulated New and Returning Member Respect vs Time

Plot the accumulated member Respect of the Genesis fractal vs time.


```python
plots.accumulated_member_respect_vs_time_stacked
plt.show()
```


    
![png](README_files/README_45_0.png)
    


### Total Accumulated Member Respect

The total accumulated member Respect integrated over all members.


```python
dataset.total_member_respect
```




    16031912.943715755



### Plot of Accumulated Team Respect vs Time

Plot the accumulated team Respect of the Genesis fractal teams vs time.


```python
plots.accumulated_team_respect_vs_time_stacked
plt.show()
```


    
![png](README_files/README_51_0.png)
    


### Total Accumulated Team Respect

The total accumulated team Respect integrated over all teams.


```python
dataset.total_team_respect
```




    7192295.102534071



### DataFrame of Team Leaderboard

The team leaderboard shows the the total accumulated team Respect for each team.


```python
GitHubMarkdownDataFrame(dataset.df_team_leader_board)
```




<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>AccumulatedRespect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>4.045049e+06</td>
    </tr>
    <tr>
      <td>1.639993e+06</td>
    </tr>
    <tr>
      <td>6.633697e+05</td>
    </tr>
    <tr>
      <td>4.798799e+05</td>
    </tr>
    <tr>
      <td>3.640037e+05</td>
    </tr>
  </tbody>
</table>



### Plot of Team Representation

Plot the fraction of members representing teams over time.


```python
plots.team_representation_vs_time
plt.show()
```


    
![png](README_files/README_60_0.png)
    


### Average Team Representation per Meeting

The average team representation per meeting. This is the number of members in attendance that are members of a team divided by the total number of members in attendance.


```python
dataset.team_representation_stats
```




    Statistics(mean=0.39, standard_deviation=0.12)



### DataFrame of Accumulated Level vs Attendance

Inspect the DataFrame for the mean accumulated level based on meeting attendance.


```python
GitHubMarkdownDataFrame(dataset.df_member_level_by_attendance_count)
```




<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>AttendanceCount</th>
      <th>Mean</th>
      <th>StandardDeviation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>2.366667</td>
      <td>1.248276</td>
    </tr>
    <tr>
      <td>2</td>
      <td>3.625000</td>
      <td>1.500000</td>
    </tr>
    <tr>
      <td>3</td>
      <td>2.041667</td>
      <td>1.488482</td>
    </tr>
    <tr>
      <td>4</td>
      <td>3.000000</td>
      <td>1.460593</td>
    </tr>
    <tr>
      <td>5</td>
      <td>3.200000</td>
      <td>1.619328</td>
    </tr>
    <tr>
      <td>6</td>
      <td>3.250000</td>
      <td>1.847442</td>
    </tr>
    <tr>
      <td>7</td>
      <td>2.285714</td>
      <td>0.487950</td>
    </tr>
    <tr>
      <td>8</td>
      <td>3.187500</td>
      <td>1.327592</td>
    </tr>
    <tr>
      <td>9</td>
      <td>3.472222</td>
      <td>1.715244</td>
    </tr>
    <tr>
      <td>10</td>
      <td>2.100000</td>
      <td>0.994429</td>
    </tr>
    <tr>
      <td>11</td>
      <td>2.600000</td>
      <td>1.241266</td>
    </tr>
    <tr>
      <td>12</td>
      <td>3.250000</td>
      <td>1.544786</td>
    </tr>
    <tr>
      <td>13</td>
      <td>3.153846</td>
      <td>1.519109</td>
    </tr>
    <tr>
      <td>14</td>
      <td>3.666667</td>
      <td>1.281513</td>
    </tr>
    <tr>
      <td>15</td>
      <td>3.700000</td>
      <td>1.512021</td>
    </tr>
    <tr>
      <td>16</td>
      <td>5.437500</td>
      <td>1.209339</td>
    </tr>
    <tr>
      <td>17</td>
      <td>3.635294</td>
      <td>1.895151</td>
    </tr>
    <tr>
      <td>18</td>
      <td>3.472222</td>
      <td>1.715244</td>
    </tr>
    <tr>
      <td>19</td>
      <td>2.710526</td>
      <td>1.183396</td>
    </tr>
    <tr>
      <td>21</td>
      <td>4.630952</td>
      <td>1.761569</td>
    </tr>
    <tr>
      <td>22</td>
      <td>3.795455</td>
      <td>1.935946</td>
    </tr>
    <tr>
      <td>23</td>
      <td>3.565217</td>
      <td>1.424425</td>
    </tr>
    <tr>
      <td>24</td>
      <td>4.100000</td>
      <td>1.716945</td>
    </tr>
    <tr>
      <td>27</td>
      <td>4.907407</td>
      <td>1.567550</td>
    </tr>
    <tr>
      <td>28</td>
      <td>4.750000</td>
      <td>1.734722</td>
    </tr>
  </tbody>
</table>



The mean accumulated level is strongly correlated with meeting attendance.


```python
GitHubMarkdownDataFrame(dataset.df_member_level_by_attendance_count[['AttendanceCount', 'Mean']].corr())
```




<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>AttendanceCount</th>
      <th>Mean</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1.000000</td>
      <td>0.668931</td>
    </tr>
    <tr>
      <td>0.668931</td>
      <td>1.000000</td>
    </tr>
  </tbody>
</table>



### Plot of Attendance Consistency vs Level

Based on this strong correlation, plot the change in level vs the number of meetings attended.


```python
plots.attendance_count_vs_level
plt.show()
```


    
![png](README_files/README_71_0.png)
    


As the plot shows, on average a member's level trends higher in subsequent weeks based on the number of past weekly consensus meetings they have participated in. Possible reasons for this phenomena include:

* Over time members learn what their fellow members value and come into alignment with those values.
* Over time members begin to imitate their higher level colleagues from watching how they conduct themselves.
* There is a self-selection process going on. This is an interesting idea for further analysis.

## Getting Started for Software Engineers

I use my M1 MacBook for software engineering, and the following steps reflect that architecture.

### Step 1 (one time setup):

Install [bazel](https://bazel.build) on your `PATH`. I do this using [bazelisk](https://github.com/bazelbuild/bazelisk). 

```bash
curl -LJO https://github.com/bazelbuild/bazelisk/releases/download/v1.11.0/bazelisk-darwin-arm64
chmod a+x bazelisk-darwin-arm64
ln -s bazelisk-darwin-arm64 bazel
```

### Step 2 (one time setup):

Install [buildifier](https://github.com/bazelbuild/buildtools/blob/master/buildifier/README.md) on your `PATH`.

You need `buildifier` for linting and formatting the bazel files [WORKSPACE](WORKSPACE) and [BUILD](BUILD) if you change them. 

```bash
curl -LJO https://github.com/bazelbuild/buildtools/releases/download/5.1.0/buildifier-darwin-arm64
chmod a+x buildifier-darwin-arm64
ln -s buildifier-darwin-arm64 buildifier
```

### Step 3 (one time setup):

Install [Xcode from the App Store](https://apps.apple.com/us/app/xcode/id497799835?mt=12).


### Step 4 (one time setup; optional):

I needed to create the following symlink on my M1 MacBook.

```base
pushd /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/
sudo ln -s MacOSX.sdk MacOSX12.1.sdk
popd
```

This symlink was required to work around this error during `bazel test //...`.

> Compiling with an SDK that doesn't seem to exist: /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX12.1.sdk
> Please check your Xcode installation

### Step 5:

Clone this repo and build all targets.

```bash
bazel build //...
```

### Step 6:

Run all unit tests.

```bash
bazel test //...
```

## Notes for Contributors

You are encouraged to collaborate and contribute to this project. Please ask questions and share your insights and discoveries in the [Modeling and Simulation](https://gofractally.com/groups/7064857/topics/7623063) topic of [gofractally.com](https://gofractally.com).

Please perform the following procedures before opening a pull request for this project. These manual procedures are temporary and will eventually be incorporated into bazel targets and enforced through CI.

### Python Dependencies

The source of truth for this project's python dependencies is the [Pipfile](Pipfile) file. The following three files are derived from this Pipfile file and must be regenerated after changing it:

1. [Pipfile.lock](Pipfile.lock)
2. [requirements.txt](requirements.txt)
3. [requirements-dev.txt](requirements-dev.txt)

This project's bazel repository, defined in [WORKSPACE](WORKSPACE), depends on [requirements.txt](requirements.txt) to define the python dependencies for bazel targets throughout this project.

The [Streamlit app](fractal_governance/streamlit/genesis_fractal.py) also depends on [requirements.txt](requirements.txt) to define its runtime python dependencies.

Developer tools, like `jupyterlab` code formatters and linters, depend on [requirements-dev.txt](requirements-dev.txt) to define its runtime python dependencies.

The following procedure is how I update these three derived files after changing the [Pipfile](Pipfile) file. You will need `pipenv` for this step, so if you don't have this development tool installed then you may want to follow the steps labeled **one time setup** in [Getting Started for Data Scientists](#getting-started-for-data-scientists).

```
pipenv install --dev
pipenv lock -r > requirements.txt
pipenv lock --dev -r > requirements-dev.txt
```

Check that the [README.ipynb](notebook/README.ipynb) notebook and [Streamlit app](fractal_governance/streamlit/genesis_fractal.py) still run by following the procedure in [Getting Started for Data Scientists](#getting-started-for-data-scientists), and that the unit tests still pass by following the procedure in [Getting Started for Software Engineers](#getting-started-for-software-engineers).

### Format and Lint Python Source Code

Please use the following procedure to format and lint the python source code after making any changes.

```bash
find fractal_governance test -name '*.py' -print0 | xargs -0 pipenv run black
find fractal_governance test -name '*.py' -print0 | xargs -0 pipenv run flake8
```

### Format and Lint Bazel Source Files

Please use the following procedure to format and lint the bazel source files.

```bash
find . -type f -name "BUILD" -or -name "WORKSPACE" -print0 | xargs -0 buildifier -lint fix
```

### Updating README.md

The source of truth for this project's [README.md](README.md) file is the [README.ipynb](notebook/README.ipynb) notebook. The following procedure is how I update the [README.md](README.md) file after changing the [README.ipynb](notebook/README.ipynb) notebook.

#### Step 1 (one time setup):
```bash
pipenv run nodeenv -p
pipenv run npm install -g doctoc
```

#### Step 2:
```bash
rm -rf README_files
pipenv run jupyter nbconvert --to markdown notebook/README.ipynb --output-dir .
pipenv run doctoc README.md
```

## Resources

Resources to learn more about Fractal Governance:

- [fractally White Paper](https://fractally.com)
- [Fractally White Paper Addendum 1](https://hive.blog/fractally/@dan/fractally-white-paper-addendum-1)
- [Refinement of Token Distribution Math](https://hive.blog/fractally/@dan/refinement-of-token-distribution-math)
- [More Equal Animals](https://moreequalanimals.com) by Daniel Larimer
- [Genesis Uncertainty Observatory](https://share.streamlit.io/matt-langston/fractal_governance/main/fractal_governance/measurement_uncertainty/streamlit/genesis_fractal.py)
- [Genesis Fractal Dashboard](https://share.streamlit.io/matt-langston/fractal_governance/main/fractal_governance/streamlit/genesis_fractal.py)
- [A Model-Independent Method to Measure Uncertainties in Fractal Governance Consensus Algorithms](https://hive.blog/fractally/@mattlangston/a-model-independent-method-to-measure-uncertainties-in-fractal-governance-consensus-algorithms)
- [On Simulating Fractal Governance](https://hive.blog/fractally/@mattlangston/on-simulating-fractal-governance)
- [First Results from the Fractal Governance Experiments](https://hive.blog/fractally/@mattlangston/first-results-from-the-fractal-governance-experiments)
- [Modeling and Simulation](https://gofractally.com/groups/7064857/topics/7623063) topic on [gofractally.com](https://gofractally.com)

If you contribute new Jupyter notebooks then please place them in the [notebook](notebook) directory.

## License

This project is licensed under the terms of the MIT license as defined in the [LICENSE](LICENSE) file.
