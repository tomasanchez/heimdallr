"""
Formatting utilities tests.
"""
from heimdallr.utils.formatting import (
    contains_letters_or_numbers,
    normalize_sentence,
    to_camel,
)


class TestToCamel:
    """
    Formatting utilities tests cases.
    """

    def test_to_camel_snake_case(self):
        """
        GIVEN a string in snake case
        WHEN the string is translated to camel case
        THEN assert the string is translated correctly
        """
        foo = "foo_bar"

        assert to_camel(foo) == "fooBar"

    def test_to_camel_with_hyphen(self):
        """
        GIVEN a string in kebab case
        WHEN the string is translated to camel case
        THEN assert the string is translated correctly
        """
        foo = "foo-bar"

        assert to_camel(foo) == "fooBar"

    def test_to_camel_with_space(self):
        """
        GIVEN a string in space case
        WHEN the string is translated to camel case
        THEN assert the string is translated correctly
        """
        foo = "foo bar"

        assert to_camel(foo) == "fooBar"

    def test_to_camel_with_mixed_case(self):
        """
        GIVEN a string in mixed case
        WHEN the string is translated to camel case
        THEN assert the string is translated correctly
        """
        foo = "fOoBaR"

        assert to_camel(foo) == "foobar"

    def test_to_camel_with_multiple_separators(self):
        """
        GIVEN a string with multiple separators
        WHEN the string is translated to camel case
        THEN assert the string is translated correctly
        """
        foo = "foo_bar-baz"

        assert to_camel(foo) == "fooBarBaz"


class TestContainsAlphanumeric:
    def test_contains_alphanumeric(self):
        """
        GIVEN a string with alphanumeric characters
        WHEN the string is checked for alphanumeric characters
        THEN assert the string contains alphanumeric characters
        """
        foo = "foo123"

        assert contains_letters_or_numbers(foo)

    def test_contains_non_alphanumeric(self):
        """
        GIVEN a string with non-alphanumeric characters
        WHEN the string is checked for alphanumeric characters
        THEN assert the string does not contain alphanumeric characters
        """
        foo = "!@#%"

        assert not contains_letters_or_numbers(foo)

    def test_contains_alphanumeric_and_non_alphanumeric(self):
        """
        GIVEN a string with alphanumeric and non-alphanumeric characters
        WHEN the string is checked for alphanumeric characters
        THEN assert the string contains alphanumeric characters
        """
        foo = "foo123!@#%"

        assert contains_letters_or_numbers(foo)


class TestTextNormalizing:
    def test_normalize_sentence(self):
        """
        GIVEN a sentence that has been split into multiple lines
        WHEN the sentence is normalized
        THEN assert the sentence is normalized correctly
        """
        sentence = "This is a sentence.\nThis is another sentence."

        assert normalize_sentence(sentence) == "This is a sentence.\nThis is another sentence."

    def test_normalize_sentence_with_lowercase(self):
        """
        GIVEN a sentence that has been split into multiple lines
        WHEN the sentence is normalized
        THEN assert the sentence is normalized correctly
        """
        sentence = "This is a sentence\nthat is continued into another line."

        assert normalize_sentence(sentence) == "This is a sentence that is continued into another line."

    def test_normalize_sentence_with_lowercase_and_uppercase(self):
        """
        GIVEN a sentence that has been split into multiple lines
        WHEN the sentence is normalized
        THEN assert the sentence is normalized correctly
        """
        line_0 = "This is a sentence\nthat is continued into another line."
        line_1 = " THIS SENTENCE IS CAPITALIZED IN THE SAME LINE."
        line_2 = "\nHowever, this uses another line."

        sentence = line_0 + line_1 + line_2

        assert normalize_sentence(sentence) != sentence

    def test_normalize_sentence_does_not_include_empty_line(self):
        """
        GIVEN a sentence that has been split into multiple lines
        WHEN the sentence is normalized
        THEN assert the sentence is normalized correctly
        """
        line_0 = "This is a line."
        line_1 = "\n  \n"
        line_2 = "This is another line."

        sentence = line_0 + line_1 + line_2

        assert normalize_sentence(sentence) == "This is a line.\nThis is another line."
