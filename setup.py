from importlib import import_module

from setuptools import setup, find_packages

try:
    version = import_module("rst_lsp").__version__
except ImportError:
    version = "0.0.4"

setup(
    name="rst-language-server",
    version=version,
    author="Chris Sewell",
    packages=find_packages(""),
    install_requires=[
        "attrs>=19",
        "docutils>=0.15.2",
        "jedi>=0.15",
        "pluggy>=0.13",
        "python-jsonrpc-server>0.3",
        "pyyaml",
        "setuptools",
        "sphinx>=2.2",
        "sqlalchemy>=1.3",
        "ujson",  # pyls json
        'typing-extensions',
        "wheel",
    ],
    extras_require={
        "testing": ["pytest>5", "pytest-regressions", "sphinxcontrib-bibtex>=1.0.0"],
        "code_style": ["black", "pre-commit==1.17.0", "flake8<3.8.0"],
    },
    entry_points={
        "console_scripts": [
            "rst-lsp-cli=rst_lsp.server:cli_entry",
            "rst-lsp-serve=rst_lsp.server.cli_entry:main",
        ],
        "rst_lsp": [
            "lint_docutils = rst_lsp.server.plugins.lint_docutils",
            "folding = rst_lsp.server.plugins.folding",
            "completions = rst_lsp.server.plugins.completions",
            "document_symbols = rst_lsp.server.plugins.doc_symbols",
            "hover = rst_lsp.server.plugins.hover",
            "definitions = rst_lsp.server.plugins.definitions",
            "references = rst_lsp.server.plugins.references",
            "format_python = rst_lsp.server.plugins.python_blocks.clens_format",
            "completions_python = rst_lsp.server.plugins.python_blocks.completions",
            "hover_python = rst_lsp.server.plugins.python_blocks.hover",
        ],
    },
)
