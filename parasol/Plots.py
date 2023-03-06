import matplotlib
#matplotlib.use('TKAgg')   # usually the right thing to do
from matplotlib.ticker import FormatStrFormatter
from PIL import Image, ImageFont, ImageDraw

import sys, os
from pylab import *
import time

import csv
import traceback
from parasol.Plots_Cache import Plots_Cache
from parasol.cast import floatDammit, intDammit
from parasol.CarpetPlot import Carpet

__author__ = "Charlie Taylor (charlietaylor@sourceforge.net)"
__version__ = "1.0 "
__date__ = "Jan 1, 2009"
__copyright__ = "Copyright (c) 2009 Charlie Taylor"
__license__ = "BSD"

__Plots_Cache = None # holds cached results for speeding up Plots

__plotNumber = 0

def putPlotInPPT( PS, filename, title):
    print('saving Plot to',os.path.split(PS.pptDocName)[-1]) 
    try:
        PS.pptDoc.addImageSlide( imgFile=filename, title=title.replace('\n','\r'))
    except:
        print("ERROR... FAILED to put plot in PowerPoint file")
        print(traceback.print_exc())

def putPlotInWord( PS, filename, *omitList):
    print('saving Plot to',os.path.split(PS.wordDocName)[-1]) 
    tableStr = [(' ',),(' ',)]
    wordTable1 = PS.wordDoc.addTable( tableStr, Range=PS.wordDoc.selectCharacter(-2) )
    wordTable1.Style = PS.tblstyl
    PS.wordDoc.addImage(filename, Range=wordTable1.Cell(1,1).Range, 
        fracPage=PS.wordDocImagefracPage )
    PS.wordDoc.setCellStyle( wordTable1, 1, 1, just='c')
    PS.wordDoc.setCellStyle( wordTable1, 2, 1, text=  PS.getDesVarSummary(*omitList) + PS.getResultVarSummary() )
    
    PS.wordDoc.selectCharacter(-1)
    PS.wordDoc.addText('  ')
    
    

_sigFontSize = 8

#  signAndDatePlot IS NO LONGER USED... now use f.text for figure() in matplotlib
def signAndDatePlot(PS, filename):
    im = Image.open( filename )
    width, height = im.size
    draw = ImageDraw.Draw(im)
    
    # make  font
    if width<600:
        arial  =  ImageFont.truetype ( "Arial.ttf", 10 )
    else:
        arial  =  ImageFont.truetype ( "Arial.ttf", 12 )
    
    s = PS.author + ' ' + time.strftime('%m/%d/%Y)')
    wLab,hLab = arial.getsize(s)
    w = width - wLab - 6
    h = height - hLab - 6
    draw.text( (w,h), s, fill="black", font=arial)
    
    s = "ParaSol v" + PS.getVersion()
    wLab,hLab = arial.getsize(s)
    w =  6
    h = height - hLab - 6
    draw.text( (w,h), s, fill="black", font=arial)    
    
    im.save( filename )


def makeSensitivityPlot(PS, 
    figureOfMerit="sysMass", desVars=["PHe","Pc","MR"],
    makeHTML=1, dpi=70, linewidth=2, extraFOM=None, omitViolPts=0):
    global __plotNumber, __Plots_Cache
    __plotNumber += 1
    
    if __Plots_Cache==None:
        __Plots_Cache = Plots_Cache(PS)
            
    try:
        _makeSensitivityPlot(PS, 
            figureOfMerit=figureOfMerit, desVars=desVars,
            makeHTML=makeHTML, dpi=dpi, linewidth=linewidth, extraFOM=extraFOM, 
            omitViolPts=omitViolPts)
    except:
        print(' >>> ERROR... could not create SensitivityPlot')
        print(traceback.print_exc())

'''
subplots_adjust(*args, **kwargs)
subplots_adjust(left=None, right=None, bottom=None, top=None, wspace=0.2, hspace=0.2)
 
Tune the subplot layout via the figure.SubplotParams mechanism.
The parameter meanings (and suggested defaults) are
 
  left  = 0.125  # the left side of the subplots of the figure
  right = 0.9    # the right side of the subplots of the figure
  bottom = 0.1   # the bottom of the subplots of the figure
  top = 0.9      # the top of the subplots of the figure
  wspace = 0.2   # the amount of width reserved for blank space between subplots
  hspace = 0.2   # the amount of height reserved for white space between subplots
 
The actual defaults are controlled by the rc file
'''
def _makeSensitivityPlot(PS, 
        figureOfMerit="sysMass", desVars=["PHe","Pc","MR"],
        makeHTML=1, dpi=70, linewidth=2, extraFOM=None, omitViolPts=1):
    '''looks like minitab trend analysis'''
    
    __Plots_Cache.saveParasolState()
    
    L = len( desVars )
    wspace = 0.2
    hspace = 0.2
    if L==1:
        nrows=1; ncols=1;
    elif L==2:
        nrows=2; ncols=1;
    elif L<=4:
        nrows=2; ncols=2;
        wspace = 0.4
    elif L<=6:
        nrows=2; ncols=3;
        wspace = 0.5
    elif L<=9:
        nrows=3; ncols=3;
        wspace = 0.5
        hspace = 0.4
    elif L<=12:
        nrows=3; ncols=4;
        wspace = 0.5
        hspace = 0.4
    elif L<=16:
        nrows=4; ncols=4;
        wspace = 0.5
        hspace = 0.4
    else :
        nrows=1 + L/5; ncols=5;
        wspace = 0.5
        hspace = 0.4
        
    dvs = '_'.join(desVars)
    filename = os.path.join( PS.outputPath,
               PS.scriptName[:-3] + '_%i_'%__plotNumber  + '_sens_'+figureOfMerit+'_vs_'+dvs+'.png' )
    print("building %i x %i sensitivity plot %s"%(nrows,ncols, os.path.split(filename)[-1] ))
    
    htmlPath = './%s/%s'%(PS.scriptName[:-3],os.path.split(filename)[-1])
    
    Nplot = 1
    ymin = 1.0E100
    ymax = -1.0E100

    
    # apply overall title
    f = figure()
    f.text(0.5, 0.975, figureOfMerit + " Sensitivity" ,horizontalalignment='center',verticalalignment='top')
    # sign chart with name and date
    f.text(0.975, 0.025, PS.author + ' ' + time.strftime('%m/%d/%Y)'),
        horizontalalignment='right',verticalalignment='top', fontsize=_sigFontSize)
        
    f.text(0.025, 0.025, "ParaSol v" + PS.getVersion(),
        horizontalalignment='left',verticalalignment='top', fontsize=_sigFontSize)

    subplots_adjust( wspace=wspace, hspace=hspace, left=0.1, right=0.95 )
    excelColL = [] #: used to collect possible Excel output
    excelColExtraL = [] #: list of labels for curves in excel
    for desVar in desVars:
        print(".", end=' ')
        subplot(nrows, ncols, Nplot)
        
        dv = PS.desVarDict[desVar]
        # don't lose current value
        dv.savedVal = PS.getDesignVar( desVar )
        
        span = dv.maxVal - dv.minVal
        x = []
        y = []
        yextra = []
        xviol = [] # any constraint violations
        yviol = []
        vioDict = {}
        for stepVal in dv.rangeL:
            PS.setDesignVar( desVar, stepVal)
            #PS.evaluate() <-- called from Plots_Cache IF REQUIRED
            __Plots_Cache.getResults()
            
            vioList = PS.violatesResultConstraint()
            if omitViolPts and len(vioList)>0:
                pass
            else:
                x.append(stepVal)
            
                y.append( PS.getResultVar(figureOfMerit) )
                if extraFOM:
                    yextra.append( PS.getResultVar(extraFOM) )
                
                if len(vioList)>0:
                    xviol.append( x[-1] )
                    yviol.append( y[-1] )
                    for viol in vioList:
                        vioDict[viol] = viol
                
                if y[-1] > ymax: ymax = y[-1]
                if y[-1] < ymin: ymin = y[-1]
                if extraFOM:
                    if yextra[-1] > ymax: ymax = yextra[-1]
                    if yextra[-1] < ymin: ymin = yextra[-1]
                
                
                
        if len(x)>0:
            plot(x, y, label=figureOfMerit, linewidth=linewidth)
            if extraFOM:
                plot(x,yextra, label=extraFOM, linewidth=linewidth)
                legend(loc='best')
                
            if PS.userOptions.excel:
                xmin = dv.rangeL[0]
                xmax = dv.rangeL[-1]
                label = '%g < %s < %g'%(xmin,dv.name,xmax) 
                xExcel = [label]
                for xval in x:
                    xvalNorm = (xval-dv.savedVal)/(xmax-xmin)
                    xExcel.append( xvalNorm )
                
                y.insert(0, label)
                excelColL.append( [xExcel,y] )
                if extraFOM:
                    yextra.insert(0, label)
                    excelColExtraL.append( [xExcel,yextra] )
                    
        
        if len( xviol )>0: # will be empty if omitViolPts is true
            if len(xviol)==1:  # plot will BOMB with only 1 entry in list
                xviol.append( xviol[-1] )
                yviol.append( yviol[-1] )
            for viol in list(vioDict.keys()):
                plot(xviol, yviol, 'ro', mfc='r', label=str(viol), linewidth=0, alpha=0.5)
                #print "violation = (%s)"%viol
            legend(loc='best')
            

        #xlabel( desVar )
        #title(desVar)
        xlabel(desVar)
        ylabel( figureOfMerit )
        axvspan( dv.savedVal-span*0.01, dv.savedVal+span*0.01, 
            facecolor='g', alpha=0.5) # show design point
        
        grid(True)
        
        #gca().xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        #gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        majorFormatter = FormatStrFormatter('%g')
        gca().yaxis.set_major_formatter(majorFormatter)
        majorFormatter = FormatStrFormatter('%g')
        gca().xaxis.set_major_formatter(majorFormatter)
        
        #print 'xticks( )', xticks( )
        #locs, labels = xticks()
        xticks( [dv.minVal, dv.maxVal], ('%g'%dv.minVal, '%g'%dv.maxVal) )
        
        Nplot += 1
    
        # restore original value
        #PS.setDesignVar( desVar, dv.savedVal)
        #PS.evaluate() <-- called from Plots_Cache IF REQUIRED # recalc design point from savedVal
        __Plots_Cache.restoreParasolState()

    
        # make csv file
        csvfilename = os.path.join( PS.outputPath,
                      PS.scriptName[:-3] + '_%i_'%__plotNumber  + '_sens_'+figureOfMerit+'_vs_'+desVar+'.csv')
        print("saving data to CSV file",os.path.split(csvfilename)[-1]) 
        csvWriter = csv.writer(open(csvfilename, "w"),  dialect='excel')
    
        sumry = PS.getDesVarSummary()
        sp = sumry.split('\n')
    
        for s in sp:
            csvWriter.writerow( ( s ,) )
    
        csvWriter.writerow( (desVar, figureOfMerit) )
        for i in range( len(x) ):
            csvWriter.writerow((x[i],y[i]))


    if ymin>=ymax:
        print('   >>> ERROR... ymin equals ymax in makeSensitivityPlot')
        print('   >>> ABANDONING PLOT')
        return
        
    Nplot = 1
    for desVar in desVars:
        print(".", end=' ')
        subplot(nrows, ncols, Nplot)
        dv = PS.desVarDict[desVar]
        axis([dv.minVal, dv.maxVal, ymin, ymax])
        Nplot += 1
    print(".")
    # after all subplots are made, save the file
    try:
        savefig(filename, dpi=dpi)
    except:
        print(traceback.print_exc())
        print('===> WARNING, could NOT save',filename)
        close()
        return None
        
    print("image saved as",filename)
    print("with dpi =",dpi)
    close()
    
    # sign and date the plot
    #signAndDatePlot(PS, filename)
    
    if makeHTML:
        PS.htmlFile.write('<center><table border="1" class="mytable">')
        PS.htmlFile.write('<th>System Sensitivity</th><tr><td>')
        PS.htmlFile.write( '<img src="%s">'%(htmlPath,) )
        
        PS.htmlFile.write('</td></tr><tr><td nowrap>')
        PS.htmlFile.write( PS.getHTMLDesVarSummary() ) # don't omit any desVar from table
        PS.htmlFile.write( PS.getHTMLResultVarSummary() )
        
        PS.htmlFile.write('</td></tr></table></center>')
    
            
    if PS.userOptions.word:
        putPlotInWord( PS, filename)# don't omit any desVar from table
            
    if PS.userOptions.ppt:
        putPlotInPPT( PS, filename, 'Sensitivity Plot')


    if PS.userOptions.excel:
        sheetName = 'Data_%i'%__plotNumber 
        chartName = 'Plot_%i'%__plotNumber 

        xLabelStr = 'Design Variables ' + ', '.join( desVars )
        yLabelStr = PS.getResultVarAxisLabel(figureOfMerit)
        
        if excelColL:
            
            rs = build_rs_from_colL(excelColL)

            PS.xlDoc.makeChart( rs, title=figureOfMerit+'_vs_'+desVar, nCurves = 1,
                      sheetName=sheetName,chartName=chartName,  showPoints=1, showLegend=1,
                      yLabel=yLabelStr, xLabel=xLabelStr)
            for i in range(1, len(rs[0])/2 ):
                PS.xlDoc.addNewSeriesToCurrentSheetChart( xColumn=1+i*2, yColumn=2+i*2)
                      
            PS.xlDoc.addTextBox(PS.getDesVarShortSummary())
            
            if extraFOM:
                sheetName = 'DataE_%i'%__plotNumber 
                chartName = 'PlotE_%i'%__plotNumber 

                yLabelStr = PS.getResultVarAxisLabel(extraFOM)
                rs = build_rs_from_colL(excelColExtraL)
        
                PS.xlDoc.makeChart( rs, title=extraFOM+'_vs_'+desVar, nCurves = 1,
                          sheetName=sheetName,chartName=chartName,  showPoints=1, showLegend=1,
                          yLabel=yLabelStr, xLabel=xLabelStr)
                for i in range(1, len(rs[0])/2 ):
                    PS.xlDoc.addNewSeriesToCurrentSheetChart( xColumn=1+i*2, yColumn=2+i*2)
                          
                PS.xlDoc.addTextBox(PS.getDesVarShortSummary())
        


