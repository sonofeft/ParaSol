from win32com.client import Dispatch

msoTextOrientationHorizontal  =0x1 # from google

msoAlignBottoms               =0x5        # from enum MsoAlignCmd
msoAlignCenters               =0x1        # from enum MsoAlignCmd
msoAlignLefts                 =0x0        # from enum MsoAlignCmd
msoAlignMiddles               =0x4        # from enum MsoAlignCmd
msoAlignRights                =0x2        # from enum MsoAlignCmd
msoAlignTops                  =0x3        # from enum MsoAlignCmd

msoAnchorBottom               =0x4        # from enum MsoVerticalAnchor
msoAnchorBottomBaseLine       =0x5        # from enum MsoVerticalAnchor
msoAnchorMiddle               =0x3        # from enum MsoVerticalAnchor
msoAnchorTop                  =0x1        # from enum MsoVerticalAnchor
msoAnchorTopBaseline          =0x2        # from enum MsoVerticalAnchor
msoVerticalAnchorMixed        =-2         # from enum MsoVerticalAnchor

msoAnchorCenter               =0x2        # from enum MsoHorizontalAnchor
msoAnchorNone                 =0x1        # from enum MsoHorizontalAnchor
msoHorizontalAnchorMixed      =-2         # from enum MsoHorizontalAnchor

msoLineDash                   =0x4        # from enum MsoLineDashStyle
msoLineDashDot                =0x5        # from enum MsoLineDashStyle
msoLineDashDotDot             =0x6        # from enum MsoLineDashStyle
msoLineDashStyleMixed         =-2         # from enum MsoLineDashStyle
msoLineLongDash               =0x7        # from enum MsoLineDashStyle
msoLineLongDashDot            =0x8        # from enum MsoLineDashStyle
msoLineRoundDot               =0x3        # from enum MsoLineDashStyle
msoLineSolid                  =0x1        # from enum MsoLineDashStyle
msoLineSquareDot              =0x2        # from enum MsoLineDashStyle
msoLineSingle                 =0x1        # from enum MsoLineStyle
msoLineStyleMixed             =-2         # from enum MsoLineStyle
msoLineThickBetweenThin       =0x5        # from enum MsoLineStyle
msoLineThickThin              =0x4        # from enum MsoLineStyle
msoLineThinThick              =0x3        # from enum MsoLineStyle
msoLineThinThin               =0x2        # from enum MsoLineStyle


msoArrowheadLengthMedium      =0x2        # from enum MsoArrowheadLength
msoArrowheadLengthMixed       =-2         # from enum MsoArrowheadLength
msoArrowheadLong              =0x3        # from enum MsoArrowheadLength
msoArrowheadShort             =0x1        # from enum MsoArrowheadLength
msoArrowheadDiamond           =0x5        # from enum MsoArrowheadStyle
msoArrowheadNone              =0x1        # from enum MsoArrowheadStyle
msoArrowheadOpen              =0x3        # from enum MsoArrowheadStyle
msoArrowheadOval              =0x6        # from enum MsoArrowheadStyle
msoArrowheadStealth           =0x4        # from enum MsoArrowheadStyle
msoArrowheadStyleMixed        =-2         # from enum MsoArrowheadStyle
msoArrowheadTriangle          =0x2        # from enum MsoArrowheadStyle
msoArrowheadNarrow            =0x1        # from enum MsoArrowheadWidth
msoArrowheadWide              =0x3        # from enum MsoArrowheadWidth
msoArrowheadWidthMedium       =0x2        # from enum MsoArrowheadWidth
msoArrowheadWidthMixed        =-2         # from enum MsoArrowheadWidth

