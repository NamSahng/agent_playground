#!/usr/bin/env bash
set -euo pipefail

# 어디에서 실행하든 이 예제 폴더를 기준으로 작업한다.
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
for dependency in codex python3 git; do
  command -v "$dependency" >/dev/null || { echo "필요한 명령: $dependency" >&2; exit 1; }
done
mkdir -p output
run_dir=$(mktemp -d "$PWD/output/run.XXXXXX")
trap 'echo "중단됐습니다. 중간 결과 확인: $run_dir" >&2' ERR

echo "[A] 메모 → 할 일 JSON"
# 작은따옴표로 $notes-to-tasks가 Bash 변수로 해석되는 것을 막는다.
# -o는 모델의 최종 응답을 파일에 저장한다.
codex exec --sandbox read-only -o "$run_dir/tasks.json" \
  '$notes-to-tasks notes.txt를 읽고 확정된 할 일을 추출해줘. 최종 응답은 JSON 배열만 출력해줘. 코드 펜스나 설명은 넣지 말고 파일은 직접 수정하지 마.'

echo "[검사] JSON과 필드 형식 확인"
python3 - "$run_dir/tasks.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as file:
    tasks = json.load(file)
if not isinstance(tasks, list):
    raise SystemExit("JSON 배열이 필요합니다.")
for task in tasks:
    if not isinstance(task, dict) or set(task) != {"task", "owner", "due"}:
        raise SystemExit("각 항목에는 task, owner, due 필드가 필요합니다.")
    if not isinstance(task["task"], str) or not task["task"].strip():
        raise SystemExit("task는 빈 문자열이 아니어야 합니다.")
    if any(task[key] is not None and not isinstance(task[key], str) for key in ("owner", "due")):
        raise SystemExit("owner와 due는 문자열 또는 null이어야 합니다.")
print(f"통과: {len(tasks)}개 작업")
PY

echo "[B] A의 JSON → 체크리스트"
# A의 결과 파일을 B의 표준 입력으로 전달한다. 이전 세션을 재개하지 않는다.
codex exec --sandbox read-only -o "$run_dir/checklist.md" \
  '표준 입력으로 받은 JSON만 사용해 체크리스트를 만들어줘. 각 항목은 "- [ ] 담당자: 할 일 (기한: 값)" 형식으로 작성해줘. 담당자나 기한이 null이면 "미정"으로 표시해줘. 빈 배열이면 "할 일 없음"으로 출력해줘. 최종 응답은 Markdown 본문만 출력하고 코드 펜스나 설명은 넣지 마. 도구 사용이나 파일 수정은 필요 없어.' \
  < "$run_dir/tasks.json"

test -s "$run_dir/checklist.md"
echo "완료: $run_dir"
cat "$run_dir/checklist.md"
