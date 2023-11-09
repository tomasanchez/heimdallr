"""
Text Processing Adapters.
"""

from sklearn.base import TransformerMixin


def clean_text(text: str) -> str:
    """
    Applies some pre-processing on the given text.

    Args:
        text (str): A text to be processed.

    Returns:
        str: The processed text.
    """
    text = text.strip().replace("\n", " ").replace("\r", " ")
    return text.lower()


class CleanTextTransformer(TransformerMixin):
    def transform(self, x: list[str], y=None, **transform_params) -> list[str]:
        """
        Performs a transformation on a list of texts.

        Returns:
            list[str]: The transformed texts.
        """
        return [clean_text(text) for text in x]

    def fit(self, x, y=None, **fit_params):
        """
        Fits the transformer - no action needed.
        """
        return self
