import sys
import os
import re
from collections import defaultdict
from typing import Dict, List, IO, Match

CLIPPINGS_PATH = "documents/My Clippings.txt"
CLIPPINGS_DELIM = "==========\n"

CLIPPING_ENTRY_RE = re.compile(
    r"^(?P<title>.*)\s*\n- Your Highlight (on page \d+|on|at)\s?\|? (?P<location_type>page|location) (?P<location_start>\d+)-(?P<location_end>\d+) \| Added on (?P<date>.+?, \d{1,2} .+? \d{4} \d{2}:\d{2}:\d{2})\s*\n(?P<content>.*)"
)


def get_content_from_match(match: Match) -> str:
    return match.group("content")


def encode_title(title: str) -> str:
    return title.replace(" ", "_") \
                .replace("(", "") \
                .replace(")", "") \
                .replace(",", "") \
                .replace(":", "")


def read_clippings(kindle_path: str) -> str:
    clippings_path_abs = os.path.join(kindle_path, CLIPPINGS_PATH)
    return open(clippings_path_abs).read()


def write_clipping(clipping: Match, file: IO[str]) -> None:
    content = get_content_from_match(clipping).replace("\n", " ")
    file.write(f"- {content}\n")


def is_partial_highlight(current_clip: Match, next_clip: Match) -> bool:
    return get_content_from_match(current_clip) in get_content_from_match(next_clip)


def process_clippings_per_book(
    title: str, clippings: List[Match], output_path: str
) -> None:
    sorted_clippings = sorted(clippings, key=lambda clip: int(clip.group("location_start")))
    file_name = os.path.join(output_path, f"{encode_title(title)}-TLDR.md")
    file_already_exists = os.path.exists(file_name)
    with open(file_name, "a") as out_file:
        if not file_already_exists:
            out_file.write(f"# TLDR for {title}\n")

        for i in range(len(sorted_clippings) - 1):
            clip = sorted_clippings[i]
            next_clip = sorted_clippings[i + 1]
            previous_clip = sorted_clippings[i - 1]

            if is_partial_highlight(clip, next_clip):
                # Is partial match, next clip contains better version
                continue

            if is_partial_highlight(clip, previous_clip):
                # Is partial match, previous clip contains better version
                continue

            write_clipping(sorted_clippings[i], out_file)

        # Write last clip as it cannot be partial
        write_clipping(sorted_clippings[-1], out_file)


def process_all_clippings(clippings: str, output_path: str) -> None:
    split_clippings = clippings.split(CLIPPINGS_DELIM)

    clip_dict: Dict[str, List[Match]] = defaultdict(list)
    for clip in split_clippings:
        matched_clip = CLIPPING_ENTRY_RE.match(clip)
        if matched_clip is None:
            # Malformed entry, ignore
            continue

        title = matched_clip.group("title").strip()
        clip_dict[title].append(matched_clip)

    for title, book_clippings in clip_dict.items():
        process_clippings_per_book(title, book_clippings, output_path)


def delete_clippings_file(kindle_path: str) -> None:
    # Clear content of clippings file
    open(os.path.join(kindle_path, CLIPPINGS_PATH), "w").close()


def main(kindle_path: str, output_path: str) -> None:
    clippings = read_clippings(kindle_path)
    process_all_clippings(clippings, output_path)
    delete_clippings_file(kindle_path)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USAGE:\n> python3 ktldr.py /path/to/kindle /path/to/output_dir")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
