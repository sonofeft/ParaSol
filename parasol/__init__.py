import os

here = os.path.abspath(os.path.dirname(__file__))

exec( open(os.path.join( here,'_version.py' )).read() )  # creates local __version__ variable

__all__ = ['ParametricSoln', 'makeSensitivityPlot', 'makeCarpetPlot', 'make2DParametricPlot',
    'makeContourPlot', 'make2DPlot', 'minimize', 'maximize']

# print( "Parasol Version:", __version__)

from parasol.parasol_main import ParametricSoln
from parasol.Optimize import minimize, maximize
from parasol.Plots import *
