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
  - [Average Attendees per Meeting](#average-attendees-per-meeting)
  - [Plot of Consistency of Attendance](#plot-of-consistency-of-attendance)
  - [Average Consistency of Attendance](#average-consistency-of-attendance)
  - [DataFrame of Member Respect Mined (or Earned) vs Time](#dataframe-of-member-respect-mined-or-earned-vs-time)
  - [Plot of Accumulated Member Respect vs Time](#plot-of-accumulated-member-respect-vs-time)
  - [Total Accumulated Member Respect](#total-accumulated-member-respect)
  - [DataFrame of Team Respect Mined (or Earned) vs Time](#dataframe-of-team-respect-mined-or-earned-vs-time)
  - [Plot of Accumulated Team Respect vs Time](#plot-of-accumulated-team-respect-vs-time)
  - [Total Accumulated Team Respect](#total-accumulated-team-respect)
  - [DataFrame of Team Leaderboard](#dataframe-of-team-leaderboard)
  - [Plot of Team Representation](#plot-of-team-representation)
  - [Average Team Representation per Meeting](#average-team-representation-per-meeting)
  - [DataFrame of Consensus Rank vs Attendance](#dataframe-of-consensus-rank-vs-attendance)
  - [DataFrame of Accumulated Consensus Rank vs Attendance](#dataframe-of-accumulated-consensus-rank-vs-attendance)
  - [Plot of Attendance Consistency vs Rank](#plot-of-attendance-consistency-vs-rank)
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
dataset = fractal_governance.dataset.Dataset.from_csv('../data/genesis-weekly_rank.csv')
```

List the attributes of this `Dataset` object to see what properties and methods we have to work with.


```python
[attribute for attribute in dir(dataset) if not attribute.startswith('__')]
```




    ['attendance_consistency_stats',
     'attendance_stats',
     'df',
     'df_member_leader_board',
     'df_member_rank_by_attendance_count',
     'df_member_respect_by_meeting_date',
     'df_member_summary_stats_by_member_id',
     'df_team_leader_board',
     'df_team_representation_by_date',
     'df_team_respect_by_meeting_date',
     'from_csv',
     'last_meeting_date',
     'team_representation_stats',
     'total_member_respect',
     'total_respect',
     'total_team_respect',
     'total_unique_members']



The curated raw data from the Genesis weekly consensus meetings is a pandas DataFrame accessed through the `df` property.

The other properties beginning with the prefix `df_` are derived DataFrames from the raw data in the `df` DataFrame.

All other properties, `total_respect` for example, are interesting values calculated from the various DataFrames.

Let's have a look at the raw data `df` DataFrame from which everything else is derived.


```python
GitHubMarkdownDataFrame(dataset.df)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Index</th>
      <th>MemberID</th>
      <th>Name</th>
      <th>MeetingID</th>
      <th>Group</th>
      <th>Rank</th>
      <th>TeamID</th>
      <th>TeamName</th>
      <th>MeetingDate</th>
      <th>Respect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>00</td>
      <td>Chace Eskimo</td>
      <td>2</td>
      <td>1</td>
      <td>4</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2022-03-05</td>
      <td>8</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>01</td>
      <td>Debraj Ghosh</td>
      <td>2</td>
      <td>2</td>
      <td>3</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2022-03-05</td>
      <td>5</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>02</td>
      <td>Nick Shock</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2022-03-05</td>
      <td>3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>03</td>
      <td>Jimmy Lee</td>
      <td>2</td>
      <td>3</td>
      <td>2</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2022-03-05</td>
      <td>3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>04</td>
      <td>Abdulsalam Ridwa</td>
      <td>2</td>
      <td>6</td>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2022-03-05</td>
      <td>2</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>354</th>
      <td>355</td>
      <td>jseymour</td>
      <td>Joshua Seymour</td>
      <td>11</td>
      <td>6</td>
      <td>5</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2022-05-14</td>
      <td>13</td>
    </tr>
    <tr>
      <th>355</th>
      <td>356</td>
      <td>jamesmart</td>
      <td>James Mart</td>
      <td>11</td>
      <td>6</td>
      <td>4</td>
      <td>1.0</td>
      <td>Team fractally</td>
      <td>2022-05-14</td>
      <td>8</td>
    </tr>
    <tr>
      <th>356</th>
      <td>357</td>
      <td>jaytaylor-node</td>
      <td>Jay Taylor</td>
      <td>11</td>
      <td>6</td>
      <td>3</td>
      <td>3.0</td>
      <td>Fractally in Orbit</td>
      <td>2022-05-14</td>
      <td>5</td>
    </tr>
    <tr>
      <th>357</th>
      <td>358</td>
      <td>douglasjames</td>
      <td>Douglas Butner</td>
      <td>11</td>
      <td>6</td>
      <td>2</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2022-05-14</td>
      <td>3</td>
    </tr>
    <tr>
      <th>358</th>
      <td>359</td>
      <td>willspatrick</td>
      <td>NaN</td>
      <td>11</td>
      <td>6</td>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2022-05-14</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
<p>359 rows × 10 columns</p>
</div>




```python
dataset.total_unique_members
```




    97



### DataFrame of Member Leaderboard

Inspect the first few rows of the member leaderboard DataFrame based on accumulated consensus Rank.


```python
GitHubMarkdownDataFrame(dataset.df_member_leader_board.head(10))
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>MemberID</th>
      <th>Name</th>
      <th>AccumulatedRank</th>
      <th>AccumulatedRespect</th>
      <th>AttendanceCount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>dansingjoy</td>
      <td>Dan Singjoy</td>
      <td>59</td>
      <td>181</td>
      <td>11</td>
    </tr>
    <tr>
      <th>2</th>
      <td>dan</td>
      <td>Daniel Larimer</td>
      <td>58</td>
      <td>194</td>
      <td>10</td>
    </tr>
    <tr>
      <th>3</th>
      <td>wildwex</td>
      <td>Gregory Wexler</td>
      <td>55</td>
      <td>178</td>
      <td>10</td>
    </tr>
    <tr>
      <th>4</th>
      <td>jseymour</td>
      <td>Joshua Seymour</td>
      <td>49</td>
      <td>130</td>
      <td>11</td>
    </tr>
    <tr>
      <th>5</th>
      <td>douglasjames</td>
      <td>Douglas Butner</td>
      <td>40</td>
      <td>111</td>
      <td>10</td>
    </tr>
    <tr>
      <th>6</th>
      <td>novacryptollc</td>
      <td>Patrick Bernard Schmid</td>
      <td>40</td>
      <td>101</td>
      <td>9</td>
    </tr>
    <tr>
      <th>7</th>
      <td>hachtu</td>
      <td>Mark Scheer</td>
      <td>39</td>
      <td>105</td>
      <td>8</td>
    </tr>
    <tr>
      <th>8</th>
      <td>jaytaylor-node</td>
      <td>Jay Taylor</td>
      <td>36</td>
      <td>72</td>
      <td>11</td>
    </tr>
    <tr>
      <th>9</th>
      <td>mikelennie</td>
      <td>Lennie Niit</td>
      <td>36</td>
      <td>86</td>
      <td>10</td>
    </tr>
    <tr>
      <th>10</th>
      <td>amih</td>
      <td>Ami Heines</td>
      <td>36</td>
      <td>82</td>
      <td>9</td>
    </tr>
  </tbody>
</table>
</div>



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
     'accumulated_team_respect_vs_time',
     'attendance_consistency_histogram',
     'attendance_count_vs_rank',
     'attendance_vs_time',
     'dataset',
     'from_csv',
     'from_dataset',
     'team_representation_vs_time']



### Plot of Attendance vs Time

Plot the attendance vs time for each weekly consensus meeting.


```python
plots.attendance_vs_time
plt.show()
```


    
![png](README_files/README_25_0.png)
    


### Average Attendees per Meeting

The average number of attendees per meeting.


```python
dataset.attendance_stats
```




    Statistics(mean=32.63636363636363, standard_deviation=9.080448527167887)



### Plot of Consistency of Attendance

Plot the consistency of attendance for the weekly consensus meetings. This is the total number of meetings attended by a unique member. The first bin counts the number of people who have only attended one weekly consensus meeting.


```python
plots.attendance_consistency_histogram
plt.show()
```


    
![png](README_files/README_31_0.png)
    


### Average Consistency of Attendance

The average number of meetings attended by a unique member.


```python
dataset.attendance_consistency_stats
```




    Statistics(mean=3.7010309278350517, standard_deviation=3.2247898783409394)



### DataFrame of Member Respect Mined (or Earned) vs Time

Inspect the DataFrame for the total amount of member Respect mined (or earned) for each weekly consensus meeting.


```python
GitHubMarkdownDataFrame(dataset.df_member_respect_by_meeting_date)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>AttendanceCount</th>
      <th>AccumulatedRespect</th>
      <th>Mean</th>
      <th>StandardDeviation</th>
    </tr>
    <tr>
      <th>MeetingDate</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2022-02-26</th>
      <td>10</td>
      <td>99</td>
      <td>3.900000</td>
      <td>1.663330</td>
    </tr>
    <tr>
      <th>2022-03-05</th>
      <td>46</td>
      <td>412</td>
      <td>3.608696</td>
      <td>1.679660</td>
    </tr>
    <tr>
      <th>2022-03-12</th>
      <td>38</td>
      <td>356</td>
      <td>3.763158</td>
      <td>1.601253</td>
    </tr>
    <tr>
      <th>2022-03-19</th>
      <td>33</td>
      <td>306</td>
      <td>3.727273</td>
      <td>1.625437</td>
    </tr>
    <tr>
      <th>2022-03-26</th>
      <td>33</td>
      <td>306</td>
      <td>3.727273</td>
      <td>1.625437</td>
    </tr>
    <tr>
      <th>2022-04-02</th>
      <td>39</td>
      <td>358</td>
      <td>3.692308</td>
      <td>1.640825</td>
    </tr>
    <tr>
      <th>2022-04-09</th>
      <td>33</td>
      <td>306</td>
      <td>3.727273</td>
      <td>1.625437</td>
    </tr>
    <tr>
      <th>2022-04-23</th>
      <td>28</td>
      <td>256</td>
      <td>3.678571</td>
      <td>1.656716</td>
    </tr>
    <tr>
      <th>2022-04-30</th>
      <td>29</td>
      <td>258</td>
      <td>3.586207</td>
      <td>1.701202</td>
    </tr>
    <tr>
      <th>2022-05-07</th>
      <td>38</td>
      <td>356</td>
      <td>3.763158</td>
      <td>1.601253</td>
    </tr>
    <tr>
      <th>2022-05-14</th>
      <td>32</td>
      <td>304</td>
      <td>3.812500</td>
      <td>1.574750</td>
    </tr>
  </tbody>
</table>
</div>



### Plot of Accumulated Member Respect vs Time

Plot the accumulated member Respect of the Genesis fractal vs time.


```python
plots.accumulated_member_respect_vs_time
plt.show()
```


    
![png](README_files/README_40_0.png)
    


### Total Accumulated Member Respect

The total accumulated member Respect integrated over all members.


```python
dataset.total_member_respect
```




    3317



### DataFrame of Team Respect Mined (or Earned) vs Time

Inspect the DataFrame for the total amount of team Respect mined (or earned) for each weekly consensus meeting.


```python
GitHubMarkdownDataFrame(dataset.df_team_respect_by_meeting_date)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TeamName</th>
      <th>MeetingDate</th>
      <th>AccumulatedRespect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>EOS Translation Foundation</td>
      <td>2022-04-23</td>
      <td>21</td>
    </tr>
    <tr>
      <th>1</th>
      <td>EOS Translation Foundation</td>
      <td>2022-04-30</td>
      <td>23</td>
    </tr>
    <tr>
      <th>2</th>
      <td>EOS Translation Foundation</td>
      <td>2022-05-07</td>
      <td>21</td>
    </tr>
    <tr>
      <th>3</th>
      <td>EOS Translation Foundation</td>
      <td>2022-05-14</td>
      <td>26</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Fractally in Orbit</td>
      <td>2022-05-14</td>
      <td>29</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Team fractally</td>
      <td>2022-03-26</td>
      <td>118</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Team fractally</td>
      <td>2022-04-02</td>
      <td>89</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Team fractally</td>
      <td>2022-04-09</td>
      <td>89</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Team fractally</td>
      <td>2022-04-23</td>
      <td>68</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Team fractally</td>
      <td>2022-04-30</td>
      <td>84</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Team fractally</td>
      <td>2022-05-07</td>
      <td>102</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Team fractally</td>
      <td>2022-05-14</td>
      <td>63</td>
    </tr>
  </tbody>
</table>
</div>



### Plot of Accumulated Team Respect vs Time

Plot the accumulated team Respect of the Genesis fractal teams vs time.


```python
plots.accumulated_team_respect_vs_time
plt.show()
```


    
![png](README_files/README_49_0.png)
    


### Total Accumulated Team Respect

The total accumulated team Respect integrated over all teams.


```python
dataset.total_team_respect
```




    733



### DataFrame of Team Leaderboard

The team leaderboard shows the the total accumulated team Respect for each team.


```python
GitHubMarkdownDataFrame(dataset.df_team_leader_board)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>AccumulatedRespect</th>
    </tr>
    <tr>
      <th>TeamName</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Team fractally</th>
      <td>613</td>
    </tr>
    <tr>
      <th>EOS Translation Foundation</th>
      <td>91</td>
    </tr>
    <tr>
      <th>Fractally in Orbit</th>
      <td>29</td>
    </tr>
  </tbody>
</table>
</div>



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




    Statistics(mean=0.2237558834087872, standard_deviation=0.06970405515216217)



### DataFrame of Consensus Rank vs Attendance

Inspect the DataFrame for the accumulated consensus Rank of contributions as discerned by the Genesis fractal for each member.


```python
GitHubMarkdownDataFrame(dataset.df_member_summary_stats_by_member_id)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>AttendanceCount</th>
      <th>AccumulatedRank</th>
      <th>AccumulatedRespect</th>
      <th>Mean</th>
      <th>StandardDeviation</th>
    </tr>
    <tr>
      <th>MemberID</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>00</th>
      <td>1</td>
      <td>4</td>
      <td>8</td>
      <td>4.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>01</th>
      <td>1</td>
      <td>3</td>
      <td>5</td>
      <td>3.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>02</th>
      <td>1</td>
      <td>2</td>
      <td>3</td>
      <td>2.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>03</th>
      <td>1</td>
      <td>2</td>
      <td>3</td>
      <td>2.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>04</th>
      <td>1</td>
      <td>1</td>
      <td>2</td>
      <td>1.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>wakeupjohnny</th>
      <td>1</td>
      <td>1</td>
      <td>2</td>
      <td>1.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>wigglesthe3r</th>
      <td>2</td>
      <td>7</td>
      <td>13</td>
      <td>3.5</td>
      <td>0.707107</td>
    </tr>
    <tr>
      <th>wildwex</th>
      <td>10</td>
      <td>55</td>
      <td>178</td>
      <td>5.5</td>
      <td>0.971825</td>
    </tr>
    <tr>
      <th>willspatrick</th>
      <td>1</td>
      <td>1</td>
      <td>2</td>
      <td>1.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>zhenek</th>
      <td>1</td>
      <td>3</td>
      <td>5</td>
      <td>3.0</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>97 rows × 5 columns</p>
</div>



### DataFrame of Accumulated Consensus Rank vs Attendance

Inspect the DataFrame for the mean accumulated consensus Rank based on meeting attendance.


```python
GitHubMarkdownDataFrame(dataset.df_member_rank_by_attendance_count)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>AttendanceCount</th>
      <th>Mean</th>
      <th>StandardDeviation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>2.674419</td>
      <td>1.357886</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>3.722222</td>
      <td>1.903729</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>3.111111</td>
      <td>1.964971</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>3.075000</td>
      <td>1.474353</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>4.450000</td>
      <td>1.468081</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>4.208333</td>
      <td>1.700542</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7</td>
      <td>2.857143</td>
      <td>1.062342</td>
    </tr>
    <tr>
      <th>7</th>
      <td>8</td>
      <td>3.600000</td>
      <td>1.481510</td>
    </tr>
    <tr>
      <th>8</th>
      <td>9</td>
      <td>3.962963</td>
      <td>1.091276</td>
    </tr>
    <tr>
      <th>9</th>
      <td>10</td>
      <td>4.233333</td>
      <td>1.640243</td>
    </tr>
    <tr>
      <th>10</th>
      <td>11</td>
      <td>4.363636</td>
      <td>1.432179</td>
    </tr>
  </tbody>
</table>
</div>



The mean accumulated consensus Rank is strongly correlated with meeting attendance.


```python
GitHubMarkdownDataFrame(dataset.df_member_rank_by_attendance_count[['AttendanceCount', 'Mean']].corr())
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>AttendanceCount</th>
      <th>Mean</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>AttendanceCount</th>
      <td>1.000000</td>
      <td>0.588231</td>
    </tr>
    <tr>
      <th>Mean</th>
      <td>0.588231</td>
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
</div>



### Plot of Attendance Consistency vs Rank

Based on this strong correlation, plot the change in Rank vs the number of meetings attended.


```python
plots.attendance_count_vs_rank
plt.show()
```


    
![png](README_files/README_72_0.png)
    


As the plot shows, on average members rank higher in subsequent weeks based on the number of past weekly consensus meetings they have participated in. Possible reasons for this phenomena include:

* Over time members learn what their fellow members value and come into alignment with those values.
* Over time members begin to imitate their higher ranked colleagues from watching how they conduct themselves.
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
find fractal_governance test -name '*.py' -print0 | xargs -0 pipenv run yapf -i
find fractal_governance test -name '*.py' -print0 | xargs -0 pipenv run pylint
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
