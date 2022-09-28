# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.addendum_1.weighted_means module"""

import unittest

import attrs
import fractal_governance.dataset
import fractal_governance.util
import pandas as pd
from fractal_governance.addendum_1.weighted_means import (
    WeightedMeanParameters,
    WeightedMeans,
)
from fractal_governance.constants import MEMBER_ID_COLUMN_NAME, PROJECT_DIR

TEST_DATA_CSV_FILE_PATH = (
    PROJECT_DIR / "data/test/addendum_1/Stats_post-Aug_6_Dist_Portions.csv"
)


@attrs.frozen
class WeightedMeanRespect:
    member_id: str
    weighted_mean_respect: float


class TestWeightedMeans(unittest.TestCase):
    """Test fixture for the fractal_governance.addendum_1.weighted_means module"""

    def test_with_default_values(self) -> None:
        dataset = fractal_governance.dataset.Dataset.from_csv()
        weighted_means = WeightedMeans(dataset=dataset)
        pivot_table = weighted_means.get_pivot_table()
        df = pd.read_csv(TEST_DATA_CSV_FILE_PATH)
        for meeting_id in (23, 24, 25):
            count_zero = 0
            count_non_zero = 0
            for member_id, weighted_mean_respect_fractally_spreadsheet in df[
                [MEMBER_ID_COLUMN_NAME, str(meeting_id)]
            ].values:
                weighted_mean_respect = pivot_table.loc[member_id, meeting_id]
                # Uncomment the following print statement for debugging if this test
                # ever fails.
                # print(
                #     f"meeting_id={meeting_id} member_id={member_id} weighted_mean_respect={weighted_mean_respect} weighted_mean_respect_fractally_spreadsheet={weighted_mean_respect_fractally_spreadsheet}"  # noqa: E501
                # )
                if weighted_mean_respect_fractally_spreadsheet == 0:
                    # A value of zero should be universal between Team fractally's
                    # spreadsheet and the calculated value from the dataset.
                    self.assertAlmostEqual(
                        weighted_mean_respect,
                        weighted_mean_respect_fractally_spreadsheet,
                        places=3,
                    )
                if weighted_mean_respect == 0:
                    count_zero += 1
                else:
                    count_non_zero += 1
            # Uncomment the following print statement for debugging if this test ever
            # fails.
            #
            # Expected output for weighted_mean_respect_fractally_spreadsheet:
            # MDL: meeting_id=23 count_zero=41 count_non_zero=77
            # MDL: meeting_id=24 count_zero=42 count_non_zero=76
            # MDL: meeting_id=25 count_zero=42 count_non_zero=76
            #
            # Expected output for weighted_mean_respect:
            # MDL: meeting_id=23 count_zero=49 count_non_zero=69
            # MDL: meeting_id=24 count_zero=50 count_non_zero=68
            # MDL: meeting_id=25 count_zero=49 count_non_zero=69
            # print(
            #     f"MDL: meeting_id={meeting_id} count_zero={count_zero} count_non_zero={count_non_zero}"  # noqa: $501
            # )

    def test_with_team_fractally_spreadsheet_values(self) -> None:
        dataset = fractal_governance.dataset.Dataset.from_csv()
        weighted_mean_parameters = WeightedMeanParameters(
            clamp_mean_respect_to_zero_when_fractal_contributor_agreement_not_signed=False  # noqa: E501
        )
        weighted_means = WeightedMeans(
            dataset=dataset, parameters=weighted_mean_parameters
        )
        pivot_table = weighted_means.get_pivot_table()
        df = pd.read_csv(TEST_DATA_CSV_FILE_PATH)
        for meeting_id in (23, 24, 25):
            count_zero = 0
            count_non_zero = 0
            for member_id, weighted_mean_respect_fractally_spreadsheet in df[
                [MEMBER_ID_COLUMN_NAME, str(meeting_id)]
            ].values:
                weighted_mean_respect = pivot_table.loc[member_id, meeting_id]
                # Uncomment the following print statement for debugging if this test
                # ever fails.
                print(
                    f"meeting_id={meeting_id} member_id={member_id} weighted_mean_respect={weighted_mean_respect} weighted_mean_respect_fractally_spreadsheet={weighted_mean_respect_fractally_spreadsheet}"  # noqa: E501
                )
                self.assertAlmostEqual(
                    weighted_mean_respect,
                    weighted_mean_respect_fractally_spreadsheet,
                    places=3,
                )
                if weighted_mean_respect == 0:
                    count_zero += 1
                else:
                    count_non_zero += 1
            # Uncomment the following print statement for debugging if this test ever
            # fails.
            #
            # Expected output for weighted_mean_respect_fractally_spreadsheet:
            # MDL: meeting_id=23 count_zero=41 count_non_zero=77
            # MDL: meeting_id=24 count_zero=42 count_non_zero=76
            # MDL: meeting_id=25 count_zero=42 count_non_zero=76
            #
            # Expected output for weighted_mean_respect:
            # MDL: meeting_id=23 count_zero=41 count_non_zero=77
            # MDL: meeting_id=24 count_zero=42 count_non_zero=76
            # MDL: meeting_id=25 count_zero=42 count_non_zero=76
            # print(
            #     f"MDL: meeting_id={meeting_id} count_zero={count_zero} count_non_zero={count_non_zero}"  # noqa: E501
            # )


if __name__ == "__main__":
    unittest.main()
