"""
Dynamically builds the meta.json file
"""

import json
from collections import defaultdict
from typing import TypedDict, List, Dict


# Mirrored in leetpy/__main__.py
class MetaData(TypedDict):
    question_count: int
    topics: List[str]
    difficulty_count: Dict[str, int]
    paid_count: int


if __name__ == "__main__":
    meta: MetaData = {}

    info_folder = "leetpy/info"

    with open(f"{info_folder}/per-question-metadata.json", "r") as f:
        qn_metadata_list: List[dict] = json.load(f)

    meta["question_count"] = len(qn_metadata_list)

    topics = set()
    for qn_metadata in qn_metadata_list:
        topics.update(qn_metadata["topics"])
    meta["topics"] = list(sorted(topics))

    difficulty_count = defaultdict(int)
    for qn_metadata in qn_metadata_list:
        difficulty_count[qn_metadata["difficulty"]] += 1
    meta["difficulty_count"] = difficulty_count

    paid_count = 0
    for qn_metadata in qn_metadata_list:
        if qn_metadata["is_paid_only"]:
            paid_count += 1
    meta["paid_count"] = paid_count

    # Save the metadata
    with open(f"{info_folder}/meta.json", "w") as f:
        json.dump(meta, f, indent=None, separators=(",", ":"))
