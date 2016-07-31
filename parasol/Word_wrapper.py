import win32com
from win32com.client import Dispatch
import string

# include word constants here
wdNormalView                  =0x1        # from enum WdViewType
wdStyleTypeTable              =0x3        # from enum WdStyleType
wdAutoFitContent              =0x1        # from enum WdAutoFitBehavior
wdAutoFitFixed                =0x0        # from enum WdAutoFitBehavior
wdAutoFitWindow               =0x2        # from enum WdAutoFitBehavior
wdWord8TableBehavior          =0x0        # from enum WdDefaultTableBehavior
wdWord9TableBehavior          =0x1        # from enum WdDefaultTableBehavior

wdAlignRowCenter              =0x1        # from enum WdRowAlignment
wdAlignRowLeft                =0x0        # from enum WdRowAlignment
wdAlignRowRight               =0x2        # from enum WdRowAlignment

justDict = {'c':wdAlignRowCenter, 'l':wdAlignRowLeft, 'r':wdAlignRowRight }

wdLineStyleNone               =0x0        # from enum WdLineStyle
wdBorderBottom                =-3         # from enum WdBorderType
wdBorderDiagonalDown          =-7         # from enum WdBorderType
wdBorderDiagonalUp            =-8         # from enum WdBorderType
wdBorderHorizontal            =-5         # from enum WdBorderType
wdBorderLeft                  =-2         # from enum WdBorderType
wdBorderRight                 =-4         # from enum WdBorderType
wdBorderTop                   =-1         # from enum WdBorderType
wdBorderVertical              =-6         # from enum WdBorderType

# for text color index
wdAuto                        =0x0        # from enum WdColorIndex
wdBlack                       =0x1        # from enum WdColorIndex
wdBlue                        =0x2        # from enum WdColorIndex
wdBrightGreen                 =0x4        # from enum WdColorIndex
wdByAuthor                    =-1         # from enum WdColorIndex
wdDarkBlue                    =0x9        # from enum WdColorIndex
wdDarkRed                     =0xd        # from enum WdColorIndex
wdDarkYellow                  =0xe        # from enum WdColorIndex
wdGray25                      =0x10       # from enum WdColorIndex
wdGray50                      =0xf        # from enum WdColorIndex
wdGreen                       =0xb        # from enum WdColorIndex
wdNoHighlight                 =0x0        # from enum WdColorIndex
wdPink                        =0x5        # from enum WdColorIndex
wdRed                         =0x6        # from enum WdColorIndex
wdTeal                        =0xa        # from enum WdColorIndex
wdTurquoise                   =0x3        # from enum WdColorIndex
wdViolet                      =0xc        # from enum WdColorIndex
wdWhite                       =0x8        # from enum WdColorIndex
wdYellow                      =0x7        # from enum WdColorIndex

textColorIndexDict = {'auto':wdAuto ,'k':wdBlack ,'b':wdBlue ,'gg':wdBrightGreen ,
    'auth':wdByAuthor ,'bb':wdDarkBlue ,'rr':wdDarkRed ,'yy':wdDarkYellow ,
    '25':wdGray25 ,'50':wdGray50 ,'g':wdGreen ,'no':wdNoHighlight ,'p':wdPink ,
    'r':wdRed ,'t':wdTeal ,'q':wdTurquoise ,'v':wdViolet ,'w':wdWhite ,
    'y':wdYellow }

