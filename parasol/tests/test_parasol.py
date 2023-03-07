import unittest
# import unittest2 as unittest # for versions of python < 2.7

"""
        Method                  Checks that
self.assertEqual(a, b)           a == b   
self.assertNotEqual(a, b)        a != b   
self.assertTrue(x)               bool(x) is True  
self.assertFalse(x)              bool(x) is False     
self.assertIs(a, b)              a is b
self.assertIsNot(a, b)           a is not b
self.assertIsNone(x)             x is None 
self.assertIsNotNone(x)          x is not None 
self.assertIn(a, b)              a in b
self.assertNotIn(a, b)           a not in b
self.assertIsInstance(a, b)      isinstance(a, b)  
self.assertNotIsInstance(a, b)   not isinstance(a, b)  

See:
      https://docs.python.org/2/library/unittest.html
         or
      https://docs.python.org/dev/library/unittest.html
for more assert options
"""

import sys, os

here = os.path.abspath(os.path.dirname(__file__)) # Needed for py.test
up_one = os.path.split( here )[0]  # Needed to find parasol development version
ref_case_dir = os.path.join( here, 'ref_cases')
box_ref_case = os.path.join( ref_case_dir, 'box.py')

if here not in sys.path[:2]:
    sys.path.insert(0, here)
if up_one not in sys.path[:2]:
    sys.path.insert(0, up_one)

# from parasol.parasol_main import ParametricSoln
from parasol import *

# sys.argv if run directly: ['C:\\py_proj_github\\ParaSol\\parasol\\examples\\box.py']
# sys.argv if run as python box.py: ['box.py']

# sys.argv if run as pytest: ['C:\\Python310\\Scripts\\pytest', '--help']

class MyTest(unittest.TestCase):

    # def setUp(self):
    #     unittest.TestCase.setUp(self)
    #     old_sys_argv = sys.argv.copy()
    #     print('... old_sys_argv =', old_sys_argv)
    #     # while sys.argv:
    #     #     sys.argv.pop()
    #     sys.argv = [box_ref_case]
    #     print('... setUp sys.argv =', sys.argv)
    #     self.myclass = ParametricSoln(subtaskName="Box", 
    #                                   author="Charlie Taylor", 
    #                                   taskName="Sample Optimization", 
    #                                   constraintTolerance=0.001,
    #                                   printFilePaths=True)

    #     sys.argv = old_sys_argv
    #     print('... restored sys.argv =', sys.argv)

    # def tearDown(self):
    #     unittest.TestCase.tearDown(self)
    #     del( self.myclass )

    def test_should_always_pass_cleanly(self):
        """Should always pass cleanly."""
        pass

    # def test_class_existence(self):
    #     """Check that myclass exists"""
    #     sys.argv = [box_ref_case]
    #     PS = ParametricSoln(subtaskName="Box", 
    #                                   author="Charlie Taylor", 
    #                                   taskName="Sample Optimization", 
    #                                   constraintTolerance=0.001,
    #                                   printFilePaths=True)

    #     # See if the self.myclass object exists
    #     self.assertTrue(PS)

    def test_box_ref_case(self):
        """Check that myclass exists"""
        sys.argv = [box_ref_case]
        PS = ParametricSoln(subtaskName="Box", 
                                      author="Charlie Taylor", 
                                      taskName="Sample Optimization", 
                                      constraintTolerance=0.001,
                                      printFilePaths=True)

        density = 0.025 #: density of cardboard (lbm/cuin)

        # add design variables to the system (these variables may be used to
        # optimize the system or to create plots)
        # design vars have: 
        #     name, value, minVal, maxVal, NSteps,  units,  description
        PS.addDesVars(
            ['L',12,1,20,19,'in','Length of Cardboard'],
            ['W',12,1,20,19,'in','Width of Cardboard'],
            ['h',4,1,6,20,'in','Height of Box'],
            ['thk',0.1,0.02,0.4,20,'in','Thickness of Cardboard'],
            )


        # now add any Result Variables That might be plotted
        # result variables have: 
        #    name,      units,  description  <,possibly loLimit, hiLimit>
        PS.addResultVars(
            ['Volume','cuin','Box Volume'],
            ['sysMass','lbm','Box Mass',0.,0.5],
            )

        # the following control routine ties together the system components
        #  with the system design variables
        def myControlRoutine(PS):
            # get current values of design variables    
            L,W,h,thk = PS.getDesVars("L","W","h","thk")

            Volume = max(0.,(W-2*h)) * max(0.,(L-2*h)) * h
            
            sysMass = max(0.,(W*L - 4*h**2)) * thk * density

            # "sysMass" is required
            PS.setResultVar("sysMass", sysMass)
            PS.setResultVar("Volume", Volume)    

        # need to tell system the name of the control routine
        PS.setControlRoutine(myControlRoutine)

        # PS.evaluate() <-- done in setControlRoutine


        if 1:
            # now optimize the system... it should match up with the carpet plots.
            maximize(PS, figureOfMerit="Volume", desVars=[ 'L', 'h'])


        if 1:
            makeSensitivityPlot(PS, 
                figureOfMerit="sysMass", desVars=['L', 'W', 'h'],
                makeHTML=1, dpi=70, linewidth=2, omitViolPts=0)

            makeSensitivityPlot(PS, 
                figureOfMerit="Volume", desVars=['L', 'W', 'h'],
                makeHTML=1, dpi=70, linewidth=2, omitViolPts=0)

            makeCarpetPlot(PS, sysParam="Volume", 
                desVarL=[["h",1,1.5,3,4],["L",17,18,19,20]], angDesVarL=[40,0],
                xResultVar="sysMass",
                makeHTML=1, dpi=70, linewidth=2, smallLegend=1, iLabelsX=0, iLabelsY=0, 
                ptData=None, ptLegend='', logX=0, logY=0, titleStr='', yLabelStr='', 
                haLabel='center', vaLabel='center')

        if 1:


            makeContourPlot(PS, sysParam="Volume", desVars=["W","h"],
                    interval = 0.0, maxNumCurves=50, nomNumCurves=12, makeHTML=1, 
                    dpi=70, colorMap="summer")


            makeContourPlot(PS, sysParam="sysMass", desVars=["W","h"],
                    interval = 0.0, maxNumCurves=50, nomNumCurves=12, makeHTML=1, 
                    dpi=70, colorMap="summer")

            make2DParametricPlot(PS, sysParam="Volume", desVar="h",
                paramVar=["L",10,15,20]  ,makeHTML=1, dpi=70, linewidth=2,
                ptData=None, ptLegend='', logX=0, logY=0)



            make2DPlot(PS, sysParam=['Volume'], desVar='L', makeHTML=1, dpi=70, linewidth=2,
                ptData=None, ptLegend='', logX=0, logY=0, xResultVar=None, colorL=None, yLabel='',
                legendOnLines=0, titleStr='')


        # now save summary of system
        PS.saveFullSummary()

        PS.close()  # finish up with output files

        


if __name__ == '__main__':
    # Can test just this file from command prompt
    #  or it can be part of test discovery from nose, unittest, pytest, etc.
    unittest.main()

