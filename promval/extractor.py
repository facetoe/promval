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
        _, labels = self.extract_labels(ctx)
        if labels:
            self.items.append(labels)
