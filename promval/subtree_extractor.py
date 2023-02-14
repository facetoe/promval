from typing import List

from antlr4 import ParserRuleContext
from promval import ParseWalker, PromQLParser


class SubtreeExtractor(ParseWalker):
    items: List = []

    def extract(self, ctx: ParserRuleContext):
        self._walk(ctx)
        items = self.items.copy()
        self.items.clear()
        return items

class AggregationGroupSubExtractor(SubtreeExtractor):
    def enterAggregation(self, ctx: PromQLParser.AggregationContext) -> None:
        agg_ctx, labels = self.extract_labels(ctx)
        if agg_ctx and labels:
            self.items.append((agg_ctx, labels))

class MetricSubExtractor(SubtreeExtractor):
    def enterInstantSelector(self, ctx: PromQLParser.InstantSelectorContext) -> None:
        metric_name = ctx.METRIC_NAME().getText()
        self.items.append(metric_name)
