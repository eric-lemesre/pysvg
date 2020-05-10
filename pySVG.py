# Pysvg is vector graphics program for python that converts data
# entered by a .txt file in an SVG graphic.
#
# Copyright (C) 2011 Isabel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
   pySVG executable.

   Command Line Usage (Abbreviated)
   ================================
    
\t>>> $pysvg [--h|--help] [--prefab=GRAPHTYPE] [--delim=VALUE] [--x=VALUE]
   ... [--y=VALUE] [--title=STRING] [--xlbl=STRING] [--ylbl=STRING]
   ... [--yrange=VALUE] [--yinc=VALUE] [--ygrid=yes | no] [--animate]
   ... [--filtered] [--legend] ... inputFile
   
   Standard Parameters:
   ====================
   
       I{B{1. Getting input data}}
           - C{E{-}-prefab=[I{bardiagram | bardiagram3d | piechart | scat |
                            lines}]:} type of chart for drawing         
           - C{E{-}-x=<value>:} Identifies the data field that will hold X
                                component.Value must be numeric.
           - C{E{-}-y=<value>:} Identifies the data field than will hold Y
                                component. Value must be numeric         
       I{B{2. Including additional elements}}    
            - C{E{-}-title=<value>:} chart title 
            - C{E{-}-legend=<value>:} If specified, controls the placement of 
                                      the legend.
            - C{E{-}-xlbl=<value>:} Specify axis X label. Only for scat and 
                                    lines chart.
            - C{E{-}-ylbl=<value>:} Specify axis Y label. Only for scat and
                                    lines chart.
            - C{E{-}-name=<value>:} Specifies legend label of the first data
                                    group. Only for scat and lines chart
            - C{E{-}-name2=<value>:} Specifies legend label of the second data 
                                     group. Only for scat and lines chart     
       I{B{3. Animating SVG}}
            - C{E{-}-animate:} Graphic shows the visual effects animation. Only
                               for pie chart.
       I{B{4. Filtering}}
            - C{E{-}-filtered:} Graphic shows the effects of filtering
       I{B{5. Helping}}
            - C{E{-}h,--help:} prints this help. 

   
   Chart Parameters:
   =================
         
   C{B{[I{BARDIAGRAM | BARDIAGRAM3D}]}} Parameters:
      - C{E{-}-color=<value>:} Color of bars
      - C{E{-}-color2=<value>:} Color of the second group of bars      
      - C{E{-}-barwidth=<value>:} Specifies the width of the filled bars. Value
                                  must be numeric.
      - C{E{-}-vals:} If is specified display numeric value near the top of
                      each bar.  
      - C{E{-}-delim=<value>:} Specifies the separation between bars or groups
                               of bars.
      - C{E{-}-yrange=<value>:} Specify an explicit axis numeric range usually 
                                the minimum and must be numeric.
      - C{E{-}-yinc=<value>:} Specify a numeric axis increment amount. Value
                              must be numeric.
      - C{E{-}-ygrid=<value>:} If "yes" specified, grid lines will be drawn.
                              
   C{B{[I{PIECHART}]}} Parameters:
      - C{E{-}-values=<value>:} Identifies the data field that will hold 
                                numeric values for the pie slices. 
                                Pie slices will be displayed as proportions 
                                of the sum of all values. 
      - C{E{-}-labels=<value>:} Identifies the data field that will hold labels
                                for the pie slices.
      - C{E{-}-colorfld=<value>:} Identifies the data field that will hold
                                  colors for the pie slices.
   C{B{[I{SCAT}]}} Parameters:
      - C{E{-}-x2=<value>:} Identifies the data field that will hold X2
                            component.Value must be numeric.
      - C{E{-}-y2=<value>:} Identifies the data field than will hold y2
                            component. Value must be numeric. 
      - C{E{-}-ptsym=<value>:} Controls the shape of the first data set point
                               symbol. The possible values can be:C{circle or
                               square or triangle or diamond or 
                               invertedtriangle}. 
      - C{E{-}-pt2sym=<value>:} Controls the shape of the second data set point
                                symbol. The possible values can be:C{circle or
                                square or triangle or diamond or 
                                invertedtriangle}.       
      - C{E{-}-ptsize=<value>:} Controls the size of the data point symbol.
      - C{E{-}-ptcolor=<value>:} Controls the color of the first data set
                                 point symbol.
      - C{E{-}-pt2color=<value>:} Controls the color of the second data set
                                  point symbol.
      - C{E{-}-corr:} Compute and display correlation and regression curve.
    
   C{B{[I{LINES}]}} Parameters:
      - C{E{-}-x2=<value>:} Identifies the data field that will hold X2
                            component.Value must be numeric.
      - C{E{-}-y2=<value>:} Identifies the data field than will hold Y2 
                            component. Value must be numeric.    
      - C{E{-}-ptsym=<value>:} Controls the shape of the first data set
                               point symbol. The possible values can be:
                               C{circle or square or triangle or diamond or 
                               invertedtriangle}. 
      - C{E{-}-pt2sym=<value>:} Controls the shape of the second data set
                                point symbol. The possible values can be:
                                C{circle or square or triangle or diamond or 
                                invertedtriangle}.
      - C{E{-}-ptsize=<value>:} Controls the size of the data point symbol.
      - C{E{-}-ptcolor=<value>:} Controls the color of the data point symbol. 
      - C{E{-}-pt2color=<value>:} Controls the color of the second data set 
                                  point symbol.      
      - C{E{-}-fill=<value>:} If specified, the area under the plotted first
                              line to be filled with the given color.
      - C{E{-}-fill2=<value>:} If specified, the area under the plotted second 
                               line to be filled with the given color.      
    
   Examples:
   =========        
   The following command will generate a bar diagram in three dimensions with
   purple bars, tittle, legend and no values above the bars.
   
