dm.incrementalsearch
====================

``dm.incrementalsearch`` is an efficient low level search execution engine.
Its primary purpose is to incrementally perform searches involving
``and``, ``or`` and ``not`` queries over ``ZODB.BTrees``.

Incrementally means here
that hits are determined one at a time: the first hit, then the second hit,
then the third hit, etc. Therefore, the first few hits can be determined
extremely fast. But even if all hits need to be determined, the
incremental execution of subqueries can lead to speedups of several orders
for some query types (especially those dominated by specific ``and`` queries).

Queries involving large ``or`` subqueries are difficult to optimize
in the standard way. But often they can be replaced by incremental
filtering. With this technique, a subquery is removed from the
original search, the modified search executed and the result filtered
by the removed subquery. ``incrementalsearch`` supports incremental filtering
and thereby can again gain serveral orders of speedup for otherwise
difficult to treat query types.

The primary concept is that of an ``ISearch`` (incremental search).
This is conceptionally a sorted list, computed incrementally
(or lazily). The elements of this list are the ``ISearch``'s hits.
The ``ISearch``'s ``keytype`` determines the type of the list
elements. Currently supported are ``OBJECT`` (comparable Python objects),
``INT`` (Python 32 bit integers) and ``LONG`` (Python 64 bit integers).

Example usage
-------------
``incrementalsearch`` is rarely used directly but usually indirectly
via a higher level search engine such as ``Products.AdvancedQuery``.
Let's nevertheless look at some examples.

Assume we want to find elements available in each of a sequence
of integer BTrees ``seq_btrees``. I.e. we are interested in elements contained
in the intersection of these BTrees.

>>> from dm.incrementalsearch import IBTree, IAnd_int, Unspecified, \
...     AT_END, INLIST_SUCCESS

We transform the BTrees into incrementally searchable objects by
applying the ``IBTree`` operator (Incremental BTree). Then
we combine them by ``IAnd_int`` and indicate that no more searches
will be added by calling ``complete``. This causes several optimizations
to take place.

>>> isearch = IAnd_int(*map(IBTree, seq_btrees))
>>> isearch.complete()

An ``ISearch`` has attributes ``value`` (the current value) and ``classification``
(it indicates whether the current value is a hit and whether there may be
more values) and methods ``advanceFrom`` and ``advanceTo`` to move forward
in the search. To determine the first hit, we can use:

>>> cl = isearch.advanceFrom(Unspecified, Unspecified)
>>> if cl != AT_END:
...     first_hit = isearch.value

The next hit is determined by

>>> cl = isearch.advanceFrom(isearch.value, Unspecified)
>>> if cl != AT_END:
...     next_hit = isearch.value

If we know that hits at or below 1000 are irrelevant, we can use

>>> cl = isearch.advanceFrom(1000, Unspecified)
>>> if cl != AT_END:
...     hit_above_1000 = isearch.value

We can also indicate that we are interested only in hits below
some upper value.

>>> cl = isearch.advanceFrom(2000, 10000)
>>> if cl == INLIST_SUCCESS:
...     hit_above_2000_below_10000 = isearch.value

We can use the ``asSet`` method to obtain all hits
as a (BTree) set. ``asSet`` should only be called on fresh, i.e. (as yet)
unadvanced isearches (we may remove this restriction later, if there
is a need to).

>>> isearch = IAnd_int(*map(IBTree, seq_btrees))
>>> isearch.complete()
>>> bset = isearch.asSet()

Isearches also support iteration.

>>> for hit in isearch:
...   ...


``ISearch`` constructors
------------------------

The primary ``ISearch`` constructors are

``IBTree``
  turns a ``ZODB.BTrees`` object (tree, bucket, set or treeset) into
  an ``ISearch``.
``IAnd``
  combines ``ISearches`` by an ``and``
``Ior``
  combines ``ISearches`` by an ``or``
``INot``
  negates an ``ISearch``
``IFilter``
  a filtering ``ISearch``
``IEmpty``
  the empty ``ISearch``
