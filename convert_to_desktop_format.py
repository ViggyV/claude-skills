#!/usr/bin/env python3
"""
Convert Claude Code skills to Claude Desktop format.
Claude Desktop requires:
- YAML frontmatter with name and description
- Directory structure: skill-name/Skill.md
- Optional: resources/ folder
"""

import os
import re
import shutil
from pathlib import Path

SOURCE_DIR = Path("/Users/vigneshvasan/dev/claude-skils/.claude/skills")
OUTPUT_DIR = Path("/Users/vigneshvasan/dev/claude-skils/claude-desktop-skills")

def extract_title_and_description(content):
    """Extract title from first H1 and description from content."""
    lines = content.strip().split('\n')

    title = None
    description = None

    for i, line in enumerate(lines):
        # Find first H1 header
        if line.startswith('# ') and not title:
            title = line[2:].strip()
            # Look for description in next non-empty lines
            for j in range(i + 1, min(i + 10, len(lines))):
                next_line = lines[j].strip()
                if next_line and not next_line.startswith('#') and not next_line.startswith('```'):
                    # Skip "You are..." lines, look for actual description
                    if next_line.startswith('You are'):
                        description = next_line[:197] + "..." if len(next_line) > 200 else next_line
                        break
                    elif len(next_line) > 20:
                        description = next_line[:197] + "..." if len(next_line) > 200 else next_line
                        break
            break

    # Fallback if no title found
    if not title:
        title = "Untitled Skill"

    # Generate description if not found
    if not description:
        # Try to find "This skill activates when" section
        activation_match = re.search(r'This skill activates when.*?:(.*?)(?=##|\Z)', content, re.DOTALL)
        if activation_match:
            activation_text = activation_match.group(1).strip()
            # Extract first few bullet points
            bullets = re.findall(r'[-*]\s+(.+)', activation_text)
            if bullets:
                description = f"Helps with: {', '.join(bullets[:3])}"[:200]

        if not description:
            description = f"A skill for {title.lower()} tasks and workflows."

    return title, description

def convert_skill(skill_path, output_base):
    """Convert a single skill to Claude Desktop format."""
    skill_name = skill_path.parent.name

    # Read original content
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has frontmatter
    if content.strip().startswith('---'):
        # Already has frontmatter, just copy
        new_content = content
        # Extract name from frontmatter
        name_match = re.search(r'^name:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
        if name_match:
            skill_name = name_match.group(1).strip().lower().replace(' ', '-')
    else:
        # Extract title and description
        title, description = extract_title_and_description(content)

        # Truncate for limits
        title = title[:64] if len(title) > 64 else title
        description = description[:200] if len(description) > 200 else description

        # Create YAML frontmatter
        frontmatter = f'''---
name: "{title}"
description: "{description}"
version: "1.0.0"
---

'''
        new_content = frontmatter + content

    # Create output directory
    output_skill_dir = output_base / skill_name
    output_skill_dir.mkdir(parents=True, exist_ok=True)

    # Write Skill.md
    output_file = output_skill_dir / "Skill.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    # Copy any additional resources if they exist
    resources_src = skill_path.parent / "resources"
    if resources_src.exists():
        resources_dst = output_skill_dir / "resources"
        shutil.copytree(resources_src, resources_dst, dirs_exist_ok=True)

    return skill_name

def main():
    # Clean output directory
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    # Find all SKILL.md files
    skill_files = list(SOURCE_DIR.rglob("SKILL.md"))

    converted = []
    errors = []

    for skill_path in skill_files:
        try:
            skill_name = convert_skill(skill_path, OUTPUT_DIR)
            converted.append(skill_name)
            print(f"✓ Converted: {skill_name}")
        except Exception as e:
            errors.append((skill_path, str(e)))
            print(f"✗ Error converting {skill_path}: {e}")

    print(f"\n{'='*50}")
    print(f"Converted: {len(converted)} skills")
    print(f"Errors: {len(errors)}")
    print(f"Output: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
