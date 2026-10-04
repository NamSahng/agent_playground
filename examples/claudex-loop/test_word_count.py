import unittest

from word_count import count_words


class WordCountTests(unittest.TestCase):
    def test_count(self):
        cases = [
            ("", 0),
            (" \t\n ", 0),
            ("hello world", 2),
            ("안녕 세상", 2),
            ("  hello\t\n world  ", 2),
            ("hello, world!", 2),
            ("hello-world", 1),
            ("안녕\u3000세상", 2),
            ("hello\u00a0world", 2),
            ("hello\u200bworld", 1),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(count_words(text), expected)

    def test_reject_non_strings(self):
        for value in (None, 123, b"hello world", ["hello", "world"]):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    count_words(value)

    def test_string_subclass(self):
        class Text(str):
            pass

        self.assertEqual(count_words(Text("hello world")), 2)

    def test_string_subclass_overriding_split(self):
        class Text(str):
            def split(self, *args, **kwargs):
                return []

        self.assertEqual(count_words(Text("hello world")), 2)


if __name__ == "__main__":
    unittest.main()