``ISearch``
  a base class to define your own ``ISearch`` es

Any ``ISearch`` needs to know its keytype. Only ``ISearch`` es
of the same keytype can be combined.

``IBTree`` and
``INot`` can determine the keytype themselves. 
For the other constructors, the keytype is the first parameter.
For convenience, ``IAnd``, ``IOr`` and ``IFilter`` have
specializations with fixed keytype, e.g. ``IAnd_int``,
``IAnd_obj`` and ``IAnd_long``.

``INot`` and ``IFilter`` need an enumerator when their ``advanceFrom``
is called. The enumerator enumerates the elements in the search
domain (the possible hits). It has the methods ``check(elem)`` which
checks whether *elem* is in the domain and ``next(elem)``
which returns the element following *elem* in the domain or
``Unspecified``. The ``Enumerator`` class in ``dm.incrementalsearch``
turns a ``BTree`` into an enumerator.

For more information, see the docstrings.

Installation
------------

There are reports that the C parts of ``dm.incrementalsearch``
do not compile under Windows. Apparently, some extension
of the GNU C preprocessor is used which is unavailable
with the Microsoft C compiler. Thus, you probably need Cygwin
when you want to use ``dm.incrementalsearch`` under Windows
(or need at least the GNU C preprocessor and convince the Microsoft
compiler to use it as preprocessor).

The C parts are tightly coupled with the ``BTrees`` implementation
(part of the ZODB). If the data structures for ``BTrees``
change drastically, then these parts may break (the danger is small, though).
In this case, the content of ``btrees_structs.h`` need to be
adapted. See the comment at the start of this file.


Advance requirement
-------------------

We must not use an ``advance`` function to move backward, in
the following precise sense:

 1. when *key* is passed as first argument to ``advanceTo``,
    then any first argument to later calls for an ``advance`` function
    of this isearch must not be smaller than *key*.

 2. when *fromKey* is passed as first argument to ``advanceFrom``,
    then any first argument to later calls for an ``advance`` function
    of this isearch must be (strictly) larger then *fromKey*.

The behaviour is undefined when the condition is violated.


Advance function return values
------------------------------

Isearches may not be completely obedient -- in that they can advance
further than you told them to. However, they will not move
over any hit. Conceptionally, an ``ISearch`` is a sorted list
of hits which is lazily computed. The ``advance`` functions'
return value tells the caller how obedient the call has been:

``INLIST_SUCCESS``
  The call did precisely what the caller told it and the
  current value is in the list (i.e. a hit)

  ``INLIST_SUCCESS`` is the integer ``0``.
``INLIST``
  The call could not do what the caller told it (there was
  no hit there) and moved further to the next hit
``CANDIDATE``
  The call could not do what the caller told it (there was
  no hit there) and moved further. The current value may
  or may not be a hit.
``NOT_INLIST``
  The call advanced to a non hit. ``advanceFrom`` (unlike ``advanceTo``) must
  not return this value.
``AT_START``
  The iteration over the list did not yet start; the current value is
  undefined
``AT_END``
  the list is exhausted, there are no more hits; the current value is
  undefined and further ``advance`` calls are no longer allowed.

The result of the last ``advance`` call is stored as attribute
``classification``.



History
-------


3.1

  Fix: handle ``None`` in trees with object keys (which failed in Python 3
  with a ``TypeError``)

  Also define ``union`` and ``difference`` (beside ``intersection``).
  (Unlike ``intersection``) they are likely less efficient than
  the corresponding ``BTrees``
  operations but can handle inhomogenous structures provided
  they have the same key type. For example, you can compute
  the union of an ``IISet`` with an ``IOBTree``.

  ``estimatedSize`` can now be set externally for ``IBTree`` objects
  (to support caching).

3.0

  For Python 2.7/3.4+, BTrees 4+
  Tested under *nix only

2.0

  For Python 2.4.5+, ZODB 3.8+ (Zope 2.11+)
  Tested under *nix only; now runs on 64 bit architecture as well

