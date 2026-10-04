# 01 — 확정 계획

- 담당 CLI: Claude Code (메인·계획자·구현자)
- 모델: Claude Opus 5.5 (`claude-opus-5-5`, 메인 세션 런타임 기준)
- 시각: 2026-10-04 17:28 KST
- 실행 설정: host=claude, builder=claude, mode=review, 계획 검토·수정·최종 검토 각 최대 2회
- 검토자: Codex CLI 0.160.0 (모델은 개인 config 기본값 전달, 명시 지정 없음)
- 구현 전 Git HEAD: `0d32d3ac08bc55302cde90b343c1dce0de1ee17b` (예제 폴더 전체가 미추적 상태)

## 확정 내용

계획 파일은 `PLAN.md`이며 수정하지 않았다. 메인이 `PLAN.md`, `word_count.py`, `test_word_count.py`를 읽고 확인한 결과
목표·요구사항·기대 결과 표·검증 명령이 모두 구체적이어서 보완할 중대한 공백이 없다고 판단했다.

### 메인 확인 사항 (recon)

- `word_count.py`는 이미 `isinstance(text, str)` 검사 후 `len(str.split(text))`를 반환한다. 요구사항과 일치한다.
- `test_word_count.py`는 기대 결과 표의 정상 사례 10개, 비문자열 4종 `TypeError`, `str` 하위 클래스, `split()` 재정의 하위 클래스를 검증한다.
- 따라서 구현 단계는 "이미 정확한 코드는 유지"(AGENTS.md) 원칙에 따라 검토 지적이 없으면 변경 없이 테스트로 확인한다.

### 계획 본문 (PLAN.md 그대로)

- 목표: `word_count.py`에 `count_words(text: str) -> int` 구현, `test_word_count.py`로 검증.
- 요구사항: `str.split()` 공백 규칙, 빈/공백 문자열 0, 구두점·하이픈 유지, 비문자열(`None`, 정수, `bytes`, 리스트) `TypeError`, `str` 하위 클래스 허용 및 `str.split(text)`로 재정의 우회, 외부 패키지·파일 I/O·웹 호출 없음.
- 기대 결과: `""`, `" \t\n "` → 0 / `"hello world"`, `"안녕 세상"`, `"  hello\t\n world  "`, `"hello, world!"` → 2 / `"hello-world"` → 1 / `"안녕　세상"`, `"hello world"` → 2 / `"hello​world"` → 1 / 하위 클래스 `"hello world"` → 2 / `split()`이 `[]`를 반환하는 하위 클래스 → 2.
- 검증: 예제 폴더에서 `python3 -m unittest discover -s . -p 'test_*.py' -v`, 모든 테스트 통과.
