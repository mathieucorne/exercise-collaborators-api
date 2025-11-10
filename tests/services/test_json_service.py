import json
import pytest
from app.services.json_service import JSONService


def test_serialize_basic_dict():
    data = {"name": "Alice", "age": 30}
    result = JSONService.serialize(data)
    assert isinstance(result, str)
    parsed = json.loads(result)
    assert parsed == data

def test_format_with_data_and_message():
    data = {"user": "Alice"}
    status = 201
    message = "Created"
    response = JSONService.format(data=data, status=status, message=message)
    
    assert isinstance(response, dict)
    assert response["status"] == status
    assert response["message"] == message
    assert response["data"] == data

def test_format_with_default_values():
    response = JSONService.format()
    assert response["status"] == 200
    assert response["message"] == "success"
    assert "data" not in response

def test_format_with_only_data():
    data = [1, 2, 3]
    response = JSONService.format(data=data)
    assert response["status"] == 200
    assert response["message"] == "success"
    assert response["data"] == data
