# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Measurement uncertainties for fractal governance data analysis"""

from enum import Enum, auto
from typing import Dict, List, Set

import attrs
import fractal_governance.dataset
import fractal_governance.util
import numpy as np
import pandas as pd
import uncertainties
import uncertainties.unumpy
from fractal_governance.constants import (
    ACCUMULATED_LEVEL_COLUMN_NAME,
    ACCUMULATED_RESPECT_COLUMN_NAME,
    ATTENDANCE_COUNT_COLUMN_NAME,
    GROUP_COLUMN_NAME,
    LEVEL_COLUMN_NAME,
    MEETING_ID_COLUMN_NAME,
    MEMBER_ID_COLUMN_NAME,
    MEMBER_NAME_COLUMN_NAME,
)

ACCURACY_COLUMN_NAME = "Accuracy"
MEASUREMENT_UNCERTAINTY_COLUMN_NAME = "MeasurementUncertainty"
PRECISION_COLUMN_NAME = "Precision"


class UncertaintyType(Enum):
    NominalValue = auto()
    StdDev = auto()


@attrs.frozen
class Dataset:
    """A wrapper around fractal governance measurement uncertainty data"""

    dataset: fractal_governance.dataset.Dataset
    df_with_self_measurements: pd.DataFrame
    df_without_self_measurements: pd.DataFrame
    _df_member_leader_board_true: pd.DataFrame = attrs.field(default=None, init=False)
    _df_member_leader_board_false: pd.DataFrame = attrs.field(default=None, init=False)

    def get_member_leader_board(
        self, *, include_self_measurement: bool
    ) -> pd.DataFrame:
        """Return the member leaderboard consisting of those who make the highest
        quality measurements of the given UncertaintyType"""

        if include_self_measurement:
            if self._df_member_leader_board_true is not None:
                return self._df_member_leader_board_true
            df = self.df_with_self_measurements
        else:
            if self._df_member_leader_board_false is not None:
                return self._df_member_leader_board_false
            df = self.df_without_self_measurements

        df = df.join(
            self.dataset.df_member_leader_board.set_index(MEMBER_ID_COLUMN_NAME)
        )

        df[ACCURACY_COLUMN_NAME] = uncertainties.unumpy.nominal_values(
            df[MEASUREMENT_UNCERTAINTY_COLUMN_NAME]
        )

        df[PRECISION_COLUMN_NAME] = uncertainties.unumpy.std_devs(
            df[MEASUREMENT_UNCERTAINTY_COLUMN_NAME]
        )

        df = df.sort_values(
            by=[
                PRECISION_COLUMN_NAME,
                ACCUMULATED_LEVEL_COLUMN_NAME,
                ATTENDANCE_COUNT_COLUMN_NAME,
                MEMBER_ID_COLUMN_NAME,
            ],
            key=lambda series: abs(series)
            if np.issubdtype(series.dtype, np.number)
            else series,
            ascending=[True, False, False, True],
        ).reset_index()
        df.index += 1

        column_names = [
            MEMBER_ID_COLUMN_NAME,
            MEMBER_NAME_COLUMN_NAME,
            ACCURACY_COLUMN_NAME,
            PRECISION_COLUMN_NAME,
            ACCUMULATED_LEVEL_COLUMN_NAME,
            ACCUMULATED_RESPECT_COLUMN_NAME,
            ATTENDANCE_COUNT_COLUMN_NAME,
        ]
        df = df[column_names]

        if include_self_measurement:
            object.__setattr__(self, "_df_member_leader_board_true", df)
        else:
            object.__setattr__(self, "_df_member_leader_board_false", df)

        return df

    @classmethod
    def from_dataset(cls, dataset: fractal_governance.dataset.Dataset) -> "Dataset":
        """Return a measurement uncertainty dataset object for the given fractal
        governance dataset"""
        df = dataset.df
        df_with_self_measurements = create_measurement_uncertainty_dataframe(
            df=df, include_self_measurements=True
        )
        df_without_self_measurements = create_measurement_uncertainty_dataframe(
            df=df, include_self_measurements=False
        )
        return cls(
            dataset=dataset,
            df_with_self_measurements=df_with_self_measurements,
            df_without_self_measurements=df_without_self_measurements,
        )

    @classmethod
    def from_csv(
        cls,
        fractal_dataset_csv_paths: fractal_governance.util.FractalDatasetCSVPaths = fractal_governance.util.FractalDatasetCSVPaths(),  # noqa: E501
    ) -> "Dataset":
        """Return a measurement uncertainty dataset object for the given file path to
        the Genesis .csv dataset"""
        dataset = fractal_governance.dataset.Dataset.from_csv(fractal_dataset_csv_paths)
        return cls.from_dataset(dataset=dataset)


