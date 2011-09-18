collective.recipe.symlink
=========================

A recipe to enable linking parts of eggs into a fixed directory that can be served via a webserver.

Usage
-----

Example of the buildout section::

  [symlink]
  recipe=collective.recipe.symlink
  egg = foo.bar
  destination = ${buildout:directory}/parts/static
  links =
    css = foo/bar/static/css
    js = foo/bar/static/js

TODO: Tests
