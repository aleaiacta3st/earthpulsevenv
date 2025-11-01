
from quake_ingest.parser import parse_data

def test_parse_data_extracts_fields():
    mock_data = {
        "features": [{
            "id": "testtesttest",
            "properties": {"place": "Atlantic_Ocean", "mag": 3.5, "tsunami": 1, "time": 189876532456},
            "geometry": {"coordinates": [7, 8, 9]}
        }]
    }
    result = parse_data(mock_data)
    assert len(result) == 1
    assert result[0]["id"] == "testtesttest"
    assert result[0]["magnitude"] == 3.5