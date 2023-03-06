
__author__ = "Charlie Taylor (charlietaylor@sourceforge.net)"
__version__ = " 1.0 "
__date__ = "Jan 1, 2009"
__copyright__ = "Copyright (c) 2009 Charlie Taylor"
__license__ = "BSD"

from parasol.Goal import Goal
from parasol.cast import floatDammit, intDammit
from scipy.optimize import fminbound

POS_INF =  1.0E300
NEG_INF = -1.0E300


class MinMaxPair( object ):
    '''
       A MinMaxPair is a paired InputParam and OutputParam 
       where the val property of the InputParam is found
       such that the val property of the OutputParam is minimized 
       or maximized for the mathematical model under consideration
       (i.e. as modeled by the function call, functionToCall).
       
       @note: The InputParam's val property will be found in the range minVal to maxVal
       such that OutputParam.val is optimized when calling functionToCall
       (i.e. a Min/Max constraint is applied to the parameter pair).
       
       @note: It is the users responsibility to assure that InputParam.val is used
       in functionToCall 
       AND that functionToCall reassigns the val property of OutputParam
    '''
    def __init__(self, inpParam=None, outParam=None, functionToCall=None,
        findmin=0, tolerance=1.0E-6, maxLoops=400, failValue=None):
            
        '''Initialize parameter properties
           
           @param inpParam: input parameter object (InputParam)
           @param outParam: output parameter object (OutputParam)
           @param functionToCall: function using InputParam to calc OutputParam (callable)
           @param findmin: findmin is a logic flag (1=minimize, 0=maximize) (int)
           @param tolerance: allowable error of OutputParam.val (float)
           @param maxLoops: maximum loops in root solver
           @param failValue: returned value if solution attempt fails, 
              (if not input use inpParam.minVal)
        '''
        self.inpParam = inpParam #: InputParam object
        self.outParam = outParam #: OutputParam object
        self.functionToCall = functionToCall #: function using InputParam to calc OutputParam
        self.findmin = floatDammit(findmin) #: flag to minimize or maximize OutputParam.val
        self.tolerance = floatDammit(tolerance) #: allowable error of OutputParam.val
        self.maxLoops = intDammit(maxLoops) #: maximum loops in root solver
        
        if failValue==None:
            failValue = inpParam.minVal
        self.failValue = failValue #: returned value if solution attempt fails
        

    def optFunc(self, val):
        self.inpParam.val = val
        self.functionToCall()
        
        #print 'in optFunc, val=',val,'  result val=',self.outParam.val
        
        if self.findmin: # minimize or maximize
            return self.outParam.val
        else:
            return -1.0 * self.outParam.val

    def reCalc(self):
        '''calculate the value of inpParam.val that optimizes outParam.val
           Show non-convergence notification messages if applicable.
        '''
        
        val, fval, ierror, numFuncCalls = fminbound(self.optFunc, 
            self.inpParam.minVal, self.inpParam.maxVal, 
            args=(), xtol=self.tolerance, maxfun=self.maxLoops, full_output=1, disp=1)
        
        #print 'val, fval, ierror, numFuncCalls=',val, fval, ierror, numFuncCalls
        
        if ierror:
            self.inpParam.val = floatDammit(self.failValue)
        else:
            self.inpParam.val = val


