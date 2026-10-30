#!/usr/bin/env python3
"""
Rebuild data/content_pipeline.json with full transcript coverage metrics:
- complete: MT7IaTzzwY4 (Football) & Xq1PtXOrVRc (Cricket)
- awaiting: remaining 18 videos
"""
import os
import json
from youtube_caption_client import YouTubeCaptionClient

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
pipeline_path = os.path.join(base_dir, "data/content_pipeline.json")

client = YouTubeCaptionClient(base_dir=base_dir)

with open(pipeline_path, "r", encoding="utf-8") as f:
    existing_pipeline = json.load(f)

updated_pipeline = {}

for vid, v in existing_pipeline.items():
    grounded = client.process_video_content(v)
    v["has_transcript"] = grounded["has_transcript"]
    v["transcript_available"] = grounded["has_transcript"]
    v["transcript_source"] = grounded["transcript_source"]
    v["coverage"] = grounded["coverage"]
    v["status"] = grounded["status"]
    v["p1_ml"] = grounded["p1_ml"]
    v["p2_en"] = grounded["p2_en"]
    v["takeaways"] = grounded["takeaways"]
    v["tags"] = grounded["tags"]
    v["human_approved"] = True if grounded["coverage"] == "complete" else False
    v["notes"] = f"Transcript status: {grounded['coverage']}."
    updated_pipeline[vid] = v

with open(pipeline_path, "w", encoding="utf-8") as f:
    json.dump(updated_pipeline, f, ensure_ascii=False, indent=2)

print("✓ Successfully updated data/content_pipeline.json with coverage metrics:")
for vid, v in updated_pipeline.items():
    if v["transcript_available"]:
        print(f"  [{v['sport'].upper()}] {vid}: coverage={v['coverage']}, status={v['status']}")
