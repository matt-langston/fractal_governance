# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Math functions for fractal governance data analysis"""

# builtins
from pathlib import Path

# 3rd party
import attr
import matplotlib.figure
import matplotlib.pyplot as plt
import matplotlib.ticker
import pandas as pd
import scipy.stats

# 2nd party
import fractal_governance.dataset
from fractal_governance.dataset import ACCUMULATED_RESPECT_COLUMN_NAME
from fractal_governance.dataset import ATTENDANCE_COUNT_COLUMN_NAME
from fractal_governance.dataset import MEAN_COLUMN_NAME
from fractal_governance.dataset import MEETING_DATE_COLUMN_NAME
from fractal_governance.dataset import STANDARD_DEVIATION_COLUMN_NAME
from fractal_governance.dataset import TEAM_NAME_COLUMN_NAME

DEFAULT_FIGSIZE = (10, 6)


@attr.define
class Plots:
    """A wrapper around e fractal governance plots"""
    dataset: fractal_governance.dataset.Dataset

    @property
    def attendance_vs_time(self) -> matplotlib.figure.Figure:
        """Return a plot of attendance vs time"""
        df = self.dataset.df  # pylint: disable=C0103
        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)  # pylint: disable=C0103
        group_by = df.groupby(MEETING_DATE_COLUMN_NAME).size()
        group_by.plot.bar(xlabel='Meeting Date', ylabel='Attendees')
        xaxis_labels = [
            meeting_date.strftime('%b %d %Y')
            for meeting_date in group_by.index
        ]
        ax.xaxis.set_major_formatter(
            matplotlib.ticker.FixedFormatter(xaxis_labels))
        ax.set_title('Attendance vs Time')
        plt.gcf().autofmt_xdate()
        return fig

    @property
    def attendance_consistency_histogram(self) -> matplotlib.figure.Figure:
        """Return a plot of attendance histogram"""
        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)  # pylint: disable=C0103
        self.dataset.df_member_leader_board[ATTENDANCE_COUNT_COLUMN_NAME].hist(
        )
        ax.set_title('Consistency of Attendance')
        ax.set_xlabel('Total Meetings Attended by a Unique Member')
        ax.set_ylabel('Counts')
        return fig

    @property
    def accumulated_member_respect_vs_time(self) -> matplotlib.figure.Figure:
        """Return a plot of the accumulated respect vs time"""
        df_member_respect_by_meeting_date = self.dataset.df_member_respect_by_meeting_date
        accumulated_respect = df_member_respect_by_meeting_date[
            ACCUMULATED_RESPECT_COLUMN_NAME].cumsum()
        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)  # pylint: disable=C0103
        accumulated_respect.plot.bar(xlabel='Meeting Date',
                                     ylabel='Accumulated Respect')
        xaxis_labels = [
            meeting_date.strftime('%b %d %Y')
            for meeting_date in accumulated_respect.index
        ]
        ax.xaxis.set_major_formatter(
            matplotlib.ticker.FixedFormatter(xaxis_labels))
        ax.set_title('Accumulated Member Respect vs Time')
        plt.gcf().autofmt_xdate()
        return fig

    @property
    def accumulated_team_respect_vs_time(self) -> matplotlib.figure.Figure:
        """Return a plot of the accumulated team vs time"""
        df_team_respect_by_meeting_date = self.dataset.df_team_respect_by_meeting_date
        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)  # pylint: disable=C0103
        x_axis_offset = pd.Timedelta(-0.3, unit='d')
        x_axis_width = pd.Timedelta(1, unit='d')
        for team_name, dfx in df_team_respect_by_meeting_date.groupby(
                TEAM_NAME_COLUMN_NAME):
            color = next(ax._get_lines.prop_cycler)['color']  # pylint: disable=W0212
            ax.bar(
                dfx[MEETING_DATE_COLUMN_NAME] + x_axis_offset,
                dfx[ACCUMULATED_RESPECT_COLUMN_NAME].cumsum(),
                color=color,
                width=x_axis_width,
                label=team_name,
            )
            x_axis_offset += x_axis_width
        ax.legend()
        ax.set_title('Accumulated Team Respect vs Time')
        ax.set_xlabel('Meeting Date')
        ax.set_ylabel('Accumulated Team Respect')
        plt.gcf().autofmt_xdate()
        return fig

    @property
    def team_representation_vs_time(self) -> matplotlib.figure.Figure:
        """Return a plot of the team representation vs time"""
        df_team_representation_by_date = self.dataset.df_team_representation_by_date
        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)  # pylint: disable=C0103
        df_team_representation_by_date.plot.bar(xlabel='Meeting Date',
                                                ylabel='Team Representation')
        xaxis_labels = [
            meeting_date.strftime('%b %d %Y')
            for meeting_date in df_team_representation_by_date.index
        ]
        ax.xaxis.set_major_formatter(
            matplotlib.ticker.FixedFormatter(xaxis_labels))
        ax.set_title('Team Representation vs Time')
        plt.gcf().autofmt_xdate()
        return fig

    @property
    def attendance_count_vs_rank(self) -> matplotlib.figure.Figure:
        """Plot the attendance count vs rank"""
        df_member_rank_by_attendance_count = self.dataset.df_member_rank_by_attendance_count

        x = df_member_rank_by_attendance_count[ATTENDANCE_COUNT_COLUMN_NAME]  # pylint: disable=C0103
        y = df_member_rank_by_attendance_count[MEAN_COLUMN_NAME]  # pylint: disable=C0103
        yerr = df_member_rank_by_attendance_count[
            STANDARD_DEVIATION_COLUMN_NAME]

        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)  # pylint: disable=C0103
        ax.errorbar(
            x=x,
            y=y,
            yerr=yerr,
            fmt='o',
        )
        ax.set_title('Attendance Count vs Rank')
        ax.set_xlabel('Attendance Count')
        ax.set_ylabel('Mean Rank')

        ax.set(ylim=(0, 8))

        # Perform a linear regression on this data and overlay it on the
        # plot to demonstrate how meeting attendance affects a member's
        # standing as perceived by their fractal.
        result = scipy.stats.linregress(x, y)

        x = x.to_list()  # pylint: disable=C0103
        x.insert(0, x[0] - 1)
        x.append(x[-1] + 1)
        x = pd.Series(x)  # pylint: disable=C0103

        ax.plot(x, result.slope * x + result.intercept, 'r')

        result_as_text = f"y = $x*{result.slope:.2f}_{{\pm{result.stderr:.2f}}} + {result.intercept:.2f}_{{\pm{result.intercept_stderr:.2f}}}$"  # pylint: disable=C0301,W1401
        ax.text(3, 6.8, result_as_text, fontsize=15)

        return fig

    @classmethod
    def from_dataset(cls,
                     dataset: fractal_governance.dataset.Dataset) -> 'Plots':
        """Return a Plots object for the given Dataset"""
        return cls(dataset=dataset)

    @classmethod
    def from_csv(cls, file_path: Path) -> 'Plots':
        """Return a Plots object for the given file path to the Genesis .csv dataset"""
        dataset = fractal_governance.dataset.Dataset.from_csv(file_path)
        return cls(dataset=dataset)
