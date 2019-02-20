About this package
==================

**ly-math**, which is a contraction of **lycée** and **math**, has been built to allow the writings of more semantical LaTeX documents at a very low level of mathematics.


I beg your pardon for my english...
===================================

English is not my native language, so be nice if you notice misunderstandings, misspellings or grammatical errors in my documents and my codes.



Changes in this version `0.2.0-beta`
====================================

**New minor version version::``0.2.0-beta`` of ¨lymath:** see all the changes below.


**English documentation will be not supported:** the author of the package will only write a french documentation `lymath-doc[fr].pdf` such as to practice more sport.


**One regression repaired :** when the option ``french`` of ``babel`` was activated, auto spacing around semi-colon was broken.


**One major change in the interface:** for macros using unbounded numbers of arguments, the use ``//`` has been replaced by the use of ``|``.


**New macro ``\lymathsep``:** this defines the separators of arguments. By default it is a coma but if this will be a semi-colon if the option ``french`` of ``babel`` is activated.


**Automatic spacings:** extra spaces are automatically added when using ``\frac`` and ``\dfrac``.


**Analysis:** one new macro ``\derpow*`` adds automatically the good number of prime for the derivative of one function.


**Geometry:** here are the new features.

    1) Two new macros ``\coord`` and ``\vcoord`` allows to write coordinates of points and vectors.

    2) The macro ``\angleorient`` allows to write oriented angles of vectors.

    3) The macros ``\dotprod`` and ``\adotprod`` are for scalar products.

    4) The macro ``\crossprod`` is for cross products of 3D vectors.

    5) The use of ``axis`` has been by the better translation ``axes``.

    6) ``\gpt`` becomes ``\pt`` because there is no more conflict with ``lyxam`` another project of the author of ``lymath``.

    7) ``\gpaxis`` and ``\gpvaxis`` have been renamed ``\paxes`` and ``\pvaxes`` because of the two new features above.


**Algebra:** you can write sets of polynomials, or of formal series and also the fractional fields of this kinds of sets.


**Internal changes in the factory:** a deep cleaning has been acheived.


Changes in this version `0.1.0-beta`
====================================

**Sets**: several changes have been done.

    1) ``\geoset*``, ``\probaset*`` and ``\fieldset*`` allow the use of subscript.

    2) One new macro ``\geneset`` for general sets inside braces.


**Functions:** two new macros ``\abs`` and ``\abs*`` for absolute values.


**Geometry:** several changes have been done.

    1) ``\pt`` becomes ``\gpt`` such as to avoid a conflict with `lyxam` another project of the author of `lymath`.

    2) ``\gpt*`` allow subscripting.

    3) ``\vect`` and ``\vect*`` will not print the point above "i" and "j" when this letters are the "main" name of the vector.

    A similar feature has been added for the macros ``\anglein``, ``\arc`` and their star versions.

    4) Two new macros ``\norm`` and ``\norm*`` for norms of vectors.

    5) Two new macros ``\axis`` and ``\axis*`` for writing names of axes in a cartesian system of coordinates.

    There are also ``\gpaxis``, ``\vaxis`` and ``\gpvaxis`` which in day to day writing can be helpful.


Changes in this version `0.0.2-beta`
====================================

**Differential calculus:** there are new star versions of ``derfrac`` and ``partialfrac`` wich uses an operator like notation.


Changes in this version `0.0.1-beta`
====================================

**Arithmetic:** macros for continued fractions.


**Geometry:** some macros for geometry.


**Integral calculus:** major changes.

  1) The macros ``hook*`` now gives a formatting with hooks that stretch vertically.

  2) The macros ``vhook`` is when you want to have a vertical line instead of hooks.

  3) The macros ``vhook*`` gives a formatting with the vertical line that stretchs vertically.


**Differential calculus:** one new macro ``dersub`` wich is similar to ``partialsub``.


**Background changes:** now ``\IDarg{}`` writes ``Argument:``, and ``\IDoption{}`` prints ``Option:``.


About this first version `0.0.0-beta`
=====================================

All informations are inside the PDF named `lymath-doc.pdf` inside the folder `lymath`.

The only thing needed to use the package is the folder `lymath`.