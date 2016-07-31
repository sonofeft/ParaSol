
from parasol_main import ParametricSoln
from parameters import POS_INF, NEG_INF 

class ProblemDescription( object ):
    def __init__(self, subtaskName="", taskName='',
            author="", constraintTolerance=0.0):
                
        self.subtaskName = subtaskName
        self.taskName = taskName
        self.author = author
        self.constraintTolerance = constraintTolerance
        
        self.desVarL = [] #: list of design variable descriptions
        self.resVarL = [] #: list of result variable descriptions
        self.resVarLimitD = {} #: dictionary of result variable limits
        
        self.controlRoutine = None #: control routine for problem
        self.renderControlRoutine = None #: control routine for POV rendering

    def setControlRoutine(self, controlRoutine):
        self.controlRoutine = controlRoutine
        
    def setRenderControlRoutine(self, renderControlRoutine):
        self.renderControlRoutine = renderControlRoutine

    def addDesVars(self, *dvLists):
        ''' add design variables to the system (these variables may be used to
            optimize the system or to create plots)
            design vars have: 
            name, value, minVal, maxVal, NSteps,  units,  description
        '''
        for row in dvLists:
            self.desVarL.append( row )

    def addResultVars(self, *rvLists):
        ''' now add any Result Variables That might be plotted
            result variables have: 
               name,      units,  description <,possibly loLimit, hiLimit>
        '''
        for row in rvLists:
            self.resVarL.append( row )
        
    def setResultVariableLimits(self, name="resultvar", loLimit=NEG_INF, hiLimit=POS_INF):
        self.resVarLimitD[name] = [loLimit, hiLimit]
