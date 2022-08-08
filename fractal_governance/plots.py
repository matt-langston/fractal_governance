# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Plots for fractal governance data analysis"""

import attr
import matplotlib.figure
import matplotlib.pyplot as plt
import matplotlib.ticker
import pandas as pd
import scipy.stats

import fractal_governance.dataset
import fractal_governance.util
from fractal_governance.util import (
    ACCUMULATED_RESPECT_COLUMN_NAME,
    ACCUMULATED_RESPECT_NEW_MEMBER_COLUMN_NAME,
    ACCUMULATED_RESPECT_RETURNING_MEMBER_COLUMN_NAME,
    ATTENDANCE_COUNT_COLUMN_NAME,
    LEVEL_COLUMN_NAME,
    MEAN_COLUMN_NAME,
    MEETING_DATE_COLUMN_NAME,
    NEW_MEMBER_COUNT_COLUMN_NAME,
    RETURNING_MEMBER_COUNT_COLUMN_NAME,
    STANDARD_DEVIATION_COLUMN_NAME,
    TEAM_NAME_COLUMN_NAME,
)

DEFAULT_FIGSIZE = (10, 6)


@attr.frozen
class Plots:
    """A wrapper around fractal governance plots"""

    dataset: fractal_governance.dataset.Dataset

    @property
    def attendance_vs_time(self) -> matplotlib.figure.Figure:
        """Return a plot of attendance vs time"""
        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
        df = self.dataset.df
        # The (MEETING_DATE_COLUMN_NAME, MEMBER_ID_COLUMN_NAME) tuple is generate after
        # the addition of multiple rounds, which is the reason for the `notna` on
        # LEVEL_COLUMN_NAME.
        df = df[df[LEVEL_COLUMN_NAME].notna()]
        group_by = df.groupby(MEETING_DATE_COLUMN_NAME).size()
        group_by.plot.bar(xlabel="Meeting Date", ylabel="Attendees")
        xaxis_labels = [
            meeting_date.strftime("%b %d %Y") for meeting_date in group_by.index
        ]
        ax.xaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(xaxis_labels))
        ax.set_title("Attendance vs Time")
        ylim = ax.get_ylim()
        ylim = tuple(left * right for left, right in zip((1, 1.3), ylim))
        ax.set_ylim(ylim)
        plt.gcf().autofmt_xdate()
        return fig

    @property
    def attendance_vs_time_stacked(self) -> matplotlib.figure.Figure:
        """Return a stacked plot of attendance vs time"""
        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
        df = self.dataset.df_member_attendance_new_and_returning_by_meeting
        df = df.set_index(MEETING_DATE_COLUMN_NAME)
        df = df[[NEW_MEMBER_COUNT_COLUMN_NAME, RETURNING_MEMBER_COUNT_COLUMN_NAME]]
        df = df[df.columns[::-1]]
        df.plot.bar(ax=ax, stacked=True)
        ax.set_xlabel("Meeting Date")
        ax.set_ylabel("Attendees")
        ax.set_title("Attendance vs Time")
        xaxis_labels = [meeting_date.strftime("%b %d %Y") for meeting_date in df.index]
        ax.xaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(xaxis_labels))
        ax.legend(["Returning Members", "New Members"])
        ylim = ax.get_ylim()
        ylim = tuple(left * right for left, right in zip((1, 1.3), ylim))
        ax.set_ylim(ylim)
        plt.gcf().autofmt_xdate()
        return fig

    @property
    def attendance_consistency_histogram(self) -> matplotlib.figure.Figure:
        """Return a plot of attendance histogram"""
        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
        df = self.dataset.df_member_leader_board
        df[ATTENDANCE_COUNT_COLUMN_NAME].hist(bins=self.dataset.total_meetings)
        ax.set_title("Consistency of Attendance")
        ax.set_xlabel("Total Meetings Attended by a Unique Member")
        ax.set_ylabel("Counts")
        return fig

    @property
    def accumulated_member_respect_vs_time(self) -> matplotlib.figure.Figure:
        """Return a plot of the accumulated member Respect vs time"""
        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
        df = self.dataset.df_member_respect_new_and_returning_by_meeting.set_index(
            MEETING_DATE_COLUMN_NAME
        )
        accumulated_respect = df[ACCUMULATED_RESPECT_COLUMN_NAME].cumsum()
        accumulated_respect.plot.bar(
            xlabel="Meeting Date", ylabel="Accumulated Respect"
        )
        xaxis_labels = [
            meeting_date.strftime("%b %d %Y")
            for meeting_date in accumulated_respect.index
        ]
        ax.xaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(xaxis_labels))
        ax.set_title("Accumulated Member Respect vs Time")
        plt.gcf().autofmt_xdate()
        return fig

    @property
    def accumulated_member_respect_vs_time_stacked(self) -> matplotlib.figure.Figure:
        """Return a stacked plot of accumulated member Respect vs time"""
        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
        df = self.dataset.df_member_respect_new_and_returning_by_meeting
        df = df.set_index(MEETING_DATE_COLUMN_NAME)
        df = df[
            [
                ACCUMULATED_RESPECT_RETURNING_MEMBER_COLUMN_NAME,
                ACCUMULATED_RESPECT_NEW_MEMBER_COLUMN_NAME,
            ]
        ]
        df[ACCUMULATED_RESPECT_RETURNING_MEMBER_COLUMN_NAME] = df[
            ACCUMULATED_RESPECT_RETURNING_MEMBER_COLUMN_NAME
        ].cumsum()
        df[ACCUMULATED_RESPECT_NEW_MEMBER_COLUMN_NAME] = df[
            ACCUMULATED_RESPECT_NEW_MEMBER_COLUMN_NAME
        ].cumsum()
        df.plot.bar(ax=ax, stacked=True)
        ax.set_xlabel("Meeting Date")
        ax.set_ylabel("Accumulated Member Respect")
        xaxis_labels = [meeting_date.strftime("%b %d %Y") for meeting_date in df.index]
        ax.xaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(xaxis_labels))
        ax.set_title("Accumulated Member Respect vs Time")
        ax.legend(["Returning Members", "New Members"])
        plt.gcf().autofmt_xdate()
        return fig

    @property
    def accumulated_team_respect_vs_time(self) -> matplotlib.figure.Figure:
        """Return a plot of the accumulated team Respect vs time"""
        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
        df = self.dataset.df_team_respect_by_meeting_date
        x_axis_offset = pd.Timedelta(-0.3, unit="d")
        x_axis_width = pd.Timedelta(1, unit="d")
        for team_name, dfx in df.groupby(TEAM_NAME_COLUMN_NAME):
            color = next(ax._get_lines.prop_cycler)["color"]
            ax.bar(
                dfx[MEETING_DATE_COLUMN_NAME] + x_axis_offset,
                dfx[ACCUMULATED_RESPECT_COLUMN_NAME].cumsum(),
                color=color,
                width=x_axis_width,
                label=team_name,
            )
            x_axis_offset += x_axis_width
        ax.legend()
        ax.set_title("Accumulated Team Respect vs Time")
        ax.set_xlabel("Meeting Date")
        ax.set_ylabel("Accumulated Team Respect")
        plt.gcf().autofmt_xdate()
        return fig

    @property
    def accumulated_team_respect_vs_time_stacked(self) -> matplotlib.figure.Figure:
        """Return a stacked plot of the accumulated team Respect vs time"""
        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
        df = self.dataset.df_team_respect_by_meeting_date.set_index(
            MEETING_DATE_COLUMN_NAME
        )
        df = df.pivot(columns=TEAM_NAME_COLUMN_NAME)
        df = df[
            pd.MultiIndex.from_product(
                [
                    [ACCUMULATED_RESPECT_COLUMN_NAME],
                    self.dataset.df_team_leader_board.index,
                ]
            )
        ]
        df.plot.bar(ax=ax, stacked=True)
        ax.set_xlabel("Meeting Date")
        ax.set_ylabel("Accumulated Team Respect")
        ax.set_title("Accumulated Team Respect vs Time")
        xaxis_labels = [meeting_date.strftime("%b %d %Y") for meeting_date in df.index]
        ax.xaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(xaxis_labels))
        ax.legend(self.dataset.df_team_leader_board.index)
        ylim = ax.get_ylim()
        ylim = tuple(left * right for left, right in zip((1, 1.3), ylim))
        ax.set_ylim(ylim)
        plt.gcf().autofmt_xdate()
        return fig

    @property
    def team_representation_vs_time(self) -> matplotlib.figure.Figure:
        """Return a plot of the team representation vs time"""
        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
        df = self.dataset.df_team_representation_by_date
        df.plot.bar(xlabel="Meeting Date", ylabel="Team Representation")
        xaxis_labels = [meeting_date.strftime("%b %d %Y") for meeting_date in df.index]
        ax.xaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(xaxis_labels))
        ax.set_title("Team Representation vs Time")
        plt.gcf().autofmt_xdate()
        return fig

    @property
    def attendance_count_vs_level(self) -> matplotlib.figure.Figure:
        """Plot the attendance count vs level"""
        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
        df = self.dataset.df_member_level_by_attendance_count
        x = df[ATTENDANCE_COUNT_COLUMN_NAME]
        y = df[MEAN_COLUMN_NAME]
        yerr = df[STANDARD_DEVIATION_COLUMN_NAME]
        ax.errorbar(
            x=x,
            y=y,
            yerr=yerr,
            fmt="o",
        )
        ax.set_title("Attendance Count vs Level")
        ax.set_xlabel("Attendance Count")
        ax.set_ylabel("Mean Level")

        ax.set(ylim=(0, 8))

        # Perform a linear regression on this data and overlay it on the
        # plot to demonstrate how meeting attendance affects a member's
        # standing as perceived by their fractal.
        result = scipy.stats.linregress(x, y)

        x = x.to_list()
        x.insert(0, x[0] - 1)
        x.append(x[-1] + 1)
        x = pd.Series(x)

        ax.plot(x, result.slope * x + result.intercept, "r")

        result_as_text = f"y = $x*{result.slope:.2f}_{{\pm{result.stderr:.2f}}} + {result.intercept:.2f}_{{\pm{result.intercept_stderr:.2f}}}$"  # noqa: E501, W605
        ax.text(3, 6.8, result_as_text, fontsize=15)

        return fig

    @classmethod
    def from_dataset(cls, dataset: fractal_governance.dataset.Dataset) -> "Plots":
        """Return a Plots object for the given Dataset"""
        return cls(dataset=dataset)

    @classmethod
    def from_csv(
        cls,
        fractal_dataset_csv_paths: fractal_governance.util.FractalDatasetCSVPaths = fractal_governance.util.FractalDatasetCSVPaths(),  # noqa: E501
    ) -> "Plots":
        """Return a Plots object for the given Fractal's .csv file paths"""
        dataset = fractal_governance.dataset.Dataset.from_csv(fractal_dataset_csv_paths)
        return cls(dataset=dataset)
