from promval.parser.PromQLLexer import PromQLLexer
from promval.parser.PromQLParser import PromQLParser
from promval.parser.PromQLParserListener import PromQLParserListener

from antlr4 import ParseTreeWalker, InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from promval.error import PromQLSyntaxError


class MyErrorListener(ErrorListener):
    def __init__(self):
        super(MyErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise PromQLSyntaxError(recognizer, offendingSymbol, line, column, msg, e)


class ParseWalker(PromQLParserListener):
    def _execute(self, promql):
        walker = ParseTreeWalker()
        tree = self._parse(promql)
        walker.walk(self, tree)

    def _parse(self, promql):
        input_stream = InputStream(promql)
        lexer = PromQLLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = PromQLParser(token_stream)
        parser.addErrorListener(MyErrorListener())
        return parser.expression()

    def extract_labels(self, ctx: PromQLParser.AggregationContext):
        by, without = ctx.by(), ctx.without()
        if by:
            context = by
            label_list = by.labelNameList().labelName()
        elif without:
            context = without
            label_list = without.labelNameList().labelName()
        else:
            context = ctx
            label_list = []
        labels = []
        for label in label_list:
            label_name = label.getText()
            labels.append(label_name)
        return context, labels
