"""Fetch a YouTube transcript and store it in the knowledge base format.

Usage:
    python -I tools/fetch_youtube_transcript.py <video_id> <video_dir> [--title SLUG] [--lang en]

Writes:
    <video_dir>/raw/segments.json   raw timed segments
    <video_dir>/transcript.md       readable transcript, paragraphs of ~110 words
                                    prefixed with their start timestamp

Requires `youtube-transcript-api` (pip install youtube-transcript-api).
yt-dlp subtitles were tried first during the initial import but hit HTTP 429.
The nectar.md file is written by hand (or by an agent) after reading the transcript.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

PARAGRAPH_WORDS = 110


def fetch_segments(video_id: str, lang: str) -> list[dict]:
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    fetched = api.fetch(video_id, languages=[lang])
    return [
        {"start": s.start, "duration": s.duration, "text": s.text.replace("\n", " ").strip()}
        for s in fetched
    ]


def fmt(seconds: float) -> str:
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def paragraphs(segments: list[dict]) -> list[tuple[float, str]]:
    out: list[tuple[float, str]] = []
    buf: list[str] = []
    start = 0.0
    for seg in segments:
        if not seg["text"]:
            continue
        if not buf:
            start = seg["start"]
        buf.append(seg["text"])
        if sum(len(t.split()) for t in buf) >= PARAGRAPH_WORDS:
            out.append((start, " ".join(buf)))
            buf = []
    if buf:
        out.append((start, " ".join(buf)))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video_id")
    parser.add_argument("video_dir", type=Path)
    parser.add_argument("--title", default=None)
    parser.add_argument("--lang", default="en")
    args = parser.parse_args()

    title = args.title or args.video_dir.name
    segments = fetch_segments(args.video_id, args.lang)

    raw_dir = args.video_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    (raw_dir / "segments.json").write_text(
        json.dumps(
            {"video_id": args.video_id, "title": title, "language": args.lang, "segments": segments},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    end = segments[-1]["start"] + segments[-1]["duration"] if segments else 0
    lines = [
        f"# Transcript — {title}",
        "",
        f"- Video ID: `{args.video_id}`",
        f"- Language: {args.lang} (auto-generated captions)",
        f"- Duration: {fmt(end)}",
        "",
        "> Source brute : `raw/segments.json`. Les timestamps marquent le début du paragraphe.",
        "",
    ]
    for start, body in paragraphs(segments):
        lines += [f"**[{fmt(start)}]** {body}", ""]
    (args.video_dir / "transcript.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(segments)} segments -> {args.video_dir}")


if __name__ == "__main__":
    main()
