from parasol import *

PS = ParametricSoln(taskName="Best Box", 
    subtaskName="Two Variable Optimization", author="Charlie Taylor")

# design vars have: 
#     name, value, minVal, maxVal, NSteps,  units,  description
PS.addDesVars(
    ['a',12,5,15,50,'in','Base Dimension of Cardboard'],
    ['b',8,2,10,50,'in','Height of Box'],
    )

# result variables have: 
#    name,      units,  description 
PS.addResultVars(
    ['Volume','cuin','Box Volume'],
    ['boxSurfArea','sqin','Box Surface Area'],
    )

PS.setResultVariableLimits(name="Volume", loLimit=500.)

# the following control routine ties together the system result variables
#  with the system design variables
def myControlRoutine(PS):
    # get current values of design variables    
    a,b = PS("a","b")

    # calculate result variables
    Volume = b * a**2
    boxSurfArea = 4.0*b*a + a**2

    # set output variable values
    PS["boxSurfArea"] = boxSurfArea
    PS["Volume"] = Volume

# need to tell system the name of the control routine
PS.setControlRoutine(myControlRoutine)

# now optimize the system.
minimize(PS, figureOfMerit="boxSurfArea", desVars=[ 'a','b'], MaxLoop=500)

# now save summary of system
PS.saveFullSummary()

makeSensitivityPlot(PS, figureOfMerit="boxSurfArea", desVars=['a','b'])

makeSensitivityPlot(PS, figureOfMerit="boxSurfArea", desVars=['a','b'], omitViolPts=1)

makeContourPlot(PS, sysParam="Volume", desVars=["a","b"])

makeContourPlot(PS, sysParam="boxSurfArea", desVars=["a","b"])

make2DParametricPlot(PS, sysParam="boxSurfArea", desVar="b", 
    paramVar=["a",8.,9.,10.,11.,12.])

# now save summary of system
PS.saveFullSummary()

PS.close()  # finish up with output files