msoShapeActionButtonBackorPrevious=0x81       # from enum MsoAutoShapeType
msoShapeActionButtonBeginning =0x83       # from enum MsoAutoShapeType
msoShapeActionButtonCustom    =0x7d       # from enum MsoAutoShapeType
msoShapeActionButtonDocument  =0x86       # from enum MsoAutoShapeType
msoShapeActionButtonEnd       =0x84       # from enum MsoAutoShapeType
msoShapeActionButtonForwardorNext=0x82       # from enum MsoAutoShapeType
msoShapeActionButtonHelp      =0x7f       # from enum MsoAutoShapeType
msoShapeActionButtonHome      =0x7e       # from enum MsoAutoShapeType
msoShapeActionButtonInformation=0x80       # from enum MsoAutoShapeType
msoShapeActionButtonMovie     =0x88       # from enum MsoAutoShapeType
msoShapeActionButtonReturn    =0x85       # from enum MsoAutoShapeType
msoShapeActionButtonSound     =0x87       # from enum MsoAutoShapeType
msoShapeArc                   =0x19       # from enum MsoAutoShapeType
msoShapeBalloon               =0x89       # from enum MsoAutoShapeType
msoShapeBentArrow             =0x29       # from enum MsoAutoShapeType
msoShapeBentUpArrow           =0x2c       # from enum MsoAutoShapeType
msoShapeBevel                 =0xf        # from enum MsoAutoShapeType
msoShapeBlockArc              =0x14       # from enum MsoAutoShapeType
msoShapeCan                   =0xd        # from enum MsoAutoShapeType
msoShapeChevron               =0x34       # from enum MsoAutoShapeType
msoShapeCircularArrow         =0x3c       # from enum MsoAutoShapeType
msoShapeCloudCallout          =0x6c       # from enum MsoAutoShapeType
msoShapeCross                 =0xb        # from enum MsoAutoShapeType
msoShapeCube                  =0xe        # from enum MsoAutoShapeType
msoShapeCurvedDownArrow       =0x30       # from enum MsoAutoShapeType
msoShapeCurvedDownRibbon      =0x64       # from enum MsoAutoShapeType
msoShapeCurvedLeftArrow       =0x2e       # from enum MsoAutoShapeType
msoShapeCurvedRightArrow      =0x2d       # from enum MsoAutoShapeType
msoShapeCurvedUpArrow         =0x2f       # from enum MsoAutoShapeType
msoShapeCurvedUpRibbon        =0x63       # from enum MsoAutoShapeType
msoShapeDiamond               =0x4        # from enum MsoAutoShapeType
msoShapeDonut                 =0x12       # from enum MsoAutoShapeType
msoShapeDoubleBrace           =0x1b       # from enum MsoAutoShapeType
msoShapeDoubleBracket         =0x1a       # from enum MsoAutoShapeType
msoShapeDoubleWave            =0x68       # from enum MsoAutoShapeType
msoShapeDownArrow             =0x24       # from enum MsoAutoShapeType
msoShapeDownArrowCallout      =0x38       # from enum MsoAutoShapeType
msoShapeDownRibbon            =0x62       # from enum MsoAutoShapeType
msoShapeExplosion1            =0x59       # from enum MsoAutoShapeType
msoShapeExplosion2            =0x5a       # from enum MsoAutoShapeType
msoShapeFlowchartAlternateProcess=0x3e       # from enum MsoAutoShapeType
msoShapeFlowchartCard         =0x4b       # from enum MsoAutoShapeType
msoShapeFlowchartCollate      =0x4f       # from enum MsoAutoShapeType
msoShapeFlowchartConnector    =0x49       # from enum MsoAutoShapeType
msoShapeFlowchartData         =0x40       # from enum MsoAutoShapeType
msoShapeFlowchartDecision     =0x3f       # from enum MsoAutoShapeType
msoShapeFlowchartDelay        =0x54       # from enum MsoAutoShapeType
msoShapeFlowchartDirectAccessStorage=0x57       # from enum MsoAutoShapeType
msoShapeFlowchartDisplay      =0x58       # from enum MsoAutoShapeType
msoShapeFlowchartDocument     =0x43       # from enum MsoAutoShapeType
msoShapeFlowchartExtract      =0x51       # from enum MsoAutoShapeType
msoShapeFlowchartInternalStorage=0x42       # from enum MsoAutoShapeType
msoShapeFlowchartMagneticDisk =0x56       # from enum MsoAutoShapeType
msoShapeFlowchartManualInput  =0x47       # from enum MsoAutoShapeType
msoShapeFlowchartManualOperation=0x48       # from enum MsoAutoShapeType
msoShapeFlowchartMerge        =0x52       # from enum MsoAutoShapeType
msoShapeFlowchartMultidocument=0x44       # from enum MsoAutoShapeType
msoShapeFlowchartOffpageConnector=0x4a       # from enum MsoAutoShapeType
msoShapeFlowchartOr           =0x4e       # from enum MsoAutoShapeType
msoShapeFlowchartPredefinedProcess=0x41       # from enum MsoAutoShapeType
msoShapeFlowchartPreparation  =0x46       # from enum MsoAutoShapeType
msoShapeFlowchartProcess      =0x3d       # from enum MsoAutoShapeType
msoShapeFlowchartPunchedTape  =0x4c       # from enum MsoAutoShapeType
msoShapeFlowchartSequentialAccessStorage=0x55       # from enum MsoAutoShapeType
msoShapeFlowchartSort         =0x50       # from enum MsoAutoShapeType
msoShapeFlowchartStoredData   =0x53       # from enum MsoAutoShapeType
msoShapeFlowchartSummingJunction=0x4d       # from enum MsoAutoShapeType
msoShapeFlowchartTerminator   =0x45       # from enum MsoAutoShapeType
msoShapeFoldedCorner          =0x10       # from enum MsoAutoShapeType
msoShapeHeart                 =0x15       # from enum MsoAutoShapeType
msoShapeHexagon               =0xa        # from enum MsoAutoShapeType
msoShapeHorizontalScroll      =0x66       # from enum MsoAutoShapeType
msoShapeIsoscelesTriangle     =0x7        # from enum MsoAutoShapeType
msoShapeLeftArrow             =0x22       # from enum MsoAutoShapeType
msoShapeLeftArrowCallout      =0x36       # from enum MsoAutoShapeType
msoShapeLeftBrace             =0x1f       # from enum MsoAutoShapeType
msoShapeLeftBracket           =0x1d       # from enum MsoAutoShapeType
msoShapeLeftRightArrow        =0x25       # from enum MsoAutoShapeType
msoShapeLeftRightArrowCallout =0x39       # from enum MsoAutoShapeType
msoShapeLeftRightUpArrow      =0x28       # from enum MsoAutoShapeType
msoShapeLeftUpArrow           =0x2b       # from enum MsoAutoShapeType
msoShapeLightningBolt         =0x16       # from enum MsoAutoShapeType
msoShapeLineCallout1          =0x6d       # from enum MsoAutoShapeType
msoShapeLineCallout1AccentBar =0x71       # from enum MsoAutoShapeType
msoShapeLineCallout1BorderandAccentBar=0x79       # from enum MsoAutoShapeType
msoShapeLineCallout1NoBorder  =0x75       # from enum MsoAutoShapeType
msoShapeLineCallout2          =0x6e       # from enum MsoAutoShapeType
msoShapeLineCallout2AccentBar =0x72       # from enum MsoAutoShapeType
msoShapeLineCallout2BorderandAccentBar=0x7a       # from enum MsoAutoShapeType
msoShapeLineCallout2NoBorder  =0x76       # from enum MsoAutoShapeType
msoShapeLineCallout3          =0x6f       # from enum MsoAutoShapeType
msoShapeLineCallout3AccentBar =0x73       # from enum MsoAutoShapeType
msoShapeLineCallout3BorderandAccentBar=0x7b       # from enum MsoAutoShapeType
msoShapeLineCallout3NoBorder  =0x77       # from enum MsoAutoShapeType
msoShapeLineCallout4          =0x70       # from enum MsoAutoShapeType
msoShapeLineCallout4AccentBar =0x74       # from enum MsoAutoShapeType
msoShapeLineCallout4BorderandAccentBar=0x7c       # from enum MsoAutoShapeType
msoShapeLineCallout4NoBorder  =0x78       # from enum MsoAutoShapeType
msoShapeMixed                 =-2         # from enum MsoAutoShapeType
msoShapeMoon                  =0x18       # from enum MsoAutoShapeType
msoShapeNoSymbol              =0x13       # from enum MsoAutoShapeType
msoShapeNotPrimitive          =0x8a       # from enum MsoAutoShapeType
msoShapeNotchedRightArrow     =0x32       # from enum MsoAutoShapeType
msoShapeOctagon               =0x6        # from enum MsoAutoShapeType
msoShapeOval                  =0x9        # from enum MsoAutoShapeType
msoShapeOvalCallout           =0x6b       # from enum MsoAutoShapeType
msoShapeParallelogram         =0x2        # from enum MsoAutoShapeType
msoShapePentagon              =0x33       # from enum MsoAutoShapeType
msoShapePlaque                =0x1c       # from enum MsoAutoShapeType
msoShapeQuadArrow             =0x27       # from enum MsoAutoShapeType
msoShapeQuadArrowCallout      =0x3b       # from enum MsoAutoShapeType
msoShapeRectangle             =0x1        # from enum MsoAutoShapeType
msoShapeRectangularCallout    =0x69       # from enum MsoAutoShapeType
msoShapeRegularPentagon       =0xc        # from enum MsoAutoShapeType
msoShapeRightArrow            =0x21       # from enum MsoAutoShapeType
msoShapeRightArrowCallout     =0x35       # from enum MsoAutoShapeType
msoShapeRightBrace            =0x20       # from enum MsoAutoShapeType
msoShapeRightBracket          =0x1e       # from enum MsoAutoShapeType
msoShapeRightTriangle         =0x8        # from enum MsoAutoShapeType
msoShapeRoundedRectangle      =0x5        # from enum MsoAutoShapeType
msoShapeRoundedRectangularCallout=0x6a       # from enum MsoAutoShapeType
msoShapeSmileyFace            =0x11       # from enum MsoAutoShapeType
msoShapeStripedRightArrow     =0x31       # from enum MsoAutoShapeType
msoShapeSun                   =0x17       # from enum MsoAutoShapeType
msoShapeTrapezoid             =0x3        # from enum MsoAutoShapeType
msoShapeUTurnArrow            =0x2a       # from enum MsoAutoShapeType
msoShapeUpArrow               =0x23       # from enum MsoAutoShapeType
msoShapeUpArrowCallout        =0x37       # from enum MsoAutoShapeType
msoShapeUpDownArrow           =0x26       # from enum MsoAutoShapeType
msoShapeUpDownArrowCallout    =0x3a       # from enum MsoAutoShapeType
msoShapeUpRibbon              =0x61       # from enum MsoAutoShapeType
msoShapeVerticalScroll        =0x65       # from enum MsoAutoShapeType
msoShapeWave                  =0x67       # from enum MsoAutoShapeType


