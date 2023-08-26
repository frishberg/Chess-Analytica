# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'Chess Analytica'
copyright = '2023, Frishberg'
author = 'Aron Frishberg'

release = '0.1'
version = '1.0.3'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

# -- Options for EPUB output
epub_show_urls = 'footnote'