\t >>> $pysvg --prefab bardiagram3d --delim=50 --x=1 --y=2 --yrange=0 --yinc=20
   ... --ygrid=yes  --barwidth=25 --color=purple --filtered 
   ... --tittle=TITTLE_BAR3D --legend --name=legend_bars3d inputdatafile.txt
"""

__docformat__ = 'epytext en'
__version__ = '0.0.2'
__author__ = 'Isabel Rodriguez Marin'
__url__ = 'http://pysvg.orgfree.com/'
__license__ = 'GPL Open Source License'

###############################################################################
# Imports
############################################################################### 

import sys
import getopt
import svgelements
import filetext
import os


###############################################################################
# Functions
############################################################################### 

# {Argument

def print_usage():
    print("Usage: pysvg [--option=argument] inputFile\nFor help use [-h | --help]")
    print("pysvg 0.0.4-Nov2011\nCopyright (C) 2011 Isabel Rodriguez")
    print("You can see the full documentation at URL:\"http://www.pysvg/orgfree.com\"")


def getprocessargs(args, prefab, xcolumn, ycolumn, xcolumn2, ycolumn2,
                   barwidth, xorigin, yorigin, delim, vals, yinc, yrange,
                   ygrid, radius, values, labels, colorfld, title,
                   legend, animate, filtered, ptsize, ptsym, pt2sym, ptcolor,
                   pt2color, corr, xlabel, ylabel, name, name2, color, color2):
    """
    Helper responsible for returning the entire document SVG code. 
    Its main functions are:
    
        1. Read the input data by calling the function "readinputfile" 
           module filetext
        2. Add the header and the end of svg document
        \t>>>     cab=svgelements.SVGElements()
            ...     begin,end=cab.printSVG()
        3. Include diagram svg code selected by the user through the command 
           line using the option "-- prefab" and stored in the variable of type
           string c{"chartSVG"}
           
         \t>>> if prefab == "bardiagram":
           ...    BarDiagram=svgelements.Bardiagram(....)
           ... elif prefab == "pie":
           ...    pieChart=svgelements.PieChart(....)                  
           ... elif prefab == "bardiagram3d":
           ...    BarDiagram3d=svgelements.Bardiagram3d(....)
           ... elif prefab == "scat":
           ...    scatterplot=svgelements.Scatterplot(....)
           ... elif prefab == "lines":
           ...    lineplot=svgelements.Lineplot(....)
           
           If the user enters a wrong option, program execution will stop 
           reporting on this situation the user with a message to standard
           output through.
           
         \t>>> else:
           ...    try:
           ...        raise ValueError
           ...        except ValueError as e:
           ...        print("The name of the chart must be: \"bardiagram\", 
           ...        \"bardiabram3d\", \"pie\", \"scat\", or \"lines\", for 
           ...        help use --help"
           ...        sys.exit(2)
           
        4. Write the svg code stored in the variable "charSVG" in the output 
           file by default set for each graph.
           
         \t>>> filetext.writeSVGFile(path,begin+chartSVG+end)
    
    @raise ValueError: If the user enters a wrong option.
    @return: Entire document SVG code       
    
    """
    # read input files
    inputargs = ""
    for inputargs in args:
        lval = filetext.readinputfile(inputargs)
    svgdoc = svgelements.Svgelements()
    begin, end = svgdoc.printsvg()
    try:
        (dirname, filename) = os.path.split(inputargs)
        # raise UnboundLocalError
    except UnboundLocalError as error:
        print("Incorrect options")
        print("Usage: pysvg [options] inputFile\nFor help use [-h | --help]\n" % error)
        print("pysvg 0.0.2-Oct2011\nCopyright (C) 2011 Isabel Rodriguez")
        print("You can see the full documentation at URL:\"http://www.pysvg/orgfree.com\"")
        sys.exit(2)
    if prefab == "bardiagram":
        try:
            path = os.path.join(str(dirname), 'vbars2D.svg')
            if path == filename:
                raise UnboundLocalError
            bardiagram = svgelements.Bardiagram(lval=lval, xorigin=xorigin,
                                                yorigin=yorigin, xcolumn=xcolumn, ycolumn=ycolumn,
                                                ycolumn2=ycolumn2, barwidth=barwidth, delim=delim,
                                                vals=vals, yinc=yinc, yrange=yrange, ygrid=ygrid,
                                                fillcolor=color, fillcolor2=color2, name=name,
                                                name2=name2, title=title, legend=legend)
            chartsvg = bardiagram.printsvg()
        except UnboundLocalError:
            print_usage()
            sys.exit(2)
    elif prefab == "pie":
        try:
            path = os.path.join(str(dirname), 'piechart.svg')
            if path == filename:
                raise UnboundLocalError
            piechart = svgelements.Piechart(xorigin=xorigin, yorigin=yorigin,
                                            radius=radius, listvalues=lval, values=values,
                                            labels=labels, colorfld=colorfld, legend=legend,
                                            animate=animate, filtered=filtered, title=title)
            chartsvg = piechart.printsvg()
        except UnboundLocalError:
            print_usage()
            sys.exit(2)
    elif prefab == "bardiagram3d":
        try:
            path = os.path.join(str(dirname), 'vbars3D.svg')
            if path == filename:
                raise UnboundLocalError
            bardiagram3d = svgelements.Bardiagram3d(lval=lval, xcolumn=xcolumn,
                                                    ycolumn=ycolumn, barwidth=barwidth,
                                                    xorigin=xorigin, yorigin=yorigin, delim=delim,
                                                    vals=vals, yinc=yinc, yrange=yrange,
                                                    ygrid=ygrid, filtered=filtered, fillcolor=color,
                                                    title=title, legend=legend, name=name)
            chartsvg = bardiagram3d.printsvg()
        except UnboundLocalError:
            print_usage()
            sys.exit(2)
    elif prefab == "scat":
        try:
            path = os.path.join(str(dirname), 'scatterplot.svg')
            if path == filename:
                raise UnboundLocalError
            scatterplot = svgelements.Scatterplot(lval=lval, xorigin=xorigin,
                                                  yorigin=yorigin, xcolumn=xcolumn, ycolumn=ycolumn,
                                                  xcolumn2=xcolumn2, ycolumn2=ycolumn2, yinc=yinc,
                                                  ptsize=ptsize, ptsym=ptsym, pt2sym=pt2sym,
                                                  ptcolor=ptcolor, pt2color=pt2color, corr=corr,
                                                  xlabel=xlabel, ylabel=ylabel, name=name,
                                                  name2=name2, legend=legend, title=title)
            chartsvg = scatterplot.printsvg()
        except UnboundLocalError:
            print_usage()
            sys.exit(2)
    elif prefab == "lines":
        try:
            path = os.path.join(str(dirname), 'lineplot.svg')
            if path == filename:
                raise UnboundLocalError
            lineplot = svgelements.Lineplot(lval=lval, xorigin=xorigin,
                                            yorigin=yorigin, xcolumn=xcolumn, ycolumn=ycolumn,
                                            xcolumn2=xcolumn2, ycolumn2=ycolumn2, yinc=yinc,
                                            ptsize=ptsize, ptsym=ptsym, pt2sym=pt2sym,
                                            ptcolor=ptcolor, pt2color=pt2color, xlabel=xlabel,
                                            ylabel=ylabel, name=name, name2=name2,
                                            legend=legend, title=title, fillcolor=color,
                                            fillcolor2=color2)
            chartsvg = lineplot.printsvg()
        except UnboundLocalError:
            print_usage()
            sys.exit(2)
    else:
        try:
            raise ValueError
        except ValueError as error:
            print("PREFABNAME= [bardiagram | bardiabram3d | pie | scat |lines]")
            print("Usage: pysvg --prefab=PREFABNAME [--option=argument] inputFile \n%sFor help use [-h | --help]" % error)
            print("pysvg 0.0.4-Nov2011\nCopyright (C) 2011 Isabel Rodriguez")
            print("You can see the full documentation at URL:\"http://www.pysvg/orgfree.com\"")
            sys.exit(2)
    filetext.writesvgfile(path, begin + chartsvg + end)


# {Interface


def main():
    """ 
    Perform all actions indicated by the given set of options and initializes 
    all variables to their default values.
    @return: the SVG document created while running mainSVG.
    @rtype: C{string} 
    """

    try:
        options, args = getopt.getopt(sys.argv[1:], "h", ["help", "prefab=",
                                                          "delim=", "x=", "y=", "x2=", "y2=", "vals", "yrange=",
                                                          "yinc=",
                                                          "ygrid=", "barwidth=", "values=", "labels=", "color=",
                                                          "color2=",
                                                          "colorfld=", "legend", "animate", "filtered", "corr",
                                                          "ptsize=",
                                                          "ptsym=", "pt2sym=", "ptcolor=", "pt2color=", "xlbl=",
                                                          "ylbl=",
                                                          "fill=", "fill2=", "name=", "name2=", "title="])
    except getopt.GetoptError as error:
        print("Usage: pysvg [--option=argument] inputFile \n%sFor help use [-h | --help]" % error)
        print("pysvg 0.0.2-Oct2011\nCopyright (C) 2011 Isabel Rodriguez")
        print("You can see the full documentation at URL:\"http://www.pysvg/orgfree.com\"")
        sys.exit(2)
    prefab = ""
    # POSITION OPTIONS
    delim, xcolumn, ycolumn, xcolumn2, ycolumn2 = 25, 1, 2, 3, 3
    vals, yorigin, xorigin = False, 100, 100
    # VBAR AND VBAR3D OPTIONS
    yrange, yinc, ygrid = 0, 10, False
    barwidth, color, color2 = 25, "none", "none"
    # PIECHART OPTIONS
    colorfld, values, labels, radius = 3, 2, 1, 100
    legend, name, name2, title = False, "Enter_text", "Enter_text", ""
    animate, filtered = False, False
    # SCATTERPLOT AND LINEPLOT OPTIONS
    corr = False
    ptsize, ptsym, pt2sym = 4, "circle", "square"
    ptcolor, pt2color = "red", "blue"
    xlbl, ylbl = "", ""
    for option, arg in options:
        if option in ("-h", "--help"):
            print(__doc__)
            sys.exit(2)
        if option == "--prefab":
            prefab = arg
        if option == "--delim":
            delim = arg
        if option == "--x":
            xcolumn = arg
        if option == "--y":
            ycolumn = arg
        if option == "--x2":
            xcolumn2 = arg
        if option == "--y2":
            ycolumn2 = arg
        if option == "--yinc":
            yinc = arg
        if option == "--yrange":
            yrange = arg
        if option == "--vals":
            vals = True
        if option == "--ygrid":
            ygrid = arg
        if option == "--barwidth":
            barwidth = arg
        if option == "--values":
            values = arg
        if option == "--color" or option == "--fill":
            color = arg
        if option == "--color2" or option == "--fill2":
            color2 = arg
        if option == "--labels":
            labels = arg
        if option == "--colorfld":
            colorfld = arg
        if option == "--legend":
            legend = True
        if option == "--animate":
            animate = True
        if option == "--filtered":
            filtered = True
        if option == "--corr":
            corr = True
        if option == "--ptsize":
            ptsize = arg
        if option == "--ptsym":
            ptsym = arg
        if option == "--pt2sym":
            pt2sym = arg
        if option == "--ptcolor":
            ptcolor = arg
        if option == "--pt2color":
            pt2color = arg
        if option == "--xlbl":
            xlbl = arg
        if option == "--ylbl":
            ylbl = arg
        if option == "--name":
            name = arg
        if option == "--name2":
            name2 = arg
        if option == "--title":
            title = arg

    getprocessargs(args=args, prefab=prefab, xcolumn=xcolumn,
                   ycolumn=ycolumn, xcolumn2=xcolumn2, ycolumn2=ycolumn2,
                   barwidth=barwidth, xorigin=xorigin, yorigin=yorigin,
                   delim=delim, vals=vals, yinc=yinc, yrange=yrange,
                   ygrid=ygrid, radius=radius, values=values,
                   labels=labels, colorfld=colorfld, title=title,
                   legend=legend, animate=animate, filtered=filtered,
                   ptsize=ptsize, ptsym=ptsym, pt2sym=pt2sym,
                   ptcolor=ptcolor, pt2color=pt2color, corr=corr,
                   xlabel=xlbl, ylabel=ylbl, name=name,
                   name2=name2, color=color, color2=color2)


if __name__ == '__main__':
    main()
