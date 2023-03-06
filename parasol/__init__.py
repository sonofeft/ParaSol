import os

here = os.path.abspath(os.path.dirname(__file__))

exec( open(os.path.join( here,'_version.py' )).read() )  # creates local __version__ variable

__all__ = ['ParametricSoln', 'makeSensitivityPlot', 'makeCarpetPlot', 'make2DParametricPlot',
    'makeContourPlot', 'make2DPlot', 'minimize', 'maximize']


from .parasol_main import ParametricSoln
from .Optimize import minimize, maximize
from .Plots import *
