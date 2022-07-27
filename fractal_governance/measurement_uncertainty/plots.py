# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Plots for fractal governance data measurement uncertainties"""

from enum import Enum, auto

import attrs
import fractal_governance.dataset
import fractal_governance.util
import matplotlib.figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats
import uncertainties
from fractal_governance.measurement_uncertainty.dataset import (
    MEASUREMENT_UNCERTAINTY_COLUMN_NAME,
    Dataset,
    UncertaintyType,
)
from fractal_governance.plots import DEFAULT_FIGSIZE
from fractal_governance.util import ATTENDANCE_COUNT_COLUMN_NAME, MEAN_COLUMN_NAME


class CorrelationType(Enum):
    MeanLevel = auto()
    AttendanceCount = auto()


@attrs.frozen
class Plots:
    """A wrapper around e fractal governance measurement uncertainty data"""

    measurement_uncertainty_dataset: Dataset
    dataset: fractal_governance.dataset.Dataset

    @property
    def measurement_uncertainty(self) -> matplotlib.figure.Figure:
        """Return a plot of the measurement uncertainty for every unique member"""
        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
        alpha = 0.5

        for include_self_measurement in (False, True):
            if include_self_measurement:
                df = self.measurement_uncertainty_dataset.df_with_self_measurements
            else:
                df = self.measurement_uncertainty_dataset.df_without_self_measurements
            color = next(ax._get_lines.prop_cycler)["color"]
            ax.errorbar(
                x=np.arange(len(df)),
                y=uncertainties.unumpy.nominal_values(
                    df[MEASUREMENT_UNCERTAINTY_COLUMN_NAME]
                ),
                yerr=uncertainties.unumpy.std_devs(
                    df[MEASUREMENT_UNCERTAINTY_COLUMN_NAME]
                ),
                fmt="o",
                alpha=alpha,
                color=color,
                label=f"Include Self Measurement: {include_self_measurement}",
            )

        ax.legend(loc="upper left")
        ax.set_title("Member Level Measurement Uncertainty vs Unique Member")
        ax.set_ylabel("Member Level Measurement Uncertainty")
        ax.set_xlabel("Unique Member")

        return fig

    def measurement_uncertainty_distribution(
        self, uncertainty_type: UncertaintyType
    ) -> matplotlib.figure.Figure:
        """Return a plot of the measurement uncertainty distribution for the given
        UncertaintyType"""
        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)

        alpha = 0.5
        bins = 30

        for include_self_measurement in (False, True):
            if include_self_measurement:
                df = self.measurement_uncertainty_dataset.df_with_self_measurements
            else:
                df = self.measurement_uncertainty_dataset.df_without_self_measurements

            if uncertainty_type == UncertaintyType.NominalValue:
                data = uncertainties.unumpy.nominal_values(
                    df[MEASUREMENT_UNCERTAINTY_COLUMN_NAME]
                )
                uncertainty_name = "Accuracy"
            elif uncertainty_type == UncertaintyType.StdDev:
                data = uncertainties.unumpy.std_devs(
                    df[MEASUREMENT_UNCERTAINTY_COLUMN_NAME]
                )
                uncertainty_name = "Precision"
            else:
                raise RuntimeError(f"LOGIC ERROR: Unknown enum {uncertainty_type}")
            color = next(ax._get_lines.prop_cycler)["color"]
            n, bins, patches = ax.hist(
                x=data,
                bins=bins,
                density=True,
                alpha=alpha,
                color=color,
            )

            mean, std = scipy.stats.norm.fit(data)
            bin_centers = bins[:-1] + (bins[:-1] - bins[1:]) / 2  # type: ignore
            expected = scipy.stats.norm.pdf(bin_centers, mean, std)
            residuals = n - expected
            chi2 = np.sum(residuals**2 / expected)
            dof = len(n) - 1
            chi2_per_dof = chi2 / dof

            label = f"Include Self Measurement: {include_self_measurement}"
            label += f", $(\\mu, \\sigma) = ({mean:.2f}, {std:.2f})$"
            label += f", $\\chi^2({dof}) = {chi2_per_dof:.2f}$"
            patches.set_label(label)

            ax.plot(
                bin_centers,
                scipy.stats.norm.pdf(bin_centers, mean, std),
                alpha=alpha,
                color=color,
            )

        ylim = ax.get_ylim()
        ylim = tuple(left * right for left, right in zip((1, 1.3), ylim))
        ax.set_ylim(ylim)

        text = "The two curves are a best fit of\n"
        text += "the data to a normal distribution\n"
        text += "with these parameters."
        bbox = dict(boxstyle="round", facecolor="white", alpha=0.5)
        ax.text(
            0.6,
            0.75,
            text,
            transform=ax.transAxes,
            fontsize=12,
            verticalalignment="top",
            bbox=bbox,
        )
        ax.annotate(
            "",
            xy=(0.73, 0.84),
            xytext=(0.73, 0.77),
            xycoords=ax.transAxes,
            arrowprops=dict(arrowstyle="->"),
        )

        xlabel = f"{uncertainty_name} of Level Measurement"
        ax.legend(loc="upper right")
        ax.set_title(f"Distribution of {xlabel}")
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Counts")

        return fig

    def measurement_uncertainty_correlation(
        self, uncertainty_type: UncertaintyType, correlation_type: CorrelationType
    ) -> matplotlib.figure.Figure:
        """Return a plot of the measurement uncertainty vs mean_level for the given
        UncertaintyType and CorrelationType"""
        fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
        alpha = 0.5

        if uncertainty_type == UncertaintyType.NominalValue:
            unumpy_func = uncertainties.unumpy.nominal_values
            uncertainty_name = "Accuracy"
        elif uncertainty_type == UncertaintyType.StdDev:
            unumpy_func = uncertainties.unumpy.std_devs
            uncertainty_name = "Precision"
        else:
            raise RuntimeError(f"LOGIC ERROR: Unknown enum {uncertainty_type}")

        if correlation_type == CorrelationType.MeanLevel:
            column_name = MEAN_COLUMN_NAME
            xlabel = "Mean Level"
        elif correlation_type == CorrelationType.AttendanceCount:
            column_name = ATTENDANCE_COUNT_COLUMN_NAME
            xlabel = "Attendance Count"
        else:
            raise RuntimeError(f"LOGIC ERROR: Unknown enum {correlation_type}")

        for include_self_measurement in (False, True):
            if include_self_measurement:
                df = self.measurement_uncertainty_dataset.df_with_self_measurements
            else:
                df = self.measurement_uncertainty_dataset.df_without_self_measurements

            dataset = self.measurement_uncertainty_dataset.dataset
            df = dataset.df_member_summary_stats_by_member_id.join(df)

            x = list()
            xerr = list()
            y = list()
            yerr = list()
            cut_start = 0.5
            cut_stop = df[column_name].max() + 1
            cut_step = 1
            for interval, dfx in df.groupby(
                pd.cut(
                    df[column_name],
                    np.arange(start=cut_start, stop=cut_stop, step=cut_step),
                )
            ):
                x_mean = dfx[column_name].mean()
                x_std_dev = dfx[column_name].std()
                data = unumpy_func(dfx[MEASUREMENT_UNCERTAINTY_COLUMN_NAME])
                if data.size == 0:
                    continue
                y_mean = np.mean(data)
                y_std_dev = np.std(data)
                x.append(x_mean)
                xerr.append(x_std_dev)
                y.append(y_mean)
                yerr.append(y_std_dev)

            color = next(ax._get_lines.prop_cycler)["color"]
            corrcoef = np.corrcoef(
                df[column_name],
                unumpy_func(df[MEASUREMENT_UNCERTAINTY_COLUMN_NAME]),
            )
            correlation_coefficient = corrcoef[0, 1]
            label = f"Correlation Coefficient: {correlation_coefficient:.2f}"
            label += f", Include Self Measurement: {include_self_measurement}"
            ax.errorbar(
                x=x,
                xerr=xerr,
                y=y,
                yerr=yerr,
                fmt="o",
                alpha=alpha,
                color=color,
                label=label,
            )

        ax.legend(loc="upper right")
        ylabel = f"{uncertainty_name} of Level Measurement"
        ax.set_title(f"{ylabel} vs {xlabel}")
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)

        return fig

    @classmethod
    def from_dataset(cls, dataset: fractal_governance.dataset.Dataset) -> "Plots":
        """Return a Plots object for the given Dataset"""
        measurement_uncertainty_dataset = Dataset.from_dataset(dataset=dataset)
        return cls(
            measurement_uncertainty_dataset=measurement_uncertainty_dataset,
            dataset=dataset,
        )

    @classmethod
    def from_csv(
        cls,
        fractal_dataset_csv_paths: fractal_governance.util.FractalDatasetCSVPaths = fractal_governance.util.FractalDatasetCSVPaths(),  # noqa: E501
    ) -> "Plots":
        """Return a Plots object for the given Fractal's .csv file paths"""
        dataset = fractal_governance.dataset.Dataset.from_csv(fractal_dataset_csv_paths)
        return cls.from_dataset(dataset=dataset)