# for color definitions
if 1:
	wdColorAqua                   =0xcccc33   # from enum WdColor
	wdColorAutomatic              =-16777216  # from enum WdColor
	wdColorBlack                  =0x0        # from enum WdColor
	wdColorBlue                   =0xff0000   # from enum WdColor
	wdColorBlueGray               =0x996666   # from enum WdColor
	wdColorBrightGreen            =0xff00     # from enum WdColor
	wdColorBrown                  =0x3399     # from enum WdColor
	wdColorDarkBlue               =0x800000   # from enum WdColor
	wdColorDarkGreen              =0x3300     # from enum WdColor
	wdColorDarkRed                =0x80       # from enum WdColor
	wdColorDarkTeal               =0x663300   # from enum WdColor
	wdColorDarkYellow             =0x8080     # from enum WdColor
	wdColorGold                   =0xccff     # from enum WdColor
	wdColorGray05                 =0xf3f3f3   # from enum WdColor
	wdColorGray10                 =0xe6e6e6   # from enum WdColor
	wdColorGray125                =0xe0e0e0   # from enum WdColor
	wdColorGray15                 =0xd9d9d9   # from enum WdColor
	wdColorGray20                 =0xcccccc   # from enum WdColor
	wdColorGray25                 =0xc0c0c0   # from enum WdColor
	wdColorGray30                 =0xb3b3b3   # from enum WdColor
	wdColorGray35                 =0xa6a6a6   # from enum WdColor
	wdColorGray375                =0xa0a0a0   # from enum WdColor
	wdColorGray40                 =0x999999   # from enum WdColor
	wdColorGray45                 =0x8c8c8c   # from enum WdColor
	wdColorGray50                 =0x808080   # from enum WdColor
	wdColorGray55                 =0x737373   # from enum WdColor
	wdColorGray60                 =0x666666   # from enum WdColor
	wdColorGray625                =0x606060   # from enum WdColor
	wdColorGray65                 =0x595959   # from enum WdColor
	wdColorGray70                 =0x4c4c4c   # from enum WdColor
	wdColorGray75                 =0x404040   # from enum WdColor
	wdColorGray80                 =0x333333   # from enum WdColor
	wdColorGray85                 =0x262626   # from enum WdColor
	wdColorGray875                =0x202020   # from enum WdColor
	wdColorGray90                 =0x191919   # from enum WdColor
	wdColorGray95                 =0xc0c0c    # from enum WdColor
	wdColorGreen                  =0x8000     # from enum WdColor
	wdColorIndigo                 =0x993333   # from enum WdColor
	wdColorLavender               =0xff99cc   # from enum WdColor
	wdColorLightBlue              =0xff6633   # from enum WdColor
	wdColorLightGreen             =0xccffcc   # from enum WdColor
	wdColorLightOrange            =0x99ff     # from enum WdColor
	wdColorLightTurquoise         =0xffffcc   # from enum WdColor
	wdColorLightYellow            =0x99ffff   # from enum WdColor
	wdColorLime                   =0xcc99     # from enum WdColor
	wdColorOliveGreen             =0x3333     # from enum WdColor
	wdColorOrange                 =0x66ff     # from enum WdColor
	wdColorPaleBlue               =0xffcc99   # from enum WdColor
	wdColorPink                   =0xff00ff   # from enum WdColor
	wdColorPlum                   =0x663399   # from enum WdColor
	wdColorRed                    =0xff       # from enum WdColor
	wdColorRose                   =0xcc99ff   # from enum WdColor
	wdColorSeaGreen               =0x669933   # from enum WdColor
	wdColorSkyBlue                =0xffcc00   # from enum WdColor
	wdColorTan                    =0x99ccff   # from enum WdColor
	wdColorTeal                   =0x808000   # from enum WdColor
	wdColorTurquoise              =0xffff00   # from enum WdColor
	wdColorViolet                 =0x800080   # from enum WdColor
	wdColorWhite                  =0xffffff   # from enum WdColor
	wdColorYellow                 =0xffff     # from enum WdColor


