"""
Builds human-readable versions of some files
"""

import json

if __name__ == "__main__":
    readable_info_folder = "info (readable)"
    info_folder = "leetpy/info"

    # TODO: glob all JSON files
    filenames = ["meta.json", "per-question-metadata.json"]

    for filename in filenames:
        with open(f"{info_folder}/{filename}", "r") as input_file:
            with open(f"{readable_info_folder}/{filename}", "w") as output_file:
                json.dump(json.load(input_file), output_file, indent=2)
