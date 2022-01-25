from typing import Set

from promval.error import Error
from promval.parser.PromQLParser import PromQLParser
from promval.validators import Validator


class AggregationGroupValidator(Validator):
    def __init__(self, expected: Set[str]):
        self.expected = expected

    def enterAggregation(self, ctx: PromQLParser.AggregationContext):
        by, without = ctx.by(), ctx.without()
        if by:
            context = by
            label_list = by.labelNameList()
        else:
            context = without
            label_list = without.labelNameList()

        groupings = set()
        for label in label_list.labelName():
            label_name = label.getText()
            groupings.add(label_name)

        missing = self.expected.difference(groupings)
        if missing:
            message = f"missing required metric names {missing}"
            self.errors.append(Error(context, message))


class AggregationLabelValueValidator(Validator):
    def __init__(self, label_value: str):
        self.target_label_value = label_value
        self.stack = []

    def enterLabelMatcherList(self, ctx: PromQLParser.LabelMatcherListContext):
        for label in ctx.labelMatcher():
            label_name = label.labelName().getText()
            label_value = label.STRING().getText()
            label_value = label_value[1:-1]  # strip quotes
            if label_value == self.target_label_value:
                labels, context = self.stack[-1]
                if label_name not in labels:
                    message = f"expected label name '{label_name}' in group clause"
                    self.errors.append(Error(context, message=message))

    def enterAggregation(self, ctx: PromQLParser.AggregationContext):
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
        self.stack.append((labels, context))
