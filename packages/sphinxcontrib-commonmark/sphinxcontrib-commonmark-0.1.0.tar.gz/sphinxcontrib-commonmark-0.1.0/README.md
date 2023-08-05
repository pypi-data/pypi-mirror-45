# sphinxcontrib-commonmark

Yet another commonmark processor for Sphinx

## Install

Install the package via pip
```
$ pip install sphinxcontrib-commonmark
```

And append `sphinxcontrib.commonmark` to extensions list in your conf.py.
```
extensions = ['sphinxcontrib.commonmark']
```

## Restrictions

* Hard line break is only available with HTML and LaTeX builders.
* Two or more level deeper headings are disallowed.  Top level headings should be 1st level.
  And nested headings should be only one level deeper than its parent.
