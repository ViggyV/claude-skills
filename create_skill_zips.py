#!/usr/bin/env python3
"""
Create ZIP files for Claude Desktop skills.
Each skill gets its own ZIP file with the correct structure:
  skill-name.zip
  └── skill-name/
      └── Skill.md
"""

import os
import zipfile
from pathlib import Path

SKILLS_DIR = Path("/Users/vigneshvasan/dev/claude-skils/claude-desktop-skills")
OUTPUT_DIR = Path("/Users/vigneshvasan/dev/claude-skils/skill-zips")

def create_skill_zip(skill_dir, output_dir):
    """Create a ZIP file for a single skill."""
    skill_name = skill_dir.name
    zip_path = output_dir / f"{skill_name}.zip"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in skill_dir.rglob('*'):
            if file_path.is_file():
                # Archive path should be: skill-name/filename
                arcname = str(file_path.relative_to(skill_dir.parent))
                zipf.write(file_path, arcname)

    return zip_path

def main():
    print("=" * 60)
    print("Claude Desktop Skills ZIP Creator")
    print("=" * 60)

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\nOutput directory: {OUTPUT_DIR}")

    # Clear existing zips
    for old_zip in OUTPUT_DIR.glob("*.zip"):
        old_zip.unlink()

    # Find all skill directories
    skill_dirs = [d for d in SKILLS_DIR.iterdir() if d.is_dir()]
    print(f"Found {len(skill_dirs)} skills")

    created = []
    failed = []
    print("\nCreating ZIP files...")

    for skill_dir in sorted(skill_dirs):
        try:
            zip_path = create_skill_zip(skill_dir, OUTPUT_DIR)
            created.append(zip_path.name)
            print(f"  ✓ {zip_path.name}")
        except Exception as e:
            failed.append((skill_dir.name, str(e)))
            print(f"  ✗ {skill_dir.name}: {e}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Successfully created: {len(created)} ZIP files")
    if failed:
        print(f"Failed: {len(failed)}")
        for name, err in failed:
            print(f"  - {name}: {err}")

    print(f"\nZIP files are ready at: {OUTPUT_DIR}")
    print("\nYou can now drag and drop these ZIP files into Claude Desktop!")

if __name__ == "__main__":
    main()
