
from pylab import *
import copy
from math import *
from matplotlib.ticker import FormatStrFormatter

#def setAxes():
#    ax = gca()
#    ax.apply_aspect()
#    
#    print ax.get_xlim() 
#    print ax.get_ylim()

class Carpet( object ):
    
    def __init__(self, func, 
        aName='A', aList=[1.,2.,3.,4.],  bName='B', bList=[1.,2.,3.,4.],
        nStepsA=20, nStepsB=20, iLabelsX=0, iLabelsY=1000, alphaInLineLabels=0.5,
        linewidth=2, inLineLabels=1, showGrid=1, showLabels=1,
        logX=0, logY=0, titleStr='', xLabelStr='', yLabelStr=''):
        '''func returns the x,y coordinates that are plotted'''

        self.func = func
        self.aName = aName
        self.aList = aList
        self.bName = bName
        self.bList = bList
        
        self.nStepsA=nStepsA
        self.nStepsB=nStepsB
        self.iLabelsX = iLabelsX
        self.iLabelsY = iLabelsY
        self.alphaInLineLabels = alphaInLineLabels
        
        self.linewidth = linewidth
        self.inLineLabels = inLineLabels
        self.showLabels = showLabels
        self.showGrid = showGrid
        self.logX = logX
        self.logY = logY
        self.titleStr = titleStr
        self.yLabelStr = yLabelStr
        self.xLabelStr = xLabelStr
        
        self.aValL = copy.deepcopy( aList )
        self.aValL.sort()
        self.bValL = copy.deepcopy( bList )
        self.bValL.sort()
        
        self.stepA = (self.aValL[-1]-self.aValL[0]) / float( self.nStepsA )
        self.stepB = (self.bValL[-1]-self.bValL[0]) / float( self.nStepsB )
        
        # make curves along const b direction
        self.bCurveXYL = []
        for b in self.bValL:
            aL = []
            xL = []
            yL = []
            for a in self.aValL:
                x,y = func(a,b)
                aL.append(a)
                xL.append(x)
                yL.append(y)
            self.bCurveXYL.append( [b,aL,xL,yL] )
            
        # fill out curves
        for b,aL,xL,yL in self.bCurveXYL:
            i = len(aL)-1
            while i>0:
                while aL[i]-aL[i-1]>self.stepA*1.2:
                    a = aL[i]-self.stepA
                    x,y = func(a,b)
                    aL.insert(i,a)
                    xL.insert(i,x)
                    yL.insert(i,y)
                i = i -1
        
        # make curves along const a direction
        self.aCurveXYL = []
        for a in self.aValL:
            bL = []
            xL = []
            yL = []
            for b in self.bValL:
                x,y = func(a,b)
                bL.append(b)
                xL.append(x)
                yL.append(y)
            self.aCurveXYL.append( [a,bL,xL,yL] )
            
        # fill out curves
        for a,bL,xL,yL in self.aCurveXYL:
            i = len(bL)-1
            while i>0:
                while bL[i]-bL[i-1]>self.stepB*1.2:
                    b = bL[i]-self.stepB
                    x,y = func(a,b)
                    bL.insert(i,b)
                    xL.insert(i,x)
                    yL.insert(i,y)
                i = i -1
                    
            
        #for ac in self.aCurveXYL:
        #    print ac
        #    print len( ac[-1] )
            
    def plotCarpet(self, afmt='red', bfmt='blue', figObj=None):
        
        if figObj:
            f = figObj
        else:
            f = figure()
        
        if self.showGrid: grid()
    
        if self.yLabelStr:
            ylabel( self.yLabelStr )
    
        if self.xLabelStr:
            xlabel( self.xLabelStr )
            
        if self.titleStr:
            title(self.titleStr)
    
        majorFormatter = FormatStrFormatter('%g')
        gca().yaxis.set_major_formatter(majorFormatter)
        majorFormatter = FormatStrFormatter('%g')
        gca().xaxis.set_major_formatter(majorFormatter)
        
        for a,bL,xL,yL in self.aCurveXYL:
            #plot(xL, yL, label='%s=%g'%(self.aName,a), linewidth=self.linewidth , color=afmt)
            lblStr = '%s=%g'%(self.aName,a)

            if self.logX and self.logY:
                loglog(xL, yL, label=lblStr, linewidth=self.linewidth , color=afmt)
            elif self.logX:
                semilogx(xL, yL, label=lblStr, linewidth=self.linewidth , color=afmt)
            elif self.logY:
                semilogy(xL, yL, label=lblStr, linewidth=self.linewidth , color=afmt)
            else:
                plot(xL, yL, label=lblStr, linewidth=self.linewidth , color=afmt)
        

        for b,aL,xL,yL in self.bCurveXYL:
            #plot(xL, yL, label='%s=%g'%(self.bName,b), linewidth=self.linewidth , color=bfmt)
            lblStr = '%s=%g'%(self.bName,b)

            if self.logX and self.logY:
                loglog(xL, yL, label=lblStr, linewidth=self.linewidth , color=bfmt)
            elif self.logX:
                semilogx(xL, yL, label=lblStr, linewidth=self.linewidth , color=bfmt)
            elif self.logY:
                semilogy(xL, yL, label=lblStr, linewidth=self.linewidth , color=bfmt)
            else:
                plot(xL, yL, label=lblStr, linewidth=self.linewidth , color=bfmt)
            
        ax = gca()
        #ax.apply_aspect()
        
        xmin,xmax = ax.get_xlim() 
        #print 'xmin,xmax',xmin,xmax
        ymin,ymax = ax.get_ylim()
        #print 'ymin,ymax',ymin,ymax
        
        # save plot limits as attributes
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        
        # make enough room around the carpet to make labels
        
        
        bbox = { 'pad':0, 'facecolor':'w', 'edgecolor':'w', \
                'clip_on':False, 'lw':0, 'alpha':0.01} 
        if self.inLineLabels:
            bbox['alpha'] = self.alphaInLineLabels
        props = {'ha':'center', 'va':'center', 'bbox':bbox}
        
        # dx = (xmax-xmin)/50.0
        # dy = (ymax-ymin)/50.0
        label = ''
        if self.iLabelsX > len(self.bValL)-2:
            self.iLabelsX = len(self.bValL)-2
        for a,bL,xL,yL in self.aCurveXYL:
            #props = {'ha':'%s'%haLabel, 'va':'%s'%vaLabel, 'color':afmt, 'rotation':0.,
            #    'bbox':dict(facecolor='white', alpha=0.1, lw=0, clip_on=False)}
            if label:
                label = '%g '%a
            else:
                label = '%s=%g '%(self.aName,a)
            
            i1 = bL.index( self.bValL[self.iLabelsX+1] )
            i0 = bL.index( self.bValL[self.iLabelsX] )
            i = int((i1+i0)/2)
            
            self.placeLabel(i, xL, yL, afmt, label,  xmin, xmax, ymin, ymax, props)

        label = ''
        if self.iLabelsY > len(self.aValL)-2:
            self.iLabelsY = len(self.aValL)-2
        for b,aL,xL,yL in self.bCurveXYL:
            #props = {'ha':'%s'%haLabel, 'va':'%s'%vaLabel, 'color':bfmt, 'rotation':0.,
            #    'bbox':dict(facecolor='white', alpha=0.1, lw=0, clip_on=False)}
            
            if label:
                label = '%g '%b
            else:
                label = '%s=%g '%(self.bName,b)
                
            ilast = aL.index( self.aValL[self.iLabelsY+1] )
            ipen = aL.index( self.aValL[self.iLabelsY] )
            i = int((ilast+ipen)/2)
            
            self.placeLabel(i, xL, yL, bfmt, label,  xmin, xmax, ymin, ymax, props)
            
    def placeLabel(self, i, xL, yL, fmt, label,  xmin, xmax, ymin, ymax, props):
        
        if not self.showLabels:
            return
        
        if len(xL)<2:
            return 
        else:
            if i>= len(xL):
                i = len(xL)-2
            dx = xL[i+1] - xL[i]
            dy = yL[i+1] - yL[i]
            fdx = 8. * dx / (xmax-xmin)
            fdy = 6. * dy / (ymax-ymin)
            
            if fdy==0.0:
                if fdx>0.0:
                    ang = 0
                else:
                    ang = 0
            else:
                try:
                    ang = int( atan( fdy / fdx ) * 180.0 / pi )
                except:
                    ang = 90
                
            xave = (xL[i+1] + xL[i])/2.
            yave = (yL[i+1] + yL[i])/2.
            offx = 0.0
            offy = 0.0
            props['va'] = 'center'
            props['ha'] = 'center'
            
            if ang > 45.0:
                offx = (xmax-xmin)/50.0
            elif ang < -45.0:
                offx = (xmax-xmin)/50.0
            else:
                offy = (ymax-ymin)/50.0
            
            props['color']=fmt
            props['rotation'] = ang
            
            if self.inLineLabels:
                text(xave, yave, label , props)
            else:
                text(xave+offx, yave+offy, label , props)
        

if __name__ == "__main__":  #self test
    
    from math import *
    def func3(a,b):
        x = a**2 + b
        y = 2*b**2 + 3*a
        return x,y
        
    C = Carpet(func3, linewidth=1, titleStr='Simple Function Test', xLabelStr='Horizontal Axis', yLabelStr='Vertical Axis')
    C.plotCarpet(figObj = figure(), afmt='green', bfmt='purple')
    show()
    