class FeasiblePair( object ):
    '''
       A FeasiblePair is a paired InputParam and OutputParam 
       where the val property of the InputParam is found (inpParam.val)
       such that (outParam.val) is equal to
       the desired feasibleVal for the mathematical model under consideration
       (i.e. as modeled by the function call, functionToCall).
       
       @note: The InputParam's val property will be found in the range minVal to maxVal
       such that OutputParam.val==feasibleVal when calling functionToCall
       (i.e. A Feasibility constraint is applied to the parameter pair).
       
       @note: It is the users responsibility to assure that InputParam.val is used
       in functionToCall 
       AND that functionToCall reassigns the val property of OutputParam
    '''
    def __init__(self, inpParam=None, outParam=None, functionToCall=None,
        feasibleVal=0.0, tolerance=1.0E-6, maxLoops=40, failValue=None):
            
        '''Initialize parameter properties
           
           @param inpParam: input parameter object (InputParam)
           @param outParam: output parameter object (OutputParam)
           @param functionToCall: function using InputParam to calc OutputParam (callable)
           @param feasibleVal: feasible value that OutputParam Must have (float)
           @param tolerance: allowable error of OutputParam.val (float)
           @param maxLoops: maximum loops in root solver
           @param failValue: returned value if solution attempt fails, 
              (if not input use inpParam.minVal)
        '''
        self.inpParam = inpParam #: InputParam object
        self.outParam = outParam #: OutputParam object
        self.functionToCall = functionToCall #: function using InputParam to calc OutputParam
        self.feasibleVal = floatDammit(feasibleVal) #: feasible value of OutputParam.val
        self.tolerance = floatDammit(tolerance) #: allowable error of OutputParam.val
        self.maxLoops = intDammit(maxLoops) #: maximum loops in root solver
        
        if failValue==None:
            failValue = inpParam.minVal
        self.failValue = failValue #: returned value if solution attempt fails
        
        self.G = Goal(goalVal=feasibleVal, minX=inpParam.minVal, maxX=inpParam.maxVal, 
            funcOfX=self.feasibleFunc, tolerance=tolerance, maxLoops=maxLoops, failValue=failValue)

    def feasibleFunc(self, val):
        self.inpParam.val = val
        self.functionToCall()
        return self.outParam.val

    def reCalc(self):
        '''calculate the value of inpParam.val that gives feasibleVal==outParam.val'''
        
        val, ierror = self.G()
        if ierror:
            self.inpParam.val = floatDammit(self.failValue)
        else:
            self.inpParam.val = val

class OutputParam( object ):
    '''
       Generic Output Parameter.  
       
       Output Parameter has a current value and limit values.
        
       @note: If loLimit and hiLimit are reversed, they are corrected;
       Their default values are effectively at negative and positive infinity.
       
       @note: If assigning val, limits are NOT checked, however, 
       "inRange" function will return false; this is because out-of-range
       assignments are allowed and expected.
    '''
    def __init__(self, name='a', description='speed of sound', units='ft/sec',
        val=1.0, loLimit=NEG_INF, hiLimit=POS_INF):
            
        '''Initialize parameter properties
           
           @param name: simple name (str)
           @param description: long description (str)
           @param units:  physical units; Blank string if no units (str)
           @param val:  current numeric value (float)
           @param loLimit:  lower limit value (float)
           @param hiLimit:  upper limit value value (float)
        '''
        
        # if loLimit, hiLimit are reversed, correct them
        if loLimit > hiLimit:
            loLimit, hiLimit = hiLimit, loLimit
        
        self.name = name #: simple name
        self.description = description #: long description
        self.units = units #: physical units; Blank string if no units
        self.val = floatDammit(val) #: current numeric value
        self.loLimit = floatDammit(loLimit) #: lower limit value
        self.hiLimit = floatDammit(hiLimit) #: upper limit value
        
    def inRange(self):
        '''returns True if val is within limits, False otherwise'''
        return self.val>=self.loLimit and self.val<=self.hiLimit
        
    def hasLowConstraint(self):
        '''returns True if loLimit is > NEG_INF'''
        return self.loLimit > NEG_INF
        
    def hasHighConstraint(self):
        '''returns True if hiLimit is < POS_INF'''
        return self.hiLimit < POS_INF
        
    def isConstrained(self):
        return self.hasLowConstraint() or self.hasHighConstraint()
        

