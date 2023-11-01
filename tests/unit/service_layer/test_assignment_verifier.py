"""
Unit test for the AssignmentVerifier class.
"""
from heimdallr.domain.models.assignment import Assignment
from heimdallr.service_layer.assignment_verifier import AssignmentVerifier


class TestAssignmentVerifier:
    SENTENCE = "This is a sentence."

    def test_compare_same_sentence(self, assignment_verifier: AssignmentVerifier):
        """
        GIVEN two sentences
        WHEN the verifier compares them
        THEN it should return a SentenceCompared event.
        """
        # given a sentence

        # when
        result = assignment_verifier.compare_sentence(
            self.SENTENCE,
            entry_sentence=self.SENTENCE,
        )

        # then
        assert result.present == self.SENTENCE
        assert result.compared == self.SENTENCE
        assert result.plagiarism == 1.0

    def test_compare_different_sentence(self, assignment_verifier: AssignmentVerifier):
        """
        GIVEN two sentences
        WHEN the verifier compares them
        THEN it should return a SentenceCompared event.
        """
        # given
        sentence = "This is a sentence."
        entry_sentence = "This is another sentence."

        # when
        result = assignment_verifier.compare_sentence(sentence, entry_sentence=entry_sentence)

        # then
        assert result.present == sentence
        assert result.compared == entry_sentence
        assert 0.0 <= result.plagiarism < 1.0

    def test_assignment_comparison(self, assignment_verifier: AssignmentVerifier):
        """
        GIVEN two assignments
        WHEN the verifier compares them
        THEN it should return a AssignmentCompared event.
        """
        # given
        assignment = Assignment(content=[self.SENTENCE])
        entry = assignment.model_copy()

        # when
        result = assignment_verifier.compare_assignments(assignment, entry)

        # then
        assert result.id == assignment.id
        assert result.author == assignment.author
        assert result.plagiarism == 1.0
