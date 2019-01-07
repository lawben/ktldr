import sys
import os
import re
from collections import defaultdict
from typing import Dict, List, IO, Match

CLIPPINGS_PATH = "documents/My Clippings.txt"
CLIPPINGS_DELIM = "==========\n"

CLIPPING_ENTRY_RE = re.compile(
    r"^(?P<title>.*)\s*\n- Your Highlight (on|at) (?P<location_type>page|location) (?P<location_start>\d+)-(?P<location_end>\d+) \| Added on (?P<date>.+?, \d{1,2} .+? \d{4} \d{2}:\d{2}:\d{2})\s*\n(?P<content>.*)"
)


def encode_title(title: str) -> str:
    return title.replace(" ", "_")


def read_clippings(kindle_path: str) -> str:
    clippings_path_abs = os.path.join(kindle_path, CLIPPINGS_PATH)
    return open(clippings_path_abs).read()


def write_clipping(clipping: Match, file: IO[str]) -> None:
    content = clipping.group("content").replace("\n", " ")
    file.write(f"- {content}\n")


def is_partial_highlight(current_clip: Match, next_clip: Match) -> bool:
    return current_clip.group("content") in next_clip.group("content")


def process_clippings_per_book(
    title: str, clippings: List[Match], output_path: str
) -> None:
    sorted_clippings = sorted(clippings, key=lambda clip: clip.group("location_start"))
    file_name = os.path.join(output_path, f"{encode_title(title)}-TLDR.md")
    with open(file_name, "w") as out_file:
        out_file.write(f"# TLDR for: {title}\n")
        for i in range(len(sorted_clippings) - 1):
            if is_partial_highlight(sorted_clippings[i], sorted_clippings[i + 1]):
                # Is partial match, next clip contains better version
                continue
            write_clipping(sorted_clippings[i], out_file)

        # Write last clip as itt cannot be partial
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


def main(kindle_path: str, output_path: str) -> None:
    clippings = read_clippings(kindle_path)
    process_all_clippings(clippings, output_path)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Need to specify /path/to/kindle and /path/to/output_dir")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
