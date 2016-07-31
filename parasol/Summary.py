
__author__ = "Charlie Taylor (charlietaylor@sourceforge.net)"
__version__ = " 1.0 "
__date__ = "Jan 1, 2009"
__copyright__ = "Copyright (c) 2009 Charlie Taylor"
__license__ = "BSD"

sepLine = '-'*40 #: 40 dashes used to separate sections of output

class Summary( object ):
    
    """
     Collect summary information regarding a study or an object.
     
     HTML output uses style classes found in HTML_supt.py

    """
    
    def __init__(self,  summaryTitle='Summary Title', subTitle='subtitle'):
        '''Initialize the summary object with title and subtile, 
               prepare lists of inputs, outputs and assumptions.
           
           @param summaryTitle: title of the summary (str)
           @param subTitle: subtitle of summary (str)
        '''
        
        self.summaryTitle = summaryTitle
        self.subTitle = subTitle
        
        self.inputs = [] #: list of input variables
        self.outputs = [] #: list of output variables
        self.assumptions = [] #: list of assumptions 
        
    def addAssumption(self, label='generic param'):
        self.assumptions.append( label )
        
    def addInput(self, label='generic param', value=0.0, units='xxx', format='%g'):
        self.inputs.append( [label, value, units, format] )
        
    def addOutput(self, label='generic param', value=0.0, units='xxx', format='%g'):
        self.outputs.append( [label, value, units, format] )
        
    def getSummTopLines(self):
        sOut = []
        sOut.append( self.summaryTitle + ': ' + self.subTitle )
        return sOut

    def getSummAssumptions(self):
        sOut = []
        if len( self.assumptions ) > 0:
            for label in self.assumptions:
                sOut.append( '        ' + label )
        return sOut

    def getSummInputs(self):
        sOut = []
        
        if len( self.inputs )>0:
            sOut.append( '     ==== INPUT ====    ' )
            # make output line up by calculating longest label length
            nadj = 15
            for label, value, units, format in self.inputs:
                if len(label)>nadj: nadj = len(label)
            for label, value, units, format in self.inputs:
                sOut.append( '        ' + label.ljust(nadj) + ' = ' + format%value + ' %s'%units )
                
        return sOut

    def getSummOutputs(self):
        sOut = []
        if len( self.outputs )>0:
            sOut.append( '     ==== OUTPUT ====    ' )
            # make output line up by calculating longest label length
            nadj = 15
            for label, value, units, format in self.outputs:
                if len(label)>nadj: nadj = len(label)
            for label, value, units, format in self.outputs:
                sOut.append( '        ' + label.ljust(nadj) + ' = ' + format%value + ' %s'%units )
        
        return sOut
        
    def getTextSummary(self):
        sOut = self.getSummTopLines() + self.getSummAssumptions() +\
            self.getSummInputs() + self.getSummOutputs()
        return '\n'.join( sOut )
        
    def getHTMLSummary(self):
        
        sOut = []
        sOut.append('<center><table class="mytable" width="680"><th colspan="4" bgcolor="#BBBBBB" align="left">')
        sOut.append('%s</th>'%(self.summaryTitle + ': ' + self.subTitle,) ) 
        
        
        if len( self.assumptions ) > 0:
            for label in self.assumptions:
                sOut.append( '<tr><td colspan="4" align="left">' + label + "</td></tr>" )

        if len( self.inputs )>0 or len( self.outputs )>0:
            sOut.append( '<tr><td colspan="2" valign="top">' )

        # Description Field Can be added in 4th column
        if len( self.inputs )>0:
            sOut.append('<table class="mytable" ><tr><td colspan="4" align="center">==== INPUT ====</td></tr>')
            sOut.append('<tr><td><b>Name</b></td><td><b>Value</b></td><td><b>Units</b></td><td><b> </b></td></tr>')
            for label, value, units, format in self.inputs:
                sOut.append( '<tr><td align="left">' + label + '</td><td align="left"> = ' +\
                    format%value + '</td><td align="left"> %s'%units + '</td><td></td></tr>' )
            sOut.append('</table>')
                    
        if len( self.inputs )>0 or len( self.outputs )>0:
            sOut.append( '</td><td colspan="2" valign="top">' )
                
        # Description Field Can be added in 4th column
        if len( self.outputs )>0:
            sOut.append('<table class="mytable" ><tr><td colspan="4" align="center">==== OUTPUT ====</td></tr>')
            sOut.append('<tr><td><b>Name</b></td><td><b>Value</b></td><td><b>Units</b></td><td><b> </b></td></tr>')
            for label, value, units, format in self.outputs:
                sOut.append( '<tr><td align="left">' + label + '</td><td align="left"> = ' +\
                    format%value + '</td><td align="left"> %s'%units + '</td><td></td></tr>' )
            sOut.append('</table>')
                    
        if len( self.inputs )>0 or len( self.outputs )>0:
            sOut.append( '</td></tr>')

                
        sOut.append('</table></center>')
        
        return '\n'.join( sOut )


if __name__ == "__main__":  #self test
    
    S = Summary( summaryTitle='Summary Title', subTitle='subtitle')
    S.addAssumption( 'Assume this is a test' )
    
    S.addInput( label='Solar Flux', value=1.0, units='BTU/sqin', format='%g')
    S.addOutput(label='Tea Temperature', value=100.0, units='C', format='%g')
    print S.getTextSummary()
    print
    print S.getHTMLSummary()
    