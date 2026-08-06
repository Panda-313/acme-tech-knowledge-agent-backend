import unittest

from src.refusal_detection import detect_refusal


class DetectRefusalTests(unittest.TestCase):
    def test_does_not_flag_phrase_crossing_word_boundary(self) -> None:
        answer = (
            "Domyślny model pracy zdalnej jest hybrydowy; "
            "szczególnie dotyczy to ról senior IC."
        )
        self.assertFalse(detect_refusal(answer, ["functions.search_docs"]))

    def test_flags_explicit_refusal_phrase(self) -> None:
        answer = "To nie dotyczy tego tematu."
        self.assertTrue(detect_refusal(answer, ["functions.search_docs"]))

    def test_flags_empty_answer_without_tools(self) -> None:
        self.assertTrue(detect_refusal("", []))


if __name__ == "__main__":
    unittest.main()
