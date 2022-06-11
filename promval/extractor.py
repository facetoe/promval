from typing import List

from promval import ParseWalker, PromQLParser
from promval.types import Label


class Extractor(ParseWalker):
    items: List = []

    def extract(self, expression):
        self._execute(expression)
        items = self.items.copy()
        self.items.clear()
        return items


class AggregationGroupExtractor(Extractor):
    def enterAggregation(self, ctx: PromQLParser.AggregationContext):
        _, labels = self.extract_labels(ctx)
        if labels:
            self.items.append(labels)


class LabelExtractor(Extractor):
    def enterLabelMatcherList(self, ctx: PromQLParser.LabelMatcherListContext):
        labels = []
        for matcher in ctx.labelMatcher():
            name = matcher.labelName().getText()
            operator = matcher.labelMatcherOperator().getText()
            value = matcher.STRING().getText()
            labels.append(Label(name, operator, value))
        self.items.append(labels)
