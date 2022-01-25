from typing import List

from promval import ParseWalker, PromQLParser


class Extractor(ParseWalker):
    items: List = []

    def extract(self, expression):
        self._execute(expression)
        items = self.items.copy()
        self.items.clear()
        return items


class AggregationGroupExtractor(Extractor):
    def enterAggregation(self, ctx: PromQLParser.AggregationContext):
        by, without = ctx.by(), ctx.without()
        if by:
            label_list = by.labelNameList().labelName()
        elif without:
            label_list = without.labelNameList().labelName()
        else:
            label_list = []

        labels = set()
        for label in label_list:
            label_name = label.getText()
            labels.add(label_name)
        if labels:
            self.items.append(labels)
