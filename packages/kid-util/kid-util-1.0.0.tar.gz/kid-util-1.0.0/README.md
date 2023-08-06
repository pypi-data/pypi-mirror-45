# KID util
Simple utils to generate and verify KID numbers with either MOD10 or MOD11.

## Installation

To install from PyPi as a module in your environment:

    pip install kid-util

To install from source as a module in your environment:

    python setup.py install

## Code usage from installation

Example code usages after installation:

    >>> import kid
    >>> kid.make('1234')
    '12344'
    >>> kid.make('1234', mode='MOD11')
    '12343'
    >>> kid.verify('12344')
    True
    >>> kid.verify('12343', mode='MOD11')
    True

## Running from command line

Generating KID from integer string:

    $ python -m kid -g 2345678
    23456783
    $ python -m kid -m mod11 -g 2345678
    23456788

Verifying KID from string:

    $ python -m kid -v 23456783
    True
    $ python -m kid -v 23456788
    False
    $ python -m kid -m mod11 -v 23456788
    True
    $ python -m kid -m mod11 -v 23456783
    False

## Testing from source

To run the tests:

    python -m unittest discover

Or if you have tox:

    tox
