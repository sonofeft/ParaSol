
.. examples


Example #1
==========

Minimize A Function
-------------------

This is problem 8 in Chapter 10 of the book "Numerical Methods in Engineering with Python" 
by Jaan Kiusalaas. 

The task is to minimize the function f(x,y) while constraining the value of y to be greater than 2.

.. code:: python

    f(x,y) = 6*x**2 + y**3 + x*y 
        where:      y >= -2
        
While this example only operates on a simple function, 
parasol is capable of operating on very large math models with many 
inputs, outputs, and constraints.

The parasol file begins as shown below, by importing parasol and defining the problem. 
(To download the source, click the link below.)

:download:`download func_opt_a.py <./_static/func_opt_a.py>`


The ParametricSoln object needs to know the title and author information 
as well as a description of the input and output variables.         

The addDesVars statement defines the "x", and "y" variables, 
their starting values, their parametric ranges, units and a long description. 

The constraint that y >= -2 is satisfied by using a range for y that 
starts at y = -2. Here we will look at both x and y over the range -2 to 2.

The addResultVars statement defines the function "F", its units (none in this case) 
and a long description.

.. code:: python

    from parasol import *

    PS = ParametricSoln(subtaskName="F(x,y)=6x^2 + y^3 + xy", 
        author="Charlie Taylor", taskName="Minimize F(x,y) with y>=-2", 
        constraintTolerance=0.001)

    # design vars have: 
    #     name, value, minVal, maxVal, NSteps,  units,  description
    PS.addDesVars(
        ['x',1.0,-2,2.,50,'','X value'],
        ['y',0.2,-2,2.,50,'','Y value'],
        )

    # result variables have: 
    #    name,      units,  description 
    PS.addResultVars(
        ['F','','Function Value'],
        )


The control routine describes the interaction of the input and output variables. 
It needs to have as input, a parasol object "PS". 
The current value of "x" and "y" are taken from "PS", and the resulting 
value of "F" is set (A more complex problem would typically import a large math model).

.. code:: python

    # the following control routine ties together the system result variables
    #  with the system design variables
    def myControlRoutine(PS):
        # get current values of design variables    
        x,y = PS("x","y")
        # set output variable values
        PS["F"] = 6.*x**2 + y**3 + x*y
        
The final task required for the setup are to give the ParametricSoln 
object the name of the control routine (myControlRoutine).

.. code:: python

    # need to tell system the name of the control routine
    PS.setControlRoutine(myControlRoutine)
    
Now that the setup is done, we can run the code. 
The statements below minimize "F", save a summary, and make some plots 
to help visualize the results.

.. code:: python

    # now optimize the system.
    minimize(PS, figureOfMerit="F", desVars=[ 'x','y'], MaxLoop=500)

    # now save summary of system
    PS.saveFullSummary()

    makeContourPlot(PS, sysParam="F", desVars=["x","y"])
    make2DParametricPlot(PS, sysParam="F", desVar="x", paramVar=["y",-2,-1,0,1,2])
    
The only remaining task is to tell parasol to finalize the output and close all files.

.. code:: python

    PS.close()  # finish up with output files
    
The output from the minimize operation is shown below. 
It shows that at the starting values for x and y of 1.0 and 0.2, 
the function value was 6.208. 

The optimizer improved that to a value of -8.16667 by changing 
x and y to 0.166669 and -2.0 respectively. 
The table below can be seen in the parasol output by opening the 
HTML output file that parasol creates.

