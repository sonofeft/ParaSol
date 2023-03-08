#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
ParaSol (Parametric Solutions) is a python framework in which mathematical models can be investigated parametrically.

Parasol enables easy optimization, sensitivity study, and visualization. 
The math model can be as big or as small as desired. 
Output is generated in plain text, HTML, and native Microsoft Suite files (Excel, Word and PowerPoint).

A problem is defined by input and output parameters. 
Results are presented in a manner that conveys insight into system trends and characteristics. 
The process of performing an analysis results in an ample assortment of graphs, charts, and images 
that display system sensitivities, variations, and characteristics. 
Barriers to creating these displays have been reduced to single commands in order to facilitate their use.

Parasol has been designed to run under Microsoft Windows. 
In that environment, creating a new project and running cases consists of the following steps:



ParaSol
Copyright (C) 2009-2016  Charlie Taylor

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

-----------------------

"""
from math import *
import traceback
import pickle as pickle
import os
here = os.path.abspath(os.path.dirname(__file__))

from parasol.parameters import InputParam, OutputParam, FeasiblePair, MinMaxPair, POS_INF, NEG_INF 


import sys, os
import time
from parasol import HTML_supt

from parasol import LikeDict
from parasol.cast import floatDammit, intDammit
from parasol.Summary import Summary


__author__ = 'Charlie Taylor'
__copyright__ = 'Copyright (c) 2009 Charlie Taylor'
__license__ = 'GPL-3'
__version__ = '' # will be set by next line of code
exec( open(os.path.join( here,'_version.py' )).read() )  # creates local __version__ variable
__email__ = "cet@appliedpython.com"
__status__ = "3 - Alpha" # "3 - Alpha", "4 - Beta", "5 - Production/Stable"


def getVersion():
    return __version__


splash ='Parametric Solutions\n'+\
        'parasol v'+getVersion() + '\n'+\
        'contact: C. Taylor, cet@appliedpython.com\n'

splashText = '------------------------------------------------------------\n'+\
        splash+\
        '------------------------------------------------------------'

# ------  check for user options (-w to make word doc, -p to make power point)
from optparse import OptionParser

class OptionParsingError(RuntimeError):
    def __init__(self, msg):
        self.msg = msg

class OptionParsingExit(Exception):
    def __init__(self, status, msg):
        self.msg = msg
        self.status = status

class ModifiedOptionParser(OptionParser):
    def error(self, msg):
        raise OptionParsingError(msg)

    def exit(self, status=0, msg=None):
        raise OptionParsingExit(status, msg)
    
_parser = ModifiedOptionParser()
_parser.add_option("-x", "--excel",
                  action="store_true", dest="excel", default=False,
                  help="create output in a Microsoft Excel document")
_parser.add_option("-w", "--word",
                  action="store_true", dest="word", default=False,
                  help="create output in a Microsoft Word document")
_parser.add_option("-p", "--ppt",
                  action="store_true", dest="ppt", default=False,
                  help="create output in a Microsoft Power Point document")
_parser.add_option("-q", "--quiet",
                  action="store_false", dest="show", default=True,
                  help="don't show Word, Excel or PowerPoint docs")
_parser.add_option("-o", "--open",
                  action="store_true", dest="open", default=False,
                  help="leave Microsoft Word, Excel or PowerPoint Open")
_parser.add_option("-i", "--isize", action="store",
                  type="string", dest="imageSize", default="m",
                  help="(vs,s,m,l,vl)image size in Word or PowerPoint")
_parser.add_option("-f", "--font", action="store",
                  type="string", dest="fontName", default="c",
                  help="font in Word (c=Courier, l=Lucida, v=Vera, o=OCR, t=type)")

# detect if running pytest
IN_PYTEST = False 
if os.path.split(sys.argv[0])[-1] == 'pytest':
    print( '---> pytest sys.argv =', sys.argv)
    IN_PYTEST = True 
    print( 'IN_PYTEST =', IN_PYTEST)

# need special handling if running pytest or on ReadTheDocs
if IN_PYTEST or 'READTHEDOCS' in os.environ:
    (_userOptions, _userArgs) = _parser.parse_args([''])
else:
    try:
        (_userOptions, _userArgs) = _parser.parse_args()
        # print( _userOptions )
        # print( _userArgs )
    except OptionParsingExit:
        sys.exit()
    except:
        print(' === optparse has a problem when running pytest ===' )
        print(traceback.print_exc())
        (_userOptions, _userArgs) = _parser.parse_args([''])


def win32Warning(appName):
        print('\n=============================================================')
        print("WARNING  WARNING  WARNING  WARNING  WARNING  WARNING  WARNING")
        print('=============================================================\n')
        print("    Could NOT start ",appName)
        print('    make sure that you have installed Python for Win32 (pywin32) extensions')
        print('    using: python -m pip install --upgrade pywin32\n')
        print('    for python version:',sys.version.split()[0])
        print('=============================================================')
        input('Hit Return to Continue w/o '+appName)

if _userOptions.excel:
    try:
        from parasol import Excel_wrapper
    except:
        _userOptions.excel = False
        win32Warning('Microsoft Excel')
        
if _userOptions.word:
    try:
        from parasol import Word_wrapper
    except:
        _userOptions.word = False
        win32Warning('Microsoft Word')
        
if _userOptions.ppt:
    try:
        from parasol import PPT_wrapper
    except:
        _userOptions.ppt = False
        win32Warning('Microsoft PowerPoint')

# -----------------
    
def headerStr( hstr, fillCh, L ):
    l2 = int((L - len(hstr) - 2) / 2)
    s = fillCh*l2 + ' ' + hstr + ' '
    return s + fillCh*(L-len(s))


class ParametricSoln(object):
    """ParaSol (Parametric Solutions) is a python framework in which mathematical models 
       can be investigated parametrically.

    """
    
    __firstParametricSoln = None #: use to keep track of 1st instance of ParametricSoln
    

    
    def getVersion(self):
        return getVersion()
    
    def __getitem__(self, name):
        '''return the value of design or result variable with name'''
        if self.hasDesignVar( name ):
            dv = self.desVarDict[name]
            return dv.val
        elif self.hasResultVar( name ):
            rv = self.resultVarDict[name]
            return rv.val
        else:
            return None
            
    def __setitem__(self, name, val):
        '''set the value of design or result variable with name'''
        if self.hasDesignVar( name ):
            self.setDesignVar(name, val)
        elif self.hasResultVar( name ):
            self.setResultVar(name, val)
        else:
            print('ERROR in ParametricSoln.__setitem__, %s is not recognized'%name)
    
    def __call__(self, *varNames):
        '''return the values of design and result variables in varNames list'''
        resultL = []
        for name in varNames:
            
            if self.hasDesignVar( name ):
                dv = self.desVarDict[name]
                resultL.append( dv.val )
                
            if self.hasResultVar( name ):
                rv = self.resultVarDict[name]
                resultL.append( rv.val )
                
        if len(resultL)==1:
            return resultL[0]
        else:
            return resultL
            

    def __init__(self, subtaskName="simple model", taskName='System Study',
        controlRoutine=None, author="", constraintTolerance=0.001,
        probDesc=None, printFilePaths=False):
        """Inits ParametricSoln."""
        
            
        if len(author)==0:
            author = 'anon'

        self.userOptions = _userOptions
        
        self.probDesc = probDesc
        
        self.author = author
        self.taskName = taskName
        self.constraintTolerance = constraintTolerance
        
        self.subtaskName = subtaskName
        self.desVarDict = LikeDict.LikeDict() #: dictionary of design Variables in system
        self.resultVarDict =  LikeDict.LikeDict() #: dict of result variables in system
        
        self.feasibleVarList = [] #: list of Feasible Pairs
        self.minmaxVarList = [] #: list of MinMax Pairs
        
        self.constraintList = [] #: Optimize.optimize might initialize
        self.controlRoutine = controlRoutine #: will be called to set component design params
        
        self.optimizeHistoryL = [] #: holds any optimization summary info as [title, summStr]
        
        self.NumEvaluations = 0 #: count number of times the evaluate method is called
        
        # set flag to indicate that self.close() was not yet called
        self._close_was_called = 0
        
        # make text output file in case's subdirectory
        scriptName =  os.path.split( sys.argv[0] )[-1]
        scriptPath = os.path.abspath(scriptName)[:]
        
        newDirPath = os.path.join( os.path.dirname( scriptPath ) , scriptName[:-3] )
        if printFilePaths:
            print("scriptName:",scriptName)
            print("scriptPath:",scriptPath)
            print("newDirPath:",newDirPath)
        
        if not os.path.isdir( newDirPath ):
            os.mkdir( newDirPath )
            if printFilePaths:
                print("created new directory",newDirPath)

        self.scriptName = scriptName
        self.outputPath = newDirPath
        self.summFileName = newDirPath + scriptName[:-2] + 'summary'
        
        # if multiple ParametricSoln objects, use same summFile
        if ParametricSoln.__firstParametricSoln:
            self.summFile = ParametricSoln.__firstParametricSoln.summFile
        else:
            self.summFile = open( self.summFileName, 'w' )
        
        self.summFile.write(splashText + '\n\n' )
        self.summFile.write( taskName + '\n   by: '+author+'\n')
        self.summFile.write(' date: '+ time.strftime('%A %B %d, %Y')+'\n\n')
        
        # if multiple ParametricSoln objects, use same summaryObj
        if ParametricSoln.__firstParametricSoln:
            self.summaryObj = ParametricSoln.__firstParametricSoln.summaryObj
        else:
            self.summaryObj = Summary(summaryTitle=subtaskName, subTitle='system')

        # may not use it, but make Pickle file name just in case
        self.pickleFileName = os.path.join(newDirPath, scriptName[:-2] + 'pickle')
        
        # now make HTML file in original script's directory
        self.htmlFileName = os.path.join( os.path.dirname( scriptPath ),
                            scriptName[:-2] + 'htm' )
        if printFilePaths:
            print('HTML file:',self.htmlFileName)
        
        # if multiple ParametricSoln objects, use same htmlFile
        if ParametricSoln.__firstParametricSoln:
            self.htmlFile = ParametricSoln.__firstParametricSoln.htmlFile
        else:
            self.htmlFile = open( self.htmlFileName, 'w' )
        
        # ============  if probDesc is input ===================
        # set any variables due to probDesc
        if probDesc:
            for a in ["subtaskName", "taskName", "author", "constraintTolerance"]:
                # if the probDesc attribute exists and has a value, assign it to self
                if hasattr(probDesc,a) and getattr(probDesc,a):
                    setattr(self, a, getattr(probDesc,a) )
        
            for row in probDesc.desVarL:
                self.addDesVars( row )
                
            for row in probDesc.resVarL:
                self.addResultVars( row )

            for name, row in list(probDesc.resVarLimitD.items()):
                print('name, row=',name, row)
                self.setResultVariableLimits( name=name, loLimit=row[0], hiLimit=row[1])
        
            if probDesc.controlRoutine:
                self.setControlRoutine(probDesc.controlRoutine)
        
            
        self.htmlFile.write( HTML_supt.getHead(\
            title=self.taskName, task=self.subtaskName, author=self.author,
            date=time.strftime('%B %d, %Y'), version='ParametricSoln v'+getVersion()))
        # ============  end of probDesc input ===================
        
        if self.userOptions.excel:
            # if multiple ParametricSoln objects, use same xlDoc
            if ParametricSoln.__firstParametricSoln:
                self.xlDoc = ParametricSoln.__firstParametricSoln.xlDoc
            else:
                if self.userOptions.show:
                    self.xlDoc = Excel_wrapper.ExcelWrap(Visible=1)
                else:
                    self.xlDoc = Excel_wrapper.ExcelWrap(Visible=0)
            
            self.xlSheetD = {}  # make sure no sheet name duplicates
            
            self.xlDocName = os.path.join( os.path.dirname( scriptPath ),
                            scriptName[:-2] + 'xlsx')
                                
            self.xlSigText = self.subtaskName + '\rParametricSoln v'+getVersion() +\
                '\rby: '+self.author +'\r' + time.strftime('%B %d, %Y') +\
                '\r' + self.taskName
            
            
        if self.userOptions.ppt:
            # if multiple ParametricSoln objects, use same pptDoc
            if ParametricSoln.__firstParametricSoln:
                self.pptDoc = ParametricSoln.__firstParametricSoln.pptDoc
            else:
                self.pptDoc = PPT_wrapper.PPTwrap()
                if self.userOptions.show:
                    self.pptDoc.show()
                    
            self.pptDocName = os.path.join( os.path.dirname( scriptPath ),
                            scriptName[:-2] + 'ppt')
                                
            pptText = self.subtaskName + '\rParametricSoln v'+getVersion() +\
                '\rby: '+self.author +'\r' + time.strftime('%B %d, %Y')
            self.pptDoc.addTextSlide( text=pptText, title=self.taskName)
            
            
        if self.userOptions.word:
            # if multiple ParametricSoln objects, use same wordDoc
            if ParametricSoln.__firstParametricSoln:
                self.wordDoc = ParametricSoln.__firstParametricSoln.wordDoc
            else:
                self.wordDoc = Word_wrapper.WordWrap()
                if self.userOptions.show:
                    self.wordDoc.show()
                else:
                    self.wordDoc.setFastOptions()
                
            self.wordDocName = os.path.join(os.path.dirname( scriptPath ),
                            scriptName[:-2] + 'doc')
                                
            self.wordDoc.addText('   ')
            tableStr = [(self.taskName,),(self.subtaskName, 'ParametricSoln v'+getVersion()),
                ('by: '+self.author, time.strftime('%B %d, %Y'))]
            wordTable1 = self.wordDoc.addTable( tableStr , Range=self.wordDoc.selectCharacter(-2), fullWidth=1 )
            self.wordDoc.mergeRow( wordTable1, NRow=1)
            #self.wordDoc.mergeRow( wordTable1, NRow=2)
            self.wordDoc.setCellStyle(wordTable1,1,1, just='c',bold=True, fontSize=18, bgcolor='15')
            self.wordDoc.setCellStyle(wordTable1,2,2, just='r')
            self.wordDoc.setCellStyle(wordTable1,3,2, just='r')
            self.wordDoc.selectCharacter(-1)
            self.wordDoc.addText('  ')
            
            fontName = "Courier New"
            if self.userOptions.fontName.lower() == "t":
                fontName = "Lucida Sans Typewriter"
            if self.userOptions.fontName.lower() == "l":
                fontName = "Lucida Console"
            if self.userOptions.fontName.lower() == "v":
                fontName = "Bitstream Vera Sans Mono"
            if self.userOptions.fontName.lower() == "v":
                fontName = "OCR A Extended"
            
            self.tblstyl = self.wordDoc.createTableStyle( name='myStyle', 
                font=fontName,size=8, borders=1, bold=0, keepTogether=1)
            
            self.wordDocImagefracPage=0.5
            if self.userOptions.imageSize.lower() == 'vs':
                self.wordDocImagefracPage=0.3
            if self.userOptions.imageSize.lower() == 's':
                self.wordDocImagefracPage=0.4
            if self.userOptions.imageSize.lower() == 'm':
                self.wordDocImagefracPage=0.5
            if self.userOptions.imageSize.lower() == 'l':
                self.wordDocImagefracPage=0.6
            if self.userOptions.imageSize.lower() == 'vl':
                self.wordDocImagefracPage=0.8
        
        if ParametricSoln.__firstParametricSoln==None:
            ParametricSoln.__firstParametricSoln = self
    
    def __del__(self):
        if not self._close_was_called:
            self.close()
    
    def close(self):
        # set flag to show self.close() was called
        print('Closing all open files')
        self._close_was_called = 1
        
        self.htmlFile.write('<table class="mytable">')
        self.htmlFile.write('<tr><td nowrap>'+ '<pre>' + splash + '</pre>' )
        self.htmlFile.write('</td><td width="90%">&nbsp;</td></tr></table>')
        
        self.htmlFile.write( HTML_supt.getFooter() )
        self.htmlFile.close()
        self.summFile.close()
        
        if self.userOptions.excel:
            if self.optimizeHistoryL:
                rs = [[' ']]
                for row in self.optimizeHistoryL:
                    title, summStr = row
                    def addText(text):
                        text=text.replace('\r','\n')
                        spL = text.split('\n')
                        for s in spL:
                            rs.append( [s] )
                    addText( title )
                    addText( summStr )
                    addText( '\n\n' )
                        
                sheetName="Optimization"
                if sheetName not in self.xlSheetD:
                    print('making excel sheet',sheetName)
                    self.xlSheetD[sheetName] = sheetName
                    self.xlDoc.makeDataSheet( rs, sheetName=sheetName, autoFit=0, rowFormatL=None,
                        textFont='Courier New', textFontSize=10)
            
            self.xlDoc.xlApp.ActiveWorkbook.SaveAs( self.xlDocName )
            if not self.userOptions.open:
                self.xlDoc.close()
        
        if self.userOptions.ppt:
            self.pptDoc.saveAs( self.pptDocName )
            if not self.userOptions.open:
                self.pptDoc.Quit()
        
        if self.userOptions.word:
            tableStr = [(splash,),]
            wordTable1 = self.wordDoc.addTable( tableStr, Range=self.wordDoc.selectCharacter(-2) , fullWidth=1)
            wordTable1.Style = self.tblstyl
            self.wordDoc.selectCharacter(-1)
            self.wordDoc.addText('  ')
            
            
            
            self.wordDoc.saveAs(self.wordDocName)
            if not self.userOptions.open:
                self.wordDoc.Quit()
        print(splashText)
    
    def setDesignVar(self, dvStr, val):
        dv = self.desVarDict[dvStr]
        dv.val = floatDammit( val )
        #print "in setDesignVar, setting ",dvStr,"to",val
        
    def getDesignVar(self, dvStr):
        dv = self.desVarDict[dvStr]
        return dv.val
        
    def getDesVars(self, *dvItems):
        '''handle either single design var or list of design vars'''
        result = []
        for dvStr in dvItems:
            if type(dvStr)==type([1,2]):
                for s in dvStr:
                    result.append( self.getDesignVar( s ) )
            else:
                result.append( self.getDesignVar( dvStr ) )
                
        if len(result)==1:
            return result[0]
        else:
            return result
        
        
    def getDesignVarAxisLabel(self, dvStr):
        dv = self.desVarDict[dvStr]
        return self.getAxisLabel( dvStr, dv )
    
    def getControlDesVarStr(self,key):
                
        feasStr = ''
        if self.hasFeasibleControlVar( key ):
            fv = self.getFeasibleVarWithControlVar( key )
            feasStr = '* -----> ' +\
                ' (%s varies to make %s = %g %s)'%(key, fv.outParam.name, fv.feasibleVal, fv.outParam.units)
            
            
        minmaxStr = ''
        if self.hasMinMaxControlVar( key ):
            mmv = self.getMinMaxVarWithControlVar( key )
            if mmv.findmin:
                oStr = 'minimize'
            else:
                oStr = 'maximize'
            minmaxStr = '* -----> ' +\
                ' (%s varies to %s %s)'%(key, oStr, mmv.outParam.name)
        return feasStr, minmaxStr
    
    def getDesVarShortSummary(self, *omitList):
        
        sList = []
        for key,dv in list(self.desVarDict.items()):
            if key in omitList:
                continue
            
            feasStr, minmaxStr = self.getControlDesVarStr(key)
            
            # do NOT show control design variables in desVar... show them in resultVars
            if not (feasStr or minmaxStr): 
                sList.append( "%s = %g %s"%(key, dv.val, dv.units ) )
                
        return '\n'.join( sList )
    
    def getDesVarSummary(self, *omitList):
        
        oList = [( 'NAME','VALUE','MINIMUM','MAXIMUM','DESCRIPTION','','')]
        
        for key,dv in list(self.desVarDict.items()):
            if key in omitList:
                continue
            desc = dv.description
            if len(dv.units) > 0:
                desc += '  (%s)'%dv.units
            
            feasStr, minmaxStr = self.getControlDesVarStr(key)
            
            # do NOT show control design variables in desVar... show them in resultVars
            if not (feasStr or minmaxStr): 
                oList.append( (key,'%g'%dv.val,'%g'%dv.minVal,'%g'%dv.maxVal, desc, feasStr, minmaxStr ) )
        nmax = 1
        vmax = 1
        mmax = 1
        Mmax = 1
        dmax = 1
        for (n,v,m,M,d,f,mms) in oList:
            nmax = max( len(n), nmax )
            vmax = max( len(v), vmax )
            mmax = max( len(m), mmax )
            Mmax = max( len(M), Mmax )
            dmax = max( len(d), dmax )
            
        sList = []
        for (n,v,m,M,d,f,mms) in oList:
            sList.append( ' %s %s %s %s %s '%(n.rjust(nmax),v.rjust(vmax),m.rjust(mmax),
                M.rjust(Mmax), d.ljust(dmax)))
                
            if len(f)>0:
                sList.append( '%s %s '%(' '.rjust(nmax),f) )
                
            if len(mms)>0:
                sList.append( '%s %s '%(' '.rjust(nmax),mms) )
            
        ast = '='*len(sList[0])
        head = headerStr( 'Design Variables', '=', len(sList[0]) )
        return head + '\n'+\
            '\n'.join( sList ) + '\n' + ast + '\n'
        
    def getHTMLDesVarSummary(self, *omitList):
        #print 'self.desVarDict.keys()=',self.desVarDict.keys()
        #print 'omitList=',omitList
        if len(omitList) + len(self.feasibleVarList)>=len(list(self.desVarDict.keys())):
            return ''
        
        summary = '<table class="mytable"><th colspan="4" bgcolor="#CCCCCC">Design Variables (nominal values)</th>' +\
            '<tr><td><b>Name</b></td><td><b>Value</b></td><td><b>Units</b></td><td><b>Description</b></td></tr>'
        
        for key,dv in list(self.desVarDict.items()):
            if key in omitList:
                continue
                
            desc = dv.description
            if len(dv.units) > 0:
                desc += '  (%s)'%dv.units
            
            feasStr, minmaxStr = self.getControlDesVarStr(key)
            if feasStr or minmaxStr:
                continue  # do NOT show control design variables in desVar... show them in resultVars
                #specStr = '<br><b>* -----&gt;<b>'
                #desc += '<br>' + feasStr[8:] + minmaxStr[8:]
            else:
                specStr = ''
                
            summary += '<tr><td align="left" valign="top">%10s</td><td align="right" valign="top">%12g%s</td><td nowrap align="left" valign="top">%s</td><td nowrap align="left" valign="top">%s</td></tr>\n'%\
                    (key,dv.val,specStr,dv.units, desc )
            
        return summary + '</table>'
    
    def getHTMLResultVarSummary(self):
        summary = '<table class="mytable"><th colspan="6" bgcolor="#CCCCCC">Result Variables </th>' +\
            '<tr><td><b>Name</b></td><td><b>Value</b></td><td><b>Units</b></td><td><b>Description</b></td><td><b>Low Limit</b></td><td><b>High Limit</b></td></tr>'

        
        # make local list of effective result variables (includes design control vars)
        resultVarL = [] #: list of result var objects (rv) including design control vars
        #  resultVarL includes desVars that are control variables, (minmax or feasible)
                
        for key,dv in list(self.desVarDict.items()):
            if self.hasMinMaxControlVar(key) or self.hasFeasibleControlVar(key):
                # control variables in minmax or feasible change like result vars
                resultVarL.append(['contVar',key,dv])
        for key,rv in list(self.resultVarDict.items()):
            resultVarL.append(['resVar',key,rv])



        for vType,key,rv in resultVarL:
            desc = rv.description
                
            conVal1 = '---'
            if vType=='contVar': # a control variable
                conVal1 = '>%g'%rv.minVal
            elif rv.loLimit>NEG_INF:
                conVal1 = '>%g'%rv.loLimit
            
            conVal2 = '---'
            if vType=='contVar': # a control variable
                conVal2 = '<%g'%rv.maxVal
            elif rv.hiLimit<POS_INF:
                conVal2 = '<%g'%rv.hiLimit
                
            if len(rv.units) > 0:
                desc += '  (%s)'%rv.units
            
            feasStr, minmaxStr = self.getControlDesVarStr(key)
            if feasStr or minmaxStr:
                specStr = '<br><b>* -----&gt;<b>'
                desc += '<br>' + feasStr[8:] + minmaxStr[8:]
            else:
                specStr = ''
            
            summary += '<tr><td align="left">%10s</td><td align="right">%12g%s</td><td nowrap align="left">%s</td><td nowrap align="left">%s</td><td nowrap align="right">%s</td><td nowrap align="right">%s</td></tr>\n'%\
                (key,rv.val,specStr,rv.units, desc, conVal1, conVal2 )
            
        return summary + '</table>'
    
    def saveDesVarSummary(self):
        print('saving Design Variable Summary to',os.path.split(self.summFileName)[-1]) 
        self.summFile.write( self.getDesVarSummary() + '\n' )
        
        self.htmlFile.write('<center><table border="1" class="mytable">')
        self.htmlFile.write('<th>Design Variable Summary</th>')
        
        self.htmlFile.write('<tr><td nowrap>')
        self.htmlFile.write( self.getHTMLDesVarSummary() )
        self.htmlFile.write( self.getHTMLResultVarSummary() )
        
        self.htmlFile.write('</td></tr></table></center>')


    def setControlRoutine(self, controlRoutine):
        self.controlRoutine = controlRoutine
        # call it to make sure all is initialized
        self.evaluate()
        

    def hasDesignVar(self, dvStr):
        return dvStr in self.desVarDict

    def addDesignVariable(self, name="desvar", InitialVal=0.0,
        minVal=-1.0E300, maxVal=1.0E300, NSteps=10,
        units='', desc='', step=None, linear=1):
            
            
        dv = InputParam(name=name, description=desc, units=units,
            val=InitialVal, minVal=minVal, maxVal=maxVal, NSteps=NSteps, 
            stepVal=None, linear=linear)
        
        self.desVarDict[name] = dv 
        
        try:
            if dv.NSteps>100:
                print('WARNING... more than 100 steps in design variable',name)
                print('  a large number of steps will increase run times')
        except:
            pass
        
    def addDesVars(self, *dvLists):
        #must be entered as lists of design variables
        for dvList in dvLists:
            #print dvList
            name,InitialVal,minVal,maxVal,NSteps,units,desc = dvList
            
            self.addDesignVariable( name=name, InitialVal=InitialVal,
                minVal=minVal, maxVal=maxVal, NSteps=NSteps,
                units=units, desc=desc, step=None, linear=1)
            
    def hasFeasibleResultVar(self, fvStr):
        ans = 0
        for fv in self.feasibleVarList:
            if fvStr.lower() == fv.outParam.name.lower():
                ans = 1
        return ans

    def hasFeasibleControlVar(self, fvCVStr):
        ans = 0
        for fv in self.feasibleVarList:
            if fvCVStr.lower() == fv.inpParam.name.lower():
                ans = 1
        return ans
    

    def getFeasibleVarWithResultVar(self, fvStr):
        ans = None
        for fv in self.feasibleVarList:
            if fvStr.lower() == fv.outParam.name.lower():
                ans = fv
        return ans
    

    def getFeasibleVarWithControlVar(self, fvCVStr):
        ans = 0
        for fv in self.feasibleVarList:
            if fvCVStr.lower() == fv.inpParam.name.lower():
                ans = fv
        return ans

            
    def makeFeasiblePair(self, outName="feasvar", feasibleVal=0.0,
        inpName='inpvar',
        tolerance=1.0E-6, maxLoops=40, failValue=None):
        
        IP = self.desVarDict[inpName]
        OP = self.resultVarDict[outName]
        
        # need to set functionToCall later, in case controlRoutine changes
        fv = FeasiblePair(  inpParam=IP, outParam=OP, functionToCall=None,
            feasibleVal=feasibleVal, tolerance=tolerance, maxLoops=maxLoops, failValue=failValue)

        self.feasibleVarList.append( fv )

    # make min/max routines
            
    def hasMinMaxVar(self, mmvStr):
        ans = 0
        for mmv in self.minmaxVarList:
            if mmvStr.lower() == mmv.name.lower():
                ans = 1
        return ans

    def hasMinMaxControlVar(self, mmvCVStr):
        ans = 0
        for mmv in self.minmaxVarList:
            if mmvCVStr.lower() == mmv.inpParam.name.lower():
                ans = 1
        return ans
    

    def getMinMaxVar(self, mmvStr):
        ans = None
        for mmv in self.minmaxVarList:
            if mmvStr.lower() == mmv.outParam.name.lower():
                ans = mmv
        return ans
    

    def getMinMaxVarWithControlVar(self, mmvCVStr):
        ans = 0
        for mmv in self.minmaxVarList:
            if mmvCVStr.lower() == mmv.inpParam.name.lower():
                ans = mmv
        return ans

            
    def makeMinMaxPair(self, outName="feasvar", findmin=0,
        inpName='inpvar',
        tolerance=1.0E-6, maxLoops=400, failValue=None):
        
        IP = self.desVarDict[inpName]
        OP = self.resultVarDict[outName]
        
        # need to set functionToCall later, in case controlRoutine changes
        mmv = MinMaxPair(  inpParam=IP, outParam=OP, functionToCall=None,
            findmin=findmin, tolerance=tolerance, maxLoops=maxLoops, failValue=failValue)

        self.minmaxVarList.append( mmv )

    def setResultVariableLimits(self, name="resultvar", 
        loLimit=NEG_INF, hiLimit=POS_INF):
            
        if self.hasResultVar(name):
            rv = self.resultVarDict[name]
            rv.loLimit = loLimit
            rv.hiLimit = hiLimit


    def addResultVariable(self, name="resultvar", units='', desc='',
            loLimit=NEG_INF, hiLimit=POS_INF):
                
        rv = OutputParam(name=name, description=desc, units=units,
            val=0.0, loLimit=loLimit, hiLimit=hiLimit)
        
        self.resultVarDict[name] = rv
        
    def addResultVars(self, *rvLists):
        for rvList in rvLists:
            #print rvList
            if len(rvList)==3:
                name,units,desc = rvList
                self.addResultVariable(name,units,desc)
            else:
                name,units,desc,loLimit, hiLimit = rvList
                self.addResultVariable(name,units,desc,loLimit, hiLimit)

    def hasResultVar(self, rvStr):
        return rvStr in self.resultVarDict
    
    def setResultVar(self, rvStr, val):
        try:
            rv = self.resultVarDict[rvStr]
            rv.val = val
        except:
            print('Ignore ERROR in setResultVar... No result variable "%s"'%str(rvStr))
        
    def getResultVar(self, rvStr):
        # accept either result variables OR native attributes
        if rvStr in self.resultVarDict:
            rv = self.resultVarDict[rvStr]
            return rv.val
        elif self.hasMinMaxControlVar(rvStr) or self.hasFeasibleControlVar(rvStr) :
            dv = self.desVarDict[rvStr]
            return dv.val
        else: # as last ditch effort assume an attribute of self
            return getattr(self, rvStr )
        
    def getAxisLabel(self, key, var):
        # accept either result variables OR native attributes
        if len(var.description)==0:
            if len(var.units)==0:
                label = var.name
            else:
                label = var.name + ', ' + var.units
        else:
            if len(var.units)==0:
                label = var.description + ' (' + var.name + ')'
            else:
                label =  var.description + ', ' + var.units + ' (' + var.name + ')'
        return label
        
    def getResultVarAxisLabel(self, rvStr):
        # accept either result variables OR native attributes
        if rvStr in self.resultVarDict:
            rv = self.resultVarDict[rvStr]
            return self.getAxisLabel( rvStr, rv )
            
        elif self.hasMinMaxControlVar(rvStr) or self.hasFeasibleControlVar(rvStr) :
            dv = self.desVarDict[rvStr]
            return self.getAxisLabel( rvStr, dv )
            
        else:
            return rvStr
    
    def getResultVarSummary(self):
        
        # make local list of effective result variables (includes design control vars)
        resultVarL = [] #: list of result var objects (rv) including design control vars
        #  resultVarL includes desVars that are control variables, (minmax or feasible)
                
        for key,dv in list(self.desVarDict.items()):
            if self.hasMinMaxControlVar(key) or self.hasFeasibleControlVar(key):
                # control variables in minmax or feasible change like result vars
                resultVarL.append(['contVar',key,dv])
        for key,rv in list(self.resultVarDict.items()):
            resultVarL.append(['resVar',key,rv])
        
        
        oList = [( 'NAME','VALUE','DESCRIPTION','LOW-LIMIT','HIGH-LIMIT','','')]
        
        for vType,key,rv in resultVarL:
            desc = rv.description
                
            conVal1 = '---'
            if vType=='contVar': # a control variable
                conVal1 = '>%g'%rv.minVal
            elif rv.loLimit>NEG_INF:
                conVal1 = '>%g'%rv.loLimit
            
            conVal2 = '---'
            if vType=='contVar': # a control variable
                conVal2 = '<%g'%rv.maxVal
            elif rv.hiLimit<POS_INF:
                conVal2 = '<%g'%rv.hiLimit
                
            if len(rv.units) > 0:
                desc += '  (%s)'%rv.units
                
            feasStr, minmaxStr = self.getControlDesVarStr(key)
                
            oList.append(('%s'%key,'%g'%rv.val, '%s'%desc, '%s'%conVal1, '%s'%conVal2, feasStr, minmaxStr ))
            
        nmax = 1
        vmax = 1
        dmax = 1
        cmax = 1
        lmax = 1
        for (n,v,d,c,l,f,mms) in oList:
            nmax = max( len(n), nmax )
            vmax = max( len(v), vmax )
            dmax = max( len(d), dmax )
            cmax = max( len(c), cmax )
            lmax = max( len(l), lmax )
            
        sList = []
        for (n,v,d,c,l,f,mms) in oList:
            sList.append( ' %s %s %s %s %s '%(n.rjust(nmax),v.rjust(vmax),d.ljust(dmax),
                c.rjust(cmax),l.rjust(lmax)))

                
            if len(f)>0:
                sList.append( '%s %s '%(' '.rjust(nmax),f) )
                
            if len(mms)>0:
                sList.append( '%s %s '%(' '.rjust(nmax),mms) )



        ast = '='*len(sList[0])
        head = headerStr( 'Result Variables', '=', len(sList[0]) )
        return head + '\n'+\
            '\n'.join( sList ) + '\n' + ast + '\n'
    
    def saveResultVarSummary(self):
        print('saving Result Variable Summary to',os.path.split(self.summFileName)[-1]) 
        self.summFile.write( self.getResultVarSummary() + '\n' )

    def violatesResultConstraint(self):
        vioList = []
        
        for key,rv in list(self.resultVarDict.items()):
            # only handle inequality constraints, 
            # equality constraints handled by feasibility variables
            
            # ignore violations in the nth decimal place
            cMult = 1.0 + abs(self.constraintTolerance)

            if rv.loLimit > rv.val*cMult:  
                vioList.append( key + ' < ' + str( rv.loLimit ) )
            if rv.hiLimit < rv.val/cMult:  
                vioList.append( key + ' > ' + str( rv.hiLimit ) )
                    
        # now make sure no feasibility variables are violated
        for fv in self.feasibleVarList:
            rv = self.resultVarDict[fv.outParam.name]
            # ignore violations in the 4th decimal place
            epsilon = self.constraintTolerance * max(abs(rv.val), abs(fv.feasibleVal))
                
            if abs(rv.val-fv.feasibleVal) > epsilon:
                vioList.append( rv.name + ' != ' + str( fv.feasibleVal ) )
                
        return vioList

    def firstEvaluateIfReqd(self): # called by Optimize.optimize
        if self.NumEvaluations==0:
            self.evaluate()
            
    def evaluate(self):
        
        self.NumEvaluations += 1 #: increment counter for each evaluate call

        def paramCallBack():
            '''special parameter callback (feasible and minmax)'''
            self.controlRoutine(self)

        # do minmax params first
        if len( self.minmaxVarList ) > 0:
            for mmv in self.minmaxVarList:
                if mmv.functionToCall is None:
                    mmv.functionToCall = paramCallBack
                mmv.reCalc() # sets inpParam.val
        
        # now do feasible params
        if len( self.feasibleVarList ) > 0:
            for fv in self.feasibleVarList:
                if fv.functionToCall is None:
                    fv.functionToCall = paramCallBack
                fv.reCalc() # sets inpParam.val

        # when done with "special" inputs, do final call to control routine
        self.controlRoutine(self) # call control routine
        
    #def reCalc(self):  # why a synonym for evaluate?  beats me.
    #    self.evaluate()
        
    def addAssumption(self, label='generic param'):
        self.summaryObj.assumptions.append( label )
        
    def addInput(self, label='generic param', value=0.0, units='xxx', format='%g'):
        self.summaryObj.inputs.append( [label, value, units, format] )
        
    def addOutput(self, label='generic param', value=0.0, units='xxx', format='%g'):
        self.summaryObj.outputs.append( [label, value, units, format] )
    
    def getAssumptions(self):
        assumpL = self.summaryObj.getSummAssumptions()
        assumpL.extend(self.summaryObj.getSummInputs())
        assumpL.extend(self.summaryObj.getSummOutputs())
        
        if assumpL:
            return '\n' + '\n'.join(assumpL)
        else:
            return ''
    
    def getSummary(self):
        return '''ParametricSoln: %s
            '''%(self.subtaskName,) + self.getAssumptions()
    
    def saveSummary(self):
        print('saving Summary to',os.path.split(self.summFileName)[-1]) 
        self.summFile.write( self.getSummary() + '\n' )
    
    def getShortSummary(self):
        summary = self.getSummary()
        
        return summary + '\n'
    
    def getShortHTMLSummary(self):
            
        lastType = ''
        summary = ['<center><table class="mytable">',
            '<th colspan="4" bgcolor="#CCCCCC">Summary </th>']
        
        if self.getAssumptions():
            summary.append('<tr><td colspan="4"><hr></td><tr>')
            assumpL = self.summaryObj.getSummAssumptions()
            assumpL.extend(self.summaryObj.getSummInputs())
            assumpL.extend(self.summaryObj.getSummOutputs())
            for assump in assumpL:
                summary.append('<tr><td colspan="4">%s</td><tr>'%(str(assump),))

        summary.append('</table></center>')
        return '\n'.join( summary )

    
    
    def saveShortSummary(self):
        print('saving Short Summary to',os.path.split(self.summFileName)[-1]) 
        self.summFile.write( self.getShortSummary() + '\n' )

        print('saving Short Summary to',os.path.split(self.htmlFileName)[-1]) 
        self.htmlFile.write( self.getShortHTMLSummary() + '<br>\n' )
        
        if self.userOptions.excel:
            xlText = self.getShortSummary()
            text=xlText.replace('\r','\n')
            spL = text.split('\n')
            rs = [['Short Summary ']]
            for s in spL:
                eqL = s.split('=')
                if len( eqL )==2:
                    #rs.append( [eqL[0],"'=",eqL[1]] )
                    if len( eqL[1].split() )>1:
                        rs.append( [eqL[0],"'=", eqL[1].split()[0], ' '.join( eqL[1].split()[1:])  ] )
                    else:
                        rs.append( [eqL[0],"'=", eqL[1]  ] )
                else:
                    rs.append( [s] )
                
            sheetName="ShortSummary"
            if sheetName not in self.xlSheetD:
                print('making sheet',sheetName)
                self.xlSheetD[sheetName] = sheetName
                self.xlDoc.makeDataSheet( rs, sheetName=sheetName, autoFit=0, rowFormatL=None)

        if self.userOptions.ppt:
            pptText = self.getShortSummary()
            self.pptDoc.addTextSlide( text=pptText.replace('\n','\r'), 
                title='Summary',textFont='Courier New', textFontSize=14,
                noBullets=1)
        
        if self.userOptions.word:
            tableStr = [(' Summary ',),(' ',)]
            wordTable1 = self.wordDoc.addTable( tableStr, Range=self.wordDoc.selectCharacter(-2) )
            wordTable1.Style = self.tblstyl
            self.wordDoc.setCellStyle(wordTable1,1,1, just='c',bold=True, 
                fontName='Arial', fontSize=14, bgcolor='15')
            self.wordDoc.setCellStyle( wordTable1, 2, 1, 
                text=  self.getShortSummary() )
            self.wordDoc.selectCharacter(-1)
            self.wordDoc.addText('  ')

        

    def getFullSummary(self):
        
        self.saveDesVarSummary()
        self.saveResultVarSummary() 
        summary = '\n\n' \
            '\n======================================' +\
            '\n==========FULL SYSTEM SUMMARY=========' +\
            '\n======================================\n' +\
            self.getSummary()
            
        return summary
        
    
    def getFullHTMLSummary(self):
        
        if self.getAssumptions():
            summary = [self.summaryObj.getItemHTMLSummary()]
        else:
            summary = []
            
            
        return ''.join(summary)

    
    def saveFullSummary(self):
        print('saving Full Summary to',os.path.split(self.summFileName)[-1]) 
        self.summFile.write( self.getFullSummary() + '\n' )

        print('saving Full Summary to',os.path.split(self.htmlFileName)[-1]) 
        self.htmlFile.write( self.getFullHTMLSummary() + '<br>\n' )
        


    def saveComment(self, comment=''):
        print('saving comment to file')
        
        sOut = []
        sOut.append('========================================')
        sOut.append( comment )
        sOut.append('========================================')
        self.summFile.write( '\n'.join( sOut ) )
        
        sOut = []
        sOut.append('<center><table class="mytable" width="680">')
        sOut.append( '<tr><td align="left">%s'%comment )
        sOut.append( '</td></tr>' )
        sOut.append('</table></center>')
        self.htmlFile.write( '\n'.join( sOut ) )

    def putImageInPPT( self, filename, title):
        print('saving Image to',os.path.split(self.pptDocName)[-1]) 
        try:
            self.pptDoc.addImageSlide( imgFile=filename, title=title.replace('\n','\r'))
        except:
            print("ERROR... FAILED to put image in PowerPoint file")
            print(traceback.print_exc())


    def putImageInWord( self, filename):
        print('saving Image to',os.path.split(self.wordDocName)[-1]) 
        tableStr = [(' ',),(' ',)]
        wordTable1 = self.wordDoc.addTable( tableStr, Range=self.wordDoc.selectCharacter(-2) )
        wordTable1.Style = self.tblstyl
        self.wordDoc.addImage(filename, Range=wordTable1.Cell(1,1).Range, 
            fracPage=self.wordDocImagefracPage )
        self.wordDoc.setCellStyle( wordTable1, 1, 1, just='c')
        self.wordDoc.setCellStyle( wordTable1, 2, 1, text=  self.getDesVarSummary() + self.getResultVarSummary() )
    
        self.wordDoc.selectCharacter(-1)
        self.wordDoc.addText('  ')


    def pickleParametricSoln(self): # pickle all of the internal variables
        
        itemL = []
        
        # now save ParametricSoln object
        print('pickling object', self.__class__.__name__)
        itemD = {}
        itemD['className'] = self.__class__.__name__
        for key,val in list(self.__dict__.items()):
            if type(val) in [type(1), type(1.1), type('s')]: # eliminated list type
                #print key,val
                itemD[key]=val
        
        # save result and design variables
        for key,rv in list(self.resultVarDict.items()):
            itemD[key] = rv.val 
                    

        for key,dv in list(self.desVarDict.items()):
            itemD[key] = dv.val 
            itemD[key+'_units'] = dv.units
            itemD[key+'_desc'] = dv.description
                
            feasStr = ''
            if self.hasFeasibleControlVar( key ):
                fv = self.getFeasibleVarWithControlVar( key )
                feasStr = '* -----> ' +\
                    ' (%s varies to make %s = %g %s)'%(key, fv.outParam.name, fv.feasibleVal, fv.outParam.units)
            itemD[key+'_feas'] = feasStr

                
            minmaxStr = ''
            if self.hasMinMaxControlVar( key ):
                mmv = self.getMinMaxVarWithControlVar( key )
                if mmv.findmin:
                    oStr = 'minimize'
                else:
                    oStr = 'maximize'
                minmaxStr = '* -----> ' +\
                    ' (%s varies to %s %s)'%(key, oStr, mmv.outParam.name)
            itemD[key+'_minmax'] = minmaxStr


        # save ParametricSoln dictionary to List
        itemL.append( itemD )
        
        print('Saving to Pickle file:',self.pickleFileName)
            
        fOut = open(self.pickleFileName, 'w')
        pickle.dump( itemL, fOut )
        fOut.close()

    

if __name__ == "__main__":  #self test
    #import Plots
    #from Optimize import optimize
        
    def test_case():
        def myControlRoutine(PS):
            a,b  = PS.getDesVars("a","b")
            
            c = a * b
            
            PS.setResultVar("c", c )
            PS.setResultVar("sysMass", c*2. )
            PS.setResultVar("sysVolume", c*20. )
            

        PS = ParametricSoln(author="C Taylor", subtaskName="simple system", 
            controlRoutine=myControlRoutine)
            
        PS.addDesVars(
        ["a",2.0, 1.0, 10.0, 10, 'sec', 'First Number'],
        ["b",6.0, 0.0, 20.0, 10, 'ft', 'Second Number']
        )
        
        PS.addResultVariable( name="c", units='ft-sec', desc='a * b',loLimit=1.0, hiLimit=10.0)

        PS.addResultVars(
            ["sysMass", "lbm", "Total System Mass"],
            ["sysVolume", "cuin", "Total System Volume"]
            )
            
        PS.makeFeasiblePair( outName="sysMass", feasibleVal=50., inpName='b')


        print()
        PS.evaluate() # <-- needed since myControlRoutine set with ParametricSoln creation
        #PS.saveShortSummary()
        #PS.saveSummary()
        
        #PS.saveDesVarSummary()
        #PS.saveResultVarSummary()
        
        PS.saveFullSummary()
        
        print(PS.getShortSummary())
        #print Hetank.getSummary()
        
        #optimize(PS, figureOfMerit="mass_lbm", desVars=["PHe"])
        print(PS.getShortSummary())
        #Plots.make2DPlot(PS, sysParam="mass_lbm", desVar="PHe")
        print()
        print('vioList')
        print(PS.violatesResultConstraint())
        
        PS.close()
    
    # if 1:
    test_case()
    # else:
    #     import hotshot, hotshot.stats
    #     prof = hotshot.Profile("test_case.prof")
    #     prof.runcall(test_case)
    #     prof.close()
        
    #     stats = hotshot.stats.load("test_case.prof")
    #     stats.strip_dirs()
    #     stats.sort_stats('time', 'calls')
    #     stats.print_stats(60)
    