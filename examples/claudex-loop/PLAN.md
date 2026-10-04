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
