#!/usr/bin/env python3
"""
Final Third — Content Review & Pipeline Management CLI
Commands:
  python3 scripts/content_review.py list
  python3 scripts/content_review.py import-transcript <video_id> <path_to_file>
  python3 scripts/content_review.py approve <video_id>
  python3 scripts/content_review.py status <video_id>
  python3 scripts/content_review.py build
"""

import os
import sys
import json
import shutil

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
pipeline_path = os.path.join(base_dir, "data/content_pipeline.json")
transcripts_dir = os.path.join(base_dir, "transcripts")
os.makedirs(transcripts_dir, exist_ok=True)

sys.path.append(os.path.join(base_dir, "scripts"))
from youtube_caption_client import YouTubeCaptionClient

def load_pipeline():
    if not os.path.exists(pipeline_path):
        return {}
    with open(pipeline_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_pipeline(data):
    with open(pipeline_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def cmd_list():
    pipeline = load_pipeline()
    print("=" * 80)
    print("FINAL THIRD — CONTENT PIPELINE STATUS")
    print("=" * 80)
    print(f"{'ID':<12} | {'Sport':<8} | {'Status':<20} | {'Transcript':<12} | {'Approved':<8} | Title")
    print("-" * 80)
    for vid, item in pipeline.items():
        t_status = "YES (" + item.get("transcript_source", "none") + ")" if item.get("transcript_available") else "NO"
        appr = "YES" if item.get("human_approved") else "NO"
        title = item.get("title", "")[:35]
        print(f"{vid:<12} | {item.get('sport'):<8} | {item.get('status'):<20} | {t_status:<12} | {appr:<8} | {title}...")
    print("-" * 80)
    total = len(pipeline)
    published = sum(1 for v in pipeline.values() if v.get("status") == "published")
    awaiting = sum(1 for v in pipeline.values() if v.get("status") == "awaiting_transcript")
    review = sum(1 for v in pipeline.values() if v.get("status") == "needs_review")
    print(f"Summary: Total {total} | Published: {published} | Awaiting Transcript: {awaiting} | Needs Review: {review}\n")

def cmd_import_transcript(video_id, file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        sys.exit(1)
    
    ext = file_path.split(".")[-1].lower()
    if ext not in ["srt", "vtt", "txt"]:
        ext = "srt"
    
    dest_path = os.path.join(transcripts_dir, f"{video_id}.{ext}")
    shutil.copyfile(file_path, dest_path)
    print(f"✓ Saved transcript to {dest_path}")
    
    # Update pipeline
    pipeline = load_pipeline()
    if video_id not in pipeline:
        pipeline[video_id] = {"id": video_id}
    
    client = YouTubeCaptionClient(base_dir=base_dir)
    with open(dest_path, "r", encoding="utf-8") as f:
        raw = f.read()
    cleaned = client.clean_transcript(raw, ext)
    
    pipeline[video_id]["transcript_available"] = True
    pipeline[video_id]["transcript_source"] = f"local_{ext}"
    pipeline[video_id]["status"] = "needs_review"
    pipeline[video_id]["human_approved"] = False
    pipeline[video_id]["transcript_word_count"] = len(cleaned.split())
    pipeline[video_id]["notes"] = "Transcript imported locally. Ready for editorial review."
    
    save_pipeline(pipeline)
    print(f"✓ Updated pipeline status for {video_id} to 'needs_review' ({len(cleaned.split())} words).")
    print("Run 'python3 scripts/content_review.py approve " + video_id + "' to approve.")

def cmd_approve(video_id):
    pipeline = load_pipeline()
    if video_id not in pipeline:
        print(f"Error: Video ID {video_id} not in pipeline.")
        sys.exit(1)
    
    pipeline[video_id]["status"] = "published"
    pipeline[video_id]["human_approved"] = True
    pipeline[video_id]["notes"] = "Approved by editor."
    save_pipeline(pipeline)
    print(f"✓ Video {video_id} marked as APPROVED (status: published).")

def cmd_build():
    print("Rebuilding pages using updated pipeline data...")
    import subprocess
    cmd = [sys.executable, os.path.join(base_dir, "scripts/generate_video_pages.py")]
    subprocess.run(cmd, check=True)
    print("✓ Website pages rebuilt.")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "list":
        cmd_list()
    elif sys.argv[1] == "import-transcript":
        if len(sys.argv) < 4:
            print("Usage: python3 scripts/content_review.py import-transcript <video_id> <path_to_file>")
            sys.exit(1)
        cmd_import_transcript(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "approve":
        if len(sys.argv) < 3:
            print("Usage: python3 scripts/content_review.py approve <video_id>")
            sys.exit(1)
        cmd_approve(sys.argv[2])
    elif sys.argv[1] == "build":
        cmd_build()
    else:
        print("Unknown command. Options: list, import-transcript, approve, build")
