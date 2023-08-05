# Copyright 2018 Goldman Sachs.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
#
# Chart Service will attempt to make public functions (not prefixed with _) from this module available. Such functions
# should be fully documented: docstrings should describe parameters and the return value, and provide a 1-line
# description. Type annotations should be provided for parameters.


import math
from .datetime import *
from .helper import plot_function
from ..errors import *
from numbers import Real

"""
Algebra library contains basic numerical and algebraic operations, including addition, division, multiplication, 
division and other functions on timeseries
"""


@plot_function
def add(x: pd.Series, y: pd.Series, method: Interpolate = Interpolate.STEP) -> pd.Series:
    """
    Add two series or scalars

    :param x: timeseries or scalar
    :param y: timeseries or scalar
    :param method: interpolation method (default: step)
    :return: timeseries of x + y

    **Usage**

    Add two series or scalar variables with the given interpolation method

    :math:`R_t =  X_t + Y_t`

    Alignment operators:

    =========   ========================================================================
    Method      Behavior
    =========   ========================================================================
    intersect   Resultant series only has values on the intersection of dates. Values
                for dates present in only one series will be ignored
    nan         Resultant series has values on the union of dates in both series. Values
                for dates only available in one series will be treated as nan in the
                other series, and therefore in the resultant series
    zero        Resultant series has values on the union of dates in both series. Values
                for dates only available in one series will be treated as zero in the
                other series
    step        Resultant series has values on the union of dates in both series. Values
                for dates only available in one series will be interpolated via step
                function in the other series
    =========   ========================================================================

    **Examples**

    Add two series:

    >>> a = generate_series(100)
    >>> b = generate_series(100)
    >>> add(a, b, Interpolate.STEP)

    **See also**

    :func:`subtract`
    """

    [x_align, y_align] = align(x, y, method)
    return x_align.add(y_align)


@plot_function
def subtract(x: pd.Series, y: pd.Series, method: Interpolate = Interpolate.STEP) -> pd.Series:
    """
    Add two series or scalars

    :param x: timeseries or scalar
    :param y: timeseries or scalar
    :param method: index alignment operator (default: intersect)
    :return: timeseries of x - y

    **Usage**

    Subtracts one series or scalar from another applying the given interpolation method

    :math:`R_t =  X_t - Y_t`

    Alignment operators:

    =========   ========================================================================
    Method      Behavior
    =========   ========================================================================
    intersect   Resultant series only has values on the intersection of dates
    union       Resultant series has values on union of dates (default of zero where
                date is not present)
    =========   ========================================================================

    **Examples**

    Subtract one series from another:

    >>> a = generate_series(100)
    >>> b = generate_series(100)
    >>> subtract(a, b, Interpolate.STEP)

    **See also**

    :func:`add`
    """

    # Determine how we want to handle observations prior to start date

    [x_align, y_align] = align(x, y, method)
    return x_align.subtract(y_align)


@plot_function
def multiply(x: pd.Series, y: pd.Series, method: Interpolate = Interpolate.STEP) -> pd.Series:
    """
    Multiply two series or scalars

    :param x: timeseries or scalar
    :param y: timeseries or scalar
    :param method: interpolation method (default: step)
    :return: timeseries of x * y

    **Usage**

    Multiply two series or scalar variables applying the given interpolation method

    :math:`R_t =  X_t \\times Y_t`

    Alignment operators:

    =========   ========================================================================
    Method      Behavior
    =========   ========================================================================
    intersect   Resultant series only has values on the intersection of dates. Values
                for dates present in only one series will be ignored
    nan         Resultant series has values on the union of dates in both series. Values
                for dates only available in one series will be treated as nan in the
                other series, and therefore in the resultant series
    zero        Resultant series has values on the union of dates in both series. Values
                for dates only available in one series will be treated as zero in the
                other series
    step        Resultant series has values on the union of dates in both series. Values
                for dates only available in one series will be interpolated via step
                function in the other series
    =========   ========================================================================

    **Examples**

    Multiply two series:

    >>> a = generate_series(100)
    >>> b = generate_series(100)
    >>> multiply(a, b, Interpolate.STEP)

    **See also**

    :func:`divide`
    """

    [x_align, y_align] = align(x, y, method)
    return x_align.multiply(y_align)


@plot_function
def divide(x: pd.Series, y: pd.Series, method: Interpolate = Interpolate.STEP) -> pd.Series:
    """
    Divide two series or scalars

    :param x: timeseries or scalar
    :param y: timeseries or scalar
    :param method: interpolation method (default: step)
    :return: timeseries of x / y

    **Usage**

    Divide two series or scalar variables applying the given interpolation method

    :math:`R_t =  X_t / Y_t`

    Alignment operators:

    =========   ========================================================================
    Method      Behavior
    =========   ========================================================================
    intersect   Resultant series only has values on the intersection of dates.
                Values for dates present in only one series will be ignored
    nan         Resultant series has values on the union of dates in both series. Values
                for dates only available in one series will be treated as nan in the
                other series, and therefore in the resultant series
    zero        Resultant series has values on the union of dates in both series. Values
                for dates only available in one series will be treated as zero in the
                other series
    step        Resultant series has values on the union of dates in both series. Values
                for dates only available in one series will be interpolated via step
                function in the other series
    =========   ========================================================================

    **Examples**

    Divide two series:

    >>> a = generate_series(100)
    >>> b = generate_series(100)
    >>> divide(a, b, Interpolate.STEP)

    **See also**

    :func:`multiply`
    """

    [x_align, y_align] = align(x, y, method)
    return x_align.divide(y_align)


