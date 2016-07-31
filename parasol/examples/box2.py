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
    ['L',12,1,20,39,'in','Length of Cardboard'],
    ['WoverL',1,0.05,1,39,'','Width/Length of Cardboard'],
    ['HoverW',.1,.05,.45,19,'','Height/Width of Box'],
    ['thk',0.1,0.02,0.4,40,'in','Thickness of Cardboard'],
    )


# now add any Result Variables That might be plotted
# result variables have: 
#    name,      units,  description <,possibly loLimit, hiLimit>
PS.addResultVars(
    ['Volume','cuin','Box Volume'],
    ['boxMass','lbm','Box Mass',0.,0.5],
    )

PS.setResultVariableLimits(name="boxMass", hiLimit=0.5)
# the following control routine ties together the system result variables
#  with the system design variables
def myControlRoutine(PS):
    # get current values of design variables    
    L,WoverL,HoverW,thk = PS.getDesVars("L","WoverL","HoverW","thk")
    
    W = WoverL * L
    h = HoverW * W

    Volume =(W-2*h) *(L-2*h) * h
    
    boxMass =(W*L - 4*h**2) * thk * density

    # set output variable values
    PS.setResultVar("boxMass", boxMass)
    PS.setResultVar("Volume", Volume)    

# need to tell system the name of the control routine
PS.setControlRoutine(myControlRoutine)

PS.evaluate()


if 1:
    # now optimize the system... it should match up with the carpet plots.
    maximize(PS, figureOfMerit="Volume", desVars=[ 'L', 'WoverL', 'HoverW'], MaxLoop=500)


if 1:
    makeSensitivityPlot(PS, 
        figureOfMerit="boxMass", desVars=['L', 'WoverL', 'HoverW'],
        makeHTML=1, dpi=70, linewidth=2, omitViolPts=0)

    makeSensitivityPlot(PS, 
        figureOfMerit="Volume", desVars=['L', 'WoverL', 'HoverW'],
        makeHTML=1, dpi=70, linewidth=2, omitViolPts=0)
if 1:

    makeCarpetPlot(PS, sysParam="Volume", 
        desVarL=[["HoverW",0.1,0.15,.2,0.25],["L",15,16,17]], angDesVarL=[40,0],
        xResultVar="boxMass",
        makeHTML=1, dpi=70, linewidth=2, smallLegend=1, iLabelsX=0, iLabelsY=0, 
        ptData=None, ptLegend='', logX=0, logY=0, titleStr='', yLabelStr='', 
        haLabel='center', vaLabel='center', omitViolPts=0)

if 1:


    makeContourPlot(PS, sysParam="Volume", desVars=["WoverL","HoverW"],
            interval = 0.0, maxNumCurves=50, nomNumCurves=12, makeHTML=1, 
            dpi=70, colorMap="summer")

if 1:
    makeContourPlot(PS, sysParam="boxMass", desVars=["WoverL","HoverW"],
            interval = 0.0, maxNumCurves=50, nomNumCurves=12, makeHTML=1, 
            dpi=70, colorMap="summer")

    make2DParametricPlot(PS, sysParam="Volume", desVar="HoverW",
        paramVar=["L",10,15,20]  ,makeHTML=1, dpi=70, linewidth=2,
        ptData=None, ptLegend='', logX=0, logY=0)


    make2DParametricPlot(PS, sysParam="Volume", desVar="HoverW",
        paramVar=["WoverL",0.2,0.4,0.6,0.8,1.]  ,makeHTML=1, dpi=70, linewidth=2,
        ptData=None, ptLegend='', logX=0, logY=0)


    make2DPlot(PS, sysParam=['Volume'], desVar='L', makeHTML=1, dpi=70, linewidth=2,
        ptData=None, ptLegend='', logX=0, logY=0, xResultVar=None, colorL=None, yLabel='',
        legendOnLines=0, titleStr='')


# now save summary of system
PS.saveFullSummary()

PS.close()  # finish up with output files