colorDict = {'a':wdColorAqua , 'auto':wdColorAutomatic , 'k':wdColorBlack , 'b':wdColorBlue , 
    'bg':wdColorBlueGray , 'gg':wdColorBrightGreen , 
    'brn':wdColorBrown , 'db':wdColorDarkBlue , 
    'dg':wdColorDarkGreen , 'dr':wdColorDarkRed , 
    'dt':wdColorDarkTeal , 'dy':wdColorDarkYellow , 
    'gold':wdColorGold , '05':wdColorGray05 , '10':wdColorGray10 , '125':wdColorGray125 , 
    '15':wdColorGray15 , '20':wdColorGray20 , '25':wdColorGray25 , '30':wdColorGray30 , 
    '35':wdColorGray35 , '375':wdColorGray375 , '40':wdColorGray40 , '45':wdColorGray45 , 
    '50':wdColorGray50 , '55':wdColorGray55 , '60':wdColorGray60 , '625':wdColorGray625 , 
    '65':wdColorGray65 , '70':wdColorGray70 , '75':wdColorGray75 , '80':wdColorGray80 , 
    '85':wdColorGray85 , '875':wdColorGray875 , '90':wdColorGray90 , '95':wdColorGray95 , 
    'g':wdColorGreen , 'i':wdColorIndigo , 'l':wdColorLavender , 'lb':wdColorLightBlue , 
    'lg':wdColorLightGreen , 'lo':wdColorLightOrange , 
    'lt':wdColorLightTurquoise , 'ly':wdColorLightYellow , 
    'lime':wdColorLime , 'olive':wdColorOliveGreen , 
    'o':wdColorOrange , 'pb':wdColorPaleBlue , 
    'p':wdColorPink , 'plum':wdColorPlum , 
    'r':wdColorRed , 'rose':wdColorRose , 'sea':wdColorSeaGreen , 
    'sky':wdColorSkyBlue , 'tan':wdColorTan , 't':wdColorTeal , 'q':wdColorTurquoise , 
    'v':wdColorViolet , 'w':wdColorWhite , 'y':wdColorYellow }


