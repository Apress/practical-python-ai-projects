# Apress-AI

This is the code described in the book, along with generators of
random instances and test drivers.


First, there is a `Makefile` that tests every model in the book.  The
reader should run a `make` before making any change to the code to
verify that everything is working.

The only change that may be
*required* is to change the value of the `PYTHONPATH` variable to
indicate where is located Google's or-tools. This variable is set on
the first line of the `Makefile`.


For each section of the book, the structure is identical.  Consider,
for instance the chapter *Staffing*. The code in the book can be found
in the file `staffing.py`; in the same file a generator of problem is
included.  And in the file `test_staffing.py` there is a driver that
generates a problem and solves it. The reader can use this as an example
on how to use the models.

