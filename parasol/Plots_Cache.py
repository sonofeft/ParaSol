
# CONSTRAINT  VIOLATIONS are detected in ParametricSoln.violatesResultConstraint()
#  when the Cached result variables are placed back in ParametricSoln.resultVarDict
#    (and possibly ParametricSoln.desVarDict if desVar is a control variable
#     for a minmax or feasible pair)

class Plots_Cache(object):
    def __init__(self, PS, maxCache=100000):
        
        self.maxCache = maxCache
        self.Nresults = 0
        self.PS = PS
        self.resultDict = {} #: has tuple of result vars, indexed by desVar values
        
        self.desVarL = [] #: list of desVar objects (dv) that will index into resultDict
        #  desVarL omits desVars that are control variables, (minmax or feasible)
        
        self.resultVarL = [] #: list of result var objects (rv) including design control vars
        #  resultVarL includes desVars that are control variables, (minmax or feasible)
                
        for key,dv in self.PS.desVarDict.items():
            if PS.hasMinMaxControlVar(key) or PS.hasFeasibleControlVar(key):
                # control varaibles in minmax or feasible change like result vars
                self.resultVarL.append(dv)
            else:
                self.desVarL.append(dv)
        
        for key,rv in self.PS.resultVarDict.items():
            self.resultVarL.append(rv)
        
        print '  ----------------------------------- '
        for dv in self.desVarL:
            print '  DESIGN===>',dv.name,'in Plots_Cache desVar List'
        for rv in self.resultVarL:
            print '  RESULT===>',rv.name,'in Plots_Cache resultVar List'
        print '  ----------------------------------- '
    
    def saveParasolState(self):
        '''Save design variables values in dictionary, dvSavedD, so the state can
           be restored at a later time by restoreParasolState
        '''
        self.dvSavedD = {}
        for dv in self.desVarL:
            self.dvSavedD[dv.name] = dv.val

    def restoreParasolState(self):
        '''Restore design variables values from dvSavedD and call 
           ParametricSoln model evaluate(), this is done to restore the last call
           to saveParasolState
        '''
        for dv in self.desVarL:
            dv.val = self.dvSavedD[dv.name]
        self.PS.evaluate()
        
    def getResults(self, dump=0):
        '''
           Either retrieve results from cache, or rerun model to get result vars
           Assume that the desVars have been set in PS to desired values
        '''
        
        dvL = []
        for dv in self.desVarL:
            dvL.append( dv.val )
        dvTuple = tuple( dvL ) # tuple of design values is index into resultDict
        
        if self.resultDict.has_key(dvTuple):
            # if already in cache, retrieve and place in resultVars "val" attribute
            rvL = self.resultDict[dvTuple]
            for i,rv in enumerate( self.resultVarL ):
                rv.val = rvL[i]
                #print rv.name,'=',rv.val
            #print 'M',dvTuple,rvL
        else:
            self.PS.evaluate()
            
            rvL = []
            for rv in self.resultVarL: # may contain desVar control vars
                rvL.append( rv.val )
        
            # if maxCache not exceeded, then store result
            if self.Nresults < self.maxCache:
                self.Nresults += 1
                self.resultDict[dvTuple] = rvL
            #print 'E',dvTuple,rvL
                
        if dump:
            keyL = self.resultDict.keys()
            keyL.sort()
            for key in keyL:
                print key,self.resultDict[key]
    
    def setUpForFuncCall(self, dvNameL=None, outNameL=None):
        '''set up so that the ParametricSoln model can be called as a simple function
           by Carpet plot routine
        
           for example:
               setUpForFuncCall( dvL=['a','b'], outL=['x','y'])
               
            would set up for:
                x, y = self.funcCall( a, b )
        '''
        
        self.funcCallDesVarNameL = dvNameL
        self.funcCAllOutVarNameL = outNameL
        
        self.violationCoordL = [] # lists all result points (plot points) of violations
        self.violationDescD = {}  # dictionary hold descriptions of violations encountered
        
        
    def funcCall(self, *dvL):
        '''Treats ParametricSoln object like a function call as defined in setUpForFuncCall 
           (only used by Carpet plot routine)
        '''
        #print 'dvL=',dvL,'   self.funcCallDesVarNameL=',self.funcCallDesVarNameL
        
        for i,dvName in enumerate(self.funcCallDesVarNameL):
            self.PS.setDesignVar( dvName, dvL[i] )
            
        self.getResults()
        
        resultL = []
        for outName in self.funcCAllOutVarNameL:
            if self.PS.hasResultVar(outName):
                resultL.append( self.PS.getResultVar(outName) )
            else:
                resultL.append( self.PS.getDesignVar(outName) )
        
        # check for constraint violations
        vioList = self.PS.violatesResultConstraint()
        if len(vioList)>0:
            self.violationCoordL.append( resultL )
            for viol in vioList:
                self.violationDescD[viol] = viol # only 1 entry per violation description
        
        return resultL  # can be combination of result variables and design variables


    def getViolationXYLists(self):
        if len(self.violationCoordL)==0:
            return [],[]
            
        jj=range(len(self.violationCoordL[0]))
        
        rl = [[li[j] for li in self.violationCoordL] for j in jj] # a list of lists
        if len(rl)==1:
            rl=rl[0] #convert list of 1 list to a list
        return rl
