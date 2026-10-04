#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
skill_dir=.agents/skills/claudex-loop
if [[ -e "$skill_dir" ]]; then
  echo "이미 설치됨: $skill_dir"
else
  source_dir=$(mktemp -d /tmp/claudex-source.XXXXXX)
  git clone --quiet --no-checkout https://github.com/chaseai-yt/claudex-loop.git "$source_dir"
  git -C "$source_dir" checkout --quiet 8cf5e2c1771c5151d90c12642391d0ba8fa71b0e
  mkdir -p .agents/skills
  cp -R "$source_dir/skills/claudex-loop" "$skill_dir"
  echo "설치 완료: $skill_dir"
  echo "다운로드 원본: $source_dir"
fi
claude_skill=.claude/skills/claudex-loop
mkdir -p .claude/skills
if [[ ! -e "$claude_skill" && ! -L "$claude_skill" ]]; then
  ln -s ../../.agents/skills/claudex-loop "$claude_skill"
fi
if [[ ! -f "$claude_skill/SKILL.md" ]]; then
  echo "Claude 스킬 경로를 확인하세요: $claude_skill" >&2
  exit 1
fi
echo "준비 완료: README.md의 claude 또는 codex 명령으로 시작하세요."
