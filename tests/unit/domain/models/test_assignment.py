"""
Test For Assignment Model
"""
import datetime

from heimdallr.domain.models.assignment import Assignment


class TestAssignment:
    def test_assignment(self):
        """
        Test for Assignment Model instantiation.
        """
        author = "author"
        title = "title"
        content = ["content"]

        assignment = Assignment(author=author, title=title, content=content, date=datetime.date.today())

        assert assignment.id is not None
        assert assignment.author == author
        assert assignment.title == title
        assert assignment.content == content
        assert assignment.date == datetime.date.today()