ppBulletNone                  =0x0        # from enum PpBulletType

ppLayoutBlank                 =0xc        # from enum PpSlideLayout
ppLayoutChart                 =0x8        # from enum PpSlideLayout
ppLayoutChartAndText          =0x6        # from enum PpSlideLayout
ppLayoutClipArtAndVerticalText=0x1a       # from enum PpSlideLayout
ppLayoutClipartAndText        =0xa        # from enum PpSlideLayout
ppLayoutFourObjects           =0x18       # from enum PpSlideLayout
ppLayoutLargeObject           =0xf        # from enum PpSlideLayout
ppLayoutMediaClipAndText      =0x12       # from enum PpSlideLayout
ppLayoutMixed                 =-2         # from enum PpSlideLayout
ppLayoutObject                =0x10       # from enum PpSlideLayout
ppLayoutObjectAndText         =0xe        # from enum PpSlideLayout
ppLayoutObjectAndTwoObjects   =0x1e       # from enum PpSlideLayout
ppLayoutObjectOverText        =0x13       # from enum PpSlideLayout
ppLayoutOrgchart              =0x7        # from enum PpSlideLayout
ppLayoutTable                 =0x4        # from enum PpSlideLayout
ppLayoutText                  =0x2        # from enum PpSlideLayout
ppLayoutTextAndChart          =0x5        # from enum PpSlideLayout
ppLayoutTextAndClipart        =0x9        # from enum PpSlideLayout
ppLayoutTextAndMediaClip      =0x11       # from enum PpSlideLayout
ppLayoutTextAndObject         =0xd        # from enum PpSlideLayout
ppLayoutTextAndTwoObjects     =0x15       # from enum PpSlideLayout
ppLayoutTextOverObject        =0x14       # from enum PpSlideLayout
ppLayoutTitle                 =0x1        # from enum PpSlideLayout
ppLayoutTitleOnly             =0xb        # from enum PpSlideLayout
ppLayoutTwoColumnText         =0x3        # from enum PpSlideLayout
ppLayoutTwoObjects            =0x1d       # from enum PpSlideLayout
ppLayoutTwoObjectsAndObject   =0x1f       # from enum PpSlideLayout
ppLayoutTwoObjectsAndText     =0x16       # from enum PpSlideLayout
ppLayoutTwoObjectsOverText    =0x17       # from enum PpSlideLayout
ppLayoutVerticalText          =0x19       # from enum PpSlideLayout
ppLayoutVerticalTitleAndText  =0x1b       # from enum PpSlideLayout
ppLayoutVerticalTitleAndTextOverChart=0x1c       # from enum PpSlideLayout