class InputParam( object ):
    '''
       Generic Input Parameter.  
       
       Has a current value and a range of possible values
       (arranged either in linear steps or geometric steps)
        
       @note: If stepVal is input, then use it to create range List (rangeL)
       Otherwise use NSteps to create range List
       
       @note: If linear is False, then use geometric steps from minVal to maxVal
       
       @note: If geometric range is illegal, switch to linear range
    '''
    def __init__(self, name='a', description='speed of sound', units='ft/sec',
        val=1.0, minVal=0.0, maxVal=10.0, NSteps=10, stepVal=None, linear=1):
            
        '''Initialize parameter properties and calculate range list (rangeL)
           
           @param name: simple name (str)
           @param description: long description (str)
           @param units:  physical units; Blank string if no units (str)
           @param val:  current numeric value (float)
           @param minVal:  minimum value (float)
           @param maxVal:  maximum value (float)
           @param NSteps:  number of steps from minVal to maxVal in rangeL (int)
           @param stepVal:  if input, then step size from minVal to maxVal in rangeL (float)
           @param linear: linear/geometric flag for steps from minVal to maxVal (boolean or int)
        '''
        
        # if minVal, maxVal are reversed, correct them
        if minVal > maxVal:
            minVal, maxVal = maxVal, minVal
        
        self.name = name #: simple name
        self.description = description #: long description
        self.units = units #: physical units; Blank string if no units
        self.val = floatDammit(val) #: current numeric value
        self.savedVal = self.val #: temporary storage location for val
        self.InitialVal = self.val #: initial val (for possible reset)
        
        self.minVal = floatDammit(minVal) #: minimum value
        self.maxVal = floatDammit(maxVal) #: maximum value
        self.linear = intDammit(linear) #: linear/geometric flag for steps from minVal to maxVal
        
        if NSteps<1: NSteps=1
        
        if stepVal and linear: #use stepVal only if linear steps
            try:
                NSteps = int( (maxVal-minVal)/stepVal )
            except:
                stepVal = (maxVal-minVal)/float(NSteps)
        else:
            stepVal = (maxVal-minVal)/float(NSteps)
            
        self.NSteps = NSteps #: number of steps from minVal to maxVal in rangeL
        self.stepVal = stepVal #: if input, then step size from minVal to maxVal in rangeL
            
                
        if linear :
            self.buildLinearRange()
        else:
            try:
                self.buildGeometricRange()
                self.stepVal = None #: undefined if using geometric range
            except:
                # only annoy the user slightly with non-critical error
                print('WARNING... Switched to linear range in parameters.InputParam for min/max=%g/%g'%(self.minVal,self.maxVal))
                self.buildLinearRange()

        # make scaleFactor for other modules to use (e.g. optimize)
        self.scaleFactor = (abs(self.minVal) + abs(self.maxVal)) / 2.0

    def buildLinearRange(self):
        self.rangeL = [self.minVal] #: list of values from minVal to maxVal (inclusive)
        N=1
        while self.rangeL[-1] + self.stepVal < self.maxVal:
            self.rangeL.append( self.minVal + self.stepVal*N )
            N += 1
        self.rangeL.append( self.maxVal )
        
        # check for tiny last step; Disallow less than stepVal/20
        if self.rangeL[-1]-self.rangeL[-2] < self.stepVal/20.0:
            del(self.rangeL[-2])
        
            
    def buildGeometricRange(self):
        self.rangeL = [self.minVal] #: list of values from minVal to maxVal (inclusive)
        N=1
        ratio = self.maxVal / self.minVal
        if ratio==0.0:
            stepRat = 1./0. # raise exception if ratio is zero
        
        stepRat = ratio**( 1.0/float(self.NSteps) )
        
        while self.rangeL[-1] * stepRat < self.maxVal:
            self.rangeL.append( self.rangeL[-1] * stepRat )
            N += 1
        self.rangeL.append( self.maxVal )
        
        # check for tiny last step; Disallow stepRat/20 difference in geometric ratio
        if ratio>1.0:
            if self.rangeL[-1]/self.rangeL[-2] < stepRat/20.0:
                del(self.rangeL[-2])
        else:
            if self.rangeL[-1]/self.rangeL[-2] > stepRat*19.0/20.0:
                del(self.rangeL[-2])

if __name__ == "__main__":
    
    IP = InputParam(name='a', description='speed of sound', units='ft/sec',
        val=1.0, minVal=1000.0, maxVal=6000.0, NSteps=5, stepVal=None, linear=1)
    print('check linear range')
    print(IP.rangeL)
            
    print('check output param')
    OP = OutputParam(name='delay', description='delay in sound arrival', units='sec',
        val=1.0, loLimit=1.0, hiLimit=10.0)
    
    OP.val = 0.0
    print(OP.val,'within limits=',OP.inRange())
    
    print()
    print('checking feasible pair')
    def feasTest():
        OP.val = 7000./IP.val # MUST reassign OutputParam.val property
        return
        
    FP = FeasiblePair(  inpParam=IP, outParam=OP, functionToCall=feasTest,
        feasibleVal=5.0, tolerance=1.0E-6, maxLoops=40, failValue=None)
    FP.reCalc()
    print('for IP.val=',IP.val,'OP.val=',OP.val,'IP.val should be 1400.0')
    
    
    print()
    print('checking min/max pair')
    def minmaxTest():
        x = (IP.val-1000.0)/1000.0
        OP.val = 10.0 * (x**2 - x**3) # MUST reassign OutputParam.val property
        return
        
    MP = MinMaxPair( inpParam=IP, outParam=OP, functionToCall=minmaxTest,
        findmin=0, tolerance=1.0E-6, maxLoops=400, failValue=None)
    MP.reCalc()
    print('for IP.val=',IP.val,'OP.val=',OP.val,'IP.val should be 1666.666...')    
    
