import os
from unittest import mock

from api.schemas import MovieCard
from services.agent_tools import GraphArtifact, agent_bundles, bundle_for


def test_movies_status_includes_date_range() -> None:
    bundle = bundle_for("get_movies")
    assert bundle is not None
    assert bundle.status_from_args is not None
    status = bundle.status_from_args(
        {"from_watched_date": "2024-01-01", "to_watched_date": "2024-12-31"},
        "ES",
    )
    assert status is not None
    assert "2024-01-01" in status
    assert "2024-12-31" in status


def test_reviews_status_includes_title() -> None:
    bundle = bundle_for("get_reviews")
    assert bundle is not None
    assert bundle.status_from_args is not None
    status = bundle.status_from_args({"name": "Heat"}, "EN")
    assert status is not None
    assert "Heat" in status


def test_graph_artifacts_from_result() -> None:
    bundle = bundle_for("get_graph")
    assert bundle is not None
    assert bundle.artifacts_from_result is not None
    artifact = bundle.artifacts_from_result(
        {"obj_type": "graph", "graph_type": "rating_distribution", "data": [4.5, 5, 3]}
    )
    assert artifact == GraphArtifact(data=[4.5, 5.0, 3.0])


def test_movie_card_from_tuple_payload() -> None:
    bundle = bundle_for("get_movie_details")
    assert bundle is not None
    assert bundle.artifacts_from_result is not None
    artifact = bundle.artifacts_from_result(
        [
            "details",
            {
                "movies": {
                    "title": "Heat",
                    "url": "https://letterboxd.com/film/heat/",
                    "image_url": "https://example.com/heat.jpg",
                    "plot": "Cops and robbers.",
                    "ratings": [
                        {"Source": "Internet Movie Database", "Value": "8.3/10"}
                    ],
                }
            },
        ]
    )
    assert artifact == MovieCard(
        title="Heat",
        url="https://letterboxd.com/film/heat/",
        image_url="https://example.com/heat.jpg",
        plot="Cops and robbers.",
        ratings=[{"Source": "Internet Movie Database", "Value": "8.3/10"}],
    )


def test_extended_details_share_movie_card_mapping() -> None:
    plain = bundle_for("get_movie_details")
    extended = bundle_for("get_movie_details_extended")
    assert plain is not None and extended is not None
    assert plain.artifacts_from_result is extended.artifacts_from_result


def test_optional_artifacts() -> None:
    movies = bundle_for("get_movies")
    graph = bundle_for("get_graph")
    assert movies is not None and graph is not None
    assert movies.artifacts_from_result is None
    assert graph.status_from_args is None


def test_agent_bundles_one_list() -> None:
    with mock.patch.dict(os.environ):
        os.environ.pop("OMDB_API_KEY", None)
        names = [bundle.name for bundle in agent_bundles()]
    assert names == ["get_movies", "get_reviews", "get_graph", "get_movie_details"]
    with mock.patch.dict(os.environ, {"OMDB_API_KEY": "dummy"}):
        names = [bundle.name for bundle in agent_bundles()]
    assert names[-1] == "get_movie_details_extended"


if __name__ == "__main__":
    test_movies_status_includes_date_range()
    test_reviews_status_includes_title()
    test_graph_artifacts_from_result()
    test_movie_card_from_tuple_payload()
    test_extended_details_share_movie_card_mapping()
    test_optional_artifacts()
    test_agent_bundles_one_list()
    print("ok")
