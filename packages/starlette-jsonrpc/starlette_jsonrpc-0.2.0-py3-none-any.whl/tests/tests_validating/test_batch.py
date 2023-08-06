from tests import client


def test_batch():
    payload = [
        {"jsonrpc": "2.0", "method": "sum", "params": [1, 2, 4], "id": "1"},
        {"jsonrpc": "2.0", "method": "notify_hello", "params": [7]},
    ]
    # payload = [
    #     {"jsonrpc": "2.0", "method": "sum", "params": [1, 2, 4], "id": "1"},
    #     {"jsonrpc": "2.0", "method": "notify_hello", "params": [7]},
    #     {"jsonrpc": "2.0", "method": "subtract_positional", "params": [42, 23], "id": "2"}, good
    #     {"foo": "boo"}, bad
    #     {"jsonrpc": "2.0", "method": "foo.get", "params": {"name": "myself"}, "id": "5"}, good
    #     {"jsonrpc": "2.0", "method": "get_data", "id": "9"} good
    # ]
    response = client.post("/api/", json=payload)
    assert response.json() == [
        {"jsonrpc": "2.0", "result": {"result": 7}, "id": "1"},
        {},
    ]
    # assert response.json() == [
    #     {"jsonrpc": "2.0", "result": {"result": 7}, "id": "1"},
    #     {},
    #     {"jsonrpc": "2.0", "result": {'result': 19}, "id": "2"},
    #     {"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": None},
    #     {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found.", "data": {}}, "id": "5"},
    #     {"jsonrpc": "2.0", "result": {"result": ["hello", 5]}, "id": "9"}
    # ]
