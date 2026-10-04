# 확정 계획

담당 CLI: Codex (현재 호스트 대화)
확인 가능한 모델: 정확한 호스트 모델 ID는 런타임에서 확인되지 않음
시각: 2026-10-04T18:23:55.252657+09:00

## 실행 설정

host=codex, builder=codex, mode=review, rounds=2; reviewer=claude, inspector=claude (새 세션). 계획 검토 최대 2회, 수정 최대 2회, 최종 검토 최대 2회. 요청 모델·추론 수준: 지정 없음, 각 CLI 기본값. 독립 검토를 생략하지 않음.

계획·관련 코드의 검토 서비스 전달 및 구현·테스트·수정은 사용자 승인 범위다. 커밋·푸시는 금지한다.

## 확인한 전제와 결정

- 요구사항과 성공 기준: PLAN.md.
- 실습 절차·runner·기록 형식: AGENTS.md 및 설치된 claudex-loop/SKILL.md와 references/runtime.md, references/build.md.
- word_count.py는 입력 확인과 len(str.split(text))를 이미 구현했다. test_word_count.py는 기대 결과 10건, 거절 입력 4종, 하위 클래스 2종을 검증한다. 요구사항을 충족하는 기존 코드는 유지한다.
- Python 3.11.5, Claude Code 2.1.289 (/home/nys/.local/bin/claude) 확인. Claude 모델 ID는 실제 응답에서 확인한다.
- 예제 전체는 Git에서 미추적 상태이며 루트 README.md에도 기존 수정이 있다. 기존 작업은 보존하고 이번 실행 변경과 구분한다. 최종 검토 스냅샷에는 기존 미추적 예제 파일도 포함되며 output은 제외된다.
- 위험·한계: 읽기 전용 검토자는 테스트를 실행할 수 없으므로 Codex가 합의된 명령을 직접 실행한다. 검토 승인은 전수 정확성 증명이 아니다.

## 확정한 PLAN.md 전문

# 단어 수 세기

## 목표

`word_count.py`에 `count_words(text: str) -> int`를 구현하고, `test_word_count.py`로 검증한다.
함수 하나를 대상으로 Claudex Loop의 계획 검토·구현·교차 검토를 실습한다.

## 요구사항

- Python `str.split()`의 공백 규칙으로 토큰 수를 센다. 연속 공백·탭·줄바꿈을 처리한다.
- 빈 문자열과 공백뿐인 문자열은 0이다.
- 구두점·하이픈은 제거하지 않는다. 형태소 분석은 하지 않는다.
- 문자열 이외 입력(`None`, 정수, `bytes`, 리스트)은 `TypeError`로 거절한다.
- `str` 하위 클래스는 허용한다. 재정의된 `split()`을 우회하도록 `str.split(text)`를 사용한다.
- 외부 패키지·파일 입출력·웹 호출은 사용하지 않는다.

## 구현 방법과 범위

- `isinstance(text, str)`로 입력을 확인하고, 문자열 외 입력은 `TypeError`를 발생시킨다.
- `len(str.split(text))`로 토큰 수를 반환한다. Python 내장 공백 규칙을 사용하며 별도 정규화는 하지 않는다.
- 변경 대상은 `word_count.py`와 `test_word_count.py`다. 현재 코드가 요구사항을 충족하면 그대로 유지한다.
- 테스트는 아래 기대 결과와 네 종류의 비문자열 입력, 일반 `str` 하위 클래스 및 `split()`을 재정의한 하위 클래스를 검증한다.
- Python 표준 라이브러리와 `unittest`만 사용한다. CLI 검토 호출은 실습 절차이며 함수의 외부 호출 금지와 별개다.

## 기대 결과

| 입력 | 결과 |
| --- | --- |
| `""`, `" \t\n "` | 0 |
| `"hello world"`, `"안녕 세상"` | 2 |
| `"  hello\t\n world  "` | 2 |
| `"hello, world!"` | 2 |
| `"hello-world"` | 1 |
| `"안녕\u3000세상"`, `"hello\u00a0world"` | 2 |
| `"hello\u200bworld"` | 1 |
| `str` 하위 클래스의 `"hello world"` | 2 |
| `split()`이 `[]`를 반환하는 하위 클래스의 `"hello world"` | 2 |

## 검증

이 예제 폴더에서 실행한다.

```sh
python3 -m unittest discover -s . -p 'test_*.py' -v
```

위 정상·예외 사례를 검증하고 모든 테스트가 통과해야 한다.
메인이 직접 테스트를 실행한 뒤, 구현자와 다른 모델의 새 세션이 최종 코드를 검토한다.