msoFalse                      =0x0        # from enum MsoTriState
msoTrue                       =-1         # from enum MsoTriState
ppAutoSizeShapeToFitText      = 1         # copied from web site http://fox.wikis.com/wc.dll?Wiki~PowerpointConstants


ppAlignCenter                 =0x2        # from enum PpParagraphAlignment
ppAlignDistribute             =0x5        # from enum PpParagraphAlignment
ppAlignJustify                =0x4        # from enum PpParagraphAlignment
ppAlignJustifyLow             =0x7        # from enum PpParagraphAlignment
ppAlignLeft                   =0x1        # from enum PpParagraphAlignment
ppAlignRight                  =0x3        # from enum PpParagraphAlignment
ppAlignThaiDistribute         =0x6        # from enum PpParagraphAlignment
ppAlignmentMixed              =-2         # from enum PpParagraphAlignment

    
def RGB(r,g,b):
    return r + g*256 + b*65536


class PPTwrap(object):
    
    def __init__(self, templatefile=None):
        
        self.PPTapp = Dispatch('Powerpoint.Application')
        if templatefile == None:
            self.ppt = self.PPTapp.Presentations.Add(1) # not visible
        else:
            self.ppt = self.PPTapp.Presentations.Open(\
                FileName=templatefile, Untitled=msoTrue)
        self.w = self.ppt.PageSetup.SlideWidth
        self.h = self.ppt.PageSetup.SlideHeight
        
        self.index = 0 # slide index
        self.slideL = []

        
    def show(self):
        # convenience when developing
        self.PPTapp.Visible = 1  
    
    def addTableSlide(self, text='my text', title='my title'):
        self.index += 1
        Slide = self.ppt.Slides.Add(Index=self.index, 
            Layout=ppLayoutTable)
        if self.PPTapp.Visible:
            Slide.Select()

        Slide.Shapes.Placeholders(1).TextFrame.TextRange.Text = title
        Font = Slide.Shapes.Placeholders(1).TextFrame.TextRange.Font
        #Font.Name = 'Courier'
        Font.Size = '32'
        
        self.slideL.append( Slide )
        
    
    
    def addTextSlide(self, text='my text', title='my title',
        textFont='', textFontSize=None, center=1, wrap=0, 
        noBullets=0, makeItFit=1):
            
        self.index += 1
        Slide = self.ppt.Slides.Add(Index=self.index, 
            Layout=ppLayoutText)
        if self.PPTapp.Visible:
            Slide.Select()
            
        self.slideL.append( Slide )

        Slide.Shapes.Placeholders(1).TextFrame.TextRange.Text = title
        Font = Slide.Shapes.Placeholders(1).TextFrame.TextRange.Font
        #Font.Name = 'Courier New'
        Font.Size = '32'
        
        textObj = Slide.Shapes.Placeholders(2)
        textRng = Slide.Shapes.Placeholders(2).TextFrame.TextRange
        FontTxt = textRng.Font
        textFrame = Slide.Shapes.Placeholders(2).TextFrame
        
        
        if noBullets:
            textRng.ParagraphFormat.Bullet.Type = ppBulletNone
        
        if textFont:
            FontTxt.Name = textFont
            
        if textFontSize != None:
            if int(textFontSize)>=8:
                FontTxt.Size = str(textFontSize)
            
        #if center:
        #    #pass
        #    textObj.Width = textRng.BoundWidth
        #    textObj.Left = max(1, (self.w-textObj.Width)/2)
            
        
        textRng.Text = text
        #textObj.Width = textRng.BoundWidth
        #textObj.Height = textRng.BoundHeight
        
        if makeItFit:
            
            fontSize = int(FontTxt.Size)
            w = textObj.Width
            h = textObj.Height
            titleObj = Slide.Shapes.Placeholders(1)
            htit = titleObj.Top + titleObj.Height
            print("w=",w,"window w=",self.w)
            print("h=",h,"window h=",self.h)
            if (w>self.w-40 or h>self.h-htit) and fontSize>8:
                fontSize = fontSize - 2
                FontTxt.Size = str(fontSize)
                textObj.Width = textRng.BoundWidth
                textObj.Height = textRng.BoundHeight
                print("reduced PowerPoint Font to",fontSize)
                w = textObj.Width
                h = textObj.Height
                print("new width=",w,"new height=",h)
                
        if not wrap:
            textFrame.WordWrap = msoFalse
        if center:
            textFrame.VerticalAnchor = msoAnchorMiddle
            textFrame.HorizontalAnchor = msoAnchorCenter
            
    def addImageSlide(self, imgFile='', title='picture'):
        if len(imgFile)<5:
            return
            
        self.index += 1
        Slide = self.ppt.Slides.Add(Index=self.index, 
            Layout=ppLayoutTitleOnly)
            
        self.slideL.append( Slide )
        
        if self.PPTapp.Visible:
            Slide.Select()
        #Slide.Shapes.Placeholders(1).Top = 50
        #Slide.Shapes.Placeholders(1).Height = 20
        #Slide.Shapes.Placeholders(1).Width = self.w - 20

        Slide.Shapes.Placeholders(1).TextFrame.TextRange.Text = title
        Font = Slide.Shapes.Placeholders(1).TextFrame.TextRange.Font
        #Font.Name = 'Courier'
        Font.Size = '32'
        
        Picture = Slide.Shapes.AddPicture(imgFile, LinkToFile=False, 
            SaveWithDocument=True, 
            Left=10, Top=12, Width=-1.0, Height=-1.0)
        #Picture.Select()
        
        tp = Slide.Shapes.Placeholders(1).Top + \
            Slide.Shapes.Placeholders(1).Height
        hp = Picture.Height
        wp = Picture.Width
        
        #Picture.Top = tp + max(0, (self.h-100-hp)/2)
        Picture.Top = tp + 10
        Picture.Left = max(1, (self.w-wp)/2)
        
    # Save 
    def saveAs(self, filename):
        self.ppt.Saved = False
        self.ppt.SaveAs(filename)
    
    def abandon(self):
        self.ppt.Saved = True
    
    def Quit(self):
        self.PPTapp.Quit()

    def addDrawingSlide(self, title='Make A Drawing'):
        self.index += 1
        Slide = self.ppt.Slides.Add(Index=self.index, 
            Layout=ppLayoutTitleOnly)
        if self.PPTapp.Visible:
            Slide.Select()

        Slide.Shapes.Placeholders(1).TextFrame.TextRange.Text = title
        Font = Slide.Shapes.Placeholders(1).TextFrame.TextRange.Font
        #Font.Name = 'Courier'
        Font.Size = '32'
        
        self.slideL.append( Slide )
    
    def drawRectangle(self, left=100, top=100, width=200, height=50, 
        colorIndex=1, rgb=None, rgbText=None, transparency=0.0, text=None, 
        font_size=0, font_name="", bold=0 ):
            
        '''Estimate at 72 points per inch, 10 inches wide, 7.5 inches high'''
        
        Slide = self.slideL[-1]
        rect = Slide.Shapes.AddShape( msoShapeRectangle, left, top, width, height )
        
        if rgb:
            rect.Fill.ForeColor.RGB = rgb
        else:
            rect.Fill.ForeColor.SchemeColor = colorIndex
        
        if text:
            rect.TextFrame.TextRange.Text = text
        
        rect.Fill.Transparency = transparency
        rect.Line.Transparency = transparency
        
        if rgbText:
            rect.TextFrame.TextRange.Font.Color.RGB = rgbText
        else:
            rect.TextFrame.TextRange.Font.Color.RGB = RGB(0,0,0)
        
        if font_size:
            rect.TextFrame.TextRange.Font.Size = font_size
        
        if bold:
            rect.TextFrame.TextRange.Font.Bold = msoTrue
        
        if font_name:
            rect.TextFrame.TextRange.Font.Name = font_name
        
        #arrow = Slide.Shapes.AddShape(msoShapeLeftArrow, left, top, 50, 50)

    def drawLine(self, xBeg=100, yBeg=100, xEnd=200, yEnd=50, 
        rgb=None, transparency=0.0, weight=0, begStyle=0, endStyle=0 ):
        '''Estimate at 72 points per inch, 10 inches wide, 7.5 inches high'''
        
        Slide = self.slideL[-1]

        line =  Slide.Shapes.AddLine(xBeg, yBeg, xEnd, yEnd)
        
        if begStyle==1:
            line.Line.BeginArrowheadStyle = msoArrowheadTriangle
        elif begStyle==2:
            line.Line.BeginArrowheadStyle = msoArrowheadOval
            
        if endStyle==1:
            line.Line.EndArrowheadStyle = msoArrowheadTriangle
        elif endStyle==2:
            line.Line.EndArrowheadStyle = msoArrowheadOval
        
        if rgb != None:
            line.Line.ForeColor.RGB = rgb
        
        if weight:
            line.Line.Weight = weight
        
        #line.Line.DashStyle = msoLineDashDotDot
        
        line.Line.Transparency = transparency
    
    def addTextBox(self,left=400, top=300, width=200, height=50, 
        text='Testing 123', font_size=0, font_name="", bold=1,
        fillrgb=RGB(255, 255, 0)):

        Slide = self.slideL[-1]
        
        newTextbox = Slide.Shapes.AddTextbox(msoTextOrientationHorizontal,
            left, top,  width, height )
        
        newTextbox.TextFrame.TextRange = str( text )
        
        newTextbox.TextFrame.AutoSize = ppAutoSizeShapeToFitText
        newTextbox.TextFrame.WordWrap = msoFalse
        newTextbox.Line.Visible = msoTrue

        newTextbox.Fill.Visible = msoTrue
        newTextbox.Fill.Solid
        if fillrgb:
            newTextbox.Fill.ForeColor.RGB = fillrgb
        newTextbox.Fill.Transparency = 0#
        
        
        if font_size:
            newTextbox.TextFrame.TextRange.Font.Size = font_size
        
        if bold:
            newTextbox.TextFrame.TextRange.Font.Bold = msoTrue
        
        if font_name:
            newTextbox.TextFrame.TextRange.Font.Name = font_name

