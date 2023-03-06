# Written by Charlie Taylor

from scipy.optimize import fmin_cobyla
import os
from parasol.cast import intDammit
import traceback

optFSys = None # set this global variable to current object being optimized
_optLoopCount = 0
_findmin = 0
_constraintLoopCount = 0

def objFunction(x):
    global _optLoopCount 
    #global _fResult
    
    for i in range(len(x)):
        dvStr = optFSys.optDesVars[i]
        dv = optFSys.desVarDict[ dvStr ]
        #print dvStr,dv.val,                        # debug print
        
        optFSys.setDesignVar( dvStr, x[i]*dv.scaleFactor)
        
    #print "calling control Routine from optimizer"
    optFSys.evaluate()
    
    # f[0] is the object's figure of merit attribute value 
    #  after the control routine implements the new value(s) of design vars.
    
    try:
        fObj = optFSys.getResultVar(optFSys.figureOfMerit)
        #print 'fObj=',fObj                        # debug print
    except:
        fObj = 0.0
        print("ERROR... calling optimizer")
    
    if not _findmin:
        fObj *= -1.0
        
    #print  "in fvals", x, _fResult,
    print(".", end=' ')
    _optLoopCount += 1
    return fObj
    
def constraintFunc(x, iconstraint):
    global _constraintLoopCount
    _constraintLoopCount += 1
    
    for i in range(len(x)):
        dvStr = optFSys.optDesVars[i]
        dv = optFSys.desVarDict[ dvStr ]
        #print dvStr,dv.val,                        # debug print
        
        optFSys.setDesignVar( dvStr, x[i]*dv.scaleFactor)
        
    #print "calling control Routine from optimizer"
    optFSys.evaluate()
    
    row = optFSys.constraintList[iconstraint]
    constrCond, key = row
    
    rv = optFSys.resultVarDict[ key ]
    
    #print '... Calling Constraint',iconstraint,key,constrCond,
    # constraint held to greater than zero
    if constrCond == "<":
        #print rv.hiLimit
        return (rv.hiLimit - rv.val) # / rv.scaleFactor
    elif constrCond == ">":
        #print rv.loLimit
        return (rv.val - rv.loLimit) # / rv.scaleFactor
    else:
        #print 'on error'
        return 1.0 # mark as satisfied if not ">" or "<"
            
    
    
def getOptVarSummary(PS, optVarList=None):
    summary = PS.getSummary() + \
        '\n====================== OPTIMIZATION DESIGN VARIABLES ==' +\
        '=====================\n' +\
        '      name         value        minimum   maximum\n'
    
    for key in optVarList:
        dv = PS.desVarDict[key]
        desc = dv.description
        if len(dv.units) > 0:
            desc += '  (%s)'%dv.units
        summary += '%10s %12g %12g %12g %s\n'%\
            (key,dv.val,dv.minVal,dv.maxVal, desc )
    
    if _findmin:
        mLabel = 'Minimize'
    else:
        mLabel = 'Maximize'
    fmerit = PS.resultVarDict[PS.figureOfMerit]
    label = fmerit.description + ' (' + fmerit.name + ')'
    summary += '\n Figure of Merit: %s = %g %s <== %s'%(label, 
        PS.getResultVar(PS.figureOfMerit), fmerit.units, mLabel)
    
    showCon = 0
    for key,rv in list(PS.resultVarDict.items()):
        if rv.isConstrained():
            if not showCon:
                showCon = 1
                summary += '\n\n========================== OPTIMIZATION CONSTRAINTS ===='\
                        + '=====================\n'\
                        + '      name         value        minimum   maximum'

            minVal = '------------'
            if rv.hasLowConstraint() :  
                minVal = '%12g'%rv.loLimit
            maxVal = '------------'
            if rv.hasHighConstraint():
                maxVal = '%12g'%rv.hiLimit
                
            if len(rv.units) > 0:
                desc += '  (%s)'%rv.units
            summary += '\n%10s %12g %12s %12s %s'%\
                (key,rv.val,minVal,maxVal, rv.description )
    
    
    return summary + '\n======================================'\
            + '======================================\n'
    
