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
import fractal_governance.dataset
import fractal_governance.plots

from fractal_governance.util import GitHubMarkdownDataFrame
```

### A Dataset of Multiple pandas DataFrames

Read the Genesis fractal's dataset into a `Dataset` object consisting of multiple convenient pandas DataFrames.


```python
dataset = fractal_governance.dataset.Dataset.from_csv('../data/genesis-weekly_measurements.csv')
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




    17




```python
dataset.total_unique_members
```




    112



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
      <th>AccumulatedLevel</th>
      <th>AccumulatedRespect</th>
      <th>AttendanceCount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>dan</td>
      <td>Daniel Larimer</td>
      <td>90</td>
      <td>302</td>
      <td>16</td>
    </tr>
    <tr>
      <td>dansingjoy</td>
      <td>Dan Singjoy</td>
      <td>86</td>
      <td>252</td>
      <td>17</td>
    </tr>
    <tr>
      <td>wildwex</td>
      <td>Gregory Wexler</td>
      <td>83</td>
      <td>251</td>
      <td>16</td>
    </tr>
    <tr>
      <td>jseymour</td>
      <td>Joshua Seymour</td>
      <td>76</td>
      <td>205</td>
      <td>17</td>
    </tr>
    <tr>
      <td>hachtu</td>
      <td>Mark Scheer</td>
      <td>70</td>
      <td>202</td>
      <td>14</td>
    </tr>
    <tr>
      <td>novacryptollc</td>
      <td>Patrick Bernard Schmid</td>
      <td>64</td>
      <td>158</td>
      <td>15</td>
    </tr>
    <tr>
      <td>pnc</td>
      <td>Pascal Ngu Cho</td>
      <td>63</td>
      <td>136</td>
      <td>16</td>
    </tr>
    <tr>
      <td>dphillippi</td>
      <td>Duane Phillippi</td>
      <td>62</td>
      <td>148</td>
      <td>16</td>
    </tr>
    <tr>
      <td>mattlangston</td>
      <td>Matt Langston</td>
      <td>62</td>
      <td>154</td>
      <td>15</td>
    </tr>
    <tr>
      <td>lionflash</td>
      <td>Felix Ruiz</td>
      <td>57</td>
      <td>125</td>
      <td>16</td>
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


    
![png](README_files/README_25_0.png)
    


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
      <td>2022-06-25</td>
      <td>17</td>
      <td>1</td>
      <td>35</td>
    </tr>
    <tr>
      <td>2022-06-18</td>
      <td>16</td>
      <td>5</td>
      <td>37</td>
    </tr>
    <tr>
      <td>2022-06-11</td>
      <td>15</td>
      <td>1</td>
      <td>34</td>
    </tr>
    <tr>
      <td>2022-06-04</td>
      <td>14</td>
      <td>4</td>
      <td>32</td>
    </tr>
    <tr>
      <td>2022-05-28</td>
      <td>13</td>
      <td>2</td>
      <td>33</td>
    </tr>
    <tr>
      <td>2022-05-21</td>
      <td>12</td>
      <td>3</td>
      <td>32</td>
    </tr>
    <tr>
      <td>2022-05-14</td>
      <td>11</td>
      <td>4</td>
      <td>28</td>
    </tr>
    <tr>
      <td>2022-05-07</td>
      <td>10</td>
      <td>5</td>
      <td>33</td>
    </tr>
    <tr>
      <td>2022-04-30</td>
      <td>9</td>
      <td>1</td>
      <td>28</td>
    </tr>
    <tr>
      <td>2022-04-23</td>
      <td>8</td>
      <td>0</td>
      <td>28</td>
    </tr>
    <tr>
      <td>2022-04-09</td>
      <td>7</td>
      <td>4</td>
      <td>29</td>
    </tr>
    <tr>
      <td>2022-04-02</td>
      <td>6</td>
      <td>9</td>
      <td>30</td>
    </tr>
  </tbody>
</table>



### Average Attendees per Meeting

The average number of attendees per meeting.


```python
dataset.attendance_stats
```




    Statistics(mean=34.00, standard_deviation=7.58)



### Plot of Consistency of Attendance

Plot the consistency of attendance for the weekly consensus meetings. This is the total number of meetings attended by a unique member. The first bin counts the number of people who have only attended one weekly consensus meeting.


```python
plots.attendance_consistency_histogram
plt.show()
```


    
![png](README_files/README_34_0.png)
    


### Average Consistency of Attendance

The average number of meetings attended by a unique member.