class WordWrap:
    """Wrapper around Word documents to make them easy to build.
    Has variables for the Applications, Document and Selection; 
    most methods add things at the end of the document"""
    def __init__(self, templatefile=None):
        self.wordApp = Dispatch('Word.Application')
        if templatefile == None:
            self.wordDoc = self.wordApp.Documents.Add()
        else:
            self.wordDoc = self.wordApp.Documents.Add( Template=templatefile)
        #set up the selection
        self.wordDoc.Range(0,0).Select()
        self.wordSel = self.wordApp.Selection
        #fetch the styles in the document - see below
        #self.getStyleDictionary()
        
    def show(self):
        # convenience when developing
        self.wordApp.Visible = 1  
        
    def showFastView(self):
        self.wordApp.Visible = 1  
        self.wordApp.Windows(1).View.Type = wdNormalView
        self.wordApp.Options.Pagination = False
        #self.wordApp.ScreenUpdating = False
        
    def setFastOptions(self):
        self.wordApp.Visible = 0
        self.wordApp.Windows(1).View.Type = wdNormalView
        self.wordApp.Options.Pagination = False
        self.wordApp.ScreenUpdating = False
        
    # Save and Print
    def saveAs(self, filename):
        self.wordDoc.SaveAs(filename)
        
    def Quit(self):
        self.wordApp.Quit()
        
    def abandonWord(self):
        #print "self.wordApp.DisplayAlerts",w.wordApp.DisplayAlerts
        wdDoNotSaveChanges            =0x0        # from enum WdSaveOptions
        self.wordApp.Quit(wdDoNotSaveChanges)
       
    def printout(self):
        self.wordDoc.PrintOut()
        
    def changeStartSelection(self, NChar=-1):
        '''changes selection by NChar characters at Start'''
        pbTextUnitCharacter = 1
        self.wordSel.MoveStart( pbTextUnitCharacter, NChar )        
        
    def changeEndSelection(self, NChar=-1):
        '''changes selection by NChar characters at End'''
        pbTextUnitCharacter = 1
        self.wordSel.MoveEnd( pbTextUnitCharacter, NChar )        
    
    # Move the selection to the end, and insert into selection
    def selectEnd(self):
        # ensures insertion point is at the end of the document
        self.wordSel.Collapse(0)
        # 0 is the constant wdCollapseEnd; don't want to depend
        # on makepy support.

    def addText(self, text):
        R = self.wordSel.InsertAfter(text)
        self.selectEnd()
        #return R

    def addSelectedText(self, text):
        R = self.wordSel.InsertBefore(text)
        #self.selectEnd()
        #return R

    '''
    Insert a paragraph in a named style
    Fast, versatile, and lets graphic designers set the styles in Word.
    >>> from win32com.client import constants
    >>> mySelection.Style = constants.wdStyleHeading1
    >>> 
    However,  (a) this is limited to the built-in styles, and 
    (b) won't work   without  MakePy.
    Our solution:  get a style list back at run time, and use it to add them by name:

    '''
    def getStyleList(self):
        # returns a dictionary of the styles in a document
        self.styles = []
        stylecount = self.wordDoc.Styles.Count
        for i in range(1, stylecount + 1):
            styleObject = self.wordDoc.Styles(i)
            self.styles.append(styleObject.NameLocal)

    def addStyledPara(self, text, stylename):
        if text[-1] <> '\n':
            text = text + '\n'
        self.wordSel.InsertAfter(text)
        self.wordSel.Style = stylename
    
    def addTable(self, tableList, styleid=None, Range=None, fullWidth=0):
        # Takes a 'list of lists' of data.
        # first we format the text.  You might want to preformat
        # numbers with the right decimal places etc. first.
        
        # replace last character in document if Range is empty
        if Range==None:
            Range = self.selectCharacter( -1 )
        
        textlines = []
        NRows = len( tableList )
        NCols = 1
        for row in tableList:
            if len(row)>NCols: 
                NCols = len(row)
        
        #Tbl = self.wordDoc.Tables.Add(Range=Range,
        #            NumRows=NRows, NumColumns=NCols) 
        if fullWidth:
            autofit = wdAutoFitWindow
        else:
            autofit = wdAutoFitContent
            
        try:  # Word 2007 bombs
            Tbl = self.wordDoc.Tables.Add( Range, NRows, NCols, wdWord9TableBehavior, autofit)
        except:
            Tbl = self.wordDoc.Tables.Add( Range, NRows, NCols)#, wdWord9TableBehavior, autofit)
                    
        #Tbl.AutoFitBehavior = wdAutoFitContent
        
        NR = 1
        for row in tableList:
            NC = 1
            for s in row:
                Tbl.Cell(NR, NC).Range.Text = str( s )
                NC += 1
            NR += 1
    
        #and format
        if styleid:
            Tbl.AutoFormat(Format=styleid)
            
        try:  # Word 2007 bombs
            Tbl.AllowPageBreaks = False
        except:
            pass
            
        return Tbl
    
    def createTableStyle(self, name='myStyle', font='Arial', 
        color='', bgcolor='',
        size=14, borders=1, bold=0, keepTogether=1):
            
        styl = self.wordDoc.Styles.Add(Name=name, Type=wdStyleTypeTable)
        styl.Font.Name = font
        styl.Font.Size = size
        
        if keepTogether:
            styl.ParagraphFormat.KeepWithNext = True
            styl.ParagraphFormat.KeepTogether = True
        
        if bold:
            styl.Font.Bold = True
        else:
            styl.Font.Bold = False
            
        if len(bgcolor)>0:
            try:
                styl.Table.Shading.BackgroundPatternColor = colorDict[bgcolor]
            except:
                pass
            
        if len(color)>0:
            try:
                #styl.Font.ColorIndex = textColorIndexDict[color]
                styl.Font.Color = colorDict[color]
            except:
                pass

        if borders:
            styl.Table.Borders.Enable = True
        else:
            styl.Table.Borders.Enable = False
            styl.Table.Borders.InsideLineStyle = wdLineStyleNone
            styl.Table.Borders.OutsideLineStyle = wdLineStyleNone
            styl.Table.Borders(wdBorderBottom).LineStyle = wdLineStyleNone
            styl.Table.Borders(wdBorderLeft).LineStyle = wdLineStyleNone
            styl.Table.Borders(wdBorderRight).LineStyle = wdLineStyleNone
            styl.Table.Borders(wdBorderTop).LineStyle = wdLineStyleNone
            styl.Table.Borders(wdBorderHorizontal).LineStyle = wdLineStyleNone
            styl.Table.Borders(wdBorderVertical).LineStyle = wdLineStyleNone
            
        return styl

    
    def addCellText(self, Table=None, row=1, col=1, text=''):
        if Table==None:
            return
            
        Table.Cell(row, col).Range.Text = str( text )
    
    def setAllTableCellStyle(self, Table=None, StyleName=None):
        if Table==None or StyleName==None:
            return
            
        for i in range(1, Table.Rows.Count+1):
            for j in range(1, Table.Columns.Count+1):
                try:
                    Table.Cell(i,j).Range.Style = StyleName
                except:
                    pass
    
    def setCellStyle(self, Table=None, row=1, col=1, text='',
        StyleName='', fontName='', fontSize=0, just='', bold=None,
        color='', bgcolor='', width=0):
        if Table==None:
            return
            
        if row<1: row=1
        if row>Table.Rows.Count: row=Table.Rows.Count
        if col<1: col=1
        if col>Table.Columns.Count: col=Table.Columns.Count
            
        if len(text)>0:
            try:
                Table.Cell(row, col).Range.Text = str( text )
            except:
                pass
            
        if len(StyleName)>0:
            try:
                Table.Cell(row,col).Range.Style = StyleName
            except:
                pass
                
        if len(fontName)>0:
            try:
                Table.Cell(row,col).Range.Font.Name = fontName
            except:
                pass
                
        if fontSize>0:
            try:
                Table.Cell(row,col).Range.Font.Size = fontSize
            except:
                pass
                
        if len(just)>0:
            try:
                Table.Cell(row,col).Range.ParagraphFormat.Alignment = justDict[just]
            except:
                pass
                
        if bold != None:
            try:
                Table.Cell(row,col).Range.Font.Bold = bold
            except:
                pass
                
        if len(color)>0:
            try:
                Table.Cell(row,col).Range.Font.Color = colorDict[color]
            except:
                pass
                
        if len(bgcolor)>0:
            try:
                Table.Cell(row,col).Range.Shading.BackgroundPatternColor = colorDict[bgcolor]
            except:
                pass
                
        if width>0:
            try:
                Table.Cell(row,col).Width=width
            except:
                pass

    def mergeRow(self, Table=None, NRow=1):
        if Table==None:
            return
            
        myrow = Table.Rows(NRow)
        myrow.Cells.Merge()

    '''Adding Charts and Images
    Let's assume we've set up and saved an 
    Excel sheet with the right chart in it already.
    '''
    def  addInlineExcelChart(self, filename, caption='', 
                     height=216, width=432):
        # adds a chart inline within the text, caption below.
        # add an InlineShape to the InlineShapes collection 
        #- could appear anywhere
        shape = self.wordDoc.InlineShapes.AddOLEObject(
            ClassType='Excel.Chart',
            FileName=filename
            )
        # set height and width in points
        shape.Height = height
        shape.Width = width
            
        # put it where we want
        shape.Range.Cut()
        self.wordSel.InsertAfter('chart will replace this')
        self.wordSel.Range.Paste()  # goes in selection
        self.addStyledPara(caption, 'Normal')
    
    def addImage(self, filename, Range=None, fracPage=0.5):
        # without a range, the picture is added at the top
        hw=self.wordDoc.InlineShapes
        if Range==None:
            Image = hw.AddPicture(filename)
        else:
            # AddPicture(FileName, LinkToFile, SaveWithDocument, Range)
            print "Range provided for image add"
            Image = hw.AddPicture(filename, False, True, Range)
            
        PageW = self.wordDoc.PageSetup.PageWidth
        desiredW = int( fracPage * PageW )
        if Image.Width > desiredW:
            ratio = float( desiredW ) / Image.Width
            Image.Width = int( ratio * Image.Width )
            Image.Height = int( ratio * Image.Height )
            
        return Image
        
    def selectParagraph(self, N=1):
        # can also use negative numbers like python indexing
        Ps = self.wordDoc.Paragraphs
        if N<0:
            N = Ps.Count + N + 1
            if N<1: N=1
        if N>Ps.Count: N = Ps.Count
            
        RN = Ps(N).Range
        RN.Select()
        return RN
        
    def selectSentence(self, N=1):
        # can also use negative numbers like python indexing
        Ss = self.wordDoc.Sentences
        if N<0:
            N = Ss.Count + N + 1
            if N<1: N=1
        if N>Ss.Count: N = Ss.Count
            
        RN = self.wordDoc.Range( Ss(N).Start, Ss(N).End)
        RN.Select()
        return RN
        
    def selectWord(self, N=1):
        # can also use negative numbers like python indexing
        Ws = self.wordDoc.Words
        if N<0:
            N = Ws.Count + N + 1
            if N<1: N=1
        if N>Ws.Count: N = Ws.Count
            
        RN = self.wordDoc.Range( Ws(N).Start, Ws(N).End)
        RN.Select()
        return RN
        
    def selectCharacter(self, N=1):
        Cs = self.wordDoc.Characters
        if N<0:
            N = Cs.Count + N + 1
            if N<1: N=1
        if N>Cs.Count: N = Cs.Count
            
        RN = self.wordDoc.Range( Cs(N).Start, Cs(N).End)
        RN.Select()
        return RN