def saveOptVarSummary(PS, optVarList=None, title=''):
    print('saving Optimization Variable Summary to',os.path.split(PS.summFileName)[-1]) 
    
    summStr =  getOptVarSummary(PS, optVarList)
    PS.summFile.write( title + summStr + '\n' )
    print(title, summStr)
    
    PS.optimizeHistoryL.append( [title, summStr] )
    
    PS.htmlFile.write('<center><table class="mytable">')
    if title:
        PS.htmlFile.write('<th bgcolor="#CCCCCC"> %s </th>'%title)
    PS.htmlFile.write('<tr><td nowrap>'+ '<pre>' + summStr + '</pre>' )
    PS.htmlFile.write('</td></tr></table></center>')
    
    if PS.userOptions.ppt:
        try:
            PS.pptDoc.addTextSlide( text=summStr.replace('\n','\r'), title=title.replace('\n','\r'),
                textFont='Courier New', textFontSize=14,
                noBullets=1)
        except:
            print("ERROR... FAILED to put plot in PowerPoint file")
            print(traceback.print_exc())
        
    if PS.userOptions.word:
        tableStr = [(title,),(' ',)]
        wordTable1 = PS.wordDoc.addTable( tableStr, Range=PS.wordDoc.selectCharacter(-2) )
        wordTable1.Style = PS.tblstyl
        PS.wordDoc.setCellStyle(wordTable1,1,1, just='c',bold=True, 
            fontName='Courier New', fontSize=14, bgcolor='15')
        PS.wordDoc.setCellStyle( wordTable1, 2, 1, 
            text=summStr )
        PS.wordDoc.selectCharacter(-1)
        PS.wordDoc.addText('  ')
        
    if PS.userOptions.excel: # save all excel output later from optimizeHistoryL
        pass


def minimize(PS, figureOfMerit="mass_lbm", desVars=None, MaxLoop=500, printLevel=1):
    optimize(PS, figureOfMerit=figureOfMerit, desVars=desVars, 
        findmin=1,  MaxLoop=MaxLoop, printLevel=printLevel)

def maximize(PS, figureOfMerit="mass_lbm", desVars=None, MaxLoop=500, printLevel=1):
    optimize(PS, figureOfMerit=figureOfMerit, desVars=desVars, 
        findmin=0,  MaxLoop=MaxLoop, printLevel=printLevel)

