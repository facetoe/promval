from promval.subtree_extractor import AggregationGroupSubExtractor, MetricSubExtractor
from promval import ParseWalker, PromQLParser


def test_aggregation_group_subextractor():
    expr = """
        avg by (first, second)(metric{label='foo'})
    """
    root = ParseWalker()._parse(expr)
    extractor = AggregationGroupSubExtractor()
    items = extractor.extract(root)
    assert isinstance(items[0][0], PromQLParser.ByContext)
    assert items[0][1] == ["first", "second"]


def test_parsing_with_comments():
    expr = """
        avg by (first, second)(metric{label='foo'})
	    # I am a comment
        and
        avg without (third, fourth)(metric{label='bar'})
    """
    root = ParseWalker()._parse(expr)
    extractor = AggregationGroupSubExtractor()
    items = extractor.extract(root)
    print(items)


def test_aggregation_group_subextractor_multiple():
    expr = """
        avg by (first, second)(metric{label='foo'})
        and
        avg without (third, fourth)(metric{label='bar'})
    """
    ctx = ParseWalker()._parse(expr)
    left, right = ctx.vectorOperation().vectorOperation()
    extractor = AggregationGroupSubExtractor()
    items_left = extractor.extract(left)
    items_right = extractor.extract(right)
    assert isinstance(items_left[0][0], PromQLParser.ByContext) and isinstance(
        items_right[0][0], PromQLParser.WithoutContext
    )
    assert items_left[0][1] == ["first", "second"] and items_right[0][1] == [
        "third",
        "fourth",
    ]


def test_aggregation_group_subextractor_no_agg():
    expr = """
        count(metric{label='thing'})
    """
    ctx = ParseWalker()._parse(expr)
    extractor = AggregationGroupSubExtractor()
    items = extractor.extract(ctx)
    assert items == []


def test_metric_subextractor():
    expr = """
        avg by (first, second)(metric{label='thing', other!='stuff'}) / thing{ass='grass'}
    """
    ctx = ParseWalker()._parse(expr)
    extractor = MetricSubExtractor()
    items = extractor.extract(ctx)
    assert items == ["metric", "thing"]
