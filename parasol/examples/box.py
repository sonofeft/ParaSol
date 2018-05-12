from parasol import *

# create system object (make sure author is correct... it's used for report)
PS = ParametricSoln(subtaskName="Cardboard Box", 
    author="Charlie Taylor", taskName="Sample Optimization", constraintTolerance=0.001)

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
