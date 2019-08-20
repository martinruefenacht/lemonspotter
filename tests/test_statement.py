from hypothesis import given, strategies as st
from lemonspotter.core.statement import Statement
from lemonspotter.core.statement import ReturnStatement


class Test_Statement:
    @given(comment=st.text())
    def test_statement_instantiation(self, comment: str):
        statement = Statement(comment=comment)

        assert comment.strip() == statement.comment

    @given(name=st.text())
    def test_statement_variable(self, name: str):
        statement = Statement()

        assert statement.has_variable(name) is False
        assert statement.get_variable(name) is None
