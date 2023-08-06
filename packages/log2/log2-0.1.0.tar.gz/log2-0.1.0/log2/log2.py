def naive(x):
    """
    Compute the log base 2 of an unsigned 32-bit word

    Use the obvious way: O(N) operations
    Shift to the right `x` until `x` equals to zero.
    The log base 2 corresponds to the index of the most significant bit set.

    Parameters
    ----------
    x : int
        The unsigned 32-bit word to find the log base 2 of.

    References
    ----------
    .. [1] https://graphics.stanford.edu/~seander/bithacks.html#IntegerLogObvious

    Returns
    -------
    int
        The log base 2 of `x`
    """
    if x < 0:
        raise ValueError('x has to be positive')

    r = -1
    while x:
        r += 1
        x >>= 1
    
    return r

MultiplyDeBruijnBitPosition = [
    0, 9, 1, 10, 13, 21, 2, 29, 11, 14, 16, 18, 22, 25, 3, 30,
    8, 12, 20, 28, 15, 17, 24, 7, 19, 27, 23, 6, 26, 5, 4, 31
]

def lookup_table(x):
    """
    Compute the log base 2 of an unsigned 32-bit word

    O(lg(N)) operations with multiply and lookup

    Parameters
    ----------
    x : int
        The unsigned 32-bit word to find the log base 2 of.

    References
    ----------
    .. [1] https://graphics.stanford.edu/~seander/bithacks.html#IntegerLogDeBruijn

    Returns
    -------
    int
        The log base 2 of `x`
    """
    x |= x >> 1
    x |= x >> 2
    x |= x >> 4
    x |= x >> 8
    x |= x >> 16

    r = MultiplyDeBruijnBitPosition[((x * 0x07C4ACDD) & 0xffffffff) >> 27]

    return r

log_table_256 = [
    -1, 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
]

def fast_lookup_table(x):
    """
    Compute the log base 2 of an unsigned 32-bit word

    Fast method using a 256 elements log2 lookup table.
    Only needs 7 operations for computing the log base 2
    of a unsigned 32-bit word. This method takes a lot more
    memory space than the one implemented in `lookup_table`
    but is faster.

    Parameters
    ----------
    x : int
        The unsigned 32-bit word to find the log base 2 of.

    References
    ----------
    .. [1] https://graphics.stanford.edu/~seander/bithacks.html#IntegerLogLookup

    Returns
    -------
    int
        The log base 2 of `x`
    """
    r = 0
    tt = x >> 16
    if tt:
        t = tt >> 8
        r = (24 + log_table_256[t]) if t else (16 + log_table_256[tt])
    else:
        t = x >> 8
        r = (8 + log_table_256[t]) if t else log_table_256[x]

    return r