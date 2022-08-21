# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Utility functions for fractal governance data analysis"""

import re
from pathlib import Path

import attrs
import pandas as pd

import fractal_governance.math

from .constants import (
    DATE_OF_FIRST_GENESIS_FRACTAL_MEETING,
    GENESIS_ACCOUNT_STATUS_CSV_PATH,
    GENESIS_LATE_CONSENSUS_CSV_PATH,
    GENESIS_TEAMS_CSV_PATH,
    GENESIS_WEEKLY_MEASUREMENTS_CSV_PATH,
    HIVE_ACCOUNT_NAME_COLUMN_NAME,
    INDEX_COLUMN_NAME,
    LEVEL_COLUMN_NAME,
    MEETING_DATE_COLUMN_NAME,
    MEETING_ID_COLUMN_NAME,
    MEETING_ID_WHEN_HIVE_SIGNATURE_REQUIRED,
    MEMBER_ID_COLUMN_NAME,
    RESPECT_COLUMN_NAME,
    SIGNATURE_ON_FILE_COLUMN_NAME,
    TEAM_ID_COLUMN_NAME,
)


def meeting_id_to_timestamp(meeting_id: int) -> pd.Timestamp:
    """Return the meeting date for the given Genesis fractal meeting_id"""
    if meeting_id < 1:
        raise ValueError(f"meeting_id={meeting_id} must be >= 1")
    week_offset = meeting_id - 1
    # April 9, 2022 was the date for the Eden on EOS elections, so the Weekly Consensus
    # meeting was cancelled to allow Genesis Fractal members to attend. This caused
    # meeting ID #7 to be pushed back to April 16, 2022.
    if week_offset >= 7:
        week_offset += 1
    return DATE_OF_FIRST_GENESIS_FRACTAL_MEETING + week_offset * pd.to_timedelta("1 w")


@attrs.frozen
class FractalDatasetCSVPaths:
    """A wrapper around the paths to a Fractal dataset's .csv files"""

    account_status: Path = attrs.field(default=GENESIS_ACCOUNT_STATUS_CSV_PATH)
    late_consensus: Path = attrs.field(default=GENESIS_LATE_CONSENSUS_CSV_PATH)
    teams: Path = attrs.field(default=GENESIS_TEAMS_CSV_PATH)
    weekly_measurements: Path = attrs.field(
        default=GENESIS_WEEKLY_MEASUREMENTS_CSV_PATH
    )

    @classmethod
    def relative_to(cls, PROJECT_DIR: Path) -> "FractalDatasetCSVPaths":
        account_status = GENESIS_ACCOUNT_STATUS_CSV_PATH.relative_to(PROJECT_DIR)
        late_consensus = GENESIS_LATE_CONSENSUS_CSV_PATH.relative_to(PROJECT_DIR)
        teams = GENESIS_TEAMS_CSV_PATH.relative_to(PROJECT_DIR)
        weekly_measurements = GENESIS_WEEKLY_MEASUREMENTS_CSV_PATH.relative_to(
            PROJECT_DIR
        )
        return cls(
            account_status=account_status,
            late_consensus=late_consensus,
            teams=teams,
            weekly_measurements=weekly_measurements,
        )


