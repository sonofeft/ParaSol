from parasol import *

PrDesc = ProblemDescription(taskName="Minimize F(x,y) with y>=-2", 
    subtaskName="F(x,y)=6x^2 + y^3 + xy", 
    author="Charlie Taylor")

# design vars have: 
#     name, value, minVal, maxVal, NSteps,  units,  description
PrDesc.addDesVars(
    ['x',1.0,-2,2.,50,'','X value'],
    ['y',0.2,-2,2.,50,'','Y value'],
    )

# result variables have: 
#    name,      units,  description 
PrDesc.addResultVars(
    ['F','','Function Value'],
    )

# the following control routine ties together the system result variables
#  with the system design variables
def myControlRoutine(PS):
    # get current values of design variables    
    x,y = PS("x","y")
    # set output variable values
    PS["F"] = 6.*x**2 + y**3 + x*y

# need to tell system the name of the control routine
PrDesc.setControlRoutine(myControlRoutine)

PS = ParametricSoln(probDesc=PrDesc)

# now optimize the system.
minimize(PS, figureOfMerit="F", desVars=[ 'x','y'], MaxLoop=500)

# now save summary of system
PS.saveFullSummary()

makeContourPlot(PS, sysParam="F", desVars=["x","y"])

make2DParametricPlot(PS, sysParam="F", desVar="x", paramVar=["y",-2,-1,0,1,2])

# now save summary of system
PS.saveFullSummary()

PS.close()  # finish up with output files
