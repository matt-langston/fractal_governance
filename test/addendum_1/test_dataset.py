# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.addendum_1.dataset module"""

import unittest

import fractal_governance.dataset
import fractal_governance.util
from fractal_governance.addendum_1.constants import Addendum1Constants
from fractal_governance.addendum_1.dataset import Addendum1Dataset
from fractal_governance.addendum_1.weighted_means import (
    WeightedMeanParameters,
    WeightedMeans,
)


class TestAddendum1Dataset(unittest.TestCase):
    """Test fixture for the fractal_governance.addendum_1.dataset module"""

    def test_with_default_values(self) -> None:
        dataset = fractal_governance.dataset.Dataset.from_csv()
        dataset_addendum_1 = Addendum1Dataset(dataset=dataset)
        self.assertIsNotNone(dataset_addendum_1)

    def test_with_team_fractally_spreadsheet_values(self) -> None:
        dataset = fractal_governance.dataset.Dataset.from_csv()
        # Team fractally's incorrect value for not clamping *weighted mean Respect* to
        # zero when a user has not signed the Fractal Contributor Agreement after a
        # Fractal-defined meeting date.
        weighted_mean_parameters = WeightedMeanParameters(
            clamp_mean_respect_to_zero_when_fractal_contributor_agreement_not_signed=False  # noqa: E501
        )
        weighted_means = WeightedMeans(
            dataset=dataset, parameters=weighted_mean_parameters
        )
        # Team fractally's incorrect calculation of pro_rata_respect.
        addendum_1_constants = Addendum1Constants(
            dataset=dataset, total_respect_before_addendum_1_individual=7022
        )
        dataset_addendum_1 = Addendum1Dataset(
            dataset=dataset,
            weighted_means=weighted_means,
            addendum_1_constants=addendum_1_constants,
        )
        self.assertIsNotNone(dataset_addendum_1)


if __name__ == "__main__":
    unittest.main()