def optimize(PS, figureOfMerit="mass_lbm", desVars=None, 
    findmin=1,  MaxLoop=500, printLevel=1):
    '''to find max, set findmin = 0'''
    
    PS.firstEvaluateIfReqd()
    
    global optFSys, _optLoopCount, _findmin, _constraintLoopCount
    optFSys = PS
    _optLoopCount = 0
    _constraintLoopCount = 0
    _findmin = findmin  # use global flag in objective function
        
    PS.figureOfMerit = figureOfMerit
    PS.optDesVars = []
    
    for dvStr in desVars:
        dv = PS.desVarDict[dvStr]
        if PS.hasFeasibleControlVar( dv.name ):
            print('WARNING... %s is a feasible design variable\n   It can NOT be used as an optimization variable.'%dvStr)
            pass
        else:
            PS.optDesVars.append( dvStr )
        
    #PS.summFile.write('\nPRIOR TO OPTIMIZATION\n')
    if _findmin:
        mLabel = 'MINIMIZE'
    else:
        mLabel = 'MAXIMIZE'
    if printLevel:
        saveOptVarSummary(PS, PS.optDesVars,'\nPRIOR TO %s OPTIMIZATION\n'%mLabel)
        
    
    ndv = len( PS.optDesVars )
    ncon = 0
   
    
    if ndv <= 0:
        print("ERROR... there are no legal design variables for optimization")
        return
 
    xlow=[]
    xhigh=[]
    xinit = []
    
    # get limits of design variables
    i = 0
    for dvStr in PS.optDesVars:
        dv = PS.desVarDict[dvStr]
        xlow.append( dv.minVal / dv.scaleFactor )
        xhigh.append( dv.maxVal / dv.scaleFactor )
        xinit.append( PS.getDesignVar( dvStr) / dv.scaleFactor )
        i += 1
        
    # count any result variables that might be constraints
    PS.constraintList[:] = []
    for key,rv in list(PS.resultVarDict.items()):
        # only handle inequality constraints, equality constraints handled by feasibility variables
        if rv.hasLowConstraint() :  
            PS.constraintList.append( ['>',key] )
            ncon += 1
        if rv.hasHighConstraint():  
            PS.constraintList.append( ['<',key] )
            ncon += 1

    #xOut = mdot.findminormax(findmin,ndv,ncon,MaxLoop, xlow,xhigh,xinit,objAndConstraints)
    
    # set up constraint calling functions
    cons = []
    
    # first do bounds on x array
    def makeLo(n):
        return lambda x: x[n] - xlow[n]
    def makeHi(n):
        return lambda x: xhigh[n] - x[n]
    for n in range( len(xlow) ):
        conLo = makeLo(n)
        conHi = makeHi(n)
        cons.append( conLo )
        cons.append( conHi )
    
    # then do any constraints on result variables
    def makeCon(n):
        return lambda x: constraintFunc(x, n)
    for n in range( len(PS.constraintList) ):
        con = makeCon(n)
        cons.append( con )
    
    
    # rhobeg can be 1.0 because x values are scaled.
    xOut = fmin_cobyla(objFunction, xinit, cons, rhobeg=1.0, rhoend=1e-6,
            disp=intDammit(printLevel), maxfun=MaxLoop)

    if printLevel:
        print()
        print("   ==> OPTIMIZATION (Loops = %i)"%_optLoopCount, "(Max = %g)"%MaxLoop, end=' ')
        print(" (%i constraint loops)\n"%_constraintLoopCount)
    
    for i in range( len(PS.optDesVars) ):
        dvStr = PS.optDesVars[i]
        dv = PS.desVarDict[ dvStr ]
        
        dvVal = xOut[i] * dv.scaleFactor
        if printLevel:
            print('optimum',dvStr,'=',dvVal)
        #PS.summFile.write( '\noptimum %10s = %g'%(dvStr, dvVal) )
    if printLevel:
        print('\nscaled desVars',PS.optDesVars,'=',xOut[:ndv])
        
        print('gives',figureOfMerit,'=',PS.getResultVar(figureOfMerit),'\n')
    
    #PS.summFile.write('\n\ngives '+ str(figureOfMerit)+\
    #    ' = '+ str(PS.getResultVar(figureOfMerit))+'\n')
    
        
    for i in range(ndv):
        dvStr = PS.optDesVars[i]
        dv = PS.desVarDict[ dvStr ]
        dvVal = xOut[i] * dv.scaleFactor
        PS.setDesignVar( dvStr, dvVal)
    PS.evaluate()
        
    #PS.summFile.write('\nAFTER OPTIMIZATION\n')
    if printLevel:
        saveOptVarSummary(PS, PS.optDesVars,'\nAFTER %s OPTIMIZATION\n'%mLabel)


if __name__ == "__main__":  #self test
        
    from parasol.parasol_main import ParametricSoln

    # create system object (make sure author is correct... it's used for report)
    PS = ParametricSoln(subtaskName="Cardboard Box", 
        author="Charlie Taylor", taskName="Sample Optimization", constraintTolerance=0.001)

    density = 0.025 #: density of cardboard (lbm/cuin)

    # add design variables to the system (these variables may be used to
    # optimize the system or to create plots)
    # design vars have: 
    #     name, value, minVal, maxVal, NSteps,  units,  description
    PS.addDesVars(
        ['L',12,1,48,20,'in','Length of Cardboard'],
        ['W',12,1,48,20,'in','Width of Cardboard'],
        ['h',4,1,6,20,'in','Height of Box'],
        ['thk',0.1,0.02,0.4,20,'in','Thickness of Cardboard'],
        )


    # now add any Result Variables That might be plotted
    # result variables have: 
    #    name,      units,  description
    PS.addResultVars(
        ['Volume','cuin','Box Volume'],
        ['sysMass','lbm','Box Mass'],
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

    PS.evaluate()


    # now optimize the system...
    optimize(PS, figureOfMerit="Volume", desVars=['h'], findmin=0)

    print(getOptVarSummary(PS, PS.optDesVars ))
    print('   ===> Answer Should Be h = 2,  Volume = 128')
    
    # now save summary of system
    PS.saveFullSummary()
