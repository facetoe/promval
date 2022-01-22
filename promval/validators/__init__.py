from typing import List

from antlr4 import ParseTreeWalker, InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from promval.error import ValidationError, PromQLSyntaxError
from promval.parser.PromQLLexer import PromQLLexer
from promval.parser.PromQLParser import PromQLParser
from promval.parser.PromQLParserListener import PromQLParserListener


class MyErrorListener(ErrorListener):
    def __init__(self):
        super(MyErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise PromQLSyntaxError(recognizer, offendingSymbol, line, column, msg, e)


class Validator(PromQLParserListener):
    errors: List = []

    def validate(self, expression):
        walker = ParseTreeWalker()
        tree = self._parse(expression)
        walker.walk(self, tree)
        errors = self.errors.copy()
        self.errors.clear()
        if errors:
            raise ValidationError("\n".join(map(str, errors)))

    def _parse(self, promql):
        input_stream = InputStream(promql)
        lexer = PromQLLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = PromQLParser(token_stream)
        parser.addErrorListener(MyErrorListener())
        return parser.expression()
