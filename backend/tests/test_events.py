from api.events import chunk_text, graph_from_tool_output, movie_from_tool_output


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


if __name__ == "__main__":
    test_chunk_text_handles_blocks()
    test_movie_from_tuple_payload()
    test_graph_from_tool_output()
    print("ok")