@attrs.frozen(kw_only=True)
class Measurement:
    """A consensus measurement made by a contributor during a weekly consensus
    meeting"""

    member_id: str
    level: int
    meeting_id: int
    group: int


@attrs.define(kw_only=True)
class Contributor:
    """A participant (aka contributor) from a weekly consensus meeting"""

    member_id: str
    measurements_by_member_id: Dict[str, Set[Measurement]] = attrs.field(factory=dict)

    _statistics_by_member_id: Dict[str, uncertainties.ufloat] = attrs.field(
        default=None, init=False
    )

    @property
    def statistics_by_member_id(self) -> Dict[str, uncertainties.ufloat]:
        if not self._statistics_by_member_id:
            statistics_by_member_id: Dict[str, uncertainties.ufloat] = dict()
            for member_id, measurements in self.measurements_by_member_id.items():
                levels = [measurement.level for measurement in measurements]
                statistics_by_member_id[member_id] = uncertainties.ufloat(
                    np.mean(levels), np.std(levels)
                )
            self._statistics_by_member_id = statistics_by_member_id
        return self._statistics_by_member_id


def _create_contributor_by_member_id(
    df: pd.DataFrame,
) -> Dict[str, Contributor]:
    contributor_by_member_id: Dict[str, Contributor] = dict()
    for ((meeting_id, group), df) in df[df[LEVEL_COLUMN_NAME].notna()].groupby(
        [MEETING_ID_COLUMN_NAME, GROUP_COLUMN_NAME]
    ):
        for member_id1 in df[MEMBER_ID_COLUMN_NAME]:
            if member_id1 not in contributor_by_member_id:
                contributor_by_member_id[member_id1] = Contributor(member_id=member_id1)
            contributor = contributor_by_member_id[member_id1]
            for member_id2, level in df[
                [MEMBER_ID_COLUMN_NAME, LEVEL_COLUMN_NAME]
            ].values:
                measurement = Measurement(
                    member_id=member_id2,
                    level=level,
                    meeting_id=meeting_id,
                    group=group,
                )
                measurements_by_member_id = contributor.measurements_by_member_id
                if member_id2 not in measurements_by_member_id:
                    measurements_by_member_id[member_id2] = set()
                measurements = measurements_by_member_id[member_id2]
                measurements.add(measurement)
    return contributor_by_member_id


def _create_measurement_uncertainty_by_member_id(
    df: pd.DataFrame, include_self_measurements: bool = False
) -> Dict[str, uncertainties.ufloat]:
    measurement_uncertainty_by_member_id: Dict[str, uncertainties.ufloat] = dict()
    contributor_by_member_id = _create_contributor_by_member_id(df)
    for member_id1, contributor1 in contributor_by_member_id.items():
        statistics_by_member_id1 = contributor1.statistics_by_member_id
        measurement_uncertainties: List[uncertainties.ufloat] = list()
        for member_id2 in statistics_by_member_id1.keys():
            if not include_self_measurements and member_id1 == member_id2:
                # Skip self measurements at the user's request.
                continue
            contributor2 = contributor_by_member_id[member_id2]
            statistics_by_member_id2 = contributor2.statistics_by_member_id
            # Measurements of member_id2 by member_id1.
            statistics1 = statistics_by_member_id1[member_id2]
            # Measurements of member_id2 by everyone except member_id1.
            statistics2 = statistics_by_member_id2[member_id2]
            measurement_uncertainty = statistics1 - statistics2
            measurement_uncertainties.append(measurement_uncertainty)
        measurement_uncertainty_by_member_id[member_id1] = np.mean(
            measurement_uncertainties
        )
    return measurement_uncertainty_by_member_id


def create_measurement_uncertainty_dataframe(
    *,
    df: pd.DataFrame,
    include_self_measurements: bool = False,
) -> pd.DataFrame:
    measurement_uncertainty_by_member_id = _create_measurement_uncertainty_by_member_id(
        df, include_self_measurements=include_self_measurements
    )
    member_ids: List[str] = list()
    uncertainties: List[float] = list()
    for (
        member_id,
        measurement_uncertainty,
    ) in measurement_uncertainty_by_member_id.items():
        member_ids.append(member_id)
        uncertainties.append(measurement_uncertainty)
    df = pd.DataFrame(
        {
            MEMBER_ID_COLUMN_NAME: member_ids,
            MEASUREMENT_UNCERTAINTY_COLUMN_NAME: uncertainties,
        }
    )
    return df.sort_values(
        by=MEASUREMENT_UNCERTAINTY_COLUMN_NAME, ascending=True
    ).set_index(MEMBER_ID_COLUMN_NAME)
