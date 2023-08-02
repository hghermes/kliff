#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import os
import sys
import subprocess
from pathlib import Path


# sys.path.insert(0, os.path.abspath('.'))

# This should be the path to the package, not the source of the doc
# e.g. ~/Applications/kliff
# NOTE, do not use sys.path.insert, especially true when you have a C extension.
# Because if you use `pip install .` or `python setup install` to build your
# extension and install the package, the C extension will not be placed in the
# source directory, but will be placed to your virtual environment. Then if you use
# sys.path.insert to insert your source directory to be the first place to look for
# your package, it will fail to find the C extension.
# Here, we add it for sphinx to find the package source package, in case we do not
# install the package.
sys.path.append(os.path.abspath("../../"))


# -- Project information -----------------------------------------------------

project = "KLIFF"
copyright = "2021-2023, OpenKIM"
author = "Mingjian Wen"

# The short X.Y version
version = "0.4"
# The full version, including alpha/beta/rc tags
release = "0.4.1"


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.imgmath",
    # 'sphinx.ext.mathjax',
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.viewcode",
    "myst_nb",
    # 'sphinx.ext.todo',
    # 'sphinx.ext.coverage',
    # "sphinx_gallery.gen_gallery",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = {
    ".rst": "restructuredtext",
    ".ipynb": "myst-nb",
    ".myst": "myst-nb",
}

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = 'sphinx'
pygments_style = "default"
# pygments_style = None


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
# html_theme = "sphinx_rtd_theme"
html_theme = "furo"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    "sidebar_hide_name": True,  # only show the logo
}

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "./img/logo.jpg"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "KLIFFdoc"


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "KLIFF.tex", "KLIFF Documentation", "Mingjian Wen", "manual")
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "kliff", "KLIFF Documentation", [author], 1)]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "KLIFF",
        "KLIFF Documentation",
        author,
        "KLIFF",
        "One line description of project.",
        "Miscellaneous",
    )
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ["search.html"]


# -- Mock setup --------------------------------------------------------------
# A list of modules to be mocked up.
# https://docs.readthedocs.io/en/stable/faq.html#i-get-import-errors-on-libraries-that-depend-on-c-modules
# This is useful when some external dependencies are not installed at build time,
# which can break the building process.
autodoc_mock_imports = [
    "numpy",
    "scipy",
    "scipy.optimize",
    "kimpy",
    "yaml",
    "ase",
    "torch",
]

# do not sort member functions of a class
autodoc_member_order = "bysource"

# -- Math setup --------------------------------------------------------------
# imgmath settings
imgmath_image_format = "svg"
imgmath_latex_preamble = "\\usepackage{bm} \\usepackage{amsmath}"

# -- myst-nb -----------------------------------------------------------------
nb_execution_timeout = 120

# -- generate api doc ----------------------------------------------------------


def get_all_modules(source: Path = "./kliff") -> list[str]:
    """
    Get all modules of the package.

    Note, this only get the first-level modules like `kliff.module_a`, not modules
    (in subpackages) like `kliff.subpackage_a.module_b`. subpackage is considered
    as a module.

    This takes advantage of
        $ sphinx-apidoc -f -e -o <outdir> <sourcedir>
    Return a list of modules names.
    """
    results = subprocess.run(
        ["sphinx-apidoc", "-f", "-e", "-o", "/tmp/kliff_apidoc", source],
        capture_output=True,
    )
    results = results.stdout.decode("utf-8")

    modules = []
    for line in results.split("\n"):
        if "Creating" in line:
            name = line.split("/")[-1].split(".")
            if len(name) >= 4:
                mod = name[1]
                if mod not in modules:
                    modules.append(mod)
    return modules


def autodoc_package(path: Path, modules: list[str]):
    """
    Create a package reference page.

    Args:
        path: directory to place the file
        modules: list of API modules
    """
    path = Path(path).resolve()
    if not path.exists():
        path.mkdir(parents=True)

    with open(path / "kliff.rst", "w") as f:
        f.write(".. _reference:\n\n")
        f.write("Package Reference\n")
        f.write("=================\n\n")
        f.write(".. toctree::\n")
        for m in modules:
            f.write("    kliff." + m + "\n")


def autodoc_module(path: Path, module: str):
    """
    Create a module reference page.

    Args:
        path: directory to place the file
        module: name of the module
    """
    path = Path(path).resolve()
    if not path.exists():
        path.mkdir(parents=True)

    module_name = "kliff." + module
    fname = path.joinpath(module_name + ".rst")
    with open(fname, "w") as f:
        f.write(f"{module_name}\n")
        f.write("-" * len(module_name) + "\n\n")
        f.write(f".. automodule:: {module_name}\n")
        f.write("    :members:\n")
        f.write("    :undoc-members:\n")
        # f.write("    :show-inheritance:\n")
        f.write("    :inherited-members:\n")


def create_apidoc(directory: Path = "./apidoc"):
    """
    Create API documentation, a separate page for each module.

    Args:
        directory:

    Returns:

    """

    # modules with the below names will not be excluded
    excludes = ["cmdline"]

    package_path = Path(__file__).parents[2] / "kliff"
    modules = get_all_modules(package_path)
    for exc in excludes:
        modules.remove(exc)
    modules = sorted(modules)

    autodoc_package(directory, modules)
    for mod in modules:
        autodoc_module(directory, mod)


create_apidoc(directory="./apidoc")