def make2DPlot(PS, sysParam="mass_lbm", desVar="PHe", makeHTML=1, dpi=70, linewidth=2,
    ptData=None, ptLegend='', logX=0, logY=0, xResultVar=None, colorL=None, yLabel='',
    legendOnLines=0, titleStr=''):
    global __plotNumber, __Plots_Cache
    __plotNumber += 1
    
    if __Plots_Cache==None:
        __Plots_Cache = Plots_Cache(PS)
            
    try:
        _make2DPlot(PS, 
            sysParam=sysParam, desVar=desVar, makeHTML=makeHTML, dpi=dpi, linewidth=linewidth,
    ptData=ptData, ptLegend=ptLegend, logX=logX, logY=logY, xResultVar=xResultVar, 
    colorL=colorL, yLabel=yLabel, legendOnLines=legendOnLines, titleStr=titleStr)
    except:
        print(' >>> ERROR... could not create 2D Plot')
        print(traceback.print_exc())


def _make2DPlot(PS, sysParam="mass_lbm", desVar="PHe", makeHTML=1, dpi=70, linewidth=2,
    ptData=None, ptLegend='', logX=0, logY=0, xResultVar=None, colorL=None, yLabel='',
    legendOnLines=0, titleStr=''):
    '''
    sysParam can be a name or list of names
    xResultVar allows plotting a result variable as the X axis (ex. xResultVar="Out1")
    '''
    
    __Plots_Cache.saveParasolState()
         
    logxy = '_'
    if logX: logxy += 'logX'
    if logY: logxy += 'logY'
        
    if xResultVar==None:
        XusesResVar = 0
    else:
        XusesResVar = 1
        
    # allow use of lists of plotted vars
    if type(sysParam) == type([]):
        sysParamList = sysParam
        sysParam = sysParamList[0]
        yLists = []
        # make a list of lists for 2D plot
        for s in sysParamList:
            yLists.append([])
    else:
        sysParamList = [sysParam]
        yLists = [[]]
    listLen = len( sysParamList )
    
    if listLen>1 or XusesResVar:
        showLegend = 1
    else:
        showLegend = 0
    
    if xResultVar==None:
        fileNamePart = desVar
    else:
        fileNamePart = desVar + '_' + xResultVar
        
    filename = os.path.join( PS.outputPath,
               PS.scriptName[:-3] + '_%i_'%__plotNumber  + logxy +'_'+ '_'.join(sysParamList) +'_vs_'+fileNamePart+'.png')
    print("building 2D plot", os.path.split(filename)[-1]) 
    htmlPath = './%s/%s'%(PS.scriptName[:-3],os.path.split(filename)[-1])
        
    dv = PS.desVarDict[desVar]
    
    # sign chart with name and date
    f = figure()
    f.text(0.975, 0.025, PS.author + ' ' + time.strftime('%m/%d/%Y)'),
        horizontalalignment='right',verticalalignment='top', fontsize=_sigFontSize)
        
    f.text(0.025, 0.025, "ParaSol v" + PS.getVersion(),
        horizontalalignment='left',verticalalignment='top', fontsize=_sigFontSize)

    if PS.hasFeasibleControlVar( dv.name ):
        print("ERROR... can not use feasible design variable %s for plot axis"%dv.name)
        return
        
    # don't lose current value
    dv.savedVal = PS.getDesignVar( desVar )
    
    x = []
    y = []
    xviol = [] # any constraint violations
    yviol = []
    vioDict = {}
    
    #set up result variable x lists just in case
    xResultL = []
    xResViolL = []
    
    for stepVal in dv.rangeL:
        PS.setDesignVar( desVar, stepVal)
        #PS.evaluate() <-- called from Plots_Cache IF REQUIRED
        __Plots_Cache.getResults()
        x.append(stepVal)
        
        if XusesResVar:
            xResultL.append(PS.getResultVar(xResultVar))
        
        # accept either result variables OR native attributes
        for i in range(listLen):
            yLists[i].append( PS.getResultVar(sysParamList[i]))
            #y.append( PS.getResultVar(sysParam) )
        
        vioList = PS.violatesResultConstraint()
        if len(vioList)>0:
            xviol.append( x[-1] )
            if XusesResVar:
                xResViolL.append( xResultL[-1] )
            
            yviol.append( yLists[i][-1] )
            for viol in vioList:
                vioDict[viol] = viol
        
    #print x
    #print y
    
    # save x list in case the X axis is using a result variable
    xDesVarL = x
    
    # swap out x arrays if x axis is using a result variable
    if XusesResVar:
        x = xResultL
        xviol = xResViolL
    
    for i in range(listLen):
        y = yLists[i]
        labelStr = sysParamList[i]
        if XusesResVar:
            labelStr = "%s = %g to %g"%(desVar,dv.minVal,dv.maxVal )
            
        try:
            fmt = cnames[ colorL[i].lower() ]
            lw = linewidth 
        except:
            fmt = getColorName(i)  # get standard color list
            lw = linewidth + 2*int(i/7) # only modify line width if NOT using input colors

    
        if logX and logY:
            loglog(x, y, label=labelStr, linewidth=lw , color=fmt)
        elif logX:
            semilogx(x, y, label=labelStr, linewidth=lw, color=fmt)
        elif logY:
            semilogy(x, y, label=labelStr, linewidth=lw, color=fmt)
        else:
            plot(x, y, label=labelStr, linewidth=lw, color=fmt)
            
        if legendOnLines:
            di = len(x) / 6
            iLabel = (1 + (i%5)) * di
            props = {'ha':'center', 'va':'bottom', 'color':fmt}
            text(x[iLabel], y[iLabel], labelStr, props)


    # Now make labels for x result variables
    if XusesResVar:
        for i in range(listLen):
            y = yLists[i]
            
            labelStr = "%s = %g"%(desVar,dv.maxVal )
            xrL = [x[-1], x[-1]] # needs to have length > 1 or plot will BOMB
            yrL = [y[-1], y[-1]] # needs to have length > 1 or plot will BOMB
            plot(xrL, yrL, 'r^', mfc='r', label=labelStr, linewidth=0, markersize=12)
            
            labelStr = "%s = %g"%(desVar,dv.minVal )
            xrL = [x[0], x[0]] # needs to have length > 1 or plot will BOMB
            yrL = [y[0], y[0]] # needs to have length > 1 or plot will BOMB
            plot(xrL, yrL, 'rv', mfc='r', label=labelStr, linewidth=0, markersize=12)


    if ptData != None:
        dx, dy = ptData
        plot(dx, dy, 'ro', mfc='b', label=ptLegend, linewidth=0)
        if len(ptLegend)>0:
            #legend(loc='best')
            showLegend = 1
        
    if len( xviol )>0:
        for viol in list(vioDict.keys()):
            if len(xviol)==1:  # plot will BOMB with only 1 entry in list
                xviol.append( xviol[-1] )
                yviol.append( yviol[-1] )
            plot(xviol, yviol, 'ro', mfc='r', label=viol, linewidth=0, alpha=0.5)
        #legend(loc='best')
        showLegend = 1
        
    if showLegend and (not legendOnLines):
        legend(loc='best')

    if XusesResVar:
        xLabelStr = PS.getResultVarAxisLabel(xResultVar)
    else:
        xLabelStr = PS.getDesignVarAxisLabel(desVar)
    xlabel( xLabelStr )
        
    yLabelStr = ''
    if not titleStr:
        if len( yLists ) > 1:
            yLabelStr = ' '.join(sysParamList)
            ylabel( yLabelStr )
            titleStr = PS.getResultVarAxisLabel(sysParam) + ' ETC...'
        else:
            yLabelStr = PS.getResultVarAxisLabel(sysParam)
            ylabel( yLabelStr )
            titleStr = PS.getResultVarAxisLabel(sysParam)
        
    if yLabel:
        ylabel( yLabel )
        yLabelStr = yLabel
    
    title(PS.subtaskName + '\n' + titleStr )
    grid(True)
        
    #from matplotlib.ticker import OldScalarFormatter
    #gca().xaxis.set_major_formatter(OldScalarFormatter())
    #gca().xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    #gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    majorFormatter = FormatStrFormatter('%g')
    gca().yaxis.set_major_formatter(majorFormatter)
    majorFormatter = FormatStrFormatter('%g')
    gca().xaxis.set_major_formatter(majorFormatter)


    #xticklabels = getp(gca(), 'xticklabels')
    #yticklabels = getp(gca(), 'yticklabels')
    #setp(yticklabels, 'color', 'black', fontsize='small', fontweight='normal')
    #setp(xticklabels, 'color', 'black', fontsize='small', fontweight='normal')
        
    try:
        savefig(filename, dpi=dpi)
    except:
        print(traceback.print_exc())
        print('===> WARNING, could NOT save',filename)
        close()
        return None
        
    print("image saved as",filename)
    print("with dpi =",dpi)
    close()
    
    #signAndDatePlot(PS, filename)
    
    # restore original value
    #PS.setDesignVar( desVar, dv.savedVal)
    #PS.evaluate() <-- called from Plots_Cache IF REQUIRED # recalc design point from savedVal
    __Plots_Cache.restoreParasolState()
    
    # make csv file
    csvfilename = os.path.join( PS.outputPath,
                  PS.scriptName[:-3] + '_%i_'%__plotNumber  + '_'+'_'+sysParam+'_vs_'+fileNamePart+'.csv')
    print("saving data to CSV file",os.path.split(csvfilename)[-1]) 
    csvWriter = csv.writer(open(csvfilename, "w"),  dialect='excel')
    
    sumry = PS.getDesVarSummary(*[desVar])
    sp = sumry.split('\n')
    
    for s in sp:
        csvWriter.writerow( ( s ,) )
    
    
    if XusesResVar:
        csvWriter.writerow( (xResultVar, sysParam, desVar) )
        for i in range( len(x) ):
            csvWriter.writerow((x[i],y[i],xDesVarL[i]))
    else:
        row = [desVar]
        row.extend( sysParamList )
        csvWriter.writerow( row )
        
        for i in range( len(x) ):
            row = [x[i]]
            for j in range(listLen):
                y = yLists[j]
                row.append( y[i] )

            csvWriter.writerow(row)

    # send to excel
    if PS.userOptions.excel:
        sheetName = 'Data_%i'%__plotNumber 
        chartName = 'Plot_%i'%__plotNumber 

        if XusesResVar:
            rs = [[xResultVar, sysParam, desVar]]
            for i in range( len(x) ):
                rs.append([x[i],y[i],xDesVarL[i]])
        else:
            row = [desVar]
            row.extend( sysParamList )
            rs = [ row ]
            
            for i in range( len(x) ):
                row = [x[i]]
                for j in range(listLen):
                    y = yLists[j]
                    row.append( y[i] )
                rs.append( row )

        
        PS.xlDoc.makeChart( rs, title=PS.subtaskName + '\n' + titleStr, nCurves = len(rs[1])-1,
                  sheetName=sheetName,chartName=chartName,  showPoints=1, showLegend=1,
                  yLabel=yLabelStr, xLabel=xLabelStr)

        PS.xlDoc.addTextBox(PS.getDesVarShortSummary(*[desVar]))
        
        # set x scale to range of design variable
        if not XusesResVar:
            dv = PS.desVarDict[desVar]
            PS.xlDoc.setXrange( dv.minVal,dv.maxVal )


    # make any HTML output
    if makeHTML:
        PS.htmlFile.write('<center><table border="1" class="mytable"><tr><td>')
        #PS.htmlFile.write( '<img src="file:///%s">'%(filename,) )
        PS.htmlFile.write( '<img src="%s">'%(htmlPath,) )
        
        PS.htmlFile.write('</td></tr><tr><td nowrap>')
        PS.htmlFile.write( PS.getHTMLDesVarSummary(*[desVar]) ) # put desVar in omitList of desVars
        
        
        PS.htmlFile.write('</td></tr></table></center>')

            
    if PS.userOptions.word:
        putPlotInWord( PS, filename,*[desVar])  # put desVar in omitList of desVars
            
    if PS.userOptions.ppt:
        putPlotInPPT( PS, filename, PS.getResultVarAxisLabel(sysParam))
    
