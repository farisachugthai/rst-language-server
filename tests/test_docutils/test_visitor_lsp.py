from textwrap import dedent

from docutils import frontend, utils
from docutils.parsers import rst

from rst_lsp.docutils_ext.inliner_lsp import InlinerLSP
from rst_lsp.docutils_ext.block_lsp import RSTParserCustom
from rst_lsp.docutils_ext.visitor_lsp import VisitorRef2Target, LSPTransform


def run_parser(source, parser_class):
    inliner = InlinerLSP(doc_text=source)
    parser = parser_class(inliner=inliner)
    option_parser = frontend.OptionParser(components=(rst.Parser,))
    settings = option_parser.get_default_values()
    settings.report_level = 5
    settings.halt_level = 5
    # settings.debug = package_unittest.debug
    document = utils.new_document("test data", settings)
    parser.parse(source, document)
    return document


def test_ref2target(file_regression):
    source = dedent(
        """\
    .. _ref:

    .. __: anonymous

    ref_ `ref`_ `phrase <ref_>`_ ref2_ anonymous__ unknown_

    _`ref2`

    |symbol| |unknown|

    [cite]_ [unknown]_

    [1]_

    .. |symbol| image:: symbol.png
    .. [cite] This is a citation.
    .. [1] This is a footnote.

    """
    )
    document = run_parser(source, parser_class=RSTParserCustom)
    visitor = VisitorRef2Target(document)
    document.walk(visitor)
    file_regression.check(document.pformat())
    assert len(visitor.anonymous_targets) == 1
    assert len(visitor.anonymous_refs) == 1


def test_sections(data_regression):
    source = dedent(
        """\
    title
    =====

    :title:`a`

    sub-title
    ---------

    :title:`b`

    sub-title2
    ----------

    :title:`c`

    sub-sub-title
    ~~~~~~~~~~~~~

    :title:`d`

    title2
    ======

    :title:`e`
    """
    )
    document = run_parser(source, parser_class=RSTParserCustom)
    transform = LSPTransform(document)
    transform.apply(source)
    data_regression.check(
        {
            "db_positions": transform.db_positions,
            "doc_symbols": transform.db_doc_symbols,
            "db_references": transform.db_references,
            "db_targets": transform.db_targets,
        }
    )


def test_target_refs(data_regression):
    source = dedent(
        """\
    .. _target:

    [1]_ target_ |symbol| [cite]_

    .. [1] This is a footnote.
    .. |symbol| image:: symbol.png
    .. [cite] This is a citation.
    """
    )
    document = run_parser(source, parser_class=RSTParserCustom)
    transform = LSPTransform(document)
    transform.apply(source)
    data_regression.check(
        {
            "db_positions": transform.db_positions,
            "doc_symbols": transform.db_doc_symbols,
            "db_references": transform.db_references,
            "db_targets": transform.db_targets,
        }
    )


def test_directives(data_regression):
    source = dedent(
        """\
    .. code:: python

       a=1

    .. image:: abc.png
    """
    )
    document = run_parser(source, parser_class=RSTParserCustom)
    transform = LSPTransform(document)
    transform.apply(source)
    data_regression.check(
        {
            "db_positions": transform.db_positions,
            "doc_symbols": transform.db_doc_symbols,
            "db_references": transform.db_references,
            "db_targets": transform.db_targets,
        }
    )


def test_mixed1(data_regression):
    source = dedent(
        """\
    .. _target:

    title
    -----

    .. note::

       [1]_ target_ |symbol| [cite]_

    .. [1] This is a footnote.
    .. |symbol| image:: symbol.png
    .. [cite] This is a citation.
    """
    )
    document = run_parser(source, parser_class=RSTParserCustom)
    transform = LSPTransform(document)
    transform.apply(source)
    data_regression.check(
        {
            "db_positions": transform.db_positions,
            "doc_symbols": transform.db_doc_symbols,
            "db_references": transform.db_references,
            "db_targets": transform.db_targets,
        }
    )
