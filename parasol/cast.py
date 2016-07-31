
__author__ = "Charlie Taylor (charlietaylor@sourceforge.net)"
__version__ = " 1.0 "
__date__ = "Jan 26, 2004"
__copyright__ = "Copyright (c) 2009 Charlie Taylor"
__license__ = "BSD"


def intDammit( val=0 ):
    """ 
        converts input to an integer, no matter what.
        returns an integer value, 0 if there's an error
        
        @param val: value to be converted to an integer
    """ 
    try:
        return int(val)
    except:
        return 0
        
def floatDammit( val=0.0 ):
    """ 
        converts input to a float, no matter what.
        returns a float value, 0.0 if there's an error
        
        @param val: value to be converted to a float
    """ 
    try:
        return float(val)
    except:
        return 0.0