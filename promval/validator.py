from typing import List

from promval import ParseWalker
from promval.error import ValidationError

from typing import Set

from promval.error import Error
from promval.parser.PromQLParser import PromQLParser


class Validator(ParseWalker):
    errors: List = []

    def validate(self, expression):
        self._execute(expression)
        errors = self.errors.copy()
        self.errors.clear()
        if errors:
            message = "\n" + "\n".join(map(str, errors))
            raise ValidationError(message)


class AggregationGroupValidator(Validator):
    def __init__(self, expected: Set[str]):
        self.expected = expected

    def enterAggregation(self, ctx: PromQLParser.AggregationContext):
        context, labels = self.extract_labels(ctx)
        missing = self.expected.difference(labels)
        if missing:
            message = f"missing required metric names {missing} in group clause"
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
        context, labels = self.extract_labels(ctx)
        self.stack.append((labels, context))
