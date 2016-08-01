
.. example2


Example #2
==========

Minimize A Constrained Function
-------------------------------

This is problem 6 in Chapter 10 of the book 
"Numerical Methods in Engineering with Python" by Jaan Kiusalaas. 

The task is to minimize the function F(x,y) where x+y <= 1 and x >= 0.6

.. code:: python

    f(x,y) = (x-1)2 + (y-1)2 
        where:    x+y <= 1 
        and:      x >= 0.6
        
The parasol file begins very much as in Example 1, except that there is a 
new, second result variable called "sumXY" with a limit placed on it. 

The setResultVariableLimits statement sets a high limit of 1.0 on "sumXY" 
in order to satisfy the x+y <= 1 constraint.

The parasol file begins as shown below, by importing parasol and defining the problem. 

:download:`download func_opt_b.py <./_static/func_opt_b.py>`



.. code:: python

    from parasol import *

    PS = ParametricSoln(taskName="Minimize F(x,y) with x>=0.6 and x+y<=1", 
         subtaskName="F(x,y)=(x-1)^2 + (y-1)^2", 
         author="Charlie Taylor", 
         constraintTolerance=0.001)
        

    # design vars have: 
    #     name, value, minVal, maxVal, NSteps,  units,  description
    PS.addDesVars(
        ['x',0.6,.6,1.,50,'','X value'],
        ['y',0.2,-0.2,0.4,50,'','Y value'],
        )

    # result variables have: 
    #    name,      units,  description 
    PS.addResultVars(
        ['F','','Function Value'],
        ['sumXY','','Sum of X and Y'],
        )

    PS.setResultVariableLimits(name="sumXY", hiLimit=1.)


The control routine is much like Example 1 except there is a 
second result variable to assign, "sumXY".

.. code:: python

    # the following control routine ties together the system result variables
    #  with the system design variables
    def myControlRoutine(PS):
        # get current values of design variables    
        x,y = PS("x","y")
        # set output variable values
        PS["F"] = (x-1.)**2 + (y-1.)**2
        PS["sumXY"] = x + y        

The final task required for the setup are to give the ParametricSoln 
object the name of the control routine (myControlRoutine).

.. code:: python

    # need to tell system the name of the control routine
    PS.setControlRoutine(myControlRoutine)    
    
Again like Example 1, the statements below minimize "F", save a summary, 
and make some plots to help visualize the results. 

This example also introduces a carpet plot to display results.

.. code:: python

    # now optimize the system.
    minimize(PS, figureOfMerit="F", desVars=[ 'x','y'], MaxLoop=500)

    make2DParametricPlot(PS, sysParam="F", desVar="x",
        paramVar=["y",0.0,.1,.2,.3,.4,]  ,makeHTML=1, dpi=70, linewidth=2,
        ptData=None, ptLegend='', logX=0, logY=0)

    makeCarpetPlot(PS, sysParam="F", xResultVar="sumXY",
        desVarL=[["x",0.6,0.8,1.0],["y",0.0,0.2,0.4]], angDesVarL=[40,0])

    makeContourPlot(PS, sysParam="F", desVars=["x","y"])

    # now save summary of system
    PS.saveFullSummary()
    
The only remaining task is to tell parasol to close all files.

.. code:: python

    PS.close()  # finish up with output files    

The output from the minimize operation is shown below. 


