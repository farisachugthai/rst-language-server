"""Module for analysing an RST document.

Provides error analysis and analysis of element positions in the document,
in a JSON format compatible with database storage.
"""

# im just gonna add this for visibility
from .main import create_sphinx_app
from .patch_globals import additional_nodes