if __name__ == "__main__": #Self Test
    
    w = WordWrap()
    w.show()
    
#    w.addText('Line 1\n\n')
#    w.addText('Line 2\n\n')
#    w.addText('Line 3\n\n')
#    w.addText('Line 4\n\n')
    
    from Summary import Summary
    S = Summary( summaryTitle='Summary Title', subTitle='subtitle')
    S.addAssumption( 'Assume this is a test' )
    
    S.addInput( label='Solar Flux', value=1.0, units='BTU/sqin', format='%g')
    S.addOutput(label='Tea Temperature', value=100.0, units='C', format='%g')
    
    summ = S
    sel = w.selectCharacter(1)
    
    w.changeEndSelection( -1 )
    
    #T1 = w.wordApp.Selection.ConvertToTable()
    
    #w.wordDoc.Styles("Endnote Reference").Font.Size = 10
    #w.wordDoc.Styles("Endnote Reference").Font.Name = "Courier New"
    #w.setAllTableCellStyle( Table=T1, StyleName="Endnote Reference")
    #T1.AutoFormat( Format=1 )
    
    #sel = w.selectCharacter(-1)
    #x = raw_input("hit return to continue:")
    
    #ps = u'Caption'
    #w.addStyledPara( 'Now is not the time for any good men to come to the aid of their country.', ps)
    
    #w.selectEnd()
    
    tableStr = [('',),('',),('',),('','')]
    wordTable1 = w.addTable( tableStr )
    w.mergeRow( Table=wordTable1, NRow=1)
    w.mergeRow( Table=wordTable1, NRow=2)
    
    w.addCellText(wordTable1, row=2, col=1, text='\n'.join(summ.getSummTopLines()))
    w.addCellText(wordTable1, row=3, col=1, text='\n'.join(summ.getSummAssumptions()))

    w.addCellText(wordTable1, row=4, col=1, text='\n'.join(summ.getSummInputs()))
    w.addCellText(wordTable1, row=4, col=2, text='\n'.join(summ.getSummOutputs()))
    
    # now format the table
    w.wordDoc.Styles("Endnote Reference").Font.Size = 14
    w.wordDoc.Styles("Endnote Reference").Font.Name = "Courier New"
    w.setAllTableCellStyle( Table=wordTable1, StyleName="Endnote Reference")
    wordTable1.AutoFormat( Format=1 )

    #w.addImage("C:\\python27\\temp\\pyTest.png", Range=wordTable1.Cell(1,1).Range, fracPage=0.4)
    #w.selectEnd()
    #wordTable1.AutoFormat( Format=1 )
    '''Dim MyPic As Shape 'or InlineShape

Set MyPic = ActiveDocument.InlineShapes.AddPicture(strPathToPicture)

With MyPic
.RelativeVerticalPosition = wdRelativeVerticalPositionPage
.Left = CentimetersToPoints(0)
.Top = wdShapeBottom
End With'''
    if 0:
        w.getStyleList()
        print w.styles
        
        keyInp = raw_input(" Hit Key to Close Word")
        w.abandonWord()