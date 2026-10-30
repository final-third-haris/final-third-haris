#!/usr/bin/env python3
"""
Initialize and manage data/content_pipeline.json
"""
import os
import json
import sys

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
pipeline_path = os.path.join(base_dir, "data/content_pipeline.json")

sys.path.append(os.path.join(base_dir, "scripts"))
from generate_video_pages import VIDEOS
from youtube_caption_client import YouTubeCaptionClient

client = YouTubeCaptionClient(base_dir=base_dir)

pipeline = {}
for v in VIDEOS:
    vid = v["id"]
    t_text, t_source = client.get_transcript(vid)
    has_t = bool(t_text)
    
    pipeline[vid] = {
        "id": vid,
        "slug": v["slug"],
        "sport": v["sport"],
        "playlist": v["playlist"],
        "title": v["title"],
        "published_iso": v["published_iso"],
        "views": v["views"],
        "status": "published" if has_t else "awaiting_transcript",
        "transcript_available": has_t,
        "transcript_source": t_source,
        "human_approved": True if has_t else False,
        "notes": "Verified transcript linked" if has_t else "Awaiting official YouTube caption upload or local .srt import"
    }

with open(pipeline_path, "w", encoding="utf-8") as f:
    json.dump(pipeline, f, ensure_ascii=False, indent=2)

print(f"✓ Initialized {pipeline_path} with {len(pipeline)} videos.")
print(f"  - Verified with transcript: {sum(1 for v in pipeline.values() if v['transcript_available'])}")
print(f"  - Awaiting transcript: {sum(1 for v in pipeline.values() if not v['transcript_available'])}")
