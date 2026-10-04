"""공백으로 구분된 토큰의 개수를 센다."""


def count_words(text: str) -> int:
    """str.split() 기준으로 단어를 세며 문자열 외 입력은 거절한다."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return len(str.split(text))
