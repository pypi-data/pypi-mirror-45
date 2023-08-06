from datetime import datetime
from urllib.parse import urlparse

from transformer.request import HttpMethod, Request, CaseInsensitiveDict
from transformer.task import Task2
from .sanitize_headers import plugin


def test_its_name_is_resolvable():
    from transformer.plugins import resolve

    assert list(resolve("transformer.plugins.sanitize_headers")) == [plugin]


TS = datetime(1970, 1, 1)


def task_with_header(name: str, value: str) -> Task2:
    return Task2(
        name="some task",
        request=Request(
            timestamp=TS,
            method=HttpMethod.GET,
            url=urlparse("https://example.com"),
            har_entry={"entry": "data"},
            name="task_name",
            headers=CaseInsensitiveDict({name: value}),
            post_data={},
            query=[],
        ),
    )


def test_it_removes_headers_beginning_with_a_colon():
    task = task_with_header(":non-rfc-header", "some value")
    sanitized_headers = plugin(task).request.headers
    assert len(sanitized_headers) == 0


def test_it_removes_cookies():
    task = task_with_header("Cookie", "some value")
    sanitized_headers = plugin(task).request.headers
    assert len(sanitized_headers) == 0


def test_it_does_not_change_nor_remove_other_headers():
    task = task_with_header("some other header", "some value")
    sanitized_headers = plugin(task).request.headers
    assert len(sanitized_headers) == 1
