# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.addendum_1.constants module"""

import unittest

import fractal_governance.dataset
from fractal_governance.addendum_1.constants import Addendum1Constants


class TestAddendum1Constants(unittest.TestCase):
    """Test fixture for the fractal_governance.addendum_1.constants module"""

    def test_with_default_values(self) -> None:
        dataset = fractal_governance.dataset.Dataset.from_csv()
        addendum_1_constants = Addendum1Constants(dataset=dataset)

        self.assertAlmostEqual(
            addendum_1_constants.total_respect_before_addendum_1_individual,
            7035,
        )
        self.assertAlmostEqual(
            addendum_1_constants.total_respect_before_addendum_1_team,
            2928,
        )
        self.assertAlmostEqual(
            addendum_1_constants.total_respect_before_addendum_1,
            9963,
        )

        self.assertAlmostEqual(
            addendum_1_constants.token_supply_before_addendum_1_individual,
            13463944.307637664,
        )

        self.assertAlmostEqual(
            addendum_1_constants.token_supply_before_addendum_1_team,
            5603756.777933629,
        )

        self.assertAlmostEqual(
            addendum_1_constants.token_supply_before_addendum_1,
            19067701.085571293,
        )

        self.assertAlmostEqual(
            addendum_1_constants.pro_rata_respect,
            1913.851358583889,
        )

    def test_with_team_fractally_spreadsheet_values(self) -> None:
        dataset = fractal_governance.dataset.Dataset.from_csv()
        # Team fractally's incorrect calculation of pro_rata_respect.
        addendum_1_constants = Addendum1Constants(
            dataset=dataset, total_respect_before_addendum_1_individual=7022
        )

        self.assertAlmostEqual(
            addendum_1_constants.total_respect_before_addendum_1_individual,
            7022,
        )
        self.assertAlmostEqual(
            addendum_1_constants.total_respect_before_addendum_1_team,
            2928,
        )
        self.assertAlmostEqual(
            addendum_1_constants.total_respect_before_addendum_1,
            9950,
        )

        self.assertAlmostEqual(
            addendum_1_constants.token_supply_before_addendum_1_individual,
            13456622.816370012,
        )

        self.assertAlmostEqual(
            addendum_1_constants.token_supply_before_addendum_1_team,
            5611078.269201282,
        )

        self.assertAlmostEqual(
            addendum_1_constants.token_supply_before_addendum_1,
            19067701.085571293,
        )

        self.assertAlmostEqual(
            addendum_1_constants.pro_rata_respect,
            1916.3518678966125,
        )


if __name__ == "__main__":
    unittest.main()
