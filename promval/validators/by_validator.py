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
            groupings.add(str(label.METRIC_NAME()))

        missing = self.expected.difference(groupings)
        if missing:
            message = f"missing required metric names {missing}"
            self.errors.append(Error(ctx, message))