.. raw:: html

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
            "http://www.w3.org/TR/html4/loose.dtd">
    <html lang="en">
    <head>
        <meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
        <title>Minimize F(x,y) with y>=-2</title>
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
    <h3 class="header">Minimize F(x,y) with y>=-2</h3></td></tr>
    <tr>
    <td align="left"><span class="header"> F(x,y)=6x^2 + y^3 + xy</span></td>
    <td align="right"><span class="header"> ParametricSoln v0.1.6</span></td></tr>
    <tr>
    <td align="left"><span class="header">by: Charlie Taylor</span></td>
    <td align="right"><span class="header">July 31, 2016</span></td>
    </tr></table></center>
    <center><table class="mytable"><th bgcolor="#CCCCCC"> 
    PRIOR TO MINIMIZE OPTIMIZATION
     </th><tr><td nowrap><pre>ParametricSoln: F(x,y)=6x^2 + y^3 + xy
                
    ====================== OPTIMIZATION DESIGN VARIABLES =======================
          name         value        minimum   maximum
             x            1           -2            2 X value
             y          0.2           -2            2 Y value

     Figure of Merit: Function Value (F) = 6.208  <== Minimize
    ============================================================================
    </pre></td></tr></table></center><center><table class="mytable"><th bgcolor="#CCCCCC"> 
    AFTER MINIMIZE OPTIMIZATION
     </th><tr><td nowrap><pre>ParametricSoln: F(x,y)=6x^2 + y^3 + xy
                
    ====================== OPTIMIZATION DESIGN VARIABLES =======================
          name         value        minimum   maximum
             x     0.166669           -2            2 X value
             y           -2           -2            2 Y value

     Figure of Merit: Function Value (F) = -8.16667  <== Minimize
    ============================================================================
    </pre></td></tr></table></center><center><table border="1" class="mytable"><th>Design Variable Summary</th><tr><td nowrap><table class="mytable"><th colspan="4" bgcolor="#CCCCCC">Design Variables (nominal values)</th><tr><td><b>Name</b></td><td><b>Value</b></td><td><b>Units</b></td><td><b>Description</b></td></tr><tr><td align="left" valign="top">         y</td><td align="right" valign="top">          -2</td><td nowrap align="left" valign="top"></td><td nowrap align="left" valign="top">Y value</td></tr>
    <tr><td align="left" valign="top">         x</td><td align="right" valign="top">    0.166669</td><td nowrap align="left" valign="top"></td><td nowrap align="left" valign="top">X value</td></tr>
    </table><table class="mytable"><th colspan="6" bgcolor="#CCCCCC">Result Variables </th><tr><td><b>Name</b></td><td><b>Value</b></td><td><b>Units</b></td><td><b>Description</b></td><td><b>Low Limit</b></td><td><b>High Limit</b></td></tr><tr><td align="left">         F</td><td align="right">    -8.16667</td><td nowrap align="left"></td><td nowrap align="left">Function Value</td><td nowrap align="right">---</td><td nowrap align="right">---</td></tr>
    </table></td></tr></table></center><br>
    <center><table border="1" class="mytable"><tr><td>
        <img src="./_static/func_opt_a_1___F_vs_x_y.png"></td></tr>
        <tr><td nowrap></td></tr></table></center><center><table border="1" class="mytable"><tr><td>
        <img src="./_static/func_opt_a_2___param_F_vs_x.png"></td></tr>
        <tr><td nowrap></td></tr></table></center><center><table border="1" class="mytable"><th>Design Variable Summary</th><tr><td nowrap><table class="mytable"><th colspan="4" bgcolor="#CCCCCC">Design Variables (nominal values)</th><tr><td><b>Name</b></td><td><b>Value</b></td><td><b>Units</b></td><td><b>Description</b></td></tr><tr><td align="left" valign="top">         y</td><td align="right" valign="top">          -2</td><td nowrap align="left" valign="top"></td><td nowrap align="left" valign="top">Y value</td></tr>
    <tr><td align="left" valign="top">         x</td><td align="right" valign="top">    0.166669</td><td nowrap align="left" valign="top"></td><td nowrap align="left" valign="top">X value</td></tr>
    </table><table class="mytable"><th colspan="6" bgcolor="#CCCCCC">Result Variables </th><tr><td><b>Name</b></td><td><b>Value</b></td><td><b>Units</b></td><td><b>Description</b></td><td><b>Low Limit</b></td><td><b>High Limit</b></td></tr><tr><td align="left">         F</td><td align="right">    -8.16667</td><td nowrap align="left"></td><td nowrap align="left">Function Value</td><td nowrap align="right">---</td><td nowrap align="right">---</td></tr>
    </table></td></tr></table></center><br>
    <table class="mytable"><tr><td nowrap><pre>Parametric Solutions
    parasol v0.1.6
    contact: C. Taylor, cet@appliedpython.com
    </pre></td><td width="90%">&nbsp;</td></tr></table></body>
    </html>
