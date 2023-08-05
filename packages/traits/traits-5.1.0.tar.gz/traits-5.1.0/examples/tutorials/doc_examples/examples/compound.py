#  Copyright (c) 2007, Enthought, Inc.
#  License: BSD Style.

# compound.py -- Example of multiple criteria in a trait definition


# --[Imports]-------------------------------------------------------------------
from __future__ import print_function
from traits.api import HasTraits, Range, Trait, TraitError


# --[Code]----------------------------------------------------------------------
# Shows the definition of a compound trait.


class Die(HasTraits):

    # Define a compound trait definition:
    value = Trait(1, Range(1, 6), "one", "two", "three", "four", "five", "six")


# --[Example*]------------------------------------------------------------------
# Create a sample Die:
die = Die()

# Try out some sample valid values:
die.value = 3
die.value = "three"
die.value = 5
die.value = "five"

# Now try out some invalid values:
try:
    die.value = 0
except TraitError as excp:
    print(excp)

try:
    die.value = "zero"
except TraitError as excp:
    print(excp)
