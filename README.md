About this package
==================

**ly-math**, which is a contraction of **lycée** and **math**, has been built to allow the writings of more semantical LaTeX documents at a low level of mathematics.


Only one french documentation is proposed but it contains a lot of examples of use : see the PDF file named `lymath-doc[fr].pdf` inside the folder `lymath`.

The only thing needed to use is the standalone package ``lymath.sty`` inside the folder `lymath`.



I beg your pardon for my english...
===================================

English is not my native language, so be nice if you notice misunderstandings, misspellings or grammatical errors in my documents and my codes.



Changes in this version `0.5.0-beta`
====================================

**New minor version ``0.5.0-beta``:** see all the changes below.


**Easy displayed mode for sums and products:** the macros ``\dsum`` and ``\dprod`` regarding to ``\sum`` and ``\prod`` work both similarly to ``\dfrac`` regarding to ``\frac``.


**Arithmetic:** new math operators `\divides`, `\notdivides` and `\modulo` have beend added.


**Geometry:** three new macros.

1. The macros ``\pts`` allow to write several points.

2. Oblic version, instead of a vertical one, of the macro ``\parallel``.


**Logic:** several new macros have benne added.

1. The macros `\eqhyp` and `\eqcond` has been added.

2. The macro `\liesimp` is an alias for `\Longleftarrow`.

3. The macros ``\vimplies``, ``\viff`` and ``\vliesimp`` are vertical versions of ``\implies``, ``\iff`` and ``\liesimp``.

4. There are also macros like ``\impliestest``, ``\iffhyp``...

5. The double starred macro `\eqdef**` gives another symbolic symbol for the equal definition symbols (this version is used by the B language).


**Automatic spacings:** extra spaces are automatically added when using ``\sqrt`` for the exponent and the value.


Changes in this version `0.4.0-beta`
====================================

**New minor version `0.4.0-beta`:** see all the changes below.


**Logic and fundations:** different kinds of inequality and not equal signs such as to stress a test to be done, a condition or an hypothesis.


**Two new packages loaded:** we have added the packages `tkz-tab` and `nicematrix` with special settings.


Changes in this version `0.3.0-beta`
====================================

**New minor version `0.3.0-beta`:** see all the changes below.


**New macro ``\lymathsubsep``:** this defines the separators of arguments for a second level. By default it is a semi-colon but if this will be a coma if the option ``french`` of ``babel`` is activated.


**Logic and fundations:** here are the new features in this new section.

1. Different kind of equal signs are available.

2. The macro ``\explain`` allows to explain efficiently formal reasonning or calculus.


**Sets:** here are the new features.

1. ``\fieldset`` has been renamed ``\algeset``.

2. One new classical set added : ``\PP`` indicates the set of prime numbers.


**Geometry:** here are the new features.

1. The macro ``\hangleorient`` writes oriented angles of vectors using a hat.

2. The macros ``\vangleorient`` and ``\vhangleorient`` are shortcuts to not use ``\vect`` when writing oriented angles of vectors without or with a hat.

3. The macros ``\vdotprod``, ``\vadotprod`` and ``\vcroosprod`` are shortcuts to not use ``\vect`` when writing dot and cross products.






<!--

Changes in this version `0.2.0-beta`
====================================

**New minor version ``0.2.0-beta`` of ``lymath``:** see all the changes below.


**English documentation will be not supported:** the author of the package will only write a french documentation `lymath-doc[fr].pdf` such as to practice more sport.


**One regression repaired:** when the option ``french`` of ``babel`` was activated, auto spacing around semi-colon was broken.


**One big bug fixed :** in the code for differential calculus the option ``\noexpandarg`` of ``xstring`` created a bug with the use of ``lyxam``. The way the code works now avoids this kind of problem.


**One major change in the interface:** for macros using unbounded numbers of arguments, the use ``//`` has been replaced by the use of ``|``.


**New macro ``\lymathsep``:** this defines the separators of arguments. By default it is a coma but if this will be a semi-colon if the option ``french`` of ``babel`` is activated.


**Automatic spacings:** extra spaces are automatically added when using ``\frac`` and ``\dfrac``.


**Analysis:** one new macro ``\derpow*`` adds automatically the good number of prime for the derivative of one function.


**Geometry:** here are the new features.

1. Two new macros ``\coord`` and ``\vcoord`` allows to write coordinates of points and vectors.

2. The macro ``\angleorient`` allows to write oriented angles of vectors.

3. The macros ``\dotprod`` and ``\adotprod`` are for scalar products.

4. The macro ``\crossprod`` is for cross products of 3D vectors.

5. The use of ``axis`` has been replaced by the better translation ``axes``.

6. ``\gpt`` becomes ``\pt`` because there is no more conflict with ``lyxam`` another project of the author of ``lymath``.

7. ``\gpaxis`` and ``\gpvaxis`` have been renamed ``\paxes`` and ``\pvaxes`` because of the two new features above.


**Algebra:**  you can write sets of polynomials, or of formal series with their fractional fields, and also sets of the polynomials and formal series of Laurent.


**Internal changes in the factory:** a deep cleaning has been achieved.


Changes in this version `0.1.0-beta`
====================================

**Sets**: several changes have been done.

1. ``\geoset*``, ``\probaset*`` and ``\fieldset*`` allow the use of subscript.

2. One new macro ``\geneset`` for general sets inside braces.


**Functions:** two new macros ``\abs`` and ``\abs*`` for absolute values.


**Geometry:** several changes have been done.

1. ``\pt`` becomes ``\gpt`` such as to avoid a conflict with `lyxam` another project of the author of `lymath`.

2. ``\gpt*`` allow subscripting.

3. ``\vect`` and ``\vect*`` will not print the point above "i" and "j" when this letters are the "main" name of the vector.
A similar feature has been added for the macros ``\anglein``, ``\arc`` and their star versions.

4. Two new macros ``\norm`` and ``\norm*`` for norms of vectors.

5. Two new macros ``\axis`` and ``\axis*`` for writing names of axes in a cartesian system of coordinates.
There are also ``\gpaxis``, ``\vaxis`` and ``\gpvaxis`` which in day to day writing can be helpful.


Changes in this version `0.0.2-beta`
====================================

**Differential calculus:** there are new star versions of ``derfrac`` and ``partialfrac`` wich uses an operator like notation.


Changes in this version `0.0.1-beta`
====================================

**Arithmetic:** macros for continued fractions.


**Geometry:** some macros for geometry.


**Integral calculus:** major changes.

1. The macros ``hook*`` now gives a formatting with hooks that stretch vertically.

2. The macros ``vhook`` is when you want to have a vertical line instead of hooks.

3. The macros ``vhook*`` gives a formatting with the vertical line that stretchs vertically.


**Differential calculus:** one new macro ``dersub`` wich is similar to ``partialsub``.


**Background changes:** now ``\IDarg{}`` writes ``Argument:``, and ``\IDoption{}`` prints ``Option:``.


About this first version `0.0.0-beta`
=====================================

All informations are inside the PDF named `lymath-doc.pdf` inside the folder `lymath`.

The only thing needed to use the package is the folder `lymath`.

-->
