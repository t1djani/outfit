#!/usr/bin/env bash
# validate-draft.sh — deterministic FORM check for an outfit-generated draft
# (a skill SKILL.md or an agent .md). It checks structure only, never quality:
#   1. a YAML frontmatter block delimited by `---` at the top
#   2. a `name:` that is a non-empty kebab-case slug
#   3. a non-empty `description:`
# Content quality stays a human/model call. Determinism stops at form.
#
# Usage: hooks/validate-draft.sh <draft-file>
# Exit:  0 = well-formed · 1 = problems found · 2 = bad invocation

set -u

file="${1:-}"
if [ -z "$file" ] || [ ! -f "$file" ]; then
  echo "validate-draft: need a readable draft file (got: '${file}')" >&2
  exit 2
fi

problems=0
fail() { echo "  ✗ $1" >&2; problems=$((problems + 1)); }

echo "outfit · validating draft: $file"

# 1. frontmatter block: first non-empty line is '---', and a closing '---' exists after it
first="$(grep -nE '\S' "$file" | head -n1)"
if [ "${first#*:}" != "---" ]; then
  fail "no YAML frontmatter — draft must start with a '---' block"
fi
# closing delimiter: at least two '---' lines total
delims="$(grep -cE '^---[[:space:]]*$' "$file")"
if [ "$delims" -lt 2 ]; then
  fail "frontmatter not closed — need an opening and a closing '---'"
fi

# 2. name: non-empty kebab-case slug
name_line="$(grep -m1 -E '^name:' "$file" || true)"
if [ -z "$name_line" ]; then
  fail "missing 'name:' in frontmatter"
else
  name_val="$(printf '%s' "$name_line" | sed -E 's/^name:[[:space:]]*//; s/[[:space:]]*$//')"
  if [ -z "$name_val" ]; then
    fail "'name:' is empty"
  elif ! printf '%s' "$name_val" | grep -qE '^[a-z0-9]+(-[a-z0-9]+)*$'; then
    fail "'name:' must be kebab-case (lowercase, digits, hyphens): got '${name_val}'"
  fi
fi

# 3. description: non-empty
desc_line="$(grep -m1 -E '^description:' "$file" || true)"
if [ -z "$desc_line" ]; then
  fail "missing 'description:' in frontmatter"
else
  desc_val="$(printf '%s' "$desc_line" | sed -E 's/^description:[[:space:]]*//; s/[[:space:]]*$//')"
  [ -z "$desc_val" ] && fail "'description:' is empty"
fi

if [ "$problems" -eq 0 ]; then
  echo "  ✓ well-formed draft"
  exit 0
fi
echo "validate-draft: ${problems} problem(s)" >&2
exit 1
