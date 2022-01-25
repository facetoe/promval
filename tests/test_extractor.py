from promval.extractor import AggregationGroupExtractor


def test_aggregation_group_extractor():
    expr = """
        avg by (first, second)(metric{label='thing'})
    """
    extractor = AggregationGroupExtractor()
    items = extractor.extract(expr)
    assert items == [["first", "second"]]


def test_aggregation_group_extractor_multiple():
    expr = """
        avg by (first, second)(metric{label='thing'})
        and
        avg by (third, fourth)(metric{label='thing'})
    """
    extractor = AggregationGroupExtractor()
    items = extractor.extract(expr)
    assert items == [["first", "second"], ["third", "fourth"]]


def test_aggregation_group_extractor_no_agg():
    expr = """
        count(metric{label='thing'})
    """
    extractor = AggregationGroupExtractor()
    items = extractor.extract(expr)
    assert items == []
