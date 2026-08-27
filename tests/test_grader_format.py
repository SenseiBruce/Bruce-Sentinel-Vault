from grader_format import format_grader_text


def test_format_grader_text_lists_verdicts():
    text = format_grader_text(
        [
            {"title": "RBI pause", "source": "Mint", "verdict": "PASSED"},
            {"title": "Fake tax slab", "verdict": "FAILED"},
        ]
    )
    assert text == "PASSED: RBI pause (Mint)\nFAILED: Fake tax slab"
