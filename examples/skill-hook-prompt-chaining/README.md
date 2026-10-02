# Skill · Hook · Prompt Chaining

메모에서 할 일을 추출하고 체크리스트를 만드는 작은 예제입니다.

| 개념 | 역할 | 파일 |
| --- | --- | --- |
| Skill | AI가 읽는 할 일 추출 지침 | [.agents/skills/notes-to-tasks/SKILL.md](.agents/skills/notes-to-tasks/SKILL.md) |
| Hook | 요청 제출 시 Python 코드로 로그 기록 | [루트 설정](../../.codex/hooks.json), [log_prompt.py](hooks/log_prompt.py) |
| Prompt Chaining | A의 결과를 B의 입력으로 전달 | [run.sh](run.sh) |

프롬프트 체이닝은 앞선 AI 호출의 결과를 다음 호출의 입력으로 전달하는 방식으로, Bash 스크립트, Python 코드, LangGraph 같은 라이브러리, 워크플로우 도구, CI 작업 등으로 구현할 수 있습니다. 여기서는 Bash로 두 Codex 작업을 연결합니다.

## 준비

로그인된 Codex CLI, Python 3, Git, Bash가 필요합니다.
저장소 루트에서 다음을 실행합니다.

```sh
cd examples/skill-hook-prompt-chaining
codex
```

`/skills`에서 `notes-to-tasks`를 확인하고, `/hooks`에서 실습용 `UserPromptSubmit` Hook을 확인·신뢰합니다.
설정을 마쳤으면 CLI를 종료하고 같은 터미널에서 아래 실습을 진행합니다.

## 실행

```sh
bash run.sh
```

스크립트는 다음 순서로 실행합니다.

1. **Codex A:** Skill을 사용해 `notes.txt`에서 할 일을 JSON으로 추출
2. **Python 검사:** JSON 배열과 필드 형식 확인. 실패하면 중단
3. **Codex B:** A의 JSON을 입력받아 Markdown 체크리스트 작성

A와 B는 별도의 `codex exec` 실행입니다. Bash가 A의 완료를 기다린 뒤 결과를 B에 전달합니다.
실행마다 `output/run.XXXXXX/` 폴더를 만들어 이전 결과와 섞이지 않게 합니다.
모델과 추론 수준은 현재 Codex 설정을 사용하며, 두 번의 실행이 계정 사용량을 씁니다.

## 결과 확인

완료 시 표시되는 폴더에서 `tasks.json`과 `checklist.md`를 확인합니다.
체크리스트는 다음과 같은 형태입니다. 문구는 실행마다 조금 다를 수 있습니다.

```markdown
- [ ] 민수: 로그인 오류 수정 (기한: 금요일)
- [ ] 지연: 도움말 초안 작성 (기한: 미정)
```

지연의 기한을 추측하지 않았는지, 배포 날짜 논의를 확정된 할 일에 넣지 않았는지 확인합니다.
`notes.txt`를 바꾸고 다시 실행하면 결과를 비교할 수 있습니다.

Hook 로그는 별도로 확인합니다.

```sh
cat output/hook-events.jsonl
```

Hook은 루트에 등록되어 이 저장소의 다른 작업에도 적용됩니다. 실습 후 `/hooks`에서 끌 수 있습니다.
로그가 없으면 Hook의 신뢰·활성화 상태를 확인합니다. Bash 체이닝과 Hook 실행은 별개의 기능입니다.

[실행 결과 예시](result.md) · [Skills](https://learn.chatgpt.com/docs/build-skills) · [Hooks](https://learn.chatgpt.com/docs/hooks) · [codex exec](https://learn.chatgpt.com/docs/non-interactive-mode)
