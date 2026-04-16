#!/usr/bin/env python3
"""
Generate agents/openai.yaml for all agency-* skills so Codex CLI
can auto-invoke them based on context (allow_implicit_invocation: true).
Run this if you add new skills or pull updates.
"""
import os, re

skills_dir = os.path.join(os.path.dirname(__file__), '..', 'skills')
skills_dir = os.path.abspath(skills_dir)

def get_field(content, field):
    m = re.search(rf'^{field}:\s*(.+)$', content, re.MULTILINE)
    return m.group(1).strip().strip('"') if m else ""

def truncate(s, max_len):
    return s[:max_len-1] + "…" if len(s) > max_len else s

count = 0
for skill_name in sorted(os.listdir(skills_dir)):
    if not skill_name.startswith("agency-"):
        continue
    skill_dir = os.path.join(skills_dir, skill_name)
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        continue

    with open(skill_md) as f:
        content = f.read()

    name = get_field(content, "name")
    description = get_field(content, "description")
    short_desc = truncate(description, 64)
    display_name = name.replace("agency-", "").replace("-", " ").title()
    default_prompt = f'Use ${name} to help with: {truncate(description, 80)}'

    agents_dir = os.path.join(skill_dir, "agents")
    os.makedirs(agents_dir, exist_ok=True)

    yaml_path = os.path.join(agents_dir, "openai.yaml")
    with open(yaml_path, "w") as f:
        f.write(f'''interface:
  display_name: "{display_name}"
  short_description: "{short_desc}"
  default_prompt: "{default_prompt}"

policy:
  allow_implicit_invocation: true
''')
    count += 1

print(f"Generated openai.yaml for {count} skills")
