from textwrap import dedent

import pytest
from pyls_jsonrpc.exceptions import JsonRpcMethodNotFound

CALL_TIMEOUT = 10


@pytest.fixture
def open_test_doc(tmp_path):
    def _open_func(client_server, content, uri="uri123", initialize=True):
        if initialize:
            response = client_server._endpoint.request(
                "initialize", {"rootPath": str(tmp_path), "initializationOptions": {}}
            ).result(timeout=CALL_TIMEOUT)
            assert "capabilities" in response
        client_server._endpoint.request(
            "text_document/did_open",
            {
                "textDocument": {
                    "uri": "uri123",
                    "languageId": "str",
                    "version": 1,
                    "text": content,
                }
            },
        )
        return {"uri": uri, "languageId": "str", "version": 1}

    return _open_func


def test_missing_message(client_server):  # pylint: disable=redefined-outer-name
    with pytest.raises(JsonRpcMethodNotFound):
        client_server._endpoint.request("unknown_method").result(timeout=CALL_TIMEOUT)


def test_initialize(client_server, tmp_path, data_regression):
    future = client_server._endpoint.request(
        "initialize", {"rootPath": str(tmp_path), "initializationOptions": {}}
    )
    response = future.result(timeout=CALL_TIMEOUT)
    data_regression.check(response)


# TODO how to test notifications, like publish diagnostics?


def test_folding_provider(client_server, open_test_doc, data_regression):
    content = dedent(
        """\
        title
        -----

        abc

        title2
        ======

        def
        """
    )
    doc = open_test_doc(client_server, content)
    response3 = client_server._endpoint.request(
        "text_document/folding_range", {"textDocument": doc}
    ).result(timeout=CALL_TIMEOUT)
    data_regression.check(response3)


def test_document_symbols(client_server, open_test_doc, data_regression):
    content = dedent(
        """\
        title
        -----

        |abc|

        :ref`abc`

        title2
        ======

        .. code:: python

            print("hi")

        def
        """
    )
    doc = open_test_doc(client_server, content)
    response3 = client_server._endpoint.request(
        "text_document/document_symbol", {"textDocument": doc}
    ).result(timeout=CALL_TIMEOUT)
    data_regression.check(response3)


def test_completion(client_server, open_test_doc, data_regression):
    # TODO this is changing dependent on if it is called,
    # when running all tests or just the test_request ones (removing roles)
    doc = open_test_doc(client_server, ":\n")
    response3 = client_server._endpoint.request(
        "text_document/completion",
        {"textDocument": doc, "position": {"line": 0, "character": 1}},
    ).result(timeout=CALL_TIMEOUT)
    data_regression.check(response3)


def test_hover_role(client_server, open_test_doc, data_regression):
    doc = open_test_doc(client_server, ":index:`abc`\n")
    response3 = client_server._endpoint.request(
        "text_document/hover",
        {"textDocument": doc, "position": {"line": 0, "character": 4}},
    ).result(timeout=CALL_TIMEOUT)
    data_regression.check(response3)


def test_hover_directive(client_server, open_test_doc, data_regression):
    doc = open_test_doc(client_server, ".. note::\n\n   Hi\n")
    response3 = client_server._endpoint.request(
        "text_document/hover",
        {"textDocument": doc, "position": {"line": 0, "character": 4}},
    ).result(timeout=CALL_TIMEOUT)
    data_regression.check(response3)


def test_definitions(client_server, open_test_doc, data_regression):
    doc = open_test_doc(client_server, "|sub|\n\n.. |sub| replace:: a")
    response3 = client_server._endpoint.request(
        "text_document/definition",
        {"textDocument": doc, "position": {"line": 0, "character": 1}},
    ).result(timeout=CALL_TIMEOUT)
    data_regression.check(response3)


def test_references(client_server, open_test_doc, data_regression):
    doc = open_test_doc(client_server, "|sub|\n\n.. |sub| replace:: a")
    response3 = client_server._endpoint.request(
        "text_document/references",
        {
            "textDocument": doc,
            "position": {"line": 2, "character": 1},
            "context": {"includeDeclaration": True},
        },
    ).result(timeout=CALL_TIMEOUT)
    data_regression.check(response3)


def test_code_lens_black(client_server, open_test_doc, data_regression):
    doc = open_test_doc(client_server, ".. code-block:: python\n\n    a='b'\n")
    response3 = client_server._endpoint.request(
        "text_document/code_lens",
        {"textDocument": doc, "position": {"line": 0, "character": 1}},
    ).result(timeout=CALL_TIMEOUT)
    data_regression.check(response3)
    # TODO test command


def test_python_completion1(client_server, open_test_doc, data_regression):
    doc = open_test_doc(client_server, ".. code-block:: python\n\n    ab = 1\n    a\n")
    response3 = client_server._endpoint.request(
        "text_document/completion",
        {"textDocument": doc, "position": {"line": 3, "character": 4}},
    ).result(timeout=CALL_TIMEOUT)
    data_regression.check(response3["items"][0])


def test_python_hover(client_server, open_test_doc, data_regression):
    doc = open_test_doc(client_server, ".. code-block:: python\n\n    print('hallo')\n")
    response3 = client_server._endpoint.request(
        "text_document/hover",
        {"textDocument": doc, "position": {"line": 2, "character": 5}},
    ).result(timeout=CALL_TIMEOUT)
    data_regression.check(response3)
