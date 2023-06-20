from typing import NamedTuple

class VoteData(NamedTuple):
    """Contains data for each vote (count: how many votes, id: later votes have a higher id)."""
    count: int
    id: int