from parasol import *

PS = ParametricSoln(taskName="Minimize F(x,y) with x>=0.6 and x+y<=1", 
     subtaskName="F(x,y)=(x-1)^2 + (y-1)^2", 
     author="Charlie Taylor", 
     constraintTolerance=0.001)
    

# design vars have: 
#     name, value, minVal, maxVal, NSteps,  units,  description
PS.addDesVars(
    ['x',0.6,.6,1.,50,'','X value'],
    ['y',0.2,-0.2,0.4,50,'','Y value'],
    )

# result variables have: 
#    name,      units,  description 
PS.addResultVars(
    ['F','','Function Value'],
    ['sumXY','','Sum of X and Y'],
    )

PS.setResultVariableLimits(name="sumXY", hiLimit=1.)

# the following control routine ties together the system result variables
#  with the system design variables
def myControlRoutine(PS):
    # get current values of design variables    
    x,y = PS("x","y")
    # set output variable values
    PS["F"] = (x-1.)**2 + (y-1.)**2
    PS["sumXY"] = x + y

# need to tell system the name of the control routine
PS.setControlRoutine(myControlRoutine)


# now optimize the system.
minimize(PS, figureOfMerit="F", desVars=[ 'x','y'], MaxLoop=500)

make2DParametricPlot(PS, sysParam="F", desVar="x",
    paramVar=["y",0.0,.1,.2,.3,.4,]  ,makeHTML=1, dpi=70, linewidth=2,
    ptData=None, ptLegend='', logX=0, logY=0)

makeCarpetPlot(PS, sysParam="F", xResultVar="sumXY",
    desVarL=[["x",0.6,0.8,1.0],["y",0.0,0.2,0.4]], angDesVarL=[40,0])

makeContourPlot(PS, sysParam="F", desVars=["x","y"])

# now save summary of system
PS.saveFullSummary()

PS.close()  # finish up with output files