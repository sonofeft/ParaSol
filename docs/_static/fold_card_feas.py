from parasol import *

PS = ParametricSoln(taskName="Best Box", 
    subtaskName="Feasible Optimization", author="Charlie Taylor")

# design vars have: 
#     name, value, minVal, maxVal, NSteps,  units,  description
PS.addDesVars(
    ['a',12,1,50,50,'in','Base Dimension of Cardboard'],
    ['b',10,2,10,50,'in','Height of Box'],
    )

# result variables have: 
#    name,      units,  description 
PS.addResultVars(
    ['Volume','cuin','Box Volume'],
    ['boxSurfArea','sqin','Box Surface Area'],
    )

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

PS.makeFeasiblePair( outName="Volume", feasibleVal=500.0, inpName='a')

# PS.evaluate() <-- done in setControlRoutine

# need to tell system the name of the control routine
PS.setControlRoutine(myControlRoutine)

aInit,bInit = PS("a","b")
PS.saveFullSummary()

# now optimize the system.
minimize(PS, figureOfMerit="boxSurfArea", desVars=[ 'b'], MaxLoop=500)

makeSensitivityPlot(PS, figureOfMerit="boxSurfArea", desVars=['b'])

make2DPlot(PS, sysParam=['boxSurfArea'], desVar='b')

make2DPlot(PS, sysParam=['a'], desVar='b')

# now save summary of system
PS.saveFullSummary()

PS.close()  # finish up with output files