```python
dataset.attendance_consistency_stats
```




    Statistics(mean=5.16, standard_deviation=5.23)



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
      <td>2022-06-25</td>
      <td>17</td>
      <td>312</td>
      <td>2</td>
      <td>310</td>
    </tr>
    <tr>
      <td>2022-06-18</td>
      <td>16</td>
      <td>364</td>
      <td>11</td>
      <td>353</td>
    </tr>
    <tr>
      <td>2022-06-11</td>
      <td>15</td>
      <td>310</td>
      <td>3</td>
      <td>307</td>
    </tr>
    <tr>
      <td>2022-06-04</td>
      <td>14</td>
      <td>312</td>
      <td>12</td>
      <td>300</td>
    </tr>
    <tr>
      <td>2022-05-28</td>
      <td>13</td>
      <td>310</td>
      <td>5</td>
      <td>305</td>
    </tr>
    <tr>
      <td>2022-05-21</td>
      <td>12</td>
      <td>310</td>
      <td>10</td>
      <td>300</td>
    </tr>
    <tr>
      <td>2022-05-14</td>
      <td>11</td>
      <td>304</td>
      <td>12</td>
      <td>292</td>
    </tr>
    <tr>
      <td>2022-05-07</td>
      <td>10</td>
      <td>356</td>
      <td>45</td>
      <td>311</td>
    </tr>
    <tr>
      <td>2022-04-30</td>
      <td>9</td>
      <td>258</td>
      <td>2</td>
      <td>256</td>
    </tr>
    <tr>
      <td>2022-04-23</td>
      <td>8</td>
      <td>256</td>
      <td>0</td>
      <td>256</td>
    </tr>
    <tr>
      <td>2022-04-09</td>
      <td>7</td>
      <td>306</td>
      <td>14</td>
      <td>292</td>
    </tr>
    <tr>
      <td>2022-04-02</td>
      <td>6</td>
      <td>358</td>
      <td>44</td>
      <td>314</td>
    </tr>
  </tbody>
</table>



### Plot of Accumulated New and Returning Member Respect vs Time

Plot the accumulated member Respect of the Genesis fractal vs time.


```python
plots.accumulated_member_respect_vs_time_stacked
plt.show()
```


    
![png](README_files/README_43_0.png)
    


### Total Accumulated Member Respect

The total accumulated member Respect integrated over all members.


```python
dataset.total_member_respect
```




    5235



### Plot of Accumulated Team Respect vs Time

Plot the accumulated team Respect of the Genesis fractal teams vs time.


```python
plots.accumulated_team_respect_vs_time_stacked
plt.show()
```


    
![png](README_files/README_49_0.png)
    


### Total Accumulated Team Respect

The total accumulated team Respect integrated over all teams.


```python
dataset.total_team_respect
```




    1797



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
      <td>1140</td>
    </tr>
    <tr>
      <td>432</td>
    </tr>
    <tr>
      <td>146</td>
    </tr>
    <tr>
      <td>79</td>
    </tr>
  </tbody>
</table>



### Plot of Team Representation

Plot the fraction of members representing teams over time.


```python
plots.team_representation_vs_time
plt.show()
```


    
![png](README_files/README_58_0.png)
    


### Average Team Representation per Meeting

The average team representation per meeting. This is the number of members in attendance that are members of a team divided by the total number of members in attendance.


```python
dataset.team_representation_stats
```




    Statistics(mean=0.33, standard_deviation=0.12)



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
      <td>2.346939</td>
      <td>1.283729</td>
    </tr>
    <tr>
      <td>2</td>
      <td>3.200000</td>
      <td>1.823819</td>
    </tr>
    <tr>
      <td>3</td>
      <td>1.333333</td>
      <td>0.500000</td>
    </tr>
    <tr>
      <td>4</td>
      <td>3.625000</td>
      <td>1.468880</td>
    </tr>
    <tr>
      <td>5</td>
      <td>3.100000</td>
      <td>1.370320</td>
    </tr>
    <tr>
      <td>6</td>
      <td>3.333333</td>
      <td>1.734396</td>
    </tr>
    <tr>
      <td>7</td>
      <td>3.095238</td>
      <td>1.513432</td>
    </tr>
    <tr>
      <td>8</td>
      <td>2.708333</td>
      <td>1.197068</td>
    </tr>
    <tr>
      <td>9</td>
      <td>3.805556</td>
      <td>1.369451</td>
    </tr>
    <tr>
      <td>10</td>
      <td>5.200000</td>
      <td>1.186127</td>
    </tr>
    <tr>
      <td>11</td>
      <td>3.242424</td>
      <td>1.871335</td>
    </tr>
    <tr>
      <td>12</td>
      <td>3.750000</td>
      <td>1.380993</td>
    </tr>
    <tr>
      <td>13</td>
      <td>3.307692</td>
      <td>1.489504</td>
    </tr>
    <tr>
      <td>14</td>
      <td>4.357143</td>
      <td>1.725930</td>
    </tr>
    <tr>
      <td>15</td>
      <td>4.200000</td>
      <td>1.214851</td>
    </tr>
    <tr>
      <td>16</td>
      <td>4.177083</td>
      <td>1.542348</td>
    </tr>
    <tr>
      <td>17</td>
      <td>4.215686</td>
      <td>1.500849</td>
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
      <td>0.667038</td>
    </tr>
    <tr>
      <td>0.667038</td>
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


    
![png](README_files/README_69_0.png)
    


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
- [More Equal Animals](https://moreequalanimals.com) by Daniel Larimer
- [First Results from the Fractal Governance Experiments](https://hive.blog/fractally/@mattlangston/first-results-from-the-fractal-governance-experiments)
- [Genesis Fractal Dashboard](https://share.streamlit.io/matt-langston/fractal_governance/main/fractal_governance/streamlit/genesis_fractal.py)
- [Modeling and Simulation](https://gofractally.com/groups/7064857/topics/7623063) topic on [gofractally.com](https://gofractally.com)

If you contribute new Jupyter notebooks then please place them in the [notebook](notebook) directory.

## License

This project is licensed under the terms of the MIT license as defined in the [LICENSE](LICENSE) file.
