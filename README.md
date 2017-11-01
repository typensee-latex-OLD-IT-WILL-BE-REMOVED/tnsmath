What about this package  ?
==========================

**ly-math**, which is a contraction of **lycée** and **math**, has been built to allow the writings of more semantical LaTeX documents at a very low level of mathematics.


What is new in this version `0.1.0-beta` ?
==========================================

**Sets**: several changes have been done.

  1) ``\geoset*``, ``\probaset*`` and ``\fieldset*`` allow the use of subscript.

  2) One new macro ``\geneset`` for general sets inside braces.


**Functions:** two new macros ``\abs`` and ``\abs*`` for absolute values.


**Geometry:** several changes have been done.

  1) ``\pt`` becomes ``\gpt`` such as to avoid a conflict with \verb+lyxam+ another project of the author of \verb+lymath+.

  2) ``\gpt*`` allow subscripting.

  3) ``\vect`` and ``\vect*`` will not print the point above "i" and "j" when this letters are the "main" name of the vector.
  A similar feature has been added for the macros ``\anglein``, ``\arc`` and their star versions.

  4) Two new macros ``\norm`` and ``\norm*`` for norms of vectors.

  5) Two new macros ``\axis`` and ``\axis*`` for writing names of axes in a cartesian system of coordinates.
  There are also ``\gpaxis``, ``\vaxis`` and ``\gpvaxis`` which in day to day writing can be helpful.


What is new in this version `0.0.2-beta` ?
==========================================

**Differential calculus:** there are new star versions of ``derfrac`` and ``partialfrac`` wich uses an operator like notation.


What is new in this version `0.0.1-beta` ?
==========================================

**Arithmetic:** macros for continued fractions.


**Geometry:** some macros for geometry.


**Integral calculus:** major changes.

  1) The macros ``hook*`` now gives a formatting with hooks that stretch vertically.

  2) The macros ``vhook`` is when you want to have a vertical line instead of hooks.

  3) The macros ``vhook*`` gives a formatting with the vertical line that stretchs vertically.


**Differential calculus:** one new macro ``dersub`` wich is similar to ``partialsub``.


**Background changes:** now ``\IDarg{}`` writes ``Argument:``, and ``\IDoption{}`` prints ``Option:``.


What about this first version `0.0.0-beta` ?
============================================

All informations are inside the PDF named `lymath-doc.pdf` inside the folder `lymath`.

The only thing needed to use the package is the folder `lymath`.


I beg your pardon for my english...
===================================

English is not my native language, so be nice if you notice misunderstandings, misspellings or grammatical errors in my documents and my codes.