@plot_function
def exp(x: pd.Series) -> pd.Series:
    """
    Exponential of series

    :param x: timeseries
    :return: exponential of each element

    **Usage**

    For each element in the series, :math:`X_t`, raise :math:`e` (Euler's number) to the power of :math:`X_t`.
    Euler's number is the base of the natural logarithm, :math:`ln`.

    :math:`R_t = e^{X_t}`

    **Examples**

    Raise :math:`e` to the power :math:`1`. Returns Euler's number, approximately 2.71828

    >>> exp(1)

    **See also**

    :func:`log`

    """
    return np.exp(x)


@plot_function
def log(x: pd.Series) -> pd.Series:
    """
    Natural logarithm of series

    :param x: timeseries
    :return: series with exponential of each element

    **Usage**

    For each element in the series, :math:`X_t`, return the natural logarithm :math:`ln` of :math:`X_t`
    The natural logarithm is the logarithm in base :math:`e`.

    :math:`R_t = log(X_t)`

    This function is the inverse of the exponential function.

    More information on `logarithms <https://en.wikipedia.org/wiki/Logarithm>`_

    **Examples**

    Take natural logarithm of 3

    >>> log(3)

    **See also**

    :func:`exp`

    """
    return np.log(x)


@plot_function
def power(x: pd.Series, y: float = 1) -> pd.Series:
    """
    Raise each element in series to power

    :param x: timeseries
    :param y: value
    :return: date-based time series of square roots

    **Usage**

    Raise each value in time series :math:`X_t` to the power :math:`y`:

    :math:`R_t = X_t^{y}`

    **Examples**

    Generate price series and raise each value to the power 2:

    >>> prices = generate_series(100)
    >>> power(prices, 2)

    **See also**

    :func:`sqrt`

    """
    return np.power(x, y)


@plot_function
def sqrt(x: Union[Real, pd.Series]) -> Union[Real, pd.Series]:
    """
    Square root of (a) each element in a series or (b) a real number

    :param x: date-based time series of prices or real number
    :return: date-based time series of square roots or square root of given number

    **Usage**

    Return the square root of each value in time series :math:`X_t`:

    :math:`R_t = \\sqrt{X_t}`

    **Examples**

    Generate price series and take square root of each value:

    >>> prices = generate_series(100)
    >>> sqrt(prices)

    **See also**

    :func:`pow`

    """
    if isinstance(x, pd.Series):
        return np.sqrt(x)

    result = math.sqrt(x)
    # return int if result is integral (should work for values up to 2**53)
    return round(result) if round(result) == result else result


@plot_function
def abs_(x: pd.Series) -> pd.Series:
    """
    Absolute value of each element in series

    :param x: date-based time series of prices
    :return: date-based time series of absolute value

    **Usage**

    Return the absolute value of :math:`X`. For each value in time series :math:`X_t`, return :math:`X_t` if :math:`X_t`
    is greater than or equal to 0; otherwise return :math:`-X_t`:

    :math:`R_t = |X_t|`

    Equivalent to :math:`R_t = \sqrt{X_t^2}`

    **Examples**

    Generate price series and take absolute value of :math:`X_t-100`

    >>> prices = generate_series(100) - 100
    >>> abs_(prices)

    **See also**

    :func:`exp` :func:`sqrt`

    """
    return abs(x)


@plot_function
def floor(x: pd.Series, value: float = 0) -> pd.Series:
    """
    Floor series at minimum value

    :param x: date-based time series of prices
    :param value: minimum value
    :return: date-based time series of maximum value

    **Usage**

    Returns series where all values are greater than or equal to the minimum value.

    :math:`R_t = max(X_t, value)`

    See `Floor and Ceil functions <https://en.wikipedia.org/wiki/Floor_and_ceiling_functions>`_ for more details

    **Examples**

    Generate price series and floor all values at 100

    >>> prices = generate_series(100)
    >>> floor(prices, 100)

    **See also**

    :func:`ceil`

    """
    assert x.index.is_monotonic_increasing
    return x.apply(lambda y: max(y, value))


@plot_function
def ceil(x: pd.Series, value: float = 0) -> pd.Series:
    """
    Cap series at maximum value

    :param x: date-based time series of prices
    :param value: maximum value
    :return: date-based time series of maximum value

    **Usage**

    Returns series where all values are less than or equal to the maximum value.

    :math:`R_t = min(X_t, value)`

    See `Floor and Ceil functions <https://en.wikipedia.org/wiki/Floor_and_ceiling_functions>`_ for more details

    **Examples**

    Generate price series and floor all values at 100

    >>> prices = generate_series(100)
    >>> floor(prices, 100)

    **See also**

    :func:`floor`

    """
    assert x.index.is_monotonic_increasing
    return x.apply(lambda y: min(y, value))
