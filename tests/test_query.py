import pytest
from app.query import query_records
def test_filter_and_group():
    rows=[{"team":"A","amount":10},{"team":"A","amount":20},{"team":"B","amount":5}]
    out=query_records(rows,{"amount":{"op":"gte","value":10}},"team","sum","amount")
    assert out["count"]==2 and out["aggregation"]=={"A":30.0}
def test_unknown_field_rejected():
    with pytest.raises(ValueError): query_records([{"a":1}],{"secret":{"op":"eq","value":1}})
