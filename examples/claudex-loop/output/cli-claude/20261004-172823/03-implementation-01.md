# 03 — 구현 1회차

- 담당 CLI: Claude Code (메인·구현자)
- 모델: Claude Opus 5.5 (`claude-opus-5-5`)
- 시각: 2026-10-04 17:29 KST
- 구현 전 Git HEAD: `0d32d3ac08bc55302cde90b343c1dce0de1ee17b`

## 변경 파일

없음. `word_count.py`, `test_word_count.py`를 수정하지 않았다.

## 설명

- 승인된 계획(`PLAN.md`, SHA256 `8740794969a647f2e30306124e125a1fa3f7c32152e0e0ef8cd600b6a33d971b`)과 기존 코드를 대조했다.
  - `word_count.py`: `isinstance(text, str)`가 아니면 `TypeError`, 맞으면 `len(str.split(text))` — 공백 규칙·하위 클래스 허용·`split()` 재정의 우회·외부 의존 없음 요구를 모두 충족.
  - `test_word_count.py`: 기대 결과 표의 정상 사례 10개(빈 문자열·공백류·한글·구두점·하이픈·U+3000·U+00A0·U+200B), 비문자열 4종(`None`, `123`, `b"hello world"`, 리스트), 하위 클래스, `split()`이 `[]`를 반환하는 하위 클래스를 모두 검증.
- AGENTS.md의 "이미 정확한 코드는 유지" 원칙에 따라 변경하지 않았다.
- 참고: 예제 폴더 전체가 Git 미추적(`?? ./`) 상태이므로 `--base` 대비 추적 diff는 비어 있고, 검토 스냅샷은 미추적 파일 목록으로 구성된다.

## 테스트

명령 (예제 폴더에서 실행):

```sh
python3 -m unittest discover -s . -p 'test_*.py' -v
```

실제 출력:

```text
test_count (test_word_count.WordCountTests.test_count) ... ok
test_reject_non_strings (test_word_count.WordCountTests.test_reject_non_strings) ... ok
test_string_subclass (test_word_count.WordCountTests.test_string_subclass) ... ok
test_string_subclass_overriding_split (test_word_count.WordCountTests.test_string_subclass_overriding_split) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
```

환경: Python 3.11.5.
