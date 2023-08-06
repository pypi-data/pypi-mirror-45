pydtw
=====

Fast Imprementation of the Dynamic Time Warping For Python.

install
=======

::

    pip install pydtw

usage
=====

Alignment for two 1-dimensional sequences
-----------------------------------------

::

    from pydtw import dtw1d
    import numpy as np
    a = np.random.rand(10)
    b = np.random.rand(15)
    cost_matrix, cost, alignmend_a, alignmend_b = dtw1d(a, b)

Alignment for two 2-dimensional sequences
-----------------------------------------

::

    from pydtw import dtw2d
    import numpy as np

    a = np.random.rand(10, 4)
    b = np.random.rand(15, 4)
    cost_matrix, cost, alignmend_a, alignmend_b = dtw2d(a, b)