.. raw:: html

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
            "http://www.w3.org/TR/html4/loose.dtd">
    <html lang="en">
    <head>
        <meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
        <title>Minimize F(x,y) with x>=0.6 and x+y<=1</title>
    <style type="text/css">
    BODY{ 
        background-color: #55607B;  
        
        margin-bottom: 0px;  
        margin-top: 0px; 
        font-family: Verdana, Arial, Helvetica, sans-serif;  
    }
    .mytable{ 
        page-break-inside: avoid;
        background-color: #FFFFFF;  
        margin-bottom: 0px;  
        margin-top: 0px; 
        font-size : 12px;
        font-family: Verdana, Arial, Helvetica, sans-serif;  
    }

    td, p, .p{
        font-family: Verdana, Arial, Helvetica, sans-serif;
        font-size : 12px;
    }

    .header {
        font-size: 14px;
        color: #A62F24;
        font-weight: bold;
        line-height: 18px;
        margin-bottom: 8px;
    }

    .subhead  {
     font-size : 12px;
     line-height: 125%;
     font-weight: bold;
     color: #A62F24;
    } 
      
    .hometext  {
        font-size: 12px;
        line-height: 140%;
        font-weight: bold;
        color: #666666;
    } 
     
    .topnav{
     font-family: Verdana, Arial, Helvetica, sans-serif;
     font-size : 10px;
     font-weight : bold;
     color: #FFFFFF;
     text-decoration: none;
     padding-bottom: 1px;
    }
    a.topnav:hover{
     color: #D0D0D0;
    }
    a.p  {
     color:#666666;
    }
    a.p:hover  {
     color: #A62F24;
    }
    a.p:visited  {
     color: #999999;
    }

    .small  {
     font-family: Verdana, Arial, Helvetica, sans-serif;
     font-size : 10px;
     line-height: 110%;
    }
    a.small  {
     color:#666666;
    }
    a.small:hover  {
     color: #A62F24;
    }
    a.small:visited  {
     color: #999999;
    }

    a.formlink  {
     color:#333333;
     text-decoration: none;
    }
    a.formlink:hover  {
     color: #A62F24;
     text-decoration: underline;
    }
    a.formlink:visited  {
     color: #999999;
     text-decoration: underline;
    }

    .breadcrumb  {
     font-family: Verdana, Arial, Helvetica, sans-serif;
     font-size : 10px;
     color:#999999;
     text-decoration: none;
    }
    .breadcrumb:hover  {
     color: #A62F24;
     text-decoration: underline;
    }

    .supplierlink  {
     font-family: Verdana, Arial, Helvetica, sans-serif;
     font-size : 10px;
     line-height: 140%;
     color:#A62F24;
     text-decoration: none;
    }
    .supplierlink:hover  {
     color: #333333;
     text-decoration: underline;
    }

    a.loclink{
        font-family: Verdana, Arial, Helvetica, sans-serif;
        font-size : 12px;
        line-height: 125%;
     color: #A62F24;
    }
    a.loclink:hover  {
     color: #666666;
    }


    .red  {
     color: #A62F24;
    }

    .x  {
     font-family: Verdana, Arial, Helvetica, sans-serif;
     font-size : 14px;
     font-weight: bold;
     color: #008000;
    }

    .footer{
     font-size : 10px;
     color: #CDCCCC;
     text-decoration: none;
     padding-top: 8px;
     padding-bottom: 0px;
    }
    .footer:hover  {
     color: #FFFFFF;
    } 

    form, input, select, option{
        margin-bottom : 0px;
        margin-left : 0px;
        margin-right : 0px;
        margin-top : 0px;
        padding-bottom : 0px;
        padding-left : 0px;
        padding-right : 0px;
        padding-top : 0px;
        font-family : Verdana, Arial, Helvetica, sans-serif;
        font-size : 10px;
        height : 14px;
        border-bottom: 1px;
        border-color: #CCCCCC;
    }


    </style>



    </head>
    <body>
    <center><table bgcolor="#FFFFFF" width="680"><tr><td colspan="2" nowrap align="center">
    <h3 class="header">Minimize F(x,y) with x>=0.6 and x+y<=1</h3></td></tr>
    <tr>
    <td align="left"><span class="header"> F(x,y)=(x-1)^2 + (y-1)^2</span></td>
    <td align="right"><span class="header"> ParametricSoln v0.1.7</span></td></tr>
    <tr>
    <td align="left"><span class="header">by: Charlie Taylor</span></td>
    <td align="right"><span class="header">August 01, 2016</span></td>
    </tr></table></center>
    <center><table class="mytable"><th bgcolor="#CCCCCC"> 
    PRIOR TO MINIMIZE OPTIMIZATION
     </th><tr><td nowrap><pre>ParametricSoln: F(x,y)=(x-1)^2 + (y-1)^2
                
    ====================== OPTIMIZATION DESIGN VARIABLES =======================
          name         value        minimum   maximum
             x          0.6          0.6            1 X value
             y          0.2         -0.2          0.4 Y value

     Figure of Merit: Function Value (F) = 0.8  <== Minimize

    ========================== OPTIMIZATION CONSTRAINTS =========================
          name         value        minimum   maximum
         sumXY          0.8 ------------            1 Sum of X and Y
    ============================================================================
    </pre></td></tr></table></center><center><table class="mytable"><th bgcolor="#CCCCCC"> 
    AFTER MINIMIZE OPTIMIZATION
     </th><tr><td nowrap><pre>ParametricSoln: F(x,y)=(x-1)^2 + (y-1)^2
                
    ====================== OPTIMIZATION DESIGN VARIABLES =======================
          name         value        minimum   maximum
             x          0.6          0.6            1 X value
             y          0.4         -0.2          0.4 Y value

     Figure of Merit: Function Value (F) = 0.52  <== Minimize

    ========================== OPTIMIZATION CONSTRAINTS =========================
          name         value        minimum   maximum
         sumXY            1 ------------            1 Sum of X and Y
    ============================================================================
    </pre></td></tr></table></center><center><table border="1" class="mytable"><th>Design Variable Summary</th><tr><td nowrap><table class="mytable"><th colspan="4" bgcolor="#CCCCCC">Design Variables (nominal values)</th><tr><td><b>Name</b></td><td><b>Value</b></td><td><b>Units</b></td><td><b>Description</b></td></tr><tr><td align="left" valign="top">         y</td><td align="right" valign="top">         0.4</td><td nowrap align="left" valign="top"></td><td nowrap align="left" valign="top">Y value</td></tr>
    <tr><td align="left" valign="top">         x</td><td align="right" valign="top">         0.6</td><td nowrap align="left" valign="top"></td><td nowrap align="left" valign="top">X value</td></tr>
    </table><table class="mytable"><th colspan="6" bgcolor="#CCCCCC">Result Variables </th><tr><td><b>Name</b></td><td><b>Value</b></td><td><b>Units</b></td><td><b>Description</b></td><td><b>Low Limit</b></td><td><b>High Limit</b></td></tr><tr><td align="left">     sumXY</td><td align="right">           1</td><td nowrap align="left"></td><td nowrap align="left">Sum of X and Y</td><td nowrap align="right">---</td><td nowrap align="right"><1</td></tr>
    <tr><td align="left">         F</td><td align="right">        0.52</td><td nowrap align="left"></td><td nowrap align="left">Function Value</td><td nowrap align="right">---</td><td nowrap align="right">---</td></tr>
    </table></td></tr></table></center><br>
    <center><table border="1" class="mytable"><tr>
    <td><img src="./_static/func_opt_b_1___param_F_vs_x.png"></td></tr><tr><td nowrap></td></tr></table></center><center><table border="1" class="mytable"><tr>
    <td><img src="./_static/func_opt_b_2___carpet_F_vs_x_y_sumXY.png"></td></tr><tr><td nowrap></td></tr></table></center><center><table border="1" class="mytable"><tr>
    <td><img src="./_static/func_opt_b_3___F_vs_x_y.png"></td></tr><tr><td nowrap></td></tr></table></center><center><table border="1" class="mytable"><th>Design Variable Summary</th><tr><td nowrap><table class="mytable"><th colspan="4" bgcolor="#CCCCCC">Design Variables (nominal values)</th><tr><td><b>Name</b></td><td><b>Value</b></td><td><b>Units</b></td><td><b>Description</b></td></tr><tr><td align="left" valign="top">         y</td><td align="right" valign="top">         0.4</td><td nowrap align="left" valign="top"></td><td nowrap align="left" valign="top">Y value</td></tr>
    <tr><td align="left" valign="top">         x</td><td align="right" valign="top">         0.6</td><td nowrap align="left" valign="top"></td><td nowrap align="left" valign="top">X value</td></tr>
    </table><table class="mytable"><th colspan="6" bgcolor="#CCCCCC">Result Variables </th><tr><td><b>Name</b></td><td><b>Value</b></td><td><b>Units</b></td><td><b>Description</b></td><td><b>Low Limit</b></td><td><b>High Limit</b></td></tr><tr><td align="left">     sumXY</td><td align="right">           1</td><td nowrap align="left"></td><td nowrap align="left">Sum of X and Y</td><td nowrap align="right">---</td><td nowrap align="right"><1</td></tr>
    <tr><td align="left">         F</td><td align="right">        0.52</td><td nowrap align="left"></td><td nowrap align="left">Function Value</td><td nowrap align="right">---</td><td nowrap align="right">---</td></tr>
    </table></td></tr></table></center><br>
    <table class="mytable"><tr><td nowrap><pre>Parametric Solutions
    parasol v0.1.7
    contact: C. Taylor, cet@appliedpython.com
    </pre></td><td width="90%">&nbsp;</td></tr></table></body>
    </html>