def funcDummy( x, y): # needed by contour plot routine
    return x*y


def makeContourPlot(PS, sysParam="mass_lbm", desVars=["PHe","Pc"],
        interval = 0.0, maxNumCurves=50, nomNumCurves=12, makeHTML=1, 
        dpi=70, colorMap="summer",alpha=0.7,titleStr=''):
    global __plotNumber, __Plots_Cache
    __plotNumber += 1
    
    if __Plots_Cache==None:
        __Plots_Cache = Plots_Cache(PS)
            
    try:
        _makeContourPlot(PS, 
            sysParam=sysParam, desVars=desVars,
            interval = interval, maxNumCurves=maxNumCurves, nomNumCurves=nomNumCurves, 
            makeHTML=makeHTML, dpi=dpi, colorMap=colorMap,alpha=alpha, titleStr=titleStr)
    except:
        print(' >>> ERROR... could not create Contour Plot')
        print(traceback.print_exc())


def _makeContourPlot(PS, sysParam="mass_lbm", desVars=["PHe","Pc"],
        interval = 0.0, maxNumCurves=50, nomNumCurves=12, makeHTML=1, 
        dpi=70, colorMap="summer",alpha=0.7,titleStr=''):
    
    __Plots_Cache.saveParasolState()
 
        
    filename = os.path.join( PS.outputPath, 
                PS.scriptName[:-3] + '_%i_'%__plotNumber  +  '_'+'_'+sysParam+'_vs_'+\
                desVars[0]+'_'+desVars[1]+'.png')
    print("building contour plot", os.path.split(filename)[-1]) 
    htmlPath = './%s/%s'%(PS.scriptName[:-3],os.path.split(filename)[-1])
        
    dv0 = PS.desVarDict[desVars[0]]
    dv1 = PS.desVarDict[desVars[1]]
    
    if PS.hasFeasibleControlVar( dv0.name ):
        print("ERROR... can not use feasible design variable %s for plot axis"%dv0.name)
        return
    
    if PS.hasFeasibleControlVar( dv1.name ):
        print("ERROR... can not use feasible design variable %s for plot axis"%dv1.name)
        return
        
    # don't lose current values
    dv0.savedVal = PS.getDesignVar( desVars[0] )
    dv1.savedVal = PS.getDesignVar( desVars[1] )
        
    minVal0 = dv0.minVal
    minVal1 = dv1.minVal
    maxVal0 = dv0.maxVal
    maxVal1 = dv1.maxVal
    
    p = dv0.rangeL
    f = dv1.rangeL

    P,F = meshgrid(p,f)
    OutArr = funcDummy(P,F)

    minval=1.0E100
    maxval=-1.0E100
    violx = []
    violy = []
    vioDict = {}
    for j in range(len(p)):
        print(".", end=' ')
        for i in range(len(f)):
            PS.setDesignVar( desVars[0], P[i,j] )
            PS.setDesignVar( desVars[1], F[i,j] )
            #PS.evaluate() <-- called from Plots_Cache IF REQUIRED
            __Plots_Cache.getResults()
            
            # accept either result variables OR native attributes
            val = PS.getResultVar(sysParam) 
            vioList = PS.violatesResultConstraint()
            if len(vioList)>0:
                violx.append( P[i,j] )
                violy.append( F[i,j] )
                for viol in vioList:
                    vioDict[viol] = viol

            OutArr[i,j] = val
            if val<minval: minval=val
            if val>maxval: maxval=val

    print(".")
    print("minval,maxval=",minval,maxval)

    if interval<=0.0:
        diff = maxval - minval
        step = diff / nomNumCurves
        interval = float( '%.1g'%step )
        print("interval=",interval)
    

    lowVal = interval * ( minval // interval )
    hiVal =  interval * ( maxval // interval )
    deltaVal = hiVal - lowVal
    print("lowVal, hiVal",lowVal, hiVal)
    
    # if max number of curves is set, use it
    if deltaVal > 0.0:
        nCurves = deltaVal / interval
        if maxNumCurves > 0 and nCurves > maxNumCurves:
            hiVal = lowVal + deltaVal * maxNumCurves
            
    
    # sign chart with name and date
    f = figure()
    f.text(0.975, 0.025, PS.author + ' ' + time.strftime('%m/%d/%Y)'),
        horizontalalignment='right',verticalalignment='top', fontsize=_sigFontSize)
        
    f.text(0.025, 0.025, "ParaSol v" + PS.getVersion(),
        horizontalalignment='left',verticalalignment='top', fontsize=_sigFontSize)
       
    # If there are any constraint violations, show them.
    if len( violx )>0:
        plot( violx, violy, 'ro', linewidth=0, markersize=12, alpha=0.5)
        vStr = 'Red Circles : '
        vioList = []
        for viol in list(vioDict.keys()):
            vioList.append( viol )
        vStr += ', '.join( vioList )
        f.text(0.95, 0.5, vStr, rotation=270, color="r",
            horizontalalignment='center',verticalalignment='center', 
            fontsize=10, fontweight="bold", alpha=0.75)

    # do contour last so fill color doesn't get skewed
    cm = matplotlib.cm
    if hasattr(cm, colorMap):
        myColorMap = getattr(cm, colorMap)
    else:
        myColorMap = cm.summer

    #im = imshow(OutArr, interpolation='bilinear', origin='lower', alpha=alpha, 
    #    cmap=myColorMap, extent=(minVal0,maxVal0,minVal1,maxVal1))

    if 1:#try:
        
        CS1 = contourf(P,F,OutArr, arange(lowVal,hiVal,interval),
                        alpha=1., 
                        cmap=myColorMap,
                        origin='lower')        
        CS = contour(P,F,OutArr, arange(lowVal,hiVal,interval),
                        origin='lower',  colors='k', 
                        linewidths=2,
                        extent=(minVal0,maxVal0,minVal1,maxVal1))
        levels = arange(lowVal,hiVal,interval)
        
        clabel(CS, #levels,
               inline=1, 
               fmt='%3g',
               fontsize=10)
        
            
    else:#except:
        CS = contour(P,F,OutArr, arange(lowVal,hiVal,interval),
                        origin='lower',
                        linewidths=2,
                        extent=(minVal0,maxVal0,minVal1,maxVal1))
        clabel(CS,
               inline=1,
               fmt='%3g',
               fontsize=10)
        axis('auto')

    desc = PS.getResultVarAxisLabel(sysParam) 
        
    if titleStr:
        title(titleStr)
    else:
        title('%s\n%s'%(PS.subtaskName,desc))
        
    xlabel(desVars[0])
    ylabel(desVars[1])
    
    xlabel( PS.getDesignVarAxisLabel(desVars[0]) )
    ylabel( PS.getDesignVarAxisLabel(desVars[1]) )

    
    axis('on')
    hot()
    #gca().xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    #gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    majorFormatter = FormatStrFormatter('%g')
    gca().yaxis.set_major_formatter(majorFormatter)
    majorFormatter = FormatStrFormatter('%g')
    gca().xaxis.set_major_formatter(majorFormatter)
    
    try:
        savefig(filename, dpi=dpi)
    except:
        print(traceback.print_exc())
        print('===> WARNING, could NOT save',filename)
        close()
        return None

    print("image saved as",filename)
    close()
    
    #signAndDatePlot(PS, filename)
        
    # restore original values
    #PS.setDesignVar( desVars[0], dv0.savedVal )
    #PS.setDesignVar( desVars[1], dv1.savedVal )
    #PS.evaluate() <-- called from Plots_Cache IF REQUIRED # recalc design point from savedVal
    __Plots_Cache.restoreParasolState()
    
    if makeHTML:
        PS.htmlFile.write('<center><table border="1" class="mytable"><tr><td>')
        #PS.htmlFile.write( '<img src="file:///%s">'%(filename,) )
        PS.htmlFile.write( '<img src="%s">'%(htmlPath,) )
        
        PS.htmlFile.write('</td></tr><tr><td nowrap>')
        PS.htmlFile.write( PS.getHTMLDesVarSummary(*desVars) ) # omit from desVar table
        
        
        PS.htmlFile.write('</td></tr></table></center>')
        
            
    if PS.userOptions.word:
        putPlotInWord( PS, filename, *desVars) # omit from desVar table
            
    if PS.userOptions.ppt:
        putPlotInPPT( PS, filename, desc)


    # send to excel
    if PS.userOptions.excel:
        
        #print 'levels=',CS.levels
        #V0 = CS.collections[0].get_verts()
        #print 'V0=',V0
        #V1 = CS.collections[1].get_verts()
        #print 'V1=',V1
        
        #pathL = CS.collections[0].get_paths()

        # need to make rs list of row values for excel
        colL = []
        for i,c in enumerate(CS.collections):
            #verts = c.get_verts()
            
            #print i,') _segments=',c._segments
            
            pathL = c.get_paths()
            segs = []
            for path in pathL:
                segs.append( path.vertices )
            #verts = c.get_path().vertices
            
            if segs: # is matplotlib.collections.LineCollection:
                segs = sort_and_join_segments( segs, minVal0,maxVal0,minVal1,maxVal1  )
                val = CS.levels[i]
                lblStr = '%s=%g'%(sysParam,val)
                xL = [lblStr]
                yL = [lblStr]
                for s in segs:
                    for x,y in s:
                        xL.append(x)
                        yL.append(y)
                    xL.append('')
                    yL.append('')
                #for x,y in verts:
                #    xL.append(x)
                #    yL.append(y)
                colL.append( [xL, yL] )
                
        rs = build_rs_from_colL(colL)
        sheetName = 'Data_%i'%__plotNumber 
        chartName = 'Plot_%i'%__plotNumber 

        xLabelStr = PS.getDesignVarAxisLabel(desVars[0]) 
        yLabelStr = PS.getDesignVarAxisLabel(desVars[1]) 

        PS.xlDoc.makeChart( rs, title=titleStr, nCurves = 1,
                  sheetName=sheetName,chartName=chartName,  showPoints=1, showLegend=1,
                  yLabel=yLabelStr, xLabel=xLabelStr)
                  

        for i in range(1, len(rs[0])/2 ):
            PS.xlDoc.addNewSeriesToCurrentSheetChart( xColumn=1+i*2, yColumn=2+i*2)

        PS.xlDoc.setXrange( minVal0,maxVal0 )
        PS.xlDoc.setYrange( minVal1,maxVal1 )
        PS.xlDoc.setMarkerSizes( size=3 )

        PS.xlDoc.addTextBox(PS.getDesVarShortSummary(*desVars))

def sort_and_join_segments( segs, minx, maxx, miny, maxy ):
    
    # turn segs into list structure
    segL = []
    for s in segs:
        segL.append( list(s) )
    
    epsX = (maxx-minx)/1000.0
    epsY = (maxy-miny)/1000.0
    def borderPoint(x,y):
        if x<minx+epsX or x>maxx-epsX or y<miny+epsY or y>maxy-epsY:
            return 1
        else:
            return 0
            
    def grabNearestNeighbor(x,y):
        n=-1
        best = 1.0E300
        for i,s in enumerate(segL):
            xt, yt = s[0][0], s[0][1]
            if not borderPoint(xt, yt):
                d = (x-xt)**2 + (y-yt)**2
                if d<best:
                    n=i
                    best=d
        # check to see if segment needs to be reversed
        rev=0
        for i,s in enumerate(segL):
            xt, yt = s[-1][0], s[-1][1]
            if not borderPoint(xt, yt):
                d = (x-xt)**2 + (y-yt)**2
                if d<best:
                    n=i
                    best=d
                    rev=1
        
        if n>=0:
            sreturn = segL.pop(n)
            if rev:
                sreturn.reverse()
            return sreturn
        else:
            return None
            
    # first only worry about non-border end of segments
    madeProgress = 1
    didLastCheck = 0
    while madeProgress:
        madeProgress = 0
        testSegs = [segL.pop(0)]
        while len( segL )>0 :
            xe,ye = testSegs[-1][-1][0],testSegs[-1][-1][1]
            if not borderPoint(xe,ye):
                seg = grabNearestNeighbor(xe,ye)
                if seg:
                    testSegs[-1].extend( seg )
                    madeProgress = 1
            else:
                testSegs.append( segL.pop(0) )
        segL = testSegs
        testSegs = []
    
        # now see if beginning of segs should join
        if didLastCheck: # but break out of loop if already done
            break
        for seg in segL:
            xe,ye = seg[-1][0],seg[-1][1]
            if borderPoint(xe,ye):
                seg.reverse()
                madeProgress = 1
            didLastCheck = 1
    
    return segL
    
    

def make2DParametricPlot(PS, sysParam="mass_lbm", desVar="PHe", xResultVar=None,
    paramVar=["MR",1.0,1.5,2.0,2.5]  ,makeHTML=1, dpi=70, linewidth=2, smallLegend=1,
    ptData=None, ptLegend='', logX=0, logY=0, titleStr='', yLabelStr='', colorL=None,
    haLabel='center', vaLabel='bottom', omitViolPts=0, reverseLabels=0):
    global __plotNumber, __Plots_Cache
    __plotNumber += 1
    
    if __Plots_Cache==None:
        __Plots_Cache = Plots_Cache(PS)
            
    try:
        _make2DParametricPlot(PS, 
            sysParam=sysParam, desVar=desVar, xResultVar=xResultVar,
            paramVar=paramVar  ,makeHTML=makeHTML, dpi=dpi, linewidth=linewidth,smallLegend=smallLegend,
            ptData=ptData, ptLegend=ptLegend, logX=logX, logY=logY, titleStr=titleStr, 
            yLabelStr=yLabelStr, colorL=colorL,haLabel=haLabel, vaLabel=vaLabel, omitViolPts=omitViolPts,
            reverseLabels=reverseLabels)
    except:
        print(' >>> ERROR... could not create 2D Parametric Plot')
        print(traceback.print_exc())

def _make2DParametricPlot(PS, sysParam="mass_lbm", desVar="PHe", xResultVar=None,
    paramVar=["MR",1.0,1.5,2.0,2.5]  ,makeHTML=1, dpi=70, linewidth=2, smallLegend=1,
    ptData=None, ptLegend='', logX=0, logY=0, titleStr='', yLabelStr='', colorL=None,
    haLabel='center', vaLabel='bottom', omitViolPts=0, reverseLabels=0):
    
    __Plots_Cache.saveParasolState()
         
    logxy = '_'
    if logX: logxy += 'logX'
    if logY: logxy += 'logY'
        
    if xResultVar==None:
        XusesResVar = 0
        fileNamePart = desVar
    else:
        fileNamePart = desVar + '_' + xResultVar
        XusesResVar = 1
        xMarkMaxL = []
        xMarkMinL = []
        yMarkMaxL = []
        yMarkMinL = []
        
    # make csv file
    csvfilename = os.path.join( PS.outputPath,
                  PS.scriptName[:-3] + '_%i_'%__plotNumber  + \
                  '_param_'+sysParam+'_vs_'+fileNamePart+'.csv')
    print("saving data to CSV file",os.path.split(csvfilename)[-1]) 
    csvWriter = csv.writer(open(csvfilename, "w"),  dialect='excel')
    
    sumry = PS.getDesVarSummary(*[desVar, paramVar[0]])
    sp = sumry.split('\n')

    for s in sp:
        csvWriter.writerow( ( s ,) )
    rs_csv = [] # will hold data for csv file
    

    # set up PNG file
    filename = os.path.join( PS.outputPath,
               PS.scriptName[:-3] + '_%i_'%__plotNumber  + logxy +\
               '_param_'+sysParam+'_vs_'+fileNamePart+'.png')
    print("building 2D plot", os.path.split(filename)[-1]) 
    htmlPath = './%s/%s'%(PS.scriptName[:-3],os.path.split(filename)[-1])
        
    dv = PS.desVarDict[desVar]
    pv = PS.desVarDict[paramVar[0]]
    
    # sign chart with name and date
    f = figure()
    f.text(0.975, 0.025, PS.author + ' ' + time.strftime('%m/%d/%Y)'),
        horizontalalignment='right',verticalalignment='top', fontsize=_sigFontSize)
        
    f.text(0.025, 0.025, "ParaSol v" + PS.getVersion(),
        horizontalalignment='left',verticalalignment='top', fontsize=_sigFontSize)

    if PS.hasFeasibleControlVar( dv.name ) or PS.hasFeasibleControlVar( pv.name ):
        print("ERROR... can not use feasible design variable %s or %s for plot axis"%(dv.name,pv.name))
        return
    
    # don't lose current value
    dv.savedVal = PS.getDesignVar( desVar )
    pv.savedVal = PS.getDesignVar( paramVar[0] )
    
    vioXD = {} # any constraint violations
    vioYD = {}
    vioDict = {}
    
    for iL,pval in enumerate(paramVar[1:]):
        print(".", end=' ')
        PS.setDesignVar( paramVar[0], pval )


        #set up result variable x lists just in case
        xResultL = []

        x = []
        y = []
        
        for stepVal in dv.rangeL:
            PS.setDesignVar( desVar, stepVal)
            #PS.evaluate() <-- called from Plots_Cache IF REQUIRED
            __Plots_Cache.getResults()
            vioList = PS.violatesResultConstraint()
            
            if omitViolPts and len(vioList)>0:
                pass
            else:
                x.append(stepVal)
            
                # accept either result variables OR native attributes
                y.append( PS.getResultVar(sysParam) )
                
                if XusesResVar:
                    xResultL.append(PS.getResultVar(xResultVar))
    
                if len(vioList)>0: # will be empty if omitViolPts is True
                    for viol in vioList:
                        
                        if viol in vioDict:
                            vioYD[viol].append( y[-1] )
                            if XusesResVar:
                                vioXD[viol].append( xResultL[-1] )
                            else:
                                vioXD[viol].append( x[-1] )
                        else:
                            vioDict[viol] = viol
                            vioYD[viol] = [ y[-1] ]
                            if XusesResVar:
                                vioXD[viol] = [ xResultL[-1] ]
                            else:
                                vioXD[viol] = [ x[-1] ]

            
        #print x
        #print y
        
        # save x list in case the X axis is using a result variable
        xDesVarL = x
        
        # swap out x arrays if x axis is using a result variable
        if XusesResVar:
            x = xResultL
            xMarkMaxL.append( x[-1] )
            xMarkMinL.append( x[0] )
            yMarkMaxL.append( y[-1] )
            yMarkMinL.append( y[0] )

        try:
            fmt = cnames[ colorL[iL].lower() ]
            lw = linewidth 
        except:
            fmt = getColorName(iL)  # get standard color list
            lw = linewidth + 2*int(iL/7) # only modify line width if NOT using input colors


        if smallLegend:
            lblStr = ''
            di = len(x) / 6
            if reverseLabels:
                iLabel = int((1 + (5-(iL%5))) * di)
            else:
                iLabel = int((1 + (iL%5)) * di)
            props = {'ha':'%s'%haLabel, 'va':'%s'%vaLabel, 'color':fmt}
            try:
                text(x[iLabel], y[iLabel], paramVar[0]+' %g'%pval , props)
            except:
                pass
        else:
            lblStr = paramVar[0]+' %g'%pval

        if logX and logY:
            loglog(x, y, label=lblStr, linewidth=lw , color=fmt)
        elif logX:
            semilogx(x, y, label=lblStr, linewidth=lw , color=fmt)
        elif logY:
            semilogy(x, y, label=lblStr, linewidth=lw , color=fmt)
        else:
            plot(x, y, label=lblStr, linewidth=lw , color=fmt)
    
    
        # prepare data for csv file
        if len(rs_csv) == 0:
            for yval in y:
                rs_csv.append( [yval] )
            rs_csv_labels = [ paramVar[0]+' = %g'%pval ]
            
        else:
            rs_csv_labels.append( paramVar[0]+' = %g'%pval )
            for icsv, yval in enumerate(y):
                try:
                    rs_csv[icsv].append( yval )
                except:
                    pass
                
        if XusesResVar:
            rs_csv_labels.insert(-1, xResultVar +' %s = %g'%(paramVar[0],pval) )
            for i, row in enumerate( rs_csv ):
                row.insert(-1, x[i] )
        
    if len( vioDict )>0: # will be empty if omitViolPts is true
            
        NViol = len(list(vioDict.keys()))
        for msize,viol in enumerate(vioDict.keys()):
            if len(vioXD[viol])==1:  # plot will BOMB with only 1 entry in list
                vioXD[viol].append( vioXD[viol][-1] )
                vioYD[viol].append( vioYD[viol][-1] )
            
            
            mfc = ['r','g','c','m','y','b'][msize%6]
            marker = ['s','s','o','D','^','v'][msize%6]
            plot(vioXD[viol], vioYD[viol], marker=marker, mfc=mfc, mec=mfc,
                        label=str(viol), linewidth=0, alpha=0.9, markersize=5+NViol*3-msize*3)
            #print "violation = (%s)"%viol
        legend(loc='best' )
    
    # write to csv file
    #if XusesResVar:
    #    csvWriter.writerow( [xResultVar+' vs '+sysParam,''] )
    #    rs_csv_labels.insert(0, xResultVar)
    #else:
    csvWriter.writerow( [desVar+' vs '+sysParam,''] )
    rs_csv_labels.insert(0, desVar)
    
    csvWriter.writerow( rs_csv_labels )

    
    for i, row in enumerate( rs_csv ):
        try:
            row.insert(0, xDesVarL[i] )
        except:
            row.insert(0,'')
        csvWriter.writerow( row )
    csvWriter.writerow( ['',''] )
    

    # Now make labels for x result variables
    if XusesResVar:
        labelStr = "%s = %g"%(desVar,dv.maxVal )
        plot(xMarkMaxL, yMarkMaxL, 'r^', mfc='r', label=labelStr, linewidth=0, markersize=12)
        
        labelStr = "%s = %g"%(desVar,dv.minVal )
        plot(xMarkMinL, yMarkMinL, 'rv', mfc='r', label=labelStr, linewidth=0, markersize=12)
    
    
    if ptData != None:
        dx, dy = ptData
        plot(dx, dy, 'ro', mfc='b', label=ptLegend, linewidth=0)

    if XusesResVar:
        xLabelStr = PS.getResultVarAxisLabel(xResultVar) + " (%s = %g to %g)"%(desVar,dv.minVal,dv.maxVal ) 
    else:
        xLabelStr = PS.getDesignVarAxisLabel(desVar)
    xlabel( xLabelStr )
    
    
    if not yLabelStr:
        yLabelStr = PS.getResultVarAxisLabel(sysParam)
    ylabel( yLabelStr )

        
    if not titleStr:
        titleStr = PS.subtaskName + '\n' + PS.getResultVarAxisLabel(sysParam) 

    title(titleStr)
    if not smallLegend:
        legend(loc='best')
    grid(True)


    if PS.userOptions.excel:
        sheetName = 'Data_%i'%__plotNumber 
        chartName = 'Plot_%i'%__plotNumber 
        
        rs = [rs_csv_labels]
        for row in rs_csv:
            rs.append( row )
        
        PS.xlDoc.makeChart( rs, title=titleStr, nCurves = len(rs_csv[0]),
                  sheetName=sheetName,chartName=chartName,  showPoints=1, showLegend=1,
                  yLabel=yLabelStr, xLabel=xLabelStr)
                  
        PS.xlDoc.addTextBox(PS.getDesVarShortSummary(*[desVar, paramVar[0]]))
        
        # set x scale to range of design variable
        if not XusesResVar:
            dv = PS.desVarDict[desVar]
            PS.xlDoc.setXrange( dv.minVal,dv.maxVal )

    #gca().xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    #gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    #gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    
    majorFormatter = FormatStrFormatter('%g')
    gca().yaxis.set_major_formatter(majorFormatter)
    majorFormatter = FormatStrFormatter('%g')
    gca().xaxis.set_major_formatter(majorFormatter)

        
    try:
        savefig(filename, dpi=dpi)
    except:
        print(traceback.print_exc())
        print('===> WARNING, could NOT save',filename)
        close()
        return None
    print(".")
    print("image saved as",filename)
    print("with dpi =",dpi)
    close()
    
    # restore original value
    #PS.setDesignVar( desVar, dv.savedVal)
    #PS.setDesignVar( paramVar[0], pv.savedVal)
    #PS.evaluate() <-- called from Plots_Cache IF REQUIRED # recalc design point from savedVal
    __Plots_Cache.restoreParasolState()
    
    
    # make any HTML output
    if makeHTML:
        PS.htmlFile.write('<center><table border="1" class="mytable"><tr><td>')
        #PS.htmlFile.write( '<img src="file:///%s">'%(filename,) )
        PS.htmlFile.write( '<img src="%s">'%(htmlPath,) )
        
        PS.htmlFile.write('</td></tr><tr><td nowrap>')
        PS.htmlFile.write( PS.getHTMLDesVarSummary(*[desVar, paramVar[0]]) ) # omit from desVars table
        
        
        PS.htmlFile.write('</td></tr></table></center>')

            
    if PS.userOptions.word:
        putPlotInWord( PS, filename, *[desVar, paramVar[0]]) # omit from desVars table
            
    if PS.userOptions.ppt:
        putPlotInPPT( PS, filename, PS.getResultVarAxisLabel(sysParam) )


def makeCarpetPlot(PS, sysParam="sysMass",
    desVarL=[["PHe",5000.,7000.,9000.,11000.],["SF",1.5,2.0,4.0]], 
    xResultVar="requiredResultVar",
    makeHTML=1, dpi=70, linewidth=2, smallLegend=1, iLabelsX=0, iLabelsY=1000, 
    inLineLabels=1,  alphaInLineLabels=1.0,
    ptData=None, ptLegend='', logX=0, logY=0, titleStr='', yLabelStr='', colorL=None,
    haLabel='center', vaLabel='center', angDesVarL=[0.,0.], omitViolPts=0):
    global __plotNumber, __Plots_Cache
    __plotNumber += 1
    
    if __Plots_Cache==None:
        __Plots_Cache = Plots_Cache(PS)
            
    try:
        _makeCarpetPlot(PS, 
            sysParam=sysParam, desVarL=desVarL, xResultVar=xResultVar,
            makeHTML=makeHTML, dpi=dpi, linewidth=linewidth,smallLegend=smallLegend,
            iLabelsX=iLabelsX, iLabelsY=iLabelsY, inLineLabels=inLineLabels, alphaInLineLabels=alphaInLineLabels,
            ptData=ptData, ptLegend=ptLegend, logX=logX, logY=logY, titleStr=titleStr, 
            yLabelStr=yLabelStr, colorL=colorL,haLabel=haLabel, vaLabel=vaLabel,
            angDesVarL=angDesVarL, omitViolPts=omitViolPts)
    except:
        print(' >>> ERROR... could not create Carpet Plot')
        print(traceback.print_exc())

def _makeCarpetPlot(PS, sysParam="sysMass",
    desVarL=[["PHe",5000.,7000.,9000.,11000.],["SF",1.5,2.0,4.0]], 
    xResultVar="requiredResultVar",
    makeHTML=1, dpi=70, linewidth=2, smallLegend=1,iLabelsX=0, iLabelsY=1000, 
    inLineLabels=1, alphaInLineLabels=1.0,
    ptData=None, ptLegend='', logX=0, logY=0, titleStr='', yLabelStr='', colorL=None,
    haLabel='center', vaLabel='center', angDesVarL=[0.,0.], omitViolPts=0):
    
    
    __Plots_Cache.saveParasolState()
         
    logxy = '_'
    if logX: logxy += 'logX'
    if logY: logxy += 'logY'
    
    # make intermediate lists
    dvNameL = [] # list of design variable names
    dvL = []  # list of design variable objects
    NumDesVar = len( desVarL )
    if NumDesVar > 2:
        print('For NOW, Carpet plots are limited to 2 design variables')
        return
    
    for row in desVarL:
        dvName = row[0]
        dv = PS.desVarDict[dvName]
        dvL.append( dv )
        dvNameL.append( dvName )
    dvNameStr = '_'.join( dvNameL )
    
    
    fileNamePart = dvNameStr + '_' + xResultVar
    filename = os.path.join( PS.outputPath,
               PS.scriptName[:-3] + '_%i_'%__plotNumber  + logxy +\
               '_carpet_'+sysParam+'_vs_'+fileNamePart+'.png' )
    print("building Carpet plot", os.path.split(filename)[-1]) 
    htmlPath = './%s/%s'%(PS.scriptName[:-3],os.path.split(filename)[-1])            
        
    # sign chart with name and date
    f = figure()
    f.text(0.975, 0.025, PS.author + ' ' + time.strftime('%m/%d/%Y)'),
        horizontalalignment='right',verticalalignment='top', fontsize=_sigFontSize)
        
    f.text(0.025, 0.025, "ParaSol v" + PS.getVersion(),
        horizontalalignment='left',verticalalignment='top', fontsize=_sigFontSize)

    for dv in dvL:
        if PS.hasFeasibleControlVar( dv.name ):
            print("ERROR... can not use feasible design variable %s for CARPET PLOT axis"%(dv.name))
            return
    
    __Plots_Cache.setUpForFuncCall( dvNameL=dvNameL, outNameL=[xResultVar, sysParam])
    #print __Plots_Cache.funcCall( 1000.0, 2.0 )
    
    CarpetObj = Carpet( __Plots_Cache.funcCall , 
        aName=dvNameL[0], aList=desVarL[0][1:],  bName=dvNameL[1], bList=desVarL[1][1:],
        nStepsA=20, nStepsB=20, iLabelsX=iLabelsX, iLabelsY=iLabelsY, showLabels=smallLegend,
        linewidth=linewidth, inLineLabels=inLineLabels, showGrid=1, alphaInLineLabels=alphaInLineLabels,
        logX=logX, logY=logY)    
    
    CarpetObj.plotCarpet(figObj = f, afmt='green', bfmt='purple')
    
    # plot any constraint violations
    #print __Plots_Cache.getViolationXYLists()
    #print __Plots_Cache.violationDescD
    if __Plots_Cache.violationDescD and not omitViolPts:
        xviolL, yviolL = __Plots_Cache.getViolationXYLists()
        if len(xviolL)==1:  # plot will BOMB with only 1 entry in list
            xviolL.append( xviolL[-1] )
            yviolL.append( yviolL[-1] )
        
        plot( xviolL, yviolL, 'ro', linewidth=0, alpha=0.5)  #, markersize=12)
        vStr = 'Red Circles : '
        vioList = []
        for viol in __Plots_Cache.violationDescD:
            vioList.append( viol )
        vStr += ', '.join( vioList )
        f.text(0.95, 0.5, vStr, rotation=270, color="r",
            horizontalalignment='center',verticalalignment='center', 
            fontsize=10, fontweight="bold", alpha=0.75)
        
        
    
    if ptData != None:
        dx, dy = ptData
        plot(dx, dy, 'ro', mfc='b', label=ptLegend, linewidth=0)

    xlabel( PS.getResultVarAxisLabel(xResultVar) )
    
    
    if not yLabelStr:
        ylabel( PS.getResultVarAxisLabel(sysParam) )
    else:
        ylabel( yLabelStr )

        
    if not titleStr:
        titleStr = PS.subtaskName + '\n(%s & %s)'%( xResultVar, sysParam) + ' vs (%s & %s)'%(dvNameL[1],dvNameL[0])

    title(titleStr)
    
    grid(True)
        
    #gca().xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    #gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    #gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    
    majorFormatter = FormatStrFormatter('%g')
    gca().yaxis.set_major_formatter(majorFormatter)
    majorFormatter = FormatStrFormatter('%g')
    gca().xaxis.set_major_formatter(majorFormatter)

        
    try:
        savefig(filename, dpi=dpi)
    except:
        print(traceback.print_exc())
        print('===> WARNING, could NOT save',filename)
        close()
        return None
    print(".")
    print("image saved as",filename)
    print("with dpi =",dpi)
    close()
    
    # restore original value
    #for dv in dvL:
    #    PS.setDesignVar( dv.name, dv.savedVal)
    #
    #PS.evaluate() <-- called from Plots_Cache IF REQUIRED # recalc design point from savedVal
    __Plots_Cache.restoreParasolState()
    

    # make any HTML output
    if makeHTML:
        PS.htmlFile.write('<center><table border="1" class="mytable"><tr><td>')
        #PS.htmlFile.write( '<img src="file:///%s">'%(filename,) )
        PS.htmlFile.write( '<img src="%s">'%(htmlPath,) )
        
        PS.htmlFile.write('</td></tr><tr><td nowrap>')
        PS.htmlFile.write( PS.getHTMLDesVarSummary(*dvNameL) ) # omit from desVar table
        
        
        PS.htmlFile.write('</td></tr></table></center>')

            
    if PS.userOptions.word:
        putPlotInWord( PS, filename, *dvNameL) # omit from desVar table
            
    if PS.userOptions.ppt:
        putPlotInPPT( PS, filename, PS.getResultVarAxisLabel(sysParam) )

    # send to excel
    if PS.userOptions.excel:
        sheetName = 'Data_%i'%__plotNumber 
        chartName = 'CarpetPlot_%i'%__plotNumber 

        yLabelStr = PS.getResultVarAxisLabel(sysParam)
        xLabelStr = PS.getResultVarAxisLabel(xResultVar)

        colL = []
        Lmax = 0
        for a,bL,xL,yL in CarpetObj.aCurveXYL:
            lblStr = '%s=%g'%(CarpetObj.aName,a)
            xL.insert(0, lblStr)
            yL.insert(0, lblStr)
            colL.append( [xL, yL] )
            if len(xL)>Lmax:
                Lmax = len(xL)
                
        numA = len( colL )

        for b,aL,xL,yL in CarpetObj.bCurveXYL:
            lblStr = '%s=%g'%(CarpetObj.bName,b)
            xL.insert(0, lblStr)
            yL.insert(0, lblStr)
            colL.append( [xL, yL] )
            if len(xL)>Lmax:
                Lmax = len(xL)


        rs = []
        for i in range( Lmax ):
            rs.append( [] )
            
        for icol in range( len(colL) ):
            xL,yL = colL[icol]
            for i in range( Lmax ):
                if i<len(xL):
                    rs[i].append( xL[i] )
                    rs[i].append( yL[i] )
                else:
                    rs[i].append( '' )
                    rs[i].append( '' )
            
        
        PS.xlDoc.makeChart( rs, title=titleStr, nCurves = 1,
                  sheetName=sheetName,chartName=chartName,  showPoints=1, showLegend=1,
                  yLabel=yLabelStr, xLabel=xLabelStr)
                  
        PS.xlDoc.setSeriesColor( NSeries=1, red=127, green=0, blue=127)
        PS.xlDoc.setLineThickness( NSeries=1, thickness=2)

        for i in range(1, len(rs[0])/2 ):
            PS.xlDoc.addNewSeriesToCurrentSheetChart( xColumn=1+i*2, yColumn=2+i*2)
            
            if i >= numA:
                PS.xlDoc.setSeriesColor( NSeries=i+1, red=60, green=200, blue=60)
                PS.xlDoc.setLineThickness( NSeries=i+1, thickness=2+i-numA)
            else:
                PS.xlDoc.setSeriesColor( NSeries=i+1, red=127, green=0, blue=127)
                PS.xlDoc.setLineThickness( NSeries=i+1, thickness=2+i)

        xmin, xmax, ymin, ymax = CarpetObj.xmin, CarpetObj.xmax, CarpetObj.ymin, CarpetObj.ymax

        PS.xlDoc.setXrange( xmin, xmax )
        PS.xlDoc.setYrange( ymin, ymax )
        PS.xlDoc.setMarkerSizes( size=3 )

        PS.xlDoc.addTextBox(PS.getDesVarShortSummary(*dvNameL))


def build_rs_from_colL(colL):
    
    Lmax = 0
    for col in colL:
        if len(col[0])>Lmax:
            Lmax = len(col[0])

    rs = []
    for i in range( Lmax ):
        rs.append( [] )
        
    for icol in range( len(colL) ):
        xL,yL = colL[icol]
        for i in range( Lmax ):
            if i<len(xL):
                rs[i].append( xL[i] )
                rs[i].append( yL[i] )
            else:
                rs[i].append( '' )
                rs[i].append( '' )
    return rs
    

stdList = ['red','green','blue','cyan','magenta','olive','brown','gold','coral',
    'darkred','darkgreen','darkblue']
def getColorName(i):
    if i < len( stdList ):
        return stdList[i]
    elif i< len(cnames):
        return cnames[ list(cnames.keys())[i] ]
    else:
        return cnames[ list(cnames.keys())[i/len(cnames)] ]
cnames = {
    'aliceblue'            : '#F0F8FF',
    'antiquewhite'         : '#FAEBD7',
    'aqua'                 : '#00FFFF',
    'aquamarine'           : '#7FFFD4',
    'azure'                : '#F0FFFF',
    'beige'                : '#F5F5DC',
    'bisque'               : '#FFE4C4',
    'black'                : '#000000',
    'blanchedalmond'       : '#FFEBCD',
    'blue'                 : '#0000FF',
    'blueviolet'           : '#8A2BE2',
    'brown'                : '#A52A2A',
    'burlywood'            : '#DEB887',
    'cadetblue'            : '#5F9EA0',
    'chartreuse'           : '#7FFF00',
    'chocolate'            : '#D2691E',
    'coral'                : '#FF7F50',
    'cornflowerblue'       : '#6495ED',
    'cornsilk'             : '#FFF8DC',
    'crimson'              : '#DC143C',
    'cyan'                 : '#00FFFF',
    'darkblue'             : '#00008B',
    'darkcyan'             : '#008B8B',
    'darkgoldenrod'        : '#B8860B',
    'darkgray'             : '#A9A9A9',
    'darkgreen'            : '#006400',
    'darkkhaki'            : '#BDB76B',
    'darkmagenta'          : '#8B008B',
    'darkolivegreen'       : '#556B2F',
    'darkorange'           : '#FF8C00',
    'darkorchid'           : '#9932CC',
    'darkred'              : '#8B0000',
    'darksalmon'           : '#E9967A',
    'darkseagreen'         : '#8FBC8F',
    'darkslateblue'        : '#483D8B',
    'darkslategray'        : '#2F4F4F',
    'darkturquoise'        : '#00CED1',
    'darkviolet'           : '#9400D3',
    'deeppink'             : '#FF1493',
    'deepskyblue'          : '#00BFFF',
    'dimgray'              : '#696969',
    'dodgerblue'           : '#1E90FF',
    'firebrick'            : '#B22222',
    'floralwhite'          : '#FFFAF0',
    'forestgreen'          : '#228B22',
    'fuchsia'              : '#FF00FF',
    'gainsboro'            : '#DCDCDC',
    'ghostwhite'           : '#F8F8FF',
    'gold'                 : '#FFD700',
    'goldenrod'            : '#DAA520',
    'gray'                 : '#808080',
    'green'                : '#008000',
    'greenyellow'          : '#ADFF2F',
    'honeydew'             : '#F0FFF0',
    'hotpink'              : '#FF69B4',
    'indigo'               : '#4B0082',
    'ivory'                : '#FFFFF0',
    'khaki'                : '#F0E68C',
    'lavender'             : '#E6E6FA',
    'lavenderblush'        : '#FFF0F5',
    'lawngreen'            : '#7CFC00',
    'lemonchiffon'         : '#FFFACD',
    'lightblue'            : '#ADD8E6',
    'lightcoral'           : '#F08080',
    'lightcyan'            : '#E0FFFF',
    'lightgoldenrodyellow' : '#FAFAD2',
    'lightgreen'           : '#90EE90',
    'lightgrey'            : '#D3D3D3',
    'lightpink'            : '#FFB6C1',
    'lightsalmon'          : '#FFA07A',
    'lightseagreen'        : '#20B2AA',
    'lightskyblue'         : '#87CEFA',
    'lightslategray'       : '#778899',
    'lightsteelblue'       : '#B0C4DE',
    'lightyellow'          : '#FFFFE0',
    'lime'                 : '#00FF00',
    'limegreen'            : '#32CD32',
    'linen'                : '#FAF0E6',
    'magenta'              : '#FF00FF',
    'maroon'               : '#800000',
    'mediumaquamarine'     : '#66CDAA',
    'mediumblue'           : '#0000CD',
    'mediumorchid'         : '#BA55D3',
    'mediumpurple'         : '#9370DB',
    'mediumseagreen'       : '#3CB371',
    'mediumslateblue'      : '#7B68EE',
    'mediumspringgreen'    : '#00FA9A',
    'mediumturquoise'      : '#48D1CC',
    'mediumvioletred'      : '#C71585',
    'midnightblue'         : '#191970',
    'mintcream'            : '#F5FFFA',
    'mistyrose'            : '#FFE4E1',
    'moccasin'             : '#FFE4B5',
    'navajowhite'          : '#FFDEAD',
    'navy'                 : '#000080',
    'oldlace'              : '#FDF5E6',
    'olive'                : '#808000',
    'olivedrab'            : '#6B8E23',
    'orange'               : '#FFA500',
    'orangered'            : '#FF4500',
    'orchid'               : '#DA70D6',
    'palegoldenrod'        : '#EEE8AA',
    'palegreen'            : '#98FB98',
    'palevioletred'        : '#AFEEEE',
    'peru'                 : '#CD853F',
    'pink'                 : '#FFC0CB',
    'plum'                 : '#DDA0DD',
    'powderblue'           : '#B0E0E6',
    'purple'               : '#800080',
    'red'                  : '#FF0000',
    'rosybrown'            : '#BC8F8F',
    'royalblue'            : '#4169E1',
    'saddlebrown'          : '#8B4513',
    'salmon'               : '#FA8072',
    'sandybrown'           : '#FAA460',
    'seagreen'             : '#2E8B57',
    'seashell'             : '#FFF5EE',
    'sienna'               : '#A0522D',
    'silver'               : '#C0C0C0',
    'skyblue'              : '#87CEEB',
    'slateblue'            : '#6A5ACD',
    'slategray'            : '#708090',
    'snow'                 : '#FFFAFA',
    'springgreen'          : '#00FF7F',
    'steelblue'            : '#4682B4',
    'tan'                  : '#D2B48C',
    'teal'                 : '#008080',
    'thistle'              : '#D8BFD8',
    'tomato'               : '#FF6347',
    'turquoise'            : '#40E0D0',
    'violet'               : '#EE82EE',
    'wheat'                : '#F5DEB3',
    'white'                : '#FFFFFF',
    'whitesmoke'           : '#F5F5F5',
    'yellow'               : '#FFFF00',
    'yellowgreen'          : '#9ACD32',
    'black'                : '#000000',
    'navy'                 : '#000080',
    'darkblue'             : '#00008B',
    'mediumblue'           : '#0000CD',
    'blue'                 : '#0000FF',
    'darkgreen'            : '#006400',
    'green'                : '#008000',
    'teal'                 : '#008080',
    'darkcyan'             : '#008B8B',
    'deepskyblue'          : '#00BFFF',
    'darkturquoise'        : '#00CED1',
    'mediumspringgreen'    : '#00FA9A',
    'lime'                 : '#00FF00',
    'springgreen'          : '#00FF7F',
    'aqua'                 : '#00FFFF',
    'cyan'                 : '#00FFFF',
    'midnightblue'         : '#191970',
    'dodgerblue'           : '#1E90FF',
    'lightseagreen'        : '#20B2AA',
    'forestgreen'          : '#228B22',
    'seagreen'             : '#2E8B57',
    'darkslategray'        : '#2F4F4F',
    'limegreen'            : '#32CD32',
    'mediumseagreen'       : '#3CB371',
    'turquoise'            : '#40E0D0',
    'royalblue'            : '#4169E1',
    'steelblue'            : '#4682B4',
    'darkslateblue'        : '#483D8B',
    'mediumturquoise'      : '#48D1CC',
    'indigo'               : '#4B0082',
    'darkolivegreen'       : '#556B2F',
    'cadetblue'            : '#5F9EA0',
    'cornflowerblue'       : '#6495ED',
    'mediumaquamarine'     : '#66CDAA',
    'dimgray'              : '#696969',
    'slateblue'            : '#6A5ACD',
    'olivedrab'            : '#6B8E23',
    'slategray'            : '#708090',
    'lightslategray'       : '#778899',
    'mediumslateblue'      : '#7B68EE',
    'lawngreen'            : '#7CFC00',
    'chartreuse'           : '#7FFF00',
    'aquamarine'           : '#7FFFD4',
    'maroon'               : '#800000',
    'purple'               : '#800080',
    'olive'                : '#808000',
    'gray'                 : '#808080',
    'skyblue'              : '#87CEEB',
    'lightskyblue'         : '#87CEFA',
    'blueviolet'           : '#8A2BE2',
    'darkred'              : '#8B0000',
    'darkmagenta'          : '#8B008B',
    'saddlebrown'          : '#8B4513',
    'darkseagreen'         : '#8FBC8F',
    'lightgreen'           : '#90EE90',
    'mediumpurple'         : '#9370DB',
    'darkviolet'           : '#9400D3',
    'palegreen'            : '#98FB98',
    'darkorchid'           : '#9932CC',
    'yellowgreen'          : '#9ACD32',
    'sienna'               : '#A0522D',
    'brown'                : '#A52A2A',
    'darkgray'             : '#A9A9A9',
    'lightblue'            : '#ADD8E6',
    'greenyellow'          : '#ADFF2F',
    'palevioletred'        : '#AFEEEE',
    'lightsteelblue'       : '#B0C4DE',
    'powderblue'           : '#B0E0E6',
    'firebrick'            : '#B22222',
    'darkgoldenrod'        : '#B8860B',
    'mediumorchid'         : '#BA55D3',
    'rosybrown'            : '#BC8F8F',
    'darkkhaki'            : '#BDB76B',
    'silver'               : '#C0C0C0',
    'mediumvioletred'      : '#C71585',
    'peru'                 : '#CD853F',
    'chocolate'            : '#D2691E',
    'tan'                  : '#D2B48C',
    'lightgrey'            : '#D3D3D3',
    'thistle'              : '#D8BFD8',
    'orchid'               : '#DA70D6',
    'goldenrod'            : '#DAA520',
    'crimson'              : '#DC143C',
    'gainsboro'            : '#DCDCDC',
    'plum'                 : '#DDA0DD',
    'burlywood'            : '#DEB887',
    'lightcyan'            : '#E0FFFF',
    'lavender'             : '#E6E6FA',
    'darksalmon'           : '#E9967A',
    'violet'               : '#EE82EE',
    'palegoldenrod'        : '#EEE8AA',
    'lightcoral'           : '#F08080',
    'khaki'                : '#F0E68C',
    'aliceblue'            : '#F0F8FF',
    'honeydew'             : '#F0FFF0',
    'azure'                : '#F0FFFF',
    'wheat'                : '#F5DEB3',
    'beige'                : '#F5F5DC',
    'whitesmoke'           : '#F5F5F5',
    'mintcream'            : '#F5FFFA',
    'ghostwhite'           : '#F8F8FF',
    'salmon'               : '#FA8072',
    'sandybrown'           : '#FAA460',
    'antiquewhite'         : '#FAEBD7',
    'linen'                : '#FAF0E6',
    'lightgoldenrodyellow' : '#FAFAD2',
    'oldlace'              : '#FDF5E6',
    'red'                  : '#FF0000',
    'fuchsia'              : '#FF00FF',
    'magenta'              : '#FF00FF',
    'deeppink'             : '#FF1493',
    'orangered'            : '#FF4500',
    'tomato'               : '#FF6347',
    'hotpink'              : '#FF69B4',
    'coral'                : '#FF7F50',
    'darkorange'           : '#FF8C00',
    'lightsalmon'          : '#FFA07A',
    'orange'               : '#FFA500',
    'lightpink'            : '#FFB6C1',
    'pink'                 : '#FFC0CB',
    'gold'                 : '#FFD700',
    'navajowhite'          : '#FFDEAD',
    'moccasin'             : '#FFE4B5',
    'bisque'               : '#FFE4C4',
    'mistyrose'            : '#FFE4E1',
    'blanchedalmond'       : '#FFEBCD',
    'lavenderblush'        : '#FFF0F5',
    'seashell'             : '#FFF5EE',
    'cornsilk'             : '#FFF8DC',
    'lemonchiffon'         : '#FFFACD',
    'floralwhite'          : '#FFFAF0',
    'snow'                 : '#FFFAFA',
    'yellow'               : '#FFFF00',
    'lightyellow'          : '#FFFFE0',
    'ivory'                : '#FFFFF0',
    }


if __name__ == "__main__":  #self test
    pass
    