from hypothesis import given, strategies as st
from pytest import raises

from lemonspotter.core.statement import Statement
from lemonspotter.core.statement import BlockStatement
from lemonspotter.core.statement import ReturnStatement


class TestStatement:
    @given(comment=st.text())
    def test_statement_instantiation(self, comment: str) -> None:
        statement = Statement(comment=comment)

        assert comment.strip() == statement.comment

    @given(name=st.text())
    def test_statement_variable(self, name: str) -> None:
        statement = Statement()

        assert statement.has_variable(name) is False
        assert statement.get_variable(name) is None


class TestBlockStatement:
    @given(comment=st.text())
    def test_statement_instantiation(self, comment: str) -> None:
        statement = BlockStatement(comment=comment)

        assert comment.strip() == statement.comment

# class DeclarationStatement:
#     @given(comment=st.text())
#     def test_instantiation(self, variable, comment):
#         statement = DeclarationStatement(variable, comment)
