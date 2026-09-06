from api.events import (
    chunk_text,
    events_from_langgraph,
    graph_from_tool_output,
    movie_from_tool_output,
)


def test_chunk_text_handles_blocks() -> None:
    assert chunk_text("hello") == "hello"
    assert chunk_text([{"type": "text", "text": "ab"}, {"type": "text", "text": "c"}]) == "abc"


def test_movie_from_tuple_payload() -> None:
    movie = movie_from_tool_output(
        [
            "details",
            {
                "movies": {
                    "title": "Heat",
                    "url": "https://letterboxd.com/film/heat/",
                    "image_url": "https://example.com/heat.jpg",
                    "plot": "Cops and robbers.",
                    "ratings": [{"Source": "Internet Movie Database", "Value": "8.3/10"}],
                }
            },
        ]
    )
    assert movie is not None
    assert movie.title == "Heat"
    assert movie.ratings[0]["Value"] == "8.3/10"


def test_graph_from_tool_output() -> None:
    data = graph_from_tool_output(
        {"obj_type": "graph", "graph_type": "rating_distribution", "data": [4.5, 5, 3]}
    )
    assert data == [4.5, 5.0, 3.0]


def test_events_from_langgraph_v2_dict() -> None:
    status = events_from_langgraph(
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
    assert len(status) == 1
    assert status[0].type == "status"

    class Chunk:
        content = "hola"

    tokens = events_from_langgraph(
        {"event": "on_chat_model_stream", "name": "chatboxd_llm", "data": {"chunk": Chunk()}},
        "ES",
    )
    assert [event.type for event in tokens] == ["token"]
    assert tokens[0].text == "hola"


if __name__ == "__main__":
    test_chunk_text_handles_blocks()
    test_movie_from_tuple_payload()
    test_graph_from_tool_output()
    test_events_from_langgraph_v2_dict()
    print("ok")