def read_csv(
    fractal_dataset_csv_paths: FractalDatasetCSVPaths = FractalDatasetCSVPaths(),
) -> pd.DataFrame:
    """Return a pandas DataFrame for the given file path to the Genesis .csv dataset"""

    account_status_file_path = fractal_dataset_csv_paths.account_status
    late_consensus_file_path = fractal_dataset_csv_paths.late_consensus
    teams_file_path = fractal_dataset_csv_paths.teams
    weekly_measurements_file_path = fractal_dataset_csv_paths.weekly_measurements

    df = pd.read_csv(weekly_measurements_file_path)
    df = df.set_index(MEMBER_ID_COLUMN_NAME)

    # Add a column for each meeting's date.
    df[MEETING_DATE_COLUMN_NAME] = df[MEETING_ID_COLUMN_NAME].apply(
        meeting_id_to_timestamp
    )

    # Add a column for the amount of Respect that corresponds to the Level in each row.
    df[RESPECT_COLUMN_NAME] = df[LEVEL_COLUMN_NAME].apply(
        fractal_governance.math.respect
    )

    df_account_status = (
        pd.read_csv(account_status_file_path)
        .drop([INDEX_COLUMN_NAME], axis=1)
        .set_index(MEMBER_ID_COLUMN_NAME)
    )
    df = df.join(df_account_status)
    df[[HIVE_ACCOUNT_NAME_COLUMN_NAME, SIGNATURE_ON_FILE_COLUMN_NAME]] = df[
        [HIVE_ACCOUNT_NAME_COLUMN_NAME, SIGNATURE_ON_FILE_COLUMN_NAME]
    ].fillna(False)

    # Per email from Gregory Wexler on July 6, 2022 with the subject
    # "Re: Differences between spreadsheet and dashboard":
    #
    # We should have zero'ed out the (NS) No-signature people early on.
    #
    # Since we published numbers, I didn't think it was right to 'pull it back'. That
    # said, given our statements in the meeting that you need to sign to participate
    # and earn respect, I started zeroing out (NS) members from that point forward.
    #
    # So the rules are:
    # 1. as of last meeting date, (NS) means you're going to get ZERO respect going
    #    forward.
    # 2. prior to that meeting, we're going to keep that respect in place.
    #
    # NOTE: The "last meeting date" that Gregory was referring to was 6/25/2022, which
    # was meeting_id 17.
    df.loc[
        ~df[SIGNATURE_ON_FILE_COLUMN_NAME]
        & (df[MEETING_ID_COLUMN_NAME] >= MEETING_ID_WHEN_HIVE_SIGNATURE_REQUIRED),
        [RESPECT_COLUMN_NAME],
    ] = 0

    df_teams = (
        pd.read_csv(teams_file_path)
        .drop([INDEX_COLUMN_NAME], axis=1)
        .set_index(TEAM_ID_COLUMN_NAME)
    )
    df = df.join(df_teams, on=TEAM_ID_COLUMN_NAME)

    df = df.reset_index()

    # Per email from Gregory Wexler on July 25, 2022 with the subject
    # "Re: Differences between spreadsheet and dashboard":
    #
    # From memory (and if you hover over the cell you might find the comment), they
    # registered their Consensus logs in to the HIVE.BLOG for beyond the 1 hour time
    # limit allowed, hence they were awarded zero respect for their tartiness. They
    # have up to 1 hour after the meeting conclusion with which to post their HIVE.BLOG
    # consensus ranks.  They entered beyond that window.
    df_late_consensus = pd.read_csv(late_consensus_file_path)
    for member_id, meeting_id in df_late_consensus[
        [MEMBER_ID_COLUMN_NAME, MEETING_ID_COLUMN_NAME]
    ].values:
        df.loc[
            (df[MEMBER_ID_COLUMN_NAME] == member_id)
            & (df[MEETING_ID_COLUMN_NAME] == meeting_id),
            [RESPECT_COLUMN_NAME],
        ] = 0

    return df


# From https://github.com/jupyter/nbconvert/issues/946#issuecomment-1055635749
class GitHubMarkdownDataFrame(pd.DataFrame):  # type: ignore
    """DataFrame that strips <style> tags when used in a Notebook."""

    def _repr_html_(self) -> str:
        """Override parent's method."""
        # original = super()._repr_html_()
        original = self.to_html(index=False)

        # See https://stackoverflow.com/a/55148480/3324095
        #
        # Replace the CSS with an empty string.
        stripped = re.sub("<style scoped>.*</style>\n", "", original, flags=re.DOTALL)
        return stripped
