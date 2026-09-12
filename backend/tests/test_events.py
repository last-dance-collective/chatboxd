from api.events import chunk_text, events_from_langgraph


def test_chunk_text_handles_blocks() -> None:
    assert chunk_text("hello") == "hello"
    assert chunk_text([{"type": "text", "text": "ab"}, {"type": "text", "text": "c"}]) == "abc"


def test_langgraph_start_becomes_status() -> None:
    events = events_from_langgraph(
        {
            "event": "on_tool_start",
            "name": "get_movies",
            "data": {
                "input": {
                    "from_watched_date": "2024-01-01",
                    "to_watched_date": "2024-12-31",
                }
            },
        },
        "ES",
    )
    assert [event.type for event in events] == ["status"]


def test_langgraph_end_becomes_graph() -> None:
    events = events_from_langgraph(
        {
            "event": "on_tool_end",
            "name": "get_graph",
            "data": {
                "output": {
                    "obj_type": "graph",
                    "graph_type": "rating_distribution",
                    "data": [4.5, 5, 3],
                }
            },
        },
        "EN",
    )
    assert [event.type for event in events] == ["graph"]
    assert events[0].data == [4.5, 5.0, 3.0]


def test_langgraph_stream_becomes_token() -> None:
    class Chunk:
        content = "hola"

    events = events_from_langgraph(
        {
            "event": "on_chat_model_stream",
            "name": "chatboxd_llm",
            "data": {"chunk": Chunk()},
        },
        "ES",
    )
    assert [event.type for event in events] == ["token"]
    assert events[0].text == "hola"


if __name__ == "__main__":
    test_chunk_text_handles_blocks()
    test_langgraph_start_becomes_status()
    test_langgraph_end_becomes_graph()
    test_langgraph_stream_becomes_token()
    print("ok")
