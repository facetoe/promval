from typing import Set

from promval.error import Error
from promval.parser.PromQLParser import PromQLParser
from promval.validators import Validator


class ByGroupValidator(Validator):
    def __init__(self, expected: Set[str]):
        self.expected = expected

    def enterBy(self, ctx: PromQLParser.ByContext):
        groupings = set()
        for label in ctx.labelNameList().labelName():
            groupings.add(str(label.METRIC_NAME().getText()))

        missing = self.expected.difference(groupings)
        if missing:
            message = f"missing required metric names {missing}"
            self.errors.append(Error(ctx, message))


class ByLabelValueValidator(Validator):
    def __init__(self, label_value: str):
        self.target_label_value = label_value
        self.stack = []

    def enterLabelMatcherList(self, ctx: PromQLParser.LabelMatcherListContext):
        for label in ctx.labelMatcher():
            label_name = label.labelName().METRIC_NAME().getText()
            label_value = label.STRING().getText()
            label_value = label_value[1:-1]  # strip quotes
            if label_value == self.target_label_value:
                by_labels, by_ctx = self.stack[-1]
                if label_name not in by_labels:
                    message = f"expected label name '{label_name}' in by clause"
                    self.errors.append(Error(by_ctx, message=message))

    def exitLabelMatcherList(self, ctx: PromQLParser.LabelMatcherListContext):
        self.stack.pop()

    def enterBy(self, ctx: PromQLParser.ByContext):
        by_labels = set()
        for label in ctx.labelNameList().labelName():
            by_labels.add(str(label.METRIC_NAME()))
        self.stack.append((by_labels, ctx))
