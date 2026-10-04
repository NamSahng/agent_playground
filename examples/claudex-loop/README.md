# Claudex Loop

Claude와 Codex가 계획·구현을 교차 검토하는 실습입니다. 대상은 **단어 수 세기 함수 하나**입니다.

## 역할과 흐름

| 단계 | Claude 메인 | Codex 메인 |
| --- | --- | --- |
| 계획 확정·보완 | Claude | Codex |
| 독립 계획 검토 | Codex | Claude |
| 구현·테스트·수정 | Claude | Codex |
| 최종 검토·재검토 | 새 Codex 세션 | 새 Claude 세션 |

이 예제는 `PLAN.md` 초안에서 시작하는 `mode=review`입니다.
메인이 계획을 확정하고 검토 지적을 판단합니다. 검토자가 수정을 요구하면 메인이 고친 뒤 다시 검토받습니다.
계획 검토·수정·최종 검토는 각각 최대 2회입니다.

## 준비

로그인된 Claude Code·Codex CLI, Python 3.11 이상, Git이 필요합니다.

```sh
cd /home/nys/Desktop/agent-playground/examples/claudex-loop
bash setup.sh
```

`setup.sh`가 고정된 버전의 원본 스킬을 설치하고 Claude에 연결합니다.
다운로드 원본은 출력된 `/tmp/claudex-source.*`에 남습니다. 확인 후 해당 폴더를 삭제해도 됩니다.

반복 승인을 줄이기 위해 아래 세션 설정을 사용합니다.

- Claude: `.claude/settings.json`에 지정한 편집·검토·테스트 명령을 허용합니다.
- Codex: 작업 폴더 쓰기·네트워크를 허용하고 플러그인·앱·훅을 끕니다.
- 검토자: 읽기 전용으로 호출하며 플러그인·MCP를 제외합니다.

전역 설정은 바꾸지 않습니다. 두 서비스에 계획·코드가 전달되며 사용량이 발생합니다.
다른 경로에 복제했다면 Claude 설정의 runner 절대 경로를 바꿉니다. 첫 실행 시 폴더 신뢰 확인이 있을 수 있습니다.

## 실행

둘 중 하나를 실행한 뒤 해당 프롬프트를 대화창에 붙여 넣습니다. 두 방향을 동시에 실행하지 않습니다.

### Claude 메인

```sh
claude --permission-mode dontAsk --settings .claude/settings.json \
  --strict-mcp-config --mcp-config '{"mcpServers":{}}'
```

복사할 프롬프트: [prompts/claude.txt](prompts/claude.txt)

### Codex 메인

```sh
codex -s workspace-write -a never \
  -c sandbox_workspace_write.network_access=true \
  --disable plugins --disable apps --disable hooks
```

복사할 프롬프트: [prompts/codex.txt](prompts/codex.txt)

허용되지 않은 작업은 질문 대신 거절될 수 있습니다. 차단·실패나 예산 안에 해결하지 못한 지적은 기록하고 종료합니다.
기존 구현이 맞으면 그대로 유지하며 커밋·푸시는 하지 않습니다.

## 결과 확인

새 기록은 `output/cli-claude/<실행 ID>/` 또는 `output/cli-codex/<실행 ID>/`에 저장합니다.

| 파일 | 내용 |
| --- | --- |
| `01-plan.md` | 메인이 확정한 계획 |
| `02-plan-review-01.md` | 다른 모델의 계획 검토와 메인의 처리 |
| `03-implementation-01.md` | 변경 내용·테스트 명령·실제 출력 |
| `04-final-review-01.md` | 새 세션의 최종 검토 |
| `05-summary.md` | 최종 판정·남은 문제·기록 위치 |

재검토는 회차별 새 파일에 기록합니다. 원본 검토 입력·stdout·stderr·result.json은 `/tmp/claudex-*`에 보존합니다.
완료 기준은 **계획·최종 검토 APPROVED + 테스트 통과**입니다.

[Claude 메인 결과](output/cli-claude/20261004-172823/05-summary.md) · [Codex 메인 결과](output/cli-codex/20261004-182355-252657/05-summary.md): 양방향 검토 승인, 각 4개 테스트 통과. 기존 구현을 확인한 실행이며 코드 수정 회차는 없었습니다. Codex 실행에서 지적된 결과 링크 누락은 이 README에서 수정했습니다.

## 파일 안내

- `PLAN.md`: 함수 요구사항과 검증 기준
- `word_count.py`, `test_word_count.py`: 구현과 테스트
- `AGENTS.md`, `CLAUDE.md`: 메인 CLI가 따를 실습 절차
- `review_runner.py`: 원본 runner의 하위 폴더 경로·검토 설정 보정

루프는 메인 CLI 대화가 진행합니다. 원본 전체 흐름의 요구사항 탐색·새 계획 작성은 `mode=full`에서 다룹니다.

[원본 스킬](https://github.com/chaseai-yt/claudex-loop/tree/8cf5e2c1771c5151d90c12642391d0ba8fa71b0e) · [Claude 권한](https://code.claude.com/docs/en/permissions) · [Codex 권한](https://learn.chatgpt.com/docs/agent-approvals-security)