'''With ActivePresentation.Slides _
(ActiveWindow.Selection.SlideRange(1).SlideIndex) _
.Shapes.AddTextbox _
(Orientation:=msoTextOrientationHorizontal, _
Left:=-16.375, Top:=120.75, _
Width:=240, Height:=60.5)

'Add tag
.Tags.Add "Type", "EditorComment"

' fill parameters
.Fill.Visible = msoTrue
.Fill.Solid
.Fill.ForeColor.RGB = RGB(255, 255, 0)
.Fill.Transparency = 0#

' line parameters
.Line.Weight = 2#
.Line.Visible = msoTrue
.Line.ForeColor.RGB = RGB(255, 0, 0)
.Line.BackColor.RGB = RGB(255, 255, 255)
'''        
        

if __name__ == "__main__": #Self Test
    import os
    here = os.path.abspath(os.path.dirname(__file__))
    examples_folder = os.path.join( here, 'examples')
    
    p = PPTwrap()
    p.show()
    
    p.addDrawingSlide(title='Make A Drawing')
    
    p.addTextBox(text='Now is the\rTime' )
    
    if 1:
        p.drawRectangle( left=400, top=300, width=0, height=0, rgb=RGB(255,255,255), 
            text=str('Now is the\rTime'), rgbText=RGB(255,0,255), 
            font_name="Comic Sans MS", bold=1, font_size=20)
            
        pixels = 25
        for i in range(5):
            for j in range(5):
                icol = 1 + i*5 + j
                print(i,j,icol)
                try:
                    rgb = RGB( i*50, j*50, 255-50*j)
                    p.drawRectangle( left=pixels + pixels*i, top=100 + pixels*j, 
                        width=pixels, height=pixels, colorIndex=icol, rgb=rgb, text=str(icol) )
                except:
                    print('error on i,j,icol=',i,j,icol)
                    
        p.drawLine( xBeg=100, yBeg=100, xEnd=400, yEnd=500, 
            rgb=RGB(0,255,0), transparency=0.5, weight=3, begStyle=2, endStyle=1 )
    
    if 1:

        p.addImageSlide( imgFile= os.path.join(examples_folder, 'irobot2.gif'),
            title='Favorite Robot')
            
        p.addImageSlide( imgFile=os.path.join(examples_folder, 'escher01.gif'),
            title='Escher Image')
            
        pptText = 'Now is the time for all good charts to blossom\r' +\
            'Now is the time for all good charts to blossom\r' +\
            'Now good charts blossom\r' +\
            'Now is the time for all good charts to blossom\r' +\
            'Now is the time for all good charts to blossom\r' +\
            'Now is the time for all all all all good charts to blossom\r' +\
            'Now good charts blossom\r' +\
            'Now is the time for all good charts to blossom\r' +\
            'Now is the time for all good charts to blossom\r' 
        p.addTextSlide(text=pptText, title='my title',
            textFont='Courier New', textFontSize=18, center=1, 
            noBullets=1, makeItFit=1)
        p.addTextSlide(text=pptText, title='my title',
            textFont='Courier New', textFontSize=18, center=1, 
            noBullets=1, makeItFit=1, wrap=1)
        
    p.abandon()
    #p.saveAs(r'.\test.ppt')
    
    #p.Quit()