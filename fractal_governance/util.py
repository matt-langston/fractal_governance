# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Utility functions for fractal governance data analysis"""

# builtins
import re
from pathlib import Path

# 3rd party
import pandas as pd

# 2nd party
import fractal_governance.math

DATE_OF_FIRST_GENESIS_FRACTAL_MEETING = pd.to_datetime('2/26/2022')


def meeting_id_to_timestamp(meeting_id: int) -> pd.Timestamp:
    """Return the meeting date for the given Genesis fractal meeting_id"""
    if meeting_id < 1:
        raise ValueError(f"meeting_id={meeting_id} must be >= 1")
    week_offset = meeting_id - 1
    # April 9, 2022 was the date for the Eden on EOS elections, so the Weekly Consensus meeting
    # was cancelled to allow Genesis Fractal members to attend. This caused meeting ID #7 to be
    # pushed back to April 16, 2022.
    if week_offset >= 7:
        week_offset += 1
    return DATE_OF_FIRST_GENESIS_FRACTAL_MEETING + week_offset * pd.to_timedelta(
        '1 w')


def read_csv(file_path: Path) -> pd.DataFrame:
    """Return a pandas DataFrame for the given file path to the Genesis .csv dataset"""
    df = pd.read_csv(file_path)  # pylint: disable=C0103

    # Add a column for each meeting's date.
    df['MeetingDate'] = df['MeetingID'].apply(meeting_id_to_timestamp)

    # Add a column for the amount of Respect that corresponds to the Rank in each row.
    df['Respect'] = df['Rank'].apply(fractal_governance.math.respect)

    return df


# From https://github.com/jupyter/nbconvert/issues/946#issuecomment-1055635749
class GitHubMarkdownDataFrame(pd.DataFrame):
    """DataFrame that strips <style> tags when used in a Notebook."""

    def _repr_html_(self) -> str:
        """Override parent's method."""
        original = super()._repr_html_()

        # See https://stackoverflow.com/a/55148480/3324095
        #
        # Replace the CSS with an empty string.
        stripped = re.sub('<style scoped>.*</style>\n',
                          '',
                          original,
                          flags=re.DOTALL)
        return stripped
