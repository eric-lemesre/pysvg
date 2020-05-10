# pySVG is vector graphics program for python that converts data
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
   This module contains all classes needed to build the graphic selected by
   the user.
   Each graph is represented by the sum of its parts. For example, the bar
   chart is composed of:
       1. A line item
       2. A line item with a text
       3. One or more elements column or rectangle depending on the input
          parameters chosen by the user

   The style of each graphic: width, height, color and so on,
   will depend on the input parameters chosen by the user
   Each element of the chart will be represented by a class which can be a
   base class or an inherited class. Base classes contain the basic elements
   of svg such as circle, rectangle, path, line, text, polygon and so on.
   Inherited classes contain svg compositions generated with various elements
   of the base classes. All classes will have their internal methods for any
   type of operation and a method called printsvg that will be responsible for
   returning the SVG source code to represent each element. For all
   mathematical operations will be necessary to import all the elements of
   math module.

   G{classtree Svgelements, Text, Verticaltext, Line, Linetext,
   Rectangle, Column, Hcolumn, Polygon, Rectangle3d, Column3d, Circle,
   Path, Linepath, Gradient, Filter, Piechart, Bardiagram, Bardiagram3d,
   Scatterplot, Lineplot}
"""

__docformat__ = 'epytext en'

###############################################################################
## Imports
###############################################################################

from math import cos, sin, pi
import sys

###############################################################################
# Svgelements Objects: Abstract Base Classes
###############################################################################


class Svgelements:
    """
    Base class to compose the SVG document in which the graphic will be
    inserted. This graphic will be chosen by the user with the C{--prefab}
    option into the command line

    Return in two vars the SVG source code of the header
    and the end SVG document object
    """

    def __init__(self):
        """
        """

    def printsvg(self):
        """
        Returns a string with the SVG code of the header and end SVG document

        Header string contains:
            - The I{B{namespace}} used by SVG, and a I{B{document}}
            - The I{B{type declaration}} or DOCTYPE associates a
            particular SGML or XML document with a document type definition.

        >>> print <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
        ...      "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
        ...      <svg xmlns="http://www.w3.org/2000/svg" width="X00px"
        ...      height="X00px">

        End string contains:
            - The I{B{tags}} to close the SVG document structure.

        >>> print </svg>

        @rtype: C{string,string}
        """

        stringcab = "<?xml version=\"1.0\"?>\n\n<!DOCTYPE svg PUBLIC \"-//W3C"\
        + "//DTD SVG 1.1//EN\"\n\"http://www.w3.org/Graphics/SVG/1.1/DTD/"\
        + "svg11.dtd\">\n\n<svg xmlns=\"http://www.w3.org/2000/svg\" "\
        + "version=\"1.1\">\n<g id=\"body\" style = \"fill-opacity:1.0; "\
        + "stroke:black; stroke-width:1;\">\n"
        stringend = "</g>\n</svg>\n"
        return stringcab, stringend

###############################################################################


class Text:
    """
    Base class to build text items in SVG code. This element will
    be drawn in horizontal direction
    """
    def __init__(self, xorigin, yorigin, fontsize, text,
                 stroke="black", idtext="text"):

        self.xorigintext = xorigin
        """@ivar: is the X initial coordinate of the object
        @type: C{number}"""
        self.yorigintext = yorigin
        """@ivar: is the Y initial coordinate of the object.
        @type: C{number}"""
        self.fontsizetext = fontsize
        """@ivar: is the size of the text.
        @type: C{number}"""
        self.text = text
        """@ivar: is the description of the text item.
        @type: C{string}"""
        self.stroketext = stroke
        """@ivar: is a fill color of the text item.
        @type: C{string}"""
        self.idtext = idtext
        """@ivar: is a identifier of the text item in SVG document
        @type: C{string}"""

    def printsvg(self):
        """
        Returns a string with SVG code for the Text object

        @return: SVG source code of the text object.
        @rtype: C{string}
        """
        string = "<text id=\"" + str(self.idtext) + "\" x=\"" \
        + str(self.xorigintext) + "\" y=\"" + str(self.yorigintext) + \
        "\" text-anchor=\"start\" font-size=\"" + str(self.fontsizetext) + \
        "\" font-family=\"arial\" stroke=\"" + str(self.stroketext) + "\"> " \
        + str(self.text) + " </text>\n"
        return string

###############################################################################


class Line:
    """ Base class to build line items in SVG code. This element will
    generally be used to draw the axes of the graphs.
    """
    def __init__(self, xorigin, yorigin, endx, endy, ygrid="no",
                 strokecolor="black", strokewidth=2):
        self.xoriginline = xorigin
        """@ivar: is the initial X coordinate of the object.
        @type: C{number}"""
        self.yoriginline = yorigin
        """@ivar: is the initial Y coordinate of the object.
        @type: C{number}"""
        self.endxline = endx
        """@ivar: is the final X coordinate of the object.
        @type: C{number}"""
        self.endyline = endy
        """@ivar: is the final Y coordinate of the object.
        @type: C{number}"""
        self.ygridline = ygrid
        """@ivar: is C{value=yes}, grid lines will be drawn.
        @type: C{yes} or C{no}"""
        self.strokecolorline = strokecolor
        """@ivar: If C{self.ygridline} is specified, this var
         determines the color of the grid lines
        @type: C{string}"""
        self.strokewidthline = strokewidth
        """@ivar: If C{self.ygridline} is specified, this var
        determines the width of the grid lines
        @type: C{number}"""

    def printsvg(self):
        """
        Returns a string with the SVG code for the Line object

        If self.ygridline='yes' the line object will be drawn with the next
        default parameters:
            - self.strokecolorline="gainsboro"
            - self.strokewidthline=2
            - strokedasharray="4, 4, 4, 4
        So the bottom lines will be visible to the user

        @return: SVG source code of the Line object.
        @rtype: C{string}

        """
        if self.ygridline == "yes":
            self.strokecolorline = "gainsboro"
            self.strokewidthline = 2
            strokedasharray = "4, 4, 4, 4"
            string = "<line x1=" + "\"" + str(self.xoriginline) + "\" y1= \"" \
            + str(self.yoriginline) + "\" x2= \"" + str(self.endxline) + \
            "\" y2= \"" + str(self.endyline) + "\"" + " stroke= \"" \
            + str(self.strokecolorline) + "\" stroke-width= \"" \
            + str(self.strokewidthline) + "\" stroke-dasharray= \"" \
            + str(strokedasharray) + "\" />" + "\n"
        else:
            string = "<line x1=" + "\"" + str(self.xoriginline) + "\" y1= \""\
            + str(self.yoriginline) + "\" x2= \"" + str(self.endxline) + \
            "\" y2= \"" + str(self.endyline) + "\"" + " stroke= \""\
            + str(self.strokecolorline) + "\" stroke-width= \"" + \
            str(self.strokewidthline) + "\" />" + "\n"
        return string

###############################################################################


class Rectangle:
    """ Base class to build rectangle items in SVG code."""
    def __init__(self, height, width, xorigin, yorigin, idrect, fill,
                 filtered=False, filterid="none"):

        #Svgelements.__init__(self)
        self.xoriginrect = xorigin
        """@ivar: is the X-coordenate of the initial point of the rectangle
        @type: C{number}"""
        self.yoriginrect = yorigin
        """@ivar: is the Y-coordenate of the initial point of the rectangle
        @type: C{number}"""
        self.heightrect = height
        """@ivar: is the height of the rectangle
        @type: C{number}"""
        self.widthrect = width
        """@ivar: is the width of the rectangle
        @type: C{number}"""
        self.idrect = idrect
        """@ivar: is the identifier of the rectangle within the SVG document.
        Used to apply filters, animations or any other effects in this element
        @type: C{string}"""
        self.fillrect = fill
        """@ivar: is the fill color of the rectangle
        @type: C{string}"""
        self.rectfiltered = filtered
        """@ivar: is a value that indicates whether to apply some filter
        to the rectangle or not.
        @type: C{boolean}"""
        self.rectfilterid = filterid
        """@ivar: is the filter identifier for rectangle element
        @type: C{string}"""

    def printsvg(self):
        """
        Returns a string with the SVG code for the Rectangle object

        If value of the instance variable C{self.rectfiltered}='True'
        rectangle will be drawn with a specified filter defined in the variable
        C{self.rectfilterid}.

        @return: SVG source code of the Rectangle object.
        @rtype: C{string}

        """
        if self.rectfiltered:
            string = "<rect id=\"" + self.idrect + "\" x=\""\
            + str(self.xoriginrect) + "\" y=\"" + str(self.yoriginrect) + \
            "\" height=\"" + str(self.heightrect) + "\" width=\""\
            + str(self.widthrect) + "\" stroke-width=\"0\" stroke=\"" + \
            str(self.fillrect) + "\" fill=\"" + self.fillrect + \
            "\"  filter=\"url(#" + self.rectfilterid + ");\"/>\n"
        else:
            string = "<rect id=\"" + self.idrect + "\" x=\""\
            + str(self.xoriginrect) + "\" y=\"" + str(self.yoriginrect) + \
            "\" height=\"" + str(self.heightrect) + "\" width=\""\
            + str(self.widthrect) + "\" stroke-width=\"1\" stroke=\"black\""\
            + " fill=\"" + self.fillrect + "\" />\n"
        return string

###############################################################################


class Polygon:

    """ Base class to build polygon items in SVG code."""

    def __init__(self, pointlist, idpolygon, fillcolor, filtered=False,
                 filterid="none"):
        self.polygonpointlist = pointlist
        """@ivar: is the set of points (X,Y) used to drawn the Polygon object
        @type: C{list of coordenates}"""
        self.idpolygon = idpolygon
        """@ivar: is the identifier polygon element in SVG document
        @type: C{string}"""
        self.polygonfillcolor = fillcolor
        """@ivar: is the fill color of the polygon element
        @type: C{string}"""
        self.polygonfilterid = filterid
        """@ivar: is the filter identifier for polygon element
        @type: C{string}"""
        self.polygonfiltered = filtered
        """@ivar: is a value that indicates whether to apply some filter
        to the polygon or not
        @type: C{boolean}"""

    def printsvg(self):
        """
        Returns a string with the SVG code for the Polygon object

        If value of the instance variable C{self.polygonfiltered}='True'
        polygon will be drawn with a specified filter defined in the variable
        C{self.polygonfilterid}.

        @return: SVG source code of the Polygon object.
        @rtype: C{string}

        """
        if not self.polygonfiltered:
            string = "<polygon id=\"" + self.idpolygon + "\" points=\""
            for i in range(len(self.polygonpointlist)):
                string += str(self.polygonpointlist[i][0]) + ","\
                + str(self.polygonpointlist[i][1]) + " "
            string += "\" style=\"stroke:black; stroke-width:1; fill:"\
            + self.polygonfillcolor + "\"/>\n"
        else:
            string = "<polygon id=\"" + self.idpolygon + "\" points=\""
            for i in range(len(self.polygonpointlist)):
                string += str(self.polygonpointlist[i][0]) + ","\
                + str(self.polygonpointlist[i][1]) + " "
            string += "\" style=\"stroke:black; stroke-width:1; fill:"\
            + self.polygonfillcolor + "; filter:url(#" + \
            self.polygonfilterid + ");\"/>\n"
        return string

###############################################################################


class Circle:

    """ Base class to build Circle items in SVG code."""

    def __init__(self, xorigin, yorigin, radius, strokewidth, strokecolor,
                 fillcolor, filtered=False, filterid="none"):
        self.xorigincircle = xorigin
        """@ivar: is the X-coordenate of the center of the circle
        @type: C{number}"""
        self.yorigincircle = yorigin
        """@ivar: is the Y-coordenate of the center of the circle
        @type: C{number}"""
        self.radiuscircle = radius
        """@ivar: is the radius of the circle
        @type: C{number}"""
        self.strokewidthcircle = strokewidth
        """@ivar: is the width of the line of the circumference
        @type: C{number}"""
        self.strokecolorcircle = strokecolor
        """@ivar: is the color of the line of the circumference
        @type: C{string}"""
        self.fillcolorcircle = fillcolor
        """@ivar: is the fill color of the circle
        @type: C{string}"""
        self.filteredcircle = filtered
        """@ivar: is a value that indicates whether to apply some filter
        to the circle or not.
        @type: C{boolean}"""
        self.filteridcircle = filterid
        """@ivar: is the filter identifier for circle element
        @type: C{string}"""

    def printsvg(self):
        """
        Returns a string with the SVG code for the Circle object

        If value of the instance variable C{self.filteredcircle}='True'
        circle will be drawn with a specified filter defined in the variable
        C{self.filteridcircle}.

        @return: SVG source code of the Circle object.
        @rtype: C{string}
        """

        if self.filteredcircle:
            return "<circle cx=\"" + str(self.xorigincircle) + "\" cy=\"" + \
                    str(self.yorigincircle) + "\" r=\""\
                    + str(self.radiuscircle) + "\"\n" + "style=\"fill:"\
                    + self.fillcolorcircle + "; stroke:"\
                    + self.strokecolorcircle + "; stroke-width:"\
                    + str(self.strokewidthcircle) + "; filter:url(#"\
                    + self.filteridcircle + ");\"/>\n"
        else:
            return "<circle cx=\"" + str(self.xorigincircle) + "\" cy=\""\
                   + str(self.yorigincircle) + "\" r=\""\
                   + str(self.radiuscircle) + "\"\n" + "style=\"fill:"\
                   + self.fillcolorcircle + "; stroke:"\
                   + self.strokecolorcircle + "; stroke-width:"\
                   + str(self.strokewidthcircle) + ";\"/>\n"
        
    
############################################################################### 

class Path:
    """
    Base class to build a specified kind of Path item in SVG code. 
    The path data consists of one-letter commands, such as M for move 
    to or L for line to, followed by the coordinate information for 
    that particular command.  
    
    This element is used to form the pie slices. To understand how it 
    is built must be taken into account the following::
        
    Commands available to define Path objects:
    ==========================================
         
        - B{M}: Moves to a certain point without painting a line. 
        - B{L}: Creating a line to the coordinate indicated. 
        - B{A}. Creating a elliptic line to the coordinates indicated. An arc 
        command begins with the A abbreviation for absolute coordinates or a 
        for relative coordinates, and is followed by seven parameters:  
            - The C{x- and y-radius} of the ellipse on which the points lie.
            - The C{x-axis-rotation} of the ellipse.
            - The C{large-arc-flag}, which is zero if the arc's measure is less
            than 180 degrees, or one if the arc's measure is greater than or 
            equal to 180 degrees.
            - The C{sweep-flag}, which is zero if the arc is to be drawn in the
            negative angle direction, or one if the arc is to be drawn in the 
            positive angle direction.
            - The C{ending x- and y- coordinates} of the ending point. 
            (The starting point is determined by the last point drawn or the 
            last move to command.)              
        - B{Z}: Close the path.
   
    Here is an example of the path used to draw the elliptical arc::
    
    >>> print <path id="pie0" d="M200,200 L300.0,200.0 A100,100 0 0,1 
    ... 168.694819148,294.973605027 Z" fill="red" stroke="black" 
    ... stroke-width="1" onmouseover="animationOn('pie0');"
    ... onmouseout="animationOff('pie0');" filter="url(#lighting);"/>
    """
    
    def __init__(self, xorigin, yorigin, radius, listvalues, colorfld, radian,
                 pos, initianradian, idpath, mouseover="", mouseout="",
                 filtered=False, filterid="none", strokewidth=0):
        self.xorigin = xorigin
        """@ivar: is the X-coordenate of the initial point of the path 
        @type: C{number}"""
        self.yorigin = yorigin
        """@ivar: is the Y-coordenate of the initial point of the path 
        @type: C{number}"""
        self.radius = radius
        """@ivar: This variable is used to draw a continuous line from the 
        initial point of the path (center of the circle) to the length of the 
        circle radius.
        @type: C{number}"""
        self.strokewidth = strokewidth
        """@ivar: is the width of the line of the path
        @type: C{number}"""
        self.listvalues = listvalues
        """@ivar: is the list of input values that will be transformed in 
        radians to draw each piece of graph
        @type: C{list of number}"""
        self.colorfld = colorfld
        """@ivar: is a number that identifies the data field that will hold 
        colors for the pie slices 
        @type: C{list of number}"""
        self.radian = radian
        """@ivar: is a float number that defines the angle units of each pie 
        slice.
        @type: C{float number}"""
        self.initianradian = initianradian
        """@ivar: is a float number that defines the initial radian for 
        the pie slices
        @type: C{float number}"""
        self.idpath = idpath
        """@ivar: is the identifier of path element in the SVG document 
        @type: C{string}"""
        self.pos = pos
        """@ivar: is a number indicating the position of the radian value 
        in a list of radians 
        @type: C{number}"""
        self.mouseover = mouseover
        """@ivar: is a string that indicates the actions to take when you 
        move the mouse over the item in question
        @type: C{string}"""
        self.mouseout = mouseout
        """@ivar: is a string that indicates the actions to take when you 
        move the mouse out the item in question
        @type: C{string}"""
        self.filtered = filtered
        """@ivar: is a value that indicates whether to apply some filter 
        to the path or not
        @type: C{boolean}"""
        self.filterid = filterid
        """@ivar: is the filter identifier for path element
        @type: C{string}"""
        
    def printsvg(self):
        """ 
        Returns a string with the code for a path as follows:: 
        
        >>> print <path d="M (X-coordenate,Y-coordenate) 
        ... L(X-endline-coordenate, Y-endline-coordenate) 
        ... A (X-radius,Y-radius 0 large-arc-flag,1 
        ... X-ending-point,Y-ending-point) Z"/> 
        
        Important considerations:
        =========================
        
        1. I{Sine function (sin)}, is defined as the ratio of the side opposite 
        the angle to the hypotenuse. 
        
            - B{C{sin S{alpha}=  side_oopposite E{/} hypotenuse}} 
                
        2. I{Cosine function (cos)}, is defined as the ratio of the adjacent 
        leg to the hypotenuse.

            - B{C{cos S{alpha}= side_adjacent E{/} hypotenuse}}        
        
        3. C{hipotenuse = self.radius} therefore::
            - C{side_opposite = sin S{alpha}*self.radius}
            - C{side_adjacent = cos S{alpha}*self.radius}
        
        4. If C{self.radian} < pi (180 degrees) => C{large-arc-flag = 0}
        5. If C{self.radian} > pi (180 degrees) => C{large-arc-flag = 1}
        
        @return: SVG source code of the Path object.
        @rtype: C{string}
                
        """
        finalradian = self.initianradian 
        if self.idpath != "":                   
            string = "<path id=\"" + self.idpath + "\"" + " d=\"M" + \
            str(self.xorigin) + "," + str(self.yorigin) + " L" + \
            str(self.xorigin + cos(self.initianradian) * self.radius) + "," \
            + str(self.yorigin + sin(self.initianradian) * self.radius) + \
            " A" + str(self.radius) + "," + str(self.radius) + " 0 "
        else: 
            string = "<path d=\"M" + str(self.xorigin) + "," + \
            str(self.yorigin) + " L" + str(self.xorigin + \
            cos(self.initianradian) * self.radius) + "," + \
            str(self.yorigin + sin(self.initianradian) * self.radius) + \
            " A" + str(self.radius) + "," + str(self.radius) + " 0 "          
        if (self.radian > pi):
            string += "1"
        else:
            string += "0" 
        finalradian += self.radian 
        if self.filtered:   
            string += ",1 " + str(self.xorigin + cos(finalradian) * \
            self.radius) + "," + str(self.yorigin + sin(finalradian) * \
            self.radius) + " Z\" fill=\"" + \
            str(self.listvalues[int(self.colorfld) - 1][self.pos]) + \
            "\" stroke=\"black\" stroke-width=\"" + \
            str(self.strokewidth) + "\" onmouseover=\"" + self.mouseover + ""\
            + "\" onmouseout=\"" + self.mouseout + \
            "\" filter=\"url(#" + self.filterid + ");\"/>\n" 
        else:
            string += ",1 " + str(self.xorigin + cos(finalradian) * \
            self.radius) + "," + str(self.yorigin + sin(finalradian) * \
            self.radius) + " Z\" fill=\"" + \
            str(self.listvalues[int(self.colorfld) - 1][self.pos]) + \
            "\" stroke=\"black\" stroke-width=\"" + str(self.strokewidth) + \
            "\" onmouseover=\"" + self.mouseover + "" + "\" onmouseout=\"" + \
            self.mouseout + "\"/>\n" 
        return string

###############################################################################


class Linepath:
    """ 
    Base class to draw a path with straight lines connecting points of 
    a list passed as parameter.
    This construction is useful to draw
        - The regression line in Scatter Plot chart
        - The points line in Line Plot chart
            
    Commands available to define Linepath objects:
    ==============================================
         
        - B{M}: Moves to a certain point without painting a line. 
        - B{L}: Creating a line to the coordinate indicated.             
        - B{Z}: Close the path.
    
    Here is an example of the path used to draw the regression line and 
    the line plot::
        
    >>> print <path id="regLine2" d=" M.0,298.0 L139.0,298.0 L139.0,231.0 
    ... L185.0,233.0 L224.0,210.0 L260.0,242.0 L277.0,287.0 L278.0,208.0 
    ... L319.0,275.0 L320.0,220.0 L335.0,218.0 L345.0,248.0 L345.0,298.0 
    ... " style="stroke:purple; stroke-width:1; fill:purple"/>
    """
    
    def __init__(self, xorigin, yorigin, idlpath, lpoints, fillcolor, 
                 strokecolor="black"):
        self.xorigin = xorigin
        """@ivar: is the X-coordenate of the initial point of the path 
        @type: C{number}"""
        self.yorigin = yorigin
        """@ivar: is the Y-coordenate of the initial point of the path 
        @type: C{number}"""
        self.idlpath = idlpath
        """@ivar: is the identifier of path element in the SVG document 
        @type: C{string}"""
        self.lpoints = lpoints
        """@ivar: is the list of X-Y coordenates to drawn the line path
        @type: C{list of points}"""
        self.fillcolor = fillcolor
        """@ivar: If specified, the area under the plotted line to be 
        filled with the given color
        @type: C{string}"""
        self.strokecolor = strokecolor
        """@ivar: is the fill color of the plotted line
        @type: C{string}"""
        
    def printsvg(self):
        """
        Returns a string with the code for a path as follows::
        
        >>> print <path d="M (X-coordenate,Y-coordenate) L(X1-coordenate,
        ...       Y1-coordenate)...L(Xn-coordenate,Yn-coordenate)"
        ...       style="stroke:...; stroke-width:..; fill:...."/> 

        Where C{n=length of the points list}

        @return: SVG source code of the Linepath object.
        @rtype: C{string}
        """
        
        string = "<path id=\"" + self.idlpath + "\" d=\" M" + \
        str(float(self.lpoints[0][0]) + self.xorigin) + "," + \
        str(float(self.lpoints[0][1]) + self.yorigin) + " "
        for i in range(len(self.lpoints)):
            if i == len(self.lpoints):
                string += "L" + str(float(self.lpoints[i][0]) + self.xorigin)\
                + "," + str(float(self.lpoints[i][1]) + self.yorigin)
            else:    
                string += "L" + str(float(self.lpoints[i][0]) + self.xorigin)\
                + "," + str(float(self.lpoints[i][1]) + self.yorigin) + " "
        string += "\" style=\"stroke:" + self.strokecolor\
        + "; stroke-width:1; fill:" + self.fillcolor + "\"/>\n"  
        return string

############################################################################### 


class Gradient:
    """
    A gradient is a a smooth color transition from one shade to another. 
    Gradients can be linear, where the color transition occurs along a straight
    line, or radial, where the transition occurs along a circular path.
    
    This base class contains all elements to built LinearGradient objects. 
    To build this kind of construction must be taken into account the colors 
    you want at specific locations, called gradient stops
    
    The B{stop element} has two required attributes:
        - The C{stop-color} that indicates what color to use at that gradient 
          stop.
        - The C{stop offset} tells the point along the line at which the color
          should be equal to the stop-color. It is expressed as a percentage
          from 0 to 100% or as a decimal value from 0 to 1.0.
    """         
        
    def __init__(self, idgradient, initcolor, endcolor, initoffset, endoffset):
        self.idgradient = idgradient
        """@ivar: is the identifier of gradient element in the SVG document 
        @type: C{string}"""
        self.initcolor = initcolor
        """@ivar: is the initial color of gradient element 
        @type: C{string}"""
        self.endcolor = endcolor
        """@ivar: is the final color of gradient element 
        @type: C{string}"""
        self.initoffset = initoffset
        """@ivar: is the initial percentage from 0 to 100% of the stop 
        offset attribute  
        @type: C{number}"""
        self.endoffset = endoffset
        """@ivar: is the final percentage from 0 to 100% of the stop offset 
        attribute  
        @type: C{number}"""
    
    def printsvg(self):
        """
        Returns a string with the SVG code for the Gradient object 
        
        @return: SVG source code of the Gradient object.
        @rtype: C{string}
        """
        strgradient = "<defs>\n\
        <linearGradient id=\"" + self.idgradient + "\">\n\
        <stop offset=\"" + str(self.initoffset) + "%\" style=\"stop-color: "\
        + str(self.initcolor) + ";\"/>\n\
        <stop offset=\"" + str(self.endoffset) + "%\" style=\"stop-color: "\
        + str(self.endcolor) + ";\"/>\n\
        </linearGradient>\"\n\
        </defs>\n"
        return strgradient
    
###############################################################################


class Filter:
    """
    A filter is an artistic tool to create effects on a bitmap graphic. They 
    can produce blurred shadows, selectively thicken or thin lines, add 
    textures to part of the drawing, make an object appear to be embossed or 
    beveled, etc. 
    
    The filter class contains all the elements needed to build three types of
    filters:
        - A I{Shadow filter:} used to create a drop shadow by offsetting a gray
          ellipse underneath a colored ellipse.
        - A I{Lighting filter:} used to give depth to an object through the 
          illumination provided 
          by a light source in three dimensions
        - A I{Darkness filter:} used to give depth darkening of a portion of 
          the object which is applied
    
    The C{<filter>} element has attributes that describe the clipping region 
    for a filter.You specify an x, y, width, and height in terms of the 
    percentage of the filtered object's bounding box. 
    Between the beginning and ending <filter> tags are the filter primitives 
    that perform the operations 
    you desire. Each primitive has one or more inputs, and exactly one output. 
    An input can be the original graphic, specified as SourceGraphic, the alpha
    (opaqueness) channel of the graphic, specified as SourceAlpha, or the 
    output of a previous filtering primitive.
    """
    
    def __init__(self, idfilter, xfilter, yfilter, widthfilter, heightfilter, 
                 filterunits="objectBoundingBox"):
        self.idfilter = idfilter
        """@ivar: is the identifier of filter element in the SVG document 
        @type: C{string}"""
        self.xfilter = xfilter
        """@ivar: is the X-coordenate of <filter> element 
        @type: C{number}"""
        self.yfilter = yfilter
        """@ivar: is the Y-coordenate of <filter> element 
        @type: C{number}"""
        self.widthfilter = widthfilter
        """@ivar: is the width attribute of <filter> element 
        @type: C{number}"""
        self.heightfilter = heightfilter
        """@ivar: is the width attribute of <filter> element 
        @type: C{number}"""
        self.filterunits = filterunits
        """@ivar: Is a value that indicates units of measurement for each 
        attribute. It has a value of objectBoundingBox by default but if you 
        wish to specify boundaries in user units, then set the attribute's 
        value to userSpaceOnUse. 
        @type: C{string}"""
       
    def printshadowfilter(self): 
        """
        Returns a string with the SVG code for the Shadow filter object.
        
        This filter is built with several primitives:
            1. A B{C{feGaussianBlur}} primitive used to produce a drop shadow 
            on the object
            2. A B{C{feOffset}} primitive used to move the drop shadow to its 
            current position. 
            3. A B{C{feMerge}} primitive that encloses a list of
            {<feMergeNode>} elements, 
            each of which specifies an input. The inputs are stacked one on top
            of another in the order that they appear.
        
        @return: SVG source code of the Shadow filter objec.
        @rtype: C{string}
        """
        return "<feGaussianBlur in=\"SourceAlpha\" stdDeviation=\"4\"" + \
        " result=\"blur\"/>\n\
        <feOffset in=\"blur\" dx=\"4\" dy=\"4\" result=\"offsetBlur\"/>\n\
        <feMerge>\n\
        <feMergeNode in=\"offsetBlur\"/>\n\
        <feMergeNode in=\"SourceGraphic\"/>\n\
        </feMerge>\n"

    def printlightingfilter(self): 
        """
        Returns a string with the SVG code for Lighting filter object.
        
        This filter as above is built with several primitives:
            1. A B{C{feSpecularLighting}} primitive used to give highlights 
            rather than illumination.
            2. A B{C{fePointLight}} primitive that indicates what kind of light
            source is used, in this case we are using a point light source,
            which means a source that radiates light in all directions.
            3. A B{C{feComposite}} primitive that determines how to combine the
            results. This element takes two inputs, specified with the in and
            in2 attributes, and an operator that tells how the two are to be
            combined.
        
        @return: SVG source code for Lighting filter object.
        @rtype: C{string}
        
        """
        
        return self.printshadowfilter() + "<feSpecularLighting in=\"blur\"\n\
        lighting-color=\"antiquewhite\"\n\
        surfaceScale=\"1\"\n\
        specularConstant=\"0.8\"\n\
        specularExponent=\"20\"\n\
        result=\"specularOutput\">\n\
        <fePointLight x=\"-5000\" y=\"-10000\" z=\"20000\"/>\n\
        </feSpecularLighting>\n\
        <feComposite in=\"specularOutput\" in2=\"SourceGraphic\"\n\
        operator=\"in\" result=\"specularOutput\"/>\n\
        <feComposite in=\"specularOutput\" in2=\"SourceGraphic\"\n\
        operator=\"arithmetic\" k1=\"0\" k2=\"1\" k3=\"1\" k4=\"0\"/>\n"

    def printdarknessfilter(self, factor):

        """
        Returns a string with the SVG code for Darkness filter object.
        
        This filter uses only a B{C{feColorMatrix}} primitive which allows
        to change color values in a very generalized way. When the type 
        attribute equals matrix, you must set the value to a series of twenty
        numbers describing the transformation. 
        
        >>> print values=
        ...         "0 0 0 red 0
        ...          0 0 0 green 0 
        ...          0 0 0 blue 0 
        ...          0 0 0 1 0"

        Where the red, green, and blue values are decimal numbers which usually 
        range from zero to 1
        
        @param factor: is a decimal value from 0 to 1 which specify the 
        darkness percentage applied to the object  
        @type factor: C{number}
        
        @return: SVG source code for Darkness filter object.
        @rtype: C{string}
        
        """
        return "<feColorMatrix type=\"matrix\" \
                    values=\"" + str(factor) + " 0 0 0 0\n\
                             0 " + str(factor) + " 0 0 0\n\
                             0 0 " + str(factor) + " 0 0\n\
                             0 0 0 1 0\"/>\n"

    def printsvg(self):
        """
        Returns a string with the SVG code for selected filter object.
        
        @return: SVG source code for selected filter object.
        @rtype: C{string}
        """
        cab = "<defs>\n<filter id=\"" + self.idfilter + "\" filterUnits=\""\
        + self.filterunits + "\" x=\"" + str(self.xfilter) + "\" y=\""\
        + str(self.yfilter) + "\" width=\"" + str(self.widthfilter)\
        + "%\" height=\"" + str(self.heightfilter) + "%\">\n"
        end = "</filter>\n</defs>\n"
        if self.idfilter == "shadow":
            return cab + self.printshadowfilter() + end
        elif self.idfilter == "lighting":
            return cab + self.printlightingfilter() + end
        elif self.idfilter == "Darkness":
            return cab + self.printdarknessfilter("0.5") + end

###############################################################################
# Svgelements Objects: Inherited Classes 
###############################################################################


class Verticaltext(Text):
    """
        C{Verticaltext} is an intermediate structure used to build vertical 
        text. Adds an new attribute to the element text I{writting-mode} 
        that allows to write text in the new direction 
    """

    def __init__(self, xorigin, yorigin, fontsize, text, width):
        """
        @param xorigin: is the initial X-coordenate
        @type xorigin: number
        @param yorigin: is the initial Y-coordenate
        @type yorigin: number
        @param fontsize: is the font size text
        @type fontsize: number
        @param text: is a description of text element
        @type text: string
        """
        Text.__init__(self, xorigin, yorigin, fontsize, text) 
        self.widthverticaltext = width
        """@ivar: is the width of the object next to the C{Verticaltext} 
        object. This variable is used to align the text in the center of 
        the object
        @type: C{number} """
  
    def printsvg(self): 
        """
        Returns a string with the SVG code for Verticaltext objec
        
        @return: SVG source code of the Verticaltext object.
        @rtype: C{string}
        """
        string = "<text x=\"" + str(self.xorigintext) + "\" y=\""\
        + str(self.yorigintext) + "\" transform=\"translate(" + \
        str(int(self.widthverticaltext) / 2) + ",0)\" text-anchor=\"start\""\
        + " writing-mode=\"tb\" font-size=\"" + \
        str(self.fontsizetext) + "\" font-family=\"arial\"> " + str(self.text)\
        + " </text>\n"
        return string 

############################################################################### 


class Linetext (Line, Text):
    """ 
       C{Linetext} is an intermediate inherited structure used to build the 
       linetext elements 
       in the axis of the graphics. This class is developed with two object: 
           - C{Line object} that will be responsible for drawing the axis 
             lines in specific position depending 
             on the value of the C{yinc} parameter at any time.
           - C{Text object} used to write the value of the C{yinc} parameter
             next to the line.
    """
    def __init__(self, xorigin, yorigin, fontsize, text):
        """
        @param xorigin: is the initial X-coordenate
        @type xorigin: C{number}
        @param yorigin: is the initial Y-coordenate
        @type yorigin: C{number}
        @param fontsize: is the font size text
        @type fontsize: C{number} 
        @param text: is a description of the text element
        @type text: C{string} 
        """
        self.offsetxlt = 10
        """@ivar: is a fixed value that indicates the X axis displacement 
        suffered by both the line item as the item text on the original source 
        on that axis. 
        @type: C{number}  
        """
        Line.__init__(self, int(xorigin) - int(self.offsetxlt), int(yorigin), 
                      xorigin, int(yorigin), "no")
        Text.__init__(self, int(xorigin) - 4 * int(self.offsetxlt), 
                      int(yorigin), fontsize, text)
                     
    def printsvg(self):
        """
        Write the SVG code for the Linetext object
              
        @return: SVG source code of the Linetext object.
        @rtype: C{string}"""
        return Line.printsvg(self) + Text.printsvg(self)

############################################################################### 

     
class Linetextvertical(Line, Verticaltext):
    """ 
    Inherited class to draw a line element with vertical text. It's built
    whith two class instances:
    
        - A Line instance used to draw line axis
        - A Verticaltext instance used to draw the text
        
    We usually use this class in bar diagram and tree dimensions bar diagram
    for creating data in the x-axis when the width of the bars is less 
    than 25 units  
    
    """
    def __init__(self, xorigin, yorigin, fontsize, inc):
        """
        @param xorigin: is the initial X-coordenate
        @type xorigin: C{number}
        @param yorigin: is the initial Y-coordenate
        @type yorigin: C{number}
        @param fontsize: is the font size text
        @type fontsize: C{number} 
        """
        self.yoffsetltv = 10
        """@ivar: is a displacement in Y-axis applied to the object 
        @type: C{number}"""
        self.incltv = inc
        """@ivar:is an incremental value that indicates the origin of each line 
        with text in both the abscissa and the ordinate axis.
        @type: C{number}"""
        Line.__init__(self, xorigin, yorigin, xorigin, 
                      yorigin + self.yoffsetltv, "no")
        Verticaltext.__init__(self, xorigin, yorigin + 
                              1.5 * int(self.yoffsetltv), 
                              fontsize, str(self.incltv), 0)
        
    def printsvg(self):
        """
        Write the SVG code for the Linetextvertical object
              
        @return: SVG source code of the Linetextvertical object.
        @rtype: C{string}
        
        """           
        return Line.printsvg(self) + Verticaltext.printsvg(self)
    
###############################################################################

       
class Column(Rectangle):
    """
    Inherited class used to drawn a column object. This contains two 
    basic elements:
        - A Rectangle object
        - A Text object
    We generally use this element in bar diagram and tree dimensions bar 
    diagram for creating text bars top and bottom
    """
   
    def __init__(self, xtext, ytext, height, width, xorigin, yorigin, 
                 fillcolor, idrect, vals):
        """
        @param height: is the height of the rectangle element
        @type height: C{number}
        @param width: is the width of the rectangle element
        @type width: C{number}
        @param xorigin: is the initial X-coordenate
        @type xorigin: C{number}
        @param yorigin: is the initial Y-coordenate
        @type yorigin: C{number}
        @param fillcolor: is the fill color of the rectangle element
        @type fillcolor: C{string}
        @param idrect: is the identifier of the rectangle in SVG document
        @type idrect: C{string}
        """
        Rectangle.__init__(self, height, width, xorigin, yorigin, idrect, 
                           fillcolor)
        self.xtextcolumn = xtext
        """@ivar: is a description of the text at the bottom of the rectangle.
        @type: C{number}"""
        self.ytextcolumn = ytext
        """@ivar: is a description of the text above the rectangle.
        @type: C{number}"""
        self.vals = vals
        """@ivar: is true if the object needs extra top text, else False. 
        @type: C{boolean}"""
    
    def printsvg(self):
        """
        Returns a string with the SVG code for Column object. If width of the 
        rectangle exceeds 25 units bottom text will be drawn in the vertical 
        direction.

        @return: SVG source code of the Column object.
        @rtype: C{string} 
        """
        offset = 10
        fontsize = 13
        top = int(self.yoriginrect) - offset
        off = int(self.xoriginrect) + (int(self.widthrect) / 2 - offset)
        bottom = int(self.yoriginrect) + (2 * offset) + int(self.heightrect)   
        yaxistext = Text(off, top, fontsize, self.ytextcolumn)
        if int(self.widthrect) > 25:
            xaxistext = Text(off, bottom, fontsize, self.xtextcolumn)
        else: 
            xaxistext = Verticaltext(off, bottom, fontsize, self.xtextcolumn, 
                                     self.widthrect)
        if self.vals:
            string = Rectangle.printsvg(self) + yaxistext.printsvg()\
            + xaxistext.printsvg()   
        else: 
            string = Rectangle.printsvg(self) + xaxistext.printsvg() 
        return string

###############################################################################


class Hcolumn (Rectangle, Text):
    """
    Inherited class used to drawn a horizontal column object. As in the kind 
    column, this object is be composed of two basic classes:
        - A Rectangle class object
        - A Text class object
    We generally use this element to drawn the legends of the graphs
    """
   
    def __init__(self, hctext, xorigin, yorigin, fill, height, width, idgroup, 
                 idrect, idtext, mouseover="", mouseout="", filtered=False,
                 filterid="none"):
        """
        @param hctext: is a description of text element
        @type hctext: C{string}
        @param xorigin: is the initial X-coordenate
        @type xorigin: C{number}
        @param yorigin: is the initial Y-coordenate
        @type yorigin: C{number}
        @param fill: is the fill color of the rectangle element
        @type fill: C{string}               
        @param width: is the width of the rectangle element
        @type width: C{number}
        @param idrect: is the identifier of the rectangle in SVG document
        @type idrect: C{string}
        @param idtext: is the identifier of the text element in SVG document
        @type idtext: C{string}
        @param filtered: if specified some filter will be applied on the 
        object.
        @type filtered: C{boolean}
        @param filterid: is the identifier of the filter
        @type filterid: C{string}
               
        """
        Rectangle.__init__(self, height, width, xorigin, yorigin, idrect, fill,
                           filtered, filterid)
        Text.__init__(self, xorigin + height + 10, (yorigin + height / 2) + 4, 
                      10, hctext, "black", idtext)
        self.idgroup = idgroup
        """@ivar: is the identifier of the group, text and rectangle
        @type: string"""
        self.mouseover = mouseover
        """@ivar: is a variable that indicates what action happens when you 
        move the mouse over this element
        @type: string"""
        self.mouseout = mouseout
        """@ivar: is a variable that indicates what action happens when you 
        move the mouse out this element
        @type: string"""
            
    def printsvg(self):
        """
        Returns a string with the SVG code for Hcolumn object.             
        
        @return: SVG source code of the Hcolumn object.
        @rtype: C{string} 
        """        
        string = "<g id=\"" + self.idgroup + "\" onmouseover=\"" + \
        self.mouseover + "" + "\" onmouseout=\"" + self.mouseout + "\">\n" + \
        Rectangle.printsvg(self) + Text.printsvg(self) + "</g>\n"
        return string

###############################################################################

 
class Rectangle3d(Rectangle, Polygon):
    """
    Inherited class used to drawn a rectangle object in three dimensions. 
    This object is be composed of two basic elements:
       - A Rectangle object
       - Two Polygon objects
    To begin adding a new parameter to the class initializer:
        - C{offset3d}: Representing the horizontal and vertical scrolling to 
        simulate depth.
    The aim is to draw the bar chart in two dimensions by adding the right side
    and roof to convert the rectangle into a cube. 
    
    >>>         _________     
    ...        /________/|     | yoffset3d
    ...        |       | |     
    ...        |       | |
    ...        |_______|/
    ...                 __
    ...                     Xoffset3d  
    
    Both elements will be drawn with a polygon element. The list of points will
    be the next:
   
    >>> Roof polygon: [[xorigin,yorigin],[xorigin+offset3d,yorigin-offset3d],
    ...               xorigin+width+offset3d,yorigin-offset3d],
    ...               [xorigin+width,yorigin]]
    ...
    ... Side polygon: [[xorigin+width,yorigin],[xorigin+width+offset3d,
    ...                yorigin-offset3d],[xorigin+width+offset3d,yorigin+
    ...                height-offset3d],[xoriginr+self.width,yorigin+height]] 
    """   
    
    def __init__(self, height, width, xorigin, yorigin, fillcolor, idrect,
                 filtered, filterid, offset):
        
        """
        @param height: is the height of the rectangle element
        @type height: C{number}
        @param width: is the width of the rectangle element
        @type width: C{number}
        @param xorigin: is the initial X-coordenate
        @type xorigin: C{number}
        @param yorigin: is the initial Y-coordenate
        @type yorigin: C{number}
        @param fillcolor: is the fill color of the rectangle element
        @type fillcolor: C{string}
        @param idrect: is the identifier of the rectangle in SVG document
        @type idrect: C{string}
        @param filtered: if is specified indicates that applies a filter on the
        object element       
        @type filtered:C{boolean}
        @param filterid: is the filter identifier
        @type filterid: C{string}               
        """
        
        self.offset3d = offset
        """@ivar: is the horizontal and vertical scrolling to simulate depth.
        @type: C{number}"""
        self.fillcolor3d = fillcolor
        """@ivar: is the fill color of the rectangle 3d
        @type: C{string}"""
        Rectangle.__init__(self, height, width, xorigin, yorigin, idrect,
                           fillcolor)
        Polygon.__init__(self, [[xorigin, yorigin], [xorigin + self.offset3d,
                        yorigin - self.offset3d], [xorigin + int(width) + 
                        self.offset3d, yorigin - self.offset3d], [xorigin + 
                        int(width), yorigin]], "polygonTop", fillcolor, 
                        filtered, filterid)
        
    def printsvg(self):
        """
        Returns a string with the SVG code for Rectangle3d object. 
        
        @return: SVG source code of the Rectangle3d object.
        @rtype: C{string} 
        """
        lpointside = [[self.xoriginrect + int(self.widthrect),
        self.yoriginrect], [self.xoriginrect + int(self.widthrect) +
        self.offset3d, self.yoriginrect - self.offset3d], [self.xoriginrect +
        int(self.widthrect) + self.offset3d, self.yoriginrect + 
        int(self.heightrect) - self.offset3d], [self.xoriginrect + 
        int(self.widthrect), self.yoriginrect + int(self.heightrect)]] 
                  
        polygonright = Polygon(lpointside, "polygonRight", self.fillcolor3d, 
                               self.polygonfiltered, self.polygonfilterid)
        string = Rectangle.printsvg(self) + Polygon.printsvg(self) + \
                                            polygonright.printsvg()     
        return string
    
###############################################################################

   
class Column3d(Rectangle3d):
    """
        Inherited class used to drawn a column object in three dimensions. 
        This object is be composed of two basic elements:
    
           - A three dimensions Rectangle object
           - Two text object
    """
    def __init__(self, xtext, ytext, height, width, xorigin, yorigin, 
                 fillcolor, idrect, filtered, filterid, offset, vals):
        """
        @param height: is the height of the 3d rectangle element
        @type height: C{number}
        @param width: is the width of the 3d rectangle element
        @type width: C{number}
        @param xorigin: is the initial X3d-coordenate
        @type xorigin: C{number}
        @param yorigin: is the initial Y3d-coordenate
        @type yorigin: C{number}
        @param fillcolor: is the fill color of the 3d rectangle element
        @type fillcolor: C{string}
        @param idrect: is the identifier of the 3d rectangle in SVG document
        @type idrect: C{string}
        """
        Rectangle3d.__init__(self, height, width, xorigin, yorigin, fillcolor,
                             idrect, filtered, filterid, offset)
        self.xtextc3d = xtext
        """@ivar: is a description of the text at the bottom of the 3d 
        rectangle.
        @type: C{number}"""
        self.ytextc3d = ytext
        """@ivar: is a description of the text at the top of the 3d rectangle.
        @type: C{number}"""
        self.vals = vals
        """@ivar: is true if the object needs extra top text, else False. 
        @type: C{boolean}"""
     
    def printsvg(self):
        """
        Returns a string with the SVG code for 3d Column object. If width of 
        the 3d rectangle exceeds 25 units bottom text will be drawn in the 
        vertical direction.
                
        @return: SVG source code of the 3d Column object.
        @rtype: C{string} 
        """
        fontsize = 14
        top3d = int(self.yoriginrect) - self.offset3d
        xoffset3d = int(self.xoriginrect) + (int(self.widthrect) / 2)
        bottom3d = int(self.yoriginrect) + (1.5 * self.offset3d) + \
        int(self.heightrect)
        toptext = Text(xoffset3d, top3d, fontsize, self.ytextc3d)
        if int(self.widthrect) <= 25:
            bottomtext = Verticaltext(self.xoriginrect, bottom3d, fontsize,
                                       self.xtextc3d, self.widthrect)
        else:         
            bottomtext = Text(self.xoriginrect, bottom3d, fontsize, 
                               self.xtextc3d)
        if self.vals:
            string = Rectangle3d.printsvg(self) + toptext.printsvg() + \
            bottomtext.printsvg()
        else:
            string = Rectangle3d.printsvg(self) + bottomtext.printsvg()      
        return string  

###############################################################################
# Svgelements Objects: Graphics Classes 
###############################################################################

 
class Piechart:
    """
    
    Pie chart:
    ==========
       
    A pie chart (or a circle graph) is a circular chart divided into sectors, 
    illustrating proportion. In a pie chart, the arc length of each sector 
    I{(and consequently its central angle and area)}, is proportional to the 
    quantity it represents.
    
    The size of each central angle is proportional to the size of the 
    corresponding quantity. The sum of the central angles has to be C{360 
    degrees}, the central angle for a quantity that is a fraction C{K} of the
    total is C{360K} degrees. 
    
    Input data are organized in a table that shows three data columns:
        - First column lists the description of each data group.
        - Second column represents the value of each group
        - Third column shows the color assigned in the pie chart for each 
        group.
      
    
    Example:
    ========
    
    The following example chart is based on preliminary results of a 
    election for the European Parliament.
    The table lists the number of seats allocated to each party group. 
    
    
    >>>   Group     Seats     Colorfield     
    ...    EUL       39         darkred    
    ...    PES      200         crimson
    ...    EFA       42         forestgreen    
    ...    EDD       15         khaki     
    ...    ELDR      67         gold     
    ...    EPP      276         darkblue     
    ...    UEN       27         cornflowerblue     
    
    Animating Pie Chart:
    ====================
    
    There are two methods of making graphic images move:
        - The first method, animation, is movement that is controlled by the 
        author. 
    
    >>> <rect x="10" y="10" width="200" height="20" stroke="black" fill="none">
    ... <animate attributeName="width" attributeType="XML" from="200" to="20"
    ... begin="0s" dur="5s" fill="freeze" />
    ... </rect>
    
        - The second method, scripting, lets the user viewing the graphic 
        interact with and modify the image. 
          
    >>>    <script type="text/ecmascript">
    ...    <![CDATA[
    ...    function enlarge_circle(evt){
    ...        var circle = evt.getTarget();
    ...        circle.setAttribute("r", 50);}
    ...    ]]>
    ...    </script>
    ...
    ...    <circle cx="150" cy="100" r="25" fill="red"
    ...            onmouseover="enlarge_circle(evt)"  
    ...    <text x="150" y="175" style="text-anchor: middle;">
    ...    Mouse over the circle to change its size.
    ...    </text>

    
    A Script is a program writed in JavaScript to interact with a SVG graphic. 
    Interaction occurs when graphic objects respond to events.The term CDATA,
    meaning character data, is used for distinct, but related, purposes in the
    markup languages SGML and XML. 
    The term indicates that a certain portion of the document is general 
    character data, rather than non-character data or character data with a
    more specific, limited structure.
    
    In our case when the user moves the mouse over each sector of pie chart or
    legend was launched by an event called C{"animationOn"} that will change 
    the attribute C{"transform"} to grow the object to a C{scale factor} of 
    1,5. Also while the program grows the pie slices or rectangles legend 
    applies a gradient on each sector of the chart.
    """  
        
    def __init__(self, xorigin, yorigin, radius, listvalues, values, labels,
                 colorfld, legend, animate, filtered, title, strokewidth=0):
        self.xorigin = xorigin
        """@ivar: is the X initial coordinate of the graph. 
        @type: C{number}"""
        self.yorigin = yorigin
        """@ivar: is the Y initial coordinate of the graph. 
        @type: C{number}"""
        self.radius = radius
        """@ivar: specifies the radius of the circumference of the pie.
        @type: C{number}"""
        self.strokewidth = strokewidth
        """@ivar: is the width of the outer circle of the pie chart. 
        @type: C{number}"""
        #{Input Data
        self.listvalues = listvalues
        """@ivar: is the list of input data
        @type: C{list of values}"""
        self.values = values
        """@ivar: Identifies the data field that will hold numeric values for
        the pie slices.
        @type: C{number}"""
        self.labels = labels
        """@ivar: Identifies the data field that will hold labels for the pie
        slices.
        @type: C{number}"""
        self.colorfld = colorfld
        """@ivar: Identifies the data field that will hold colors for the pie
        slices.
        @type: C{number}"""
        #}
        self.title = title
        """@ivar: Specify pie title
        @type: C{string}"""
        self.legend = legend
        """@ivar: If is specified controls the placement of the legend
        @type: C{boolean}"""
        #{Effects        
        self.animate = animate
        """@ivar: If is specified the pie chart contains animations
        @type: C{boolean}"""            
        self.filtered = filtered 
        """@ivar: If is specified some filter will be applied to the pie chart.
        @type: C{boolean}"""
        #}
        #{Values and Radian Control
        self.sumvalues = 0
        """@ivar: This variable stores the total sum of input values
        @type: C{number}"""
        self.radianvalues = ""
        """@ivar: is a list of radian values of input values
        @type: C{list}"""
        self.initianradian = 0
        """@ivar: is the initial radian from which draw each pie chart sector
        @type: C{float number}"""       
        #}
        #{Control position
        self.xradius = self.xorigin + self.radius
        """@ivar: is the X-coordenate of the center of the circle 
        @type: C{number}"""
        self.yradius = self.yorigin + self.radius
        """@ivar: is the Y-coordenate of the center of the circle 
        @type: C{number}"""
        self.pos = 0
        """@ivar: is the position of the sector in the pie chart
        @type: C{number}"""
        #}
        #{Legend
        self.xtranslatefactor = 75
        """@ivar: is the translation in X axis suffered during animation legend
        @type: C{number}"""
        self.ytranslatefactor = 10
        """@ivar: is the translation in Y axis suffered during animation legend
        @type: C{number}"""
        self.yposlegend = 10
        """@ivar: represents the separation of each rectangle of the legend on
        the y axis
        @type: C{number}"""
        self.pielegendsize = 20
        """@ivar: represents the size of each rectangle of the legend
        @type: C{number}"""
        self.yinitorigin = self.yorigin
        """@ivar: is the initial coordinate in the Y axis of each rectangle of
        the legens
        @type: C{number}"""
        #}
        self.totalsum()
        self.valuestoradians()    
 
    def totalsum(self):
        """
        Returns the sum of the column of data file specified by the parameter
        named values.
        
        @return: The sum of input data column specified by the parameter named
        values.
        @rtype: C{number} 
        
        """
        for value in self.listvalues[int(self.values) - 1]:
            self.sumvalues += int(value)
        return self.sumvalues
    
    def valuestoradians(self):
        """
        Returns the values of the column of data file specified by the 
        parameter named value into degrees.
        
        To achieve this, multiply each value in the list for two pi and divide
        by the sum of values
        
        >>>                listValues[value]*2*pi
        ... radianValue = --------------------------
        ...                    sumValues
        
        @return: values of the column of data file specified by the parameter
        named value into degrees.
        @rtype: C{list of float number}
        
        """
        self.radianvalues = [(int(value) * 2 * pi) / self.sumvalues for value 
                             in self.listvalues[int(self.values) - 1]]  
        return self.radianvalues     
 
    def getanimationscript(self):
        
        """
        Returns the JavaScript code that runs when an event occurs.
        
        This code is based primarily on size and time animations 
        by modifying the attributes of scale and translation of objects.
        
            - B{I{Function animationOn(id):}}This function is activated 
              when you put the mouse on the object caller:
              
              >>> function animationOn(id){
              ...    timevalue = - timerincrement;  [1]
              ...    pie = document.getElementById(id);
              ...    legendrect = document.getElementById(id+'rect');
              ...    legendtext = document.getElementById(id+'text');
              ...    initcolor = pie.getAttribute("fill");
              ...    pie.setAttribute("fill", "url(#" + id + "gradient)");  [2]
              ...    scaleIn();    [3]              
              ...    if (legendrect != null)
              ...       legendscaleIn(); [3]
              ...    }
              
               
                1. Update the timer to the initial value
                2. Add an element gradient in the sector on which the animation
                takes place
                3. Release functions responsible for generating the animation:
                    1. B{I{Function ScaleIn():}}This role will be responsible
                    for generating the animation of the selected sector of
                    pie chart.
                         
                       >>> function scaleIn() {
                       ...    timevalue = timevalue + timerincrement;
                       ...    if (timevalue > maxtime)    [1]
                       ...     return;
                       ...    scalefactor = ...;    [2]
                       ...    xtranslatefactor = ...;
                       ...    ytranslatefactor =...;
                       ...    pie.setAttribute("transform", "scale(scalefactor)
                       ...    translate(xtranslatefactor,
                       ...    ytranslatefactor)");    [3]
                       ...    setTimeout("scaleIn()",timerincrement);}    [4]
                                                
                             - First check if the animation has reached the end
                               by checking 
                               the timer, if so, return of function.     B{[1]}
                             - The following is to establish the scale factor 
                               which will 
                               progressively increase from 1 to 1.5    B{[2]}
                             - Third modify the attributes of scale and 
                               translation to achieve the desired magnification 
                               effect.    B{[3]}
                            -  Finally with C{setTimeout} launch function again 
                               after waiting the time specified by the variable 
                               C{timer_increment}    B{[4]}
                               
                    2. B{I{Function LegendScaleIn():}} This function will 
                    generate the animation in the legend for the selected 
                    sector.
                    
                        >>> function legendscaleIn(){
                        ...    xlegendscalefactor=1.5;    [1]
                        ...    xlegendtranslatefactor = 
                        ...    (( - xlegendscalefactor * 375) + 370) / 
                        ...    xlegendscalefactor;    [2]
                        ...    if (legendrect != null){
                        ...        legendrect.setAttribute("xradius", "5"); [3]
                        ...        legendrect.setAttribute("yradius", "5"); [3]
                        ...        legendrect.setAttribute("transform", 
                        ...        "scale(" + xlegendscalefactor + "," 
                        ...         + 1 + ")    [4]
                        ...        legendtext.setAttribute("font-weight", 
                        ...        "bold");
                        ...        legendtext.setAttribute("stroke", 
                        ...        init_color);}   [5]
                        ...      }     
                            
                        - First set the scale factor to 1.5 B{[1]}
                        - Second we set the translation factor . B{[2]}. 
                        - The next thing is specify the x- and y-radius of the
                          corner curvature to Round the legend rectangle B{[3]}   
                        - To give effect expansion scale only the x-axis and
                          shifting the rectangle to the left of this axis
                          B{[4]}
                        - Finally we modify the style attribute to make the
                          text legend in bold and the same color of each sector
                          of the pie chart  B{[5]}
       
            - B{I{Function animationOff(id):}}This function is responsible for
            turnning off the animation when the mouse leaves the area of that 
            item. It used the function C{"MouseOut"}
                - B{I{function MouseOut():}} Restores the initial values prior
                  to the animation:
                
                        >>> function mouseOut() {
                        ...    timevalue = maxtime;
                        ...    pie.setAttribute("transform", "scale(1)");
                        ...    pie.setAttribute("fill", initcolor);
                        ...    if (legendrect != null){
                        ...         legendrect.setAttribute("transform", 
                        ...         "scale(1)");
                        ...         legendrect.setAttribute("fill",init_color);
                        ...         legendrect.setAttribute("xradius", "0");
                        ...         legendrect.setAttribute("yradius", "0");
                        ...         legendtext.setAttribute("font-weight", 
                        ...         "normal");
                        ...         legendtext.setAttribute("stroke", 
                        ...         "black");}}    
   
        
        @return: Javascript source code for the animation of the chart.
        @rtype: C{string}      
            
        """
        
        return "  <script type=\"text/javascript\">\n\
       <![CDATA[\n\
       var timerincrement = 100;\n\
       var timevalue=0;\n\
       var maxtime = 3000;\n\
       var initcolor;\n\
       var legend;\n\
       var legendrect;\n\
       var pie;\n\
       var evt;\n\
       function animationOn(id){\n\
            timevalue = - timerincrement;\n\
            pie = document.getElementById(id);\n\
            legendrect = document.getElementById(id + 'rect');\n\
            legendtext = document.getElementById(id + 'text');\n\
            initcolor = pie.getAttribute(\"fill\");\n\
            pie.setAttribute(\"fill\", \"url(#\" + id + \"gradient)\");\n\
            scaleIn();\n\
            if (legendrect != null)\n\
                legendscaleIn();\n\
            }\n\
        function scaleIn() {\n\
            timevalue = timevalue + timerincrement;\n\
            if (timevalue > maxtime)\n\
                return;\n\
            scalefactor = 1 + timevalue / (2 * maxtime);\n\
            xtranslatefactor = (( - scalefactor * " + str(float(self.xradius))\
            + ") + " + str(float(self.xradius)) + ")/scalefactor;\n\
            ytranslatefactor = (( - scalefactor * " + str(float(self.yradius))\
            + ")+" + str(float(self.yradius)) + ")/scalefactor;\n\
            pie.setAttribute(\"transform\", \"scale(\"+scalefactor+\") "\
            "translate(\" + xtranslatefactor+\", \" + ytranslatefactor + "\
            "\")\");\n\
            setTimeout(\"scaleIn()\", timerincrement);\n\
        }\n\
        function legendscaleIn(){\n\
            xlegendscalefactor = 1.5;\n\
            xlegendtranslatefactor = (( - xlegendscalefactor * " + \
            str(self.xradius + self.xorigin + self.xtranslatefactor) + ") +" \
            + str(self.xradius + self.xorigin + self.xtranslatefactor - \
                self.pielegendsize / 4) + ") / xlegendscalefactor;\n\
            legendrect.setAttribute(\"rx\", \"5\");\n\
            legendrect.setAttribute(\"ry\", \"5\");\n\
            legendrect.setAttribute(\"transform\", \"scale(\" + "\
            "xlegendscalefactor+\",\" + 1 + \") translate(\" + "\
            "xlegendtranslatefactor+\", \" + 0 + \")\");\n\
            legendtext.setAttribute(\"font-weight\", \"bold\");\n\
            legendtext.setAttribute(\"stroke\",initcolor);\n\
        }\n\
        function animationOff(id){\n\
            mouseOut();\n\
        }\n\
        function mouseOut() {\n\
            timevalue = maxtime;\n\
            pie.setAttribute(\"transform\", \"scale(1)\");\n\
            pie.setAttribute(\"fill\", initcolor);\n\
            if (legendrect != null){\n\
                legendrect.setAttribute(\"transform\", \"scale(1)\");\n\
                legendrect.setAttribute(\"fill\", initcolor);\n\
                legendrect.setAttribute(\"rx\", \"0\");\n\
                legendrect.setAttribute(\"ry\", \"0\");\n\
                legendtext.setAttribute(\"font-weight\", \"normal\");\n\
                legendtext.setAttribute(\"stroke\", \"black\");}\n\
        }\n\
       ]]>\n\
      </script>\n\n"
    
    def printsvg(self):
        """Returns a string with SVG code for pie chart.
             
        Analyzing the pie chart we can see that is composed 
        of two distinct parts, the pie and the legend
            1. The B{I{"cake" or set of sectors:}} Is composed of many path,
            text and gradient elements as values are set in the input data. 
            These values are converted to radians to set the correct X, Y 
            coordinates of each sector by using the C{ValuestoRadians} 
            function. To draw this part of the graph must take into account 
            the following:
                    
                - First find the percentage at which each input value is equal. 
                  This percentage will draw a text element, which will be
                  positioned next 
                  to the corresponding sector. Because this element grow to the
                  right will increase its separation from the sector by 
                  20% between 135 degrees (3/4 S{pi}) and 225 degrees 
                  (5/4 S{pi}). B{[1]}
                - Then set the color needed to apply the gradient effect to
                  each piece of the pie. B{[2]}
                - Before drawing any sector will be checked first if there 
                  are animated by checking the value of the variable 
                  C{self.animate} B{[3]}
                - The initian radian be continuously updated so that each 
                  sector is in the correct position. B{[4]}  
                     
                >>> for value in listradianvalues:        
                ... ...
                ...    if (initianradian + radianvalues[pos] / 2 > 
                ...    (3 * pi / 4))
                ...    and (initianradian + radianvalues[pos] / 2 < 
                ...    (5 * pi / 4)):
                ...         percentage = Text(xradius + cos(initianradian + 
                ...         radianvalues[pos] / 2) * (radius * 1.4),
                ...         yradius + sin(initianradian + radianvalues[pos] / 
                ...         2) * (radius * 1.4), 10, str(sectorvalue) + "%", 
                ...         "black", nameid + "%text")    [1]
                ...    else:
                ...         percentage = Text(xradius + cos(initianradian + 
                ...         radianValues[pos] / 2) * (radius * 1.2),
                ...         yradius + sin(initianradian + radianvalues[pos] / 
                ...         2) * (radius * 1.2), 10, str(sectorvalue) + "%", 
                ...         "black", nameid + "%text")
                ...     
                ...    colorgradient = listvalues[colorfld][pos]        [2]
                ...    gradient = Gradient(nameid + "gradient", colorgradient,
                ...               "white", 0, 100)
                ...    ...
                ...    if animate:    [3]
                ...         piesector = Path(xradius, yradius, radius, 
                ...         strokewidth, listvalues, colorfld, 
                ...         radianvalues[pos], pos, initianradian, nameid, 
                ...         mouseover, mouseout, filtered, "lighting")
                ...    else: 
                ...         piesector = Path(xradius, yradius, radius,
                ...         strokewidth, listvalues, colorfld, 
                ...         radianvalues[pos], pos, initianradian, "", "", "",
                ...         filtered, "lighting")
                ...   string += piesector.printsvg()+ percentage.printsvg()       
                ...   initianradian += radianvalues[pos]    [4]
                ...   ...

            2. The B{I{Legend:}} Is composed of many elements Hcolumn, 
            as input values have. 
                >>> for value in radianValues:
                ... ... 
                ...    if legend:
                ...       if animate:
                ...          pielegend = Hcolumn(listvalues[labels][pos], 
                ...          xradius + radius + xtranslatefactor, yinitorigin, 
                ...          listvalues[colorfld][pos], pielegendsize, 
                ...          pielegendsize, nameid + "legend", nameid + "rect",
                ...          nameid + "text", mouseover, mouseout, filtered, 
                ...          "lighting")
                ...       else: 
                ...          pielegend = Hcolumn(listvalues[labels][pos], 
                ...          xradius + radius + xtranslatefactor, yinitorigin, 
                ...          listvalues[colorfld][pos], pielegendsize,
                ...          pielegendsize, nameid + "legend", nameid + "rect",
                ...          nameid + "text", "", "", filtered, "lighting")
                ...    string += pielegend.printsvg()  
                ...     ...
            
        As elements of both parts we have the decorations and improvements 
        applied to the base diagram: Filters and animation
            - B{First} we create instances of these classes filters to 
              create optical effects in the graph. A light filter with 
              the ID "ligthing" in the sectors as well as the legend 
              and a dark filter with the ID "shadow" in the outer circle
              to give a sense of depth
              
              >>> shadowfilter = Filter("shadow", 0, 0, 120, 120, 
              ...                       "userSpaceOnUse")
              ... lightingfilter = Filter("lighting", 0, 0, 120, 120)
              ... ...
              ... string += shadowfilter.printsvg() + lightingfilter.printsvg()
              
            - B{Secondly} animation check by checking the value of the
            parameter C{self.animate}. 
              >>> if self.animate:
              ...  string = self.getanimationscript()
        
        @return: SVG source code for pie chart.
        @rtype: C{string} 
        
        """
        try:
            #Filter Instances needed to build the optical effects for the pie 
            #chart
            string = ""
            if (len(self.listvalues) != int(self.colorfld)):
                try:
                    raise ValueError
                except ValueError:
                    print "Incorrect input data"\
                    + "\nPlease check the number of columns in the input"\
                    + "file" + "\nFor help use --help or -h"\
                    + "\nPysvg 0.0.4-Nov2011\nCopyright (C) 2011 Isabel "\
                    + "Rodriguez \nYou can see the full documentation at URL:"\
                    + " \"http://www.pysvg/orgfree.com\""                     
                    sys.exit(2)
            shadowfilter = Filter("shadow", 0, 0, 120, 120, "userSpaceOnUse")
            lightingfilter = Filter("lighting", 0, 0, 120, 120)
            circle = Circle(self.xradius, self.yradius, self.radius, 
                            self.strokewidth, "black", "black", self.filtered,
                            "shadow")
            #checking animation
            if self.animate:
                string += self.getanimationscript()    
            # Draw filters    
            string += shadowfilter.printsvg() + lightingfilter.printsvg() + \
            circle.printsvg()
            # Draw pie chart
            for value in self.radianvalues:
                nameid = "pie" + str(self.pos)
                mouseover = "animationOn('" + nameid + "');"
                mouseout = "animationOff('" + nameid + "');"
                sectorvalue = float(float(self.listvalues[int(self.values) - 1]
                              [self.pos]) / float(self.sumvalues) * 100)
                sectorvalue = round(sectorvalue, 1)
                if ((self.initianradian + value / 2 > (3 * pi / 4)) and
                (self.initianradian + value / 2 < (5 * pi / 4))):
                    percentage = Text(self.xradius + cos(self.initianradian + 
                                     value / 2) * (self.radius * 1.4), 
                                     self.yradius + sin(self.initianradian + 
                                     value / 2) * (self.radius * 1.4), 10, 
                                     str(sectorvalue) + "%", "black", nameid + 
                                     "%text")
                else:
                    percentage = Text(self.xradius + cos(self.initianradian + 
                                 value / 2) * (self.radius * 1.2), 
                                 self.yradius + sin(self.initianradian + 
                                 value / 2) * (self.radius * 1.2), 10, 
                                 str(sectorvalue) + "%", "black", nameid +
                                 "%text")
                string += percentage.printsvg()          
                colorgrad = self.listvalues[int(self.colorfld) - 1][self.pos]
                gradient = Gradient(nameid + "gradient", colorgrad, 
                           "white", 0, 100)
                string += "<!-- ***** PATH,GRADIENT,LEGEND " + str(self.pos)\
                + " ***** -->\n" + gradient.printsvg()
                if self.animate:
                    piesector = Path(self.xradius, self.yradius, self.radius, 
                                self.listvalues, self.colorfld, value, 
                                self.pos, self.initianradian, nameid, 
                                mouseover, mouseout, self.filtered, "lighting")
                else: 
                    piesector = Path(self.xradius, self.yradius, self.radius, 
                                self.listvalues, self.colorfld, value, 
                                self.pos, self.initianradian, nameid, "", "",
                                self.filtered, "lighting")         
                self.initianradian += value
                string += piesector.printsvg()
                #Checking and drawning the legend
                if self.legend:
                    if self.animate:
                        pielegend = Hcolumn(self.listvalues[int(self.labels) 
                                    - 1][self.pos], self.xradius + self.radius
                                    + self.xtranslatefactor, self.yinitorigin,
                                    self.listvalues[int(self.colorfld) - 1]
                                    [self.pos], self.pielegendsize, 
                                    self.pielegendsize, nameid + "legend",
                                    nameid + "rect", nameid + "text", 
                                    mouseover, mouseout, self.filtered,
                                    "lighting")
                    else: 
                        pielegend = Hcolumn(self.listvalues[int(self.labels) 
                                    - 1][self.pos], self.xradius + self.radius
                                    + self.xtranslatefactor, self.yinitorigin,
                                    self.listvalues[int(self.colorfld) - 1]
                                    [self.pos], self.pielegendsize,
                                    self.pielegendsize, nameid + "legend",
                                    nameid + "rect", nameid + "text", "", "",
                                    self.filtered, "lighting")
                    string += pielegend.printsvg()
                
                self.pos += 1
                self.yinitorigin += self.pielegendsize + self.yposlegend
            if self.title != "":
                pietitle = Text(self.xradius, self.yorigin / 2, 14, self.title)
                string += pietitle.printsvg()                
            return string
        except IndexError:
            print "The number of columns in data file must be equal to the "\
            + "maximum value indicated by the parameters x, y, x2, y2\n"\
            + "Please review the input data \nFor help use --help"
            sys.exit(2)         
    
###############################################################################


class Bardiagram:
    """
    Bar Chart
    =========
    
    A bar chart or bar graph is a chart with rectangular bars with 
    lengths proportional to the values that they represent.
    Bar charts are used for plotting discrete data which has 
    discrete values. This is very useful if you are trying to 
    record certain information data.
    
    This chart has an added enhancement that allows represent 
    two groups of discrete data to compare with each other.
    If y and y2 are specified, two sets of bars will 
    be produced. These components Identify the data field 
    that will hold Y axis.
    
    As the pie chart this chart have the graphic element 
    and a legend element, both formed by the combination 
    of several basic elements.
    
    
    Input Data
    ==========
    
        If the component y2 is not specified input data must be arranged in a 
        table that shows two data columns:
            - First column lists the description of each data group. (X-axis
            data)
            - Second column represents the value of each group (Y-axis data)
        Otherwise input data must be organized in a table with three data 
        columns
            - First column lists the description of each data group.
            (X-axis data)
            - Second column represents the first values group (Y-axis data)
            - Third column shows the second values group (Y2-axis data) 
     
             >>>   Group   Seats(2004)     Seats(1999)
             ...    EUL         666         49  
             ...    EFA         42          56
             ...    EDD         15          19
             ...    ELDR        67          60
             ...    EPP         276         272
             ...    UEN         27          36
             ...    Other       66          29
        
    """ 
   
    def __init__(self, lval, xcolumn, ycolumn, ycolumn2, barwidth, xorigin, 
                 yorigin, delim, vals, yinc, yrange, ygrid, fillcolor,
                 fillcolor2, name, name2, title, legend):
        #{Input Data
        self.lval = lval
        """@ivar:Represents the list of input values
        @type:C{list of values}"""
        self.xcolumn = xcolumn
        """@ivar:Identifies the data field that will hold X component.
        @type: C{number}""" 
        self.ycolumn = ycolumn
        """@ivar:Identifies the data field that will hold Y component.
        @type:C{number}""" 
        self.ycolumn2 = ycolumn2
        """@ivar:Identifies the data field that will hold Y2 component.
        @type:C{number}"""  
        #}     
        #{Position
        self.xorigin = xorigin
        """@ivar: Is the X initial coordinate of the graph. 
        @type:C{number}"""
        self.yorigin = yorigin
        """@ivar: Is the Y initial coordinate of the graph. 
        @type:C{number}"""
        self.yinc = yinc
        """@ivar:Specify a numeric axis increment amount normally one value.
        @type:C{number}"""        
        self.yrange = yrange
        """@ivar:Specify an explicit axis numeric range usually the minimum. 
        @type: C{number}"""
        #}
        #{Style
        self.barwidth = barwidth
        """@ivar: Specifies the width of the filled bars.
        @type: C{number}"""       
        self.delim = delim
        """@ivar: Specifies the separation between bars or groups of bars. 
        @type: C{number}"""
        self.vals = vals
        """@ivar:If is specified, display numeric values near the top of each 
        bar. 
        @type: C{number}"""        
        self.ygrid = ygrid
        """@ivar: If specified, grid lines will be drawn.mum 
        @type: C{yes or no}"""
        self.fillcolor = fillcolor
        """@ivar: Color of first group of bars
        @type: C{string}"""
        self.fillcolor2 = fillcolor2
        """@ivar: Color of second group of bars
        @type: C{string}"""
        #}     
        #{title and Legend
        self.legend = legend
        """@ivar: If is specified controls the placement of the legend
        @type: C{boolean}"""        
        self.name = name
        """@ivar: Specifies legend label of first input data group
        @type: C{string}"""
        self.name2 = name2
        """@ivar: Specifies legend label of second input data group
        @type: C{string}"""
        self.title = title
        """@ivar: If is specified, a plot title to be centered at the top.
        @type: C{string}"""
        #}
        self.heightmaxbar = 0
        """@ivar: is an auxiliary variable that stores the height of the bar
        higher.
        @type: C{number}"""        
        
        try:
            self.setmaximumbars(lval)
        except IndexError:
            print "The number of columns in data file must be equal to the"\
            + "maximum value indicated by the parameters x, y, x2, y2\n"\
            + "Please review the input data \nFor help use --help"\
            + "\nPysvg 0.0.4-Nov2011\nCopyright (C) 2011 Isabel Rodriguez"\
            + "\nYou can see the full documentation at URL:"\
            + " \"http://www.pysvg/orgfree.com\""             
            sys.exit(2) 

    def setmaximumbars(self, lval):
        """
        Auxiliary function which returns in the variable 
        C{self.heightmaxbar} maximum value from the list of ycolumn and 
        ycolumn2 input data.
        
        @return: Height of the bar higher
        @rtype: C{string}
        """
        try:
            self.heightmaxbar = int(lval[int(self.ycolumn) - 1][0])
            auxmaxbar = int(lval[int(self.ycolumn) - 1][0])
            for num in range(len(lval[int(self.ycolumn) - 1])):
                if self.heightmaxbar < int(lval[int(self.ycolumn) - 1][num]):
                    self.heightmaxbar = int(lval[int(self.ycolumn) - 1][num])
            if len(lval) == int(self.ycolumn2):
                for num2 in range(len(lval[int(self.ycolumn2) - 1])):
                    if auxmaxbar < int(lval[int(self.ycolumn2) - 1][num2]):
                        auxmaxbar = int(lval[int(self.ycolumn2) - 1][num2])  
                if self.heightmaxbar < auxmaxbar:
                    self.heightmaxbar = auxmaxbar         
            return self.heightmaxbar 
        except ValueError:
            print "The input values must be numeric, can not be strings:"\
            + "\nPysvg 0.0.4-Nov2011\nCopyright (C) 2011 Isabel Rodriguez"\
            + "\nYou can see the full documentation at URL:"\
            + " \"http://www.pysvg/orgfree.com\""             
            sys.exit(2)  

    def printsvg(self):
        """
        Returns a string with SVG code for bar chart.
               
        To construct this graph will follow the following steps:
            1. B{I{Creation of the axes:}} 
                - First we have find the number of bars to be drawn on 
                  the x-axis to know what will be the final x-axis coordinate.
                   
                  
                      >>> numbars = length(lval[Y])+length(lval[Y2])
                      ... endbars = xorigin+(delim*numbars)+(barwidth*numbars)
                      
                - Then draw the vertical line corresponding to the vertical 
                  axis and write the numbers on this axis. To do this we will 
                  create linetext objects until the value of C{self.inc} is 
                  greater than the bar higher. If the variable called C{ygrid}
                  is specified, draw the lines of background with discontinuous
                  lines objects.
                    
                    >>> counter=0
                    ... inc=yrange
                    ... while inc <= heightmaxbar: 
                    ...     linetext = Linetext(xorigin, yorigin + heightmaxbar
                    ...                - inc, fontsize, str(inc))                               
                    ...     if self.ygrid == "yes":
                    ...         backgroundline = Line(xorigin, yorigin + 
                    ...         heightmaxbar - inc, endbars, yorigin + 
                    ...         heightmaxbar - inc, ygrid)                          
                    ...     counter += 1
                    ...     inc = yrange + (yinc * counter)
                
                            
                
            2. B{I{Drawing bars:}}
                - First establish the origin of the first bar or group of bars,
                  if ycolumn2 is specified, on the horizontal axis. This will 
                  be the sum of the initial origin of the bar chart and the 
                  value of separation between bars chosen by the user at 
                  the command line. In his way the graph is clearer.
            
                        >>> xorigin = xorigin + delim 
                        
                - Then you create a loop through the values of the bars: 
            
                        >>> xorigin = xorigin + delim
                        ... for cont in range(length(lval[xcolumn])):
                        ...     xvalue = lval[xcolumn][cont]
                        ...     yvalue = lval[ycolumn][cont]
                        ...     yoriginbar = yorigin + heightmaxbar - 
                        ...     int(yvalue)
                        ...     column = Column(xvalue, yvalue, int(yvalue) -
                        ...     yrange, barwidth, xorigin, yoriginbar, 
                        ...     fillcolor, "colum" + str(cont), vals)
                        ...     len(lval)==int(ycolumn2):
                        ...         yvalue2 = self.lval[int(self.ycolumn2) - 1]
                        ...         [cont]
                        ...         yorigin2 = yorigin + heightmaxbar - 
                        ...         int(yvalue2)
                        ...         column = Column("", yvalue2, int(yvalue2) -
                        ...         yrange, barwidth, xorigin + barwidth, 
                        ...         yorigin2, fillcolor2, "colum" + str(cont),
                        ...         vals)
                        ...         string += column.printsvg() + 
                        ...         column2.printsvg()
                        ...         xorigin = xorigin + delim + 2 * barwidth
                        ...     else:
                        ...         string +=column.printsvg()
                        ...         xorigin =xorigin + delim
                                    
                   We will explain how this loop:
                        - Each bar is drawn with a column element whose height
                          and top text (if the variable C{self.vals} is 
                          specified) will be equal to the data value in this
                          position of the column Y or Y2 in the input file. If
                          the value of C{self.yrange} is other than 0, subtract
                          the value to the height of the column to place it in
                          the correct position. C{xvalue} and C{yvalue} are 
                          the input data of each bar. 
                          
                          >>> C{column = Column(xvalue, yvalue, int(yvalue) - 
                          yrange, barwidth, xorigin, origin, fillcolor, "colum" 
                          + str(cont), vals)}
                              
                        - If the Ycolumn2 component is specified its position 
                          in the horizontal axis will:
                        
                              >>> xorigin = xorigin + delim + 2 * barwidth
                        
                          
                          
            3. B{I{Plotting title:}}Then check item title. If so will draw a
            text description of that element, centered at the top of the chart
            with fontsize = 14.
                
                    >>> if title != "":
                    ...    bartitle = Text(endbars / 2, yorigin / 2, 14, title)
                                
            4. B{I{Drawing the legend:}} This item consists of many horizontal
               columns as input values in the file data. 

                    >>> if legend:
                    ...    NameLegend = Hcolumn(name, endbars + offsetlegend, 
                    ...    yorigin, fillcolor, vbarsizelegend, vbarsizelegend,
                    ...    "vbarlegend", "vbarect", "vbartext", "", "", 
                    ...    filtered, "none")

               There are no filters applied in this part so that the value 
               of C{self.filterid} is equal to "none"                  
        
        @return: SVG source code of the bar chart.
        @rtype: C{string}
        """
        fontsize = 11
        vbarsizelegend = 15
        offsetlegend = 25
        try:
            #drawing Y-axis lines 
            if len(self.lval) == int(self.ycolumn2):
                numbars = (len(self.lval[int(self.ycolumn) - 1]) + 
                           len(self.lval[int(self.ycolumn2) - 1]))
                endbars = int(self.xorigin) + (int(self.delim) *
                          (int(numbars) / 2)) + (int(self.barwidth) *
                           int(numbars))
            else:
                numbars = len(self.lval[int(self.ycolumn) - 1])
                endbars = int(self.xorigin) + (int(self.delim) *
                          (int(numbars))) + (int(self.barwidth) * int(numbars))
            vertical_line = Line(self.xorigin, (self.yorigin + 
                            self.heightmaxbar - int(self.yrange)),
                            self.xorigin, self.yorigin)
            string = vertical_line.printsvg()
            counter = 0
            inc = int(self.yrange)
            while inc <= (self.heightmaxbar):
                linetext = Linetext(self.xorigin, self.yorigin + 
                                    self.heightmaxbar - inc, fontsize, 
                                    str(inc))
                string += linetext.printsvg()                                
                if self.ygrid == "yes":
                    backgroundline = Line(self.xorigin, int(self.yorigin) + 
                                          self.heightmaxbar - inc, endbars, 
                                          self.yorigin + self.heightmaxbar -
                                          inc, self.ygrid)
                    string += backgroundline.printsvg()
                counter += 1
                inc = int(self.yrange) + int(self.yinc) * counter      
            #Draw the bars
            self.xorigin = self.xorigin + int(self.delim) 
            for cont in range(len(self.lval[int(self.xcolumn) - 1])):
                #colum text
                xvalue = self.lval[int(self.xcolumn) - 1][cont]
                yvalue = self.lval[int(self.ycolumn) - 1][cont]
                yoriginbar = self.yorigin + self.heightmaxbar - int(yvalue)
                column = Column(xvalue, yvalue, int(yvalue) - int(self.yrange), 
                                self.barwidth, self.xorigin, yoriginbar, 
                                self.fillcolor, "colum1_" + str(cont), 
                                self.vals)
                if len(self.lval) == int(self.ycolumn2):
                    yvalue2 = self.lval[int(self.ycolumn2) - 1][cont]
                    yoriginbar2 = (self.yorigin + self.heightmaxbar - 
                                  int(yvalue2))
                    column2 = Column("", yvalue2, int(yvalue2) - 
                                     int(self.yrange), self.barwidth,
                                     int(self.xorigin) + int(self.barwidth),
                                     yoriginbar2, self.fillcolor2, "colum2_" + 
                                     str(cont), self.vals)
                    string += column.printsvg() + column2.printsvg()
                    self.xorigin = (self.xorigin + int(self.delim) + 
                                    2 * int(self.barwidth))
                else:
                    string += column.printsvg()
                    self.xorigin = (self.xorigin + int(self.delim) + 
                                    int(self.barwidth))
            #Draw the title
            if self.title != "":
                bartitle = Text(endbars / 2, self.yorigin / 2, 14, self.title)
                string += bartitle.printsvg()
            #draw the legend
            if self.legend:
                namelegend1 = Hcolumn(self.name, endbars + offsetlegend, 
                                      self.yorigin, self.fillcolor, 
                                      vbarsizelegend, vbarsizelegend,
                                      "vbarlegend1", "vbarect1", "vbartext1")
                if len(self.lval) == int(self.ycolumn2):
                    namelegend2 = Hcolumn(self.name2, endbars + offsetlegend,
                                          self.yorigin + 2 * vbarsizelegend,
                                          self.fillcolor2, vbarsizelegend,
                                          vbarsizelegend, "vbarlegend1",
                                          "vbarrect2", "vbartext2")
                    string += namelegend1.printsvg() + namelegend2.printsvg()   
                else:
                    string += namelegend1.printsvg()
            return string
        except IndexError:
            print "The number of columns in data file must be equal to the"\
            + " maximum value indicated by the parameters x, y, x2, y2\n"\
            + "Please review the input data \nFor help use --help"\
            + "\nPysvg 0.0.4-Nov2011\nCopyright (C) 2011 Isabel Rodriguez"\
            + "\nYou can see the full documentation at URL:"\
            + " \"http://www.pysvg/orgfree.com\""             
            sys.exit(2) 

###############################################################################


class Bardiagram3d:
    """
    In this class we will modify the bar chart to make it a three 
    dimensional graphic.
    
    As the bar chart will be formed by the axes, bars, data and legend but 
    this time we will use objects of class rectangule3d to built the bars. 
    These objects are a class derived from a plain rectangle that 
    we have added a right side and a roof by a polygon element.
    
    To give a greater sense of depth is added a three-dimensional rectangle 
    element at the bottom of the chart and and have dark sides and roof 
    of it to produce the desired effect. We also modified the coordinate 
    axes, creating a new component to generate the Z-axis displacement.
    
            >>>     y-axis
            ...        |  / 
            ...        | / z-axis
            ...        |/_____ x-axis
                                 
    Input Data
    ==========
    
    This time can only enter values for data set, thus not admitting 
    the Y2 component.
      
        >>>   Group   Seats(2004)
        ...    EUL         366  
        ...    EFA         42
        ...    EDD         15
        ...    ELDR        67
        ...    EPP         276
        ...    UEN         27
        ...    Other       66
    
    
    
        
    """ 
   
    def __init__(self, lval, xcolumn, ycolumn, barwidth, xorigin, yorigin,
                 delim, vals, yinc, yrange, ygrid, filtered, fillcolor, title,
                 legend, name):
        #{Input Data
        self.lval = lval
        """@ivar:Represents the list of input values
        @type:C{list of values}"""
        self.xcolumn = xcolumn
        """@ivar:Identifies the data field that will hold X component.
        @type: C{number}""" 
        self.ycolumn = ycolumn
        """@ivar:Identifies the data field that will hold Y component.
        @type:C{number}""" 
        #}     
        #{Position
        self.xorigin = xorigin
        """@ivar: Is the X initial coordinate of the graph. 
        @type:C{number}"""
        self.yorigin = yorigin
        """@ivar: Is the Y initial coordinate of the graph. 
        @type:C{number}"""
        self.yinc = yinc
        """@ivar:Specify a numeric axis increment amount normally one value.
        @type:C{number}"""        
        self.yrange = yrange
        """@ivar:Specify an explicit axis numeric range usually the minimum. 
        @type: C{number}"""
        #}
        #{Style
        self.barwidth = barwidth
        """@ivar: Specifies the width of the filled bars.
        @type: C{number}"""       
        self.delim = delim
        """@ivar: Specifies the separation between bars or groups of bars. 
        @type: C{number}"""
        self.vals = vals
        """@ivar:If is specified, display numeric values near the top of 
        each bar. 
        @type: C{number}"""        
        self.ygrid = ygrid
        """@ivar: If specified, grid lines will be drawn.mum 
        @type: C{yes or no}"""
        self.fillcolor = fillcolor
        """@ivar: Color of first group of bars
        @type: C{string}"""
        #}
        #{Effects        
        self.filtered = filtered
        """@ivar: If is specified some filter will be applied to the bar chart.
        @type: C{boolean}"""        

        #{title and Legend
        self.legend = legend
        """@ivar: If is specified controls the placement of the legend
        @type: C{boolean}"""        
        self.name = name
        """@ivar: Specifies legend label of first input data group
        @type: C{string}"""
        self.title = title
        """@ivar: If is specified, a plot title to be centered at the top.
        @type: C{string}"""
        #}
        self.heightmaxbar = 0
        """@ivar: is an auxiliary variable that stores the height of the bar
        higher.
        @type: C{number}""" 
        
        try:
            self.setmaximumbars(lval[int(ycolumn) - 1])
        except IndexError:
            print "The number of values of the parameters x, y or y2 must"\
            + " be equal, please review the input data"\
            + "\nFor help use --help"\
            + "\nPysvg 0.0.4-Nov2011\nCopyright (C) 2011 Isabel Rodriguez"\
            + "\nYou can see the full documentation at URL:"\
            + " \"http://www.pysvg/orgfree.com\""                    
            sys.exit(2)

    def setmaximumbars(self, lval):
        """
        Auxiliary function which returns in the variable C{self.heightmaxbar}
        maximum value from the list of Y input data.
        
        @param lval: is the list of input data.
        @type lval: C{list of values}  
        
        @return: Height of the bar higher
        @rtype: C{string}
        """
        try:
            self.heightmaxbar = int(lval[0])
            for num in range(len(lval)):
                if self.heightmaxbar < int(lval[num]):
                    self.heightmaxbar = int(lval[num])
            return self.heightmaxbar  
        except ValueError:
            print "The input values must be numeric, can not be strings"\
            + "\nPysvg 0.0.4-Nov2011\nCopyright (C) 2011 Isabel Rodriguez"\
            + "\nYou can see the full documentation at URL:"\
            + " \"http://www.pysvg/orgfree.com\""             
            sys.exit(2)
 
    def printsvg(self):
        
        """
        Returns SVG code for bar chart in three dimensions
        
        The construction of this graph is very similar to the 
        bar chart.
        
            - First we create the axes, taking into account that to draw the
              baselines generated two lines, one in the Z axis and one on the
              X axis. To draw these lines called "backgroundline1" (z-axis)
              and "backgroundline2" (x-axis) we need "offset" parameter.
              This shows the horizontal and vertical scrolling to simulate 
              depth. 
              
                >>> while inc <= heightmaxbar: 
                ...   linetext = Linetext(...) 
                ...   ...   
                ...   if ygrid == "yes":
                ...     backgroundline1 = Line(xorigin, yorigin + heightmaxbar
                ...                       -inc, xorigin + offset, yorigin + 
                ...                       heightmaxbar - inc - offset, ygrid)
                ...     backgroundline2 = Line(xorigin + offset, yorigin + 
                ...                       heightmaxbar - inc - offset, endbars
                ...                       + offset + yorigin + heightmaxbar -
                ...                       inc - offset, ygrid)
                ...    ...
             
            - Secondly we create the grey bottom rectangle and bars. To do this
              we use the rectangle element and three-dimensional column
              ("Rectangle3d" and Column3d". Both rectangles have applied a
              filter of darkness in the side and top to produce the required
              effect. 
              
                >>> rect_bottom3d = Rectangle3d (yinc / 2, endbars - xorigin,
                ...                 xorigin, yorigin + heightmaxbar - yrange,        
                ...                 "grey", "rbottom", filtered, "Darkness",
                ...                 offset)
                ... ...           
                ... for cont in range(length(self.lval[xcolumn]):
                ...     ...
                ...     if int(self.yrange) <= int(yvalue):
                ...         column3d = Column3d(xvalue, yvalue, int(yvalue) -
                ...                    yrange, barwidth, xorigin, yoriginbar,
                ...                    fillcolor, "colum3d" + str(cont),
                ...                    filtered, "Darkness", offset, vals) 
                ...    else:
                ...         try:
                ...             raise ValueError
                ...         except ValueError:
                ...         print "yrange value must be less than the minimum
                ...         value of the input data"
                ...         sys.exit(2)

            - If the value of the minimum range of vertical axis is less 
              than any of the values of the input data, an exception occurs
              informing the user of this event and stop the execution.
              
            - Finally, we will build the legend with the item horizontal column 
              as in the bar chart.
                >>> if self.legend:
                ...    legend3d = Hcolumn(name, endbars + 2 * offset,
                ...               (yorigin + heightmaxbar) / 2, fillcolor, 
                ...               heighwidthlegend, heighwidthlegend, 
                ...               "vbar3dlegend", "vba3drect","vbar3dtext", "",
                ...               "", filtered, "none")
                  
        @return: SVG source code of the bar chart.
        @rtype: C{string}   
        
        @raise ValueError: If the value of the minimum range of vertical axis
        is less than any of the values of the input data.      
              
        """
        fontsize = 10
        offset = 15
        heighwidthlegend = 15
        try:
            #Create the filter for rectangle3d element
            darknessfilter = Filter("Darkness", 0, 0, 120, 120,
                                    "userSpaceOnUse")
            string = darknessfilter.printsvg()
            #Draw the axis in three dimensions
            numbars = len(self.lval[0])
            endbars = int(self.xorigin) + (int(self.delim) * int(numbars)) + \
            (int(self.barwidth) * int(numbars))     
            vertical_line = Line(self.xorigin, self.yorigin, self.xorigin, 
                                 self.yorigin + self.heightmaxbar -
                                 int(self.yrange), "no")
            string += vertical_line.printsvg()
            #Draw the number of the Y axis
            counter = 0
            inc = int(self.yrange)
            while inc <= self.heightmaxbar: 
                linetext = Linetext(self.xorigin, self.yorigin + 
                                    self.heightmaxbar - inc, fontsize, 
                                    str(inc))
                string += linetext.printsvg()                                
                if self.ygrid == "yes":
                    backgroundline1 = Line(self.xorigin, int(self.yorigin) +
                                    self.heightmaxbar - inc, self.xorigin
                                    + offset, int(self.yorigin) + 
                                    self.heightmaxbar - inc - offset,
                                    self.ygrid)
                    backgroundline2 = Line(self.xorigin + offset, 
                                    int(self.yorigin) + self.heightmaxbar
                                    - inc - offset, endbars + offset, 
                                    int(self.yorigin) + self.heightmaxbar
                                    - inc - offset, self.ygrid)
                    string += backgroundline1.printsvg() + \
                    backgroundline2.printsvg()                            
                counter += 1
                inc = int(self.yrange) + int(self.yinc) * counter            
     
            #draw filtered bottom rectangle 
            rect_bottom3d = Rectangle3d(int(self.yinc) / 2, endbars - 
                                        self.xorigin, self.xorigin, 
                                        self.yorigin + self.heightmaxbar -
                                        int(self.yrange), "grey", "rbottom",
                                        self.filtered, "Darkness", offset)
            string += rect_bottom3d.printsvg()
            #draw filtered bars in three dimensions                
            self.xorigin = self.xorigin + int(self.delim) 
            for cont in range(len(self.lval[int(self.xcolumn) - 1])):
                xvalue = self.lval[int(self.xcolumn) - 1][cont]
                yvalue = self.lval[int(self.ycolumn) - 1][cont]
                yoriginbar = self.yorigin + self.heightmaxbar - int(yvalue)
                if int(self.yrange) <= int(yvalue):
                    column3d = Column3d(xvalue, yvalue, int(yvalue) -
                                        int(self.yrange), self.barwidth, 
                                        self.xorigin, yoriginbar, 
                                        self.fillcolor, "colum3d" + str(cont),
                                        self.filtered, "Darkness", offset, 
                                        self.vals)
                    string += column3d.printsvg()
                else:
                    try:
                        raise ValueError
                    except ValueError:
                        print "Yrange value must be less than the minimum"\
                        + "value of the input data" + "\npysvg 0.0.4-Nov2011"\
                        + "\nCopyright (C) 2011 Isabel Rodriguez"\
                        + "\nYou can see the full documentation at URL:"\
                        + " \"http://www.pysvg/orgfree.com\""
                        sys.exit(2)
                    
                self.xorigin = self.xorigin + int(self.delim) + \
                int(self.barwidth)
            #Draw the title
            if self.title != "":
                bar3dtitle = Text(endbars / 2, self.yorigin / 2, 14, 
                                  self.title)
                string += bar3dtitle.printsvg() 
            #Draw the legend        
            if self.legend:
                legend3d = Hcolumn(self.name, endbars + 2 * offset,
                                  (self.yorigin + self.heightmaxbar) / 2,
                                  self.fillcolor, heighwidthlegend, 
                                  heighwidthlegend, "vbar3dlegend", 
                                  "vba3drect", "vbar3dtext")
                string += legend3d.printsvg()      
            return string
        except IndexError:
            print "The number of columns in data file must be equal to the "\
            + "maximum value indicated by the parameters x, y, x2, y2\n"\
            + "Please review the input data \nFor help use --help"\
            + "\npysvg 0.0.4-Nov2011\nCopyright (C) 2011 Isabel Rodriguez"\
            + "\nYou can see the full documentation at URL:"\
            + " \"http://www.pysvg/orgfree.com\""             
            sys.exit(2) 
            
###############################################################################


class Scatterplot:
    """
    Description
    ===========
    
    A scatter plot or scattergraph is a type of mathematical diagram using 
    Cartesian coordinates to display values for two variables for a set of
    data.

    The data is displayed as a collection of points, each having the value of
    one variable determining the position on the horizontal axis and the value 
    of the other variable determining the position on the vertical axis.
    
    A scatter plot is used when I{a variable exists that is under the control 
    of the user}. If a parameter exists that is systematically incremented
    and/or decremented by the user, it is called B{independent variable} and
    is customarily plotted along the B{horizontal axis}. The B{measured or
    dependent variable} is customarily plotted along the vertical axis. 
    
    If B{no dependent variable exists}, either type of variable can be plotted 
    on either axis and a scatter plot will illustrate only the B{degree of
    correlation} (not causation) between two variables.
    
    Correlation
    -----------
    
    A scatter plot can suggest various kinds of correlations between variables 
    with a certain confidence interval. Correlations or statistical 
    relationship between two sets of data, may be positive (rising), negative
    (falling), or null (uncorrelated).
    
    A line of best fit (alternatively called 'trendline') can be drawn in order
    to study the correlation between the variables. 
    
        - If the pattern of dots slopes from lower left to upper right, it 
          suggests a positive correlation.
          
              >>>       ./.     
              ...   . . /.
              ...  ..  / .
              ...   . / .
           
        - If the pattern of dots slopes from upper left to lower right, it
          suggests a negative correlation. 
          
              >>>  ..\  .     
              ...   . \ ..
              ...  .. .\ .
              ...   . . \.
                  
    An equation for the correlation between the variables can be determined by
    established best-fit procedures. For a linear correlation, the best-fit
    procedure is known as B{linear regression} and is guaranteed to generate a
    correct solution in a finite time.
    
    Linear regression
    -----------------
    In statistics the linear fit or linear regression is a mathematical method
    that models the relationship between a dependent variable Y and independent
    variables Xi: B{Y=S{sum}S{beta}iXi+S{epsilon}} where S{epsilon} is the
    random disturbance which includes all those factors not controllable or
    observable reality and therefore are associated with random.
    
    The B{regression lines} are the lines that best fit the point cloud
    generated by a binomial distribution. The way to get these lines is by the
    process known as the method of least squares. We look for a line with
    equation B{y = a + bx} to be the best approach. Each point xi of the first
    variable will, on the one hand, the value corresponding to the second 
    variable yi, and secondly, his image by the regression line B{y = a + bxi}.
    Thus the regression line of Y on X is: 
    
        -    B{(y-S{Delta}y)=(S{sigma}xy/(S{sigma}x*S{sigma}x))*(x-S{Delta}x)}
    
    Where:
        -    B{S{Delta}y=(S{sum}y1..yk)/k} and B{S{Delta}x=(S{sum}x1..xk)/k}
             average of y and x respectively             
        -    B{S{sigma}xy=Cov(X,Y)}: indicating the degree of dependence
             between the values of X and Y respectly.
                 - B{Cov(X,Y)>0}: indicates that there is direct dependence
                   (positive), large values of x correspond to large values
                   of y. 
                 - B{Cov (X,Y)=0}: A covariance 0 is interpreted as the absence
                   of a linear relationship between the variables studied.
                -  B{Cov(X,Y)<0}: dependence is inverse or negative, large
                   values of x are small values of y.
        -    B{S{sigma}x*S{sigma}x=Variance(X)}: is a measure of dispersion
             defined as the expectation of the square of the deviation of that
             variable from its mean.
        -    B{a=S{Delta}y-b*S{Delta}x}: intercept point.        
        -    B{b=(S{sigma}xy/(S{sigma}x*S{sigma}x))}: is the slope of the 
             regression line.
    """
    
    def __init__(self, lval, xorigin, yorigin, xcolumn, ycolumn, xcolumn2,
                 ycolumn2, yinc, ptsize, ptsym, pt2sym, ptcolor,
                 pt2color, corr, xlabel, ylabel, name, name2, legend, title):
        #{Input Data
        self.lval = lval
        """@ivar:Represents the list of input values
        @type:C{list of values}"""
        self.xcolumn = xcolumn
        """@ivar:Identifies the data field that will hold X component.
        @type: C{number}"""
        self.xcolumn2 = xcolumn2 
        """@ivar:Identifies the data field that will hold X2 component.
        @type: C{number}"""        
        self.ycolumn = ycolumn
        """@ivar:Identifies the data field that will hold Y component.
        @type:C{number}""" 
        self.ycolumn2 = ycolumn2
        """@ivar:Identifies the data field that will hold Y2 component.
        @type:C{number}"""  
        #}     
        #{Position
        self.xorigin = xorigin
        """@ivar: Is the X initial coordinate of the graph. 
        @type:C{number}"""
        self.yorigin = yorigin
        """@ivar: Is the Y initial coordinate of the graph. 
        @type:C{number}"""
        self.yinc = yinc
        """@ivar: It is the increase experienced by the numbering of the axes
        @type:C{number}"""        
        #}
        #{Style
        self.ptcolor = ptcolor
        """@ivar: Color of first group of plots
        @type: C{string}"""
        self.pt2color = pt2color
        """@ivar: Color of second group of plots
        @type: C{string}"""
        self.ptsize = ptsize
        """@ivar: Controls the size of data point 
        @type: C{number}"""        
        self.ptsym = ptsym
        """@ivar: Controls the shape of the first group data point  
        @type: C{circle or square or triangle or diamond or invertedtriangle}
        """          
        self.pt2sym = pt2sym
        """@ivar: Controls the shape of the first group data point  
        @type: C{circle or square or triangle or diamond or invertedtriangle}
        """          
        self.xlabel = xlabel
        """@ivar: Specifies x-axis label 
        @type: C{string}"""         
        self.ylabel = ylabel  
        """@ivar: Specifies y-axis label 
        @type: C{string}"""
        #}       
        #{title and Legend
        self.legend = legend
        """@ivar: If is specified controls the placement of the legend
        @type: C{boolean}"""        
        self.name = name
        """@ivar: Specifies legend label of first input data group
        @type: C{string}"""
        self.name2 = name2
        """@ivar: Specifies legend label of second input data group
        @type: C{string}"""
        self.title = title
        """@ivar: If is specified, a plot title to be centered at the top.
        @type: C{string}"""
        #}
        self.corr = corr
        """@ivar: Compute correlation and display regression line.
        @type: C{boolean}"""
    
    def getaverage(self, lval):
        """
        Auxiliary function that returns the average of a list of
        values given.
        
        @param lval: list of values
        @type lval: C{list}
        
        @return: The average of a list of value
        @rtype: C{number} 
        """
        sumlval = 0
        for num in range(len(lval)):
            sumlval += int(lval[num])   
        return int(sumlval / len(lval))

    def getvariance(self, lval):
        """
        Auxiliary function that returns the variance of a list of
        values given. To do this use the average function as follows:
        
            - B{Var(X)= S{sum}((xi-S{Delta}x)*(xi-S{Delta}x))/n}
        
        Where I{n} is the lenght of the list.
        
        @param lval: list of values
        @type lval: C{list}
        
        @return: The variance of a list of value
        @rtype: C{number}                 
        """

        var = 0
        for num in range(len(lval)):
            var += (int(lval[num]) - int(self.getaverage(lval))) \
            * (int(lval[num]) - int(self.getaverage(lval)))
        return int(var / len(lval)) 
    
    def getcovariance(self, lval):
        """
        Auxiliary function that returns the covariance of a list of
        values given. To do this use the average and the variance
        function as follows:
        
            - B{Cov(X,Y)= S{sum}((xi-S{Delta}x)*(yi-S{Delta}y))/n}
        
        Where I{n} is the lenght of the list.
        
        @param lval: list of values
        @type lval: C{list}
        
        @return: The covariance of a list of value
        @rtype: C{number}                 
        """        
        covar = 0
        for num in range(len(lval[int(self.xcolumn) - 1])):
            #covar+=(x-promedioX)*(y-promedioY)
            covar += (int(lval[int(self.xcolumn) - 1][num]) - 
                      int(self.getaverage(lval[int(self.xcolumn) - 1]))) * \
                      (int(lval[int(self.ycolumn) - 1][num]) -
                       int(self.getaverage(lval[int(self.ycolumn) - 1])))    
        return int(covar / len(lval[int(self.xcolumn) - 1]))
   
   #dibuja recta de regression 
    def getregressionline(self, lval):
        
        """
        Returns the regression line for a given set of data. To get this list
        of values using the above functions, variance, average and covariance.
        The two fundamental parameters to build this line will be:
        
            -    B{a=S{Delta}y-b*S{Delta}x}: intercept point.        
            -    B{b=(S{sigma}xy/(S{sigma}x*S{sigma}x))}: is the slope of the
                 regression line.
        
        @param lval: list of values
        @type lval: C{list}
        
        @return: The regression line for input list
        @rtype: C{list}  
        """
        
        reglist = []
        bcomponent = float(self.getcovariance(lval)) / \
        float(self.getvariance(lval[int(self.xcolumn) - 1]))
        
        for cont in range(len(lval[int(self.xcolumn) - 1])):
            ylist = bcomponent * (float(lval[int(self.xcolumn) - 1][cont]) - \
                    float(self.getaverage(lval[int(self.xcolumn) - 1]))) + \
                    self.getaverage(lval[int(self.ycolumn) - 1])

            reglist.append([float(lval[int(self.xcolumn) - 1][cont]), ylist])
        return reglist
    
    def getmaxpoint(self, lval):
        """
        Returns the maximum value of a list of data input passed as parameter.

        @param lval: list of values
        @type lval: C{list}
        
        @return: Maximum value of the list
        @rtype: C{number}         
                
        """  
        try:
            maxpoint = int(lval[0])
            for num in range(len(lval)):
                if maxpoint < int(lval[num]):
                    maxpoint = int(lval[num])
            return maxpoint
        except ValueError:
            print "The input values must be numeric, can not be strings"\
            + "\npysvg 0.0.4-Nov2011\nCopyright (C) 2011 Isabel Rodriguez"\
            + "\nYou can see the full documentation at URL:"\
            + " \"http://www.pysvg/orgfree.com\""             
            sys.exit(2) 
    
    def getmaxaxis(self, lval):
        """
        Returns the maximum value of a two list of data input.

        @param lval: list of values
        @type lval: C{list}
        
        @return: Maximum xvalue and yvalue of the axis
        @rtype: C{number}         
                
        """         
        ymaxaxis = self.getmaxpoint(lval[int(self.ycolumn) - 1])
        xmaxaxis = self.getmaxpoint(lval[int(self.xcolumn) - 1])
        if (len(lval) > int(self.xcolumn2)):
            ycolumn2 = len(lval)
            ymaxpoint2 = self.getmaxpoint(lval[int(ycolumn2) - 1])
            xmaxpoint2 = self.getmaxpoint(lval[int(self.xcolumn2) - 1])
            if ymaxpoint2 > ymaxaxis:
                ymaxaxis = ymaxpoint2
            if xmaxpoint2 > xmaxaxis:
                xmaxaxis = xmaxpoint2
        return xmaxaxis, ymaxaxis
        
    #PARA TRANSFORMAR LA LISTA DE REGRESION A LAS COORDENADAS NORMALES
    def regtocoordenates(self, lval, ymaxpoint):
        """
        Function that transforms the coordinates of the regression line in 
        SVG coordinates to draw it in the chart.
        
        To perform this modification will be made the following changes 
        to each value of the input list:
        
            >>> Xcoordenate = float(lval[i])
            ... Ycoordenate = float(ymaxpoint) - float(lval[i])
        
        Where "i" is the position of value within the list.
        
        @param lval: list of values
        @type lval: C{list}
        @param ymaxpoint: Is the maximum value from the list of input data in
        the y-axis. 
        @type ymaxpoint: C{number}
        @return: List of SVG coordenates
        @rtype: C{number}
        """
        newlpoints = []  
        for num in range(len(lval)):
            xcoordenate = float(lval[num][int(self.xcolumn) - 1])
            ycoordenate = float(ymaxpoint) \
            - float(lval[num][int(self.ycolumn) - 1])
            newlpoints.append([xcoordenate, ycoordenate])
        return newlpoints

    def getsvgpoint(self, xpoint, ypoint, sym, color, size):
        """ 
        Auxiliary function that returns the shape of a given point.
        
        @param xpoint: x-coordenate of the point.
        @type xpoint: C{number}
        @param ypoint: y-coordenate of the point.
        @type ypoint: C{number}
        @param sym: Is the simbol of the point.
        @type sym: C{string}
        @param color: Is the fill color of the point.
        @type color: C{string}
        @param size: Is the size of the point.
        @type size: C{number}
        
        @return: A string with SVG code of eath point.
        @rtype: C{string}
        
        """     
        if sym == "circle":                
            shapepoint = Circle(str(xpoint), str(ypoint), size / 2, 1, "black",
                                color)
        elif sym == "square":
            shapepoint = Rectangle(size, size, str(xpoint - size / 2),
                                   str(ypoint - size / 2), sym, color)
        elif sym == "triangle":
            trianglepoints = [[xpoint, ypoint - size / 2], [xpoint - size / 2,
                               ypoint + size / 2], [xpoint + size / 2, 
                               ypoint + size / 2]]
            shapepoint = Polygon(trianglepoints, sym, color)
        elif sym == "invertedtriangle":  
            invertedtrianglepoints = [[xpoint - size / 2, ypoint - size / 2],
                                      [xpoint, ypoint + size / 2], [xpoint + 
                                       size / 2, ypoint - size / 2]]
            shapepoint = Polygon(invertedtrianglepoints, sym, color)
        elif sym == "diamond":
            diamondpoints = [[xpoint, ypoint - size / 2], [xpoint + size / 2,
                              ypoint], [xpoint, ypoint + size / 2],
                            [xpoint - size / 2, ypoint]]
            shapepoint = Polygon(diamondpoints, sym, color)
        strshape = shapepoint.printsvg()
        return strshape        
        
    def printsvg(self):
        
        """
        Returns the SVG code for the dispersion diagram.
        To compose each part of this graph we take the following 
        steps:
        
            - First check the maximum value of the input data on the y axis for
              both component, Y and Y2, order to B{build the regression line}
              with the correct coordinates. To do this we use the functions:
                  - getmaxpoint(self, lval)
                  - getregressionline(self, lval)
                  - regtocoordenates(self, lval, ymaxpoint)
              Thus, in the variables C{"lpoints"} and C{"lpoints2"}, if Y2
              component is specified, we will have the SVG coordinates of the
              regression lines.
              
            - The next thing is to B{built the chart axes}. This will create
              two simple lines, one in horizontal for X-axis data and a 
              vertical one for y-axis data. Then, include the number of them
              using aloop that will check if the value of increasing the
              numbering has exceeded the maximum point of the axis.
              
              >>> cont=0; auxinc=self.yinc;
              ... while self.yinc <= maxaxis:
              ...   linetextAxis = Linetext(xorigin,yorigin-inc,..)
              ...   linetextAxis.printsvg()
              ...   inc = auxinc * cont
              ...   cont += 1
              
              The increased value of the axes will be selected by the user for
              greater accuracy in the visualization of the data sample. 
              However, the minimum value of each axis will always be zero for
              a clearer representation of the data.
              
            - Third proceed to B{create the points}. To do this we have through
              the list of input data C{"lval"} to obtain the value of x,y
              coordinate of each point. These can be five different shapes: 
              I{rectangle, diamond, circle, triangle and inverted triangle}. 
              Depending on the shape in C{"ptsym"} parameter chosen by the
              user, using an object or another and will be filled by the color
              indicating the variable C{self.ptcolor}.
              
              >>>   if self.ptsym == "circle":                
              ...       shapePoint = Circle(.....)
              ...   elif self.ptsym == "square":
              ...       shapePoint = Rectangle(.....)
              ...   elif self.ptsym == "triangle":
              ...       shapePoint = Polygon(...)
              ...   elif self.ptsym == "invertedtriangle":
              ...       shapePoint = Polygon(.....)
              ...   elif self.ptsym == "diamond":
              ...       shapePoint = Polygon(.....)  
              
              This process will also in case of a second set of data marked by
              the existence of the component Y2. in this case the parameters
              are respectively C{elf.pt2sym} and C{self.pt2color}. 
              Next to each point, draw a text with the value of x and y 
              coordinates of that point. This value will be stored in the
              variable C{pointText} for the first group of data and 
              C{pointText2} for the second group.
        
            - After you draw the axes and the points will see if the user has
              chosen the option of including the regression line in the 
              diagram. This parameter will check the existence of 
              C{"self.corr"}. If this parameter has a value of "True" drawn 
              by an object of class Linepath a line that will indicate the 
              level of dependency between x and y values of each group
              respectively.
              
                  >>> if self.corr:
                  ...   regLine = Linepath(......)
                  
              This line will be the same color as the data seta.
                
            - Finally we add the external elements such as x and y axis labels
              and legend. The value of these labels will be stored in variables
              C{"self.xlabel"} and C{"self.ylabel"} respectively.
              
                  >>> if self.xlabel != "":
                  ...   textX = Text(.....)
                  ... if self.ylabel != "":
                  ...   textY = Verticaltext(.....)
              
            - As in previous graphs, to create the legend will draw as many 
              items I{"Hcolumn"} as data group has the input file.
              
                  >>>  if self.legend:          
                            scatLegend1 = Hcolumn(....)
     
        @return: SVG code for scatter plot graph.
        @rtype: C{string}
        """
        fontsize = 10
        scatlegendsize = 7
        try:
            self.ptsize = float(self.ptsize)   
            xmaxaxis, ymaxaxis = self.getmaxaxis(self.lval)
            #draw lines axis
            vline = Line(self.xorigin, self.yorigin, self.xorigin, 
                                self.yorigin + ymaxaxis, "no")
            hline = Line(self.xorigin, self.yorigin + ymaxaxis,
                                  self.xorigin + xmaxaxis, 
                                  self.yorigin + ymaxaxis, "no")
            string = vline.printsvg() + hline.printsvg()
            cont = 0
            auxinc = int(self.yinc)
            while int(self.yinc) <= ymaxaxis:
                ylinetext = Linetext(self.xorigin, self.yorigin + ymaxaxis - 
                                     int(self.yinc), fontsize, self.yinc)
                string += ylinetext.printsvg()
                self.yinc = auxinc * cont
                cont += 1
            cont = 0
            self.yinc = auxinc
            while int(self.yinc) <= xmaxaxis:
                xlinetext = Linetextvertical(self.xorigin + int(self.yinc),
                                             self.yorigin + ymaxaxis, fontsize, 
                                             self.yinc)
                string += xlinetext.printsvg()
                self.yinc = auxinc * cont
                cont += 1
                
            #draw points
            for cont in range(len(self.lval[int(self.xcolumn) - 1])):
                xpoint = int(self.lval[int(self.xcolumn) - 1][cont]) \
                        + int(self.xorigin)
                ypoint = int(self.yorigin) + ymaxaxis \
                         - int(self.lval[int(self.ycolumn) - 1][cont])
                
                string += self.getsvgpoint(xpoint, ypoint, self.ptsym,
                                           self.ptcolor, self.ptsize)

                if (len(self.lval) > int(self.xcolumn2)):
                    ycolumn2 = len(self.lval)
                    xpoint2 = int(self.lval[int(self.xcolumn2) - 1]
                                  [cont]) + int(self.xorigin)
                    ypoint2 = int(self.yorigin) + ymaxaxis - \
                              int(self.lval[int(ycolumn2) - 1][cont]) 
                    string += self.getsvgpoint(xpoint2, ypoint2, self.pt2sym,
                                               self.pt2color, self.ptsize)
                  
            #draw regression line        
            if self.corr:
                lpoints = self.regtocoordenates(
                                            self.getregressionline(self.lval),
                                            self.getmaxpoint(self.lval[int(
                                            self.ycolumn) - 1]))                
                regline = Linepath(self.xorigin, self.yorigin, "regline",
                                   lpoints, "none", self.ptcolor)
                if (len(self.lval) > int(self.xcolumn2)):
                    lpoints2 = self.regtocoordenates(self.getregressionline(
                                            self.lval[2:]), self.getmaxpoint(
                                            self.lval[int(ycolumn2) - 1]))               
                    regline2 = Linepath(self.xorigin, self.yorigin, "regline2",
                                        lpoints2, "none", self.pt2color)
                    string += regline.printsvg() + regline2.printsvg()
                else:
                    string += regline.printsvg()
                    
            #draw the axis labels
            if self.xlabel != "":
                xtext = Text(self.xorigin + (xmaxaxis / 2), 1.5 * \
                              self.yorigin + ymaxaxis, fontsize, self.xlabel)
                string += xtext.printsvg()
            if self.ylabel != "":
                ytext = Verticaltext(self.xorigin - self.xorigin / 2,
                                     self.yorigin + (ymaxaxis / 2),
                                     fontsize, self.ylabel, 0) 
                string += ytext.printsvg()
                
            #draw the legend
            if self.legend:          
                scatlegend1 = Hcolumn(self.name, self.xorigin, 
                                      self.yorigin + ymaxaxis + 70,
                                      self.ptcolor, scatlegendsize,
                                      scatlegendsize, "scatlegend1", 
                                      "scatect1", "scatext1")
                if (len(self.lval) > int(self.xcolumn2)):                   
                    scatlegend2 = Hcolumn(self.name2, self.xorigin, 
                                          self.yorigin + ymaxaxis + 70 + 
                                          1.5 * scatlegendsize, self.pt2color,
                                          scatlegendsize, scatlegendsize,
                                          "scatlegend1", "scatrect2",
                                          "scatext2")
                    string += scatlegend1.printsvg() + scatlegend2.printsvg()   
                else:
                    string += scatlegend1.printsvg()
            if self.title != "":
                scattitle = Text((self.xorigin + xmaxaxis) / 2, 
                                 self.yorigin / 2, 14, self.title)
                string += scattitle.printsvg() 
            return string
        except IndexError:
            print "The number of columns in data file must be equal to the"\
            + "maximum value indicated by the parameters x, y, x2, y2\n"\
            + "Please review the input data \nFor help use --help"
            sys.exit(2) 

###############################################################################


class Lineplot (Scatterplot):
    
    """
    Description
    ===========
    
    A line chart is a type of graph, which displays information as a series of 
    data points connected by straight line segments. It is a basic type of 
    chart common in many fields. It is an extension of a scatter graph, and
    is created by connecting a series of points that represent individual 
    measurements with line segments. A line chart is often used to visualize
    a trend in data over intervals of time.
            
    Thus the line is often drawn chronologically. For this reason, not enough
    to draw the line, you must pre-ordering the data.
    
    Input Data
    ==========
    
    As in the dispersion diagram, the input data are represented in four 
    columns maximum. The first two are the coordinates x,y of the first data
    set and the remaining coordinates x,y the second group of points.
    
    Each column is identified by a specific variable:
        - B{C{self.x}}: for the x coordinate of the first data set.
        - B{C{self.y}}: for the y coordinate of the first data set.
        - B{C{self.x2}}: for the x coordinate of the second data set.
        - B{C{self.y2}}: for the y coordinate of the second data set.
    
    >>>      x     y   x2  y2
    ...     95    57  285  65
    ...     150   27  359  67
    ...     84    175 278  90
    ...     123   45  345  50
    ...     156   118 220 178
    ...     169   98  245  80 
    ...     143   74  260  56
    ...     133   87  254  88 
    ...     95    239 277  11
    ...     100   10  219  123
    
    These values will be stored in a variable of type list called C{self.lval}
    which will be transformed to SVG coordinates and ordered by a B{sorting
    algorithm} to represent the line of points correctly. 
        
    For this diagram we have chosen the fastest sorting algorithm called
    B{Quicksort}.   

    """    
    
    def __init__(self, lval, xorigin, yorigin, xcolumn, ycolumn, yinc,
                 fillcolor, ptsize, ptsym, ptcolor, xlabel, ylabel,
                 xcolumn2, ycolumn2, pt2sym, pt2color, name, name2, legend,
                 fillcolor2, title):
        
        Scatterplot.__init__(self, lval, xorigin, yorigin, xcolumn, ycolumn,
                             xcolumn2, ycolumn2, yinc, ptsize, ptsym, pt2sym,
                             ptcolor, pt2color, False, xlabel, ylabel, name,
                             name2, legend, title)
        #{Style
        self.fillcolor = fillcolor
        """@ivar:Is the fill color of the lower area of the dotted line for the
        first set of data
        @type: C{string}"""
        self.fillcolor2 = fillcolor2
        """@ivar:Is the fill color of the lower area of the dotted line for the
        second set of data
        @type: C{string}"""        
        #}   
         
    def transformtocoordenates(self, lval, ymaxpoint):
        """
        Helper function that transforms each coordinate given in the 
        input file to SVG coordinates as follows:        
        
            >>> Xcoordenate = int(lval[int(self.x) - 1][num])
            ... Ycoordenate = int(ymaxpoint) - 
            ...               int(lval[int(self.ycolumn) - 1][num])
        
        Where "num" is the position of value within the list.
        
        @param lval: list of input data
        @type lval: C{list}
        @param ymaxpoint: Is the maximum value from the list of input data in
        the y-axis. 
        @type ymaxpoint: C{number}
        @return: List of SVG coordenates
        @rtype: C{number}        
        """        
        newlpoints = []   
        for num in range(len(lval[int(self.xcolumn) - 1])):
            xcoordenate = int(lval[int(self.xcolumn) - 1][num])
            ycoordenate = (int(ymaxpoint) - 
                          int(lval[int(self.ycolumn) - 1][num]))
            newlpoints.append([xcoordenate, ycoordenate])
        return newlpoints          

    def ordenatewithquicksort(self, lval, first, last):
        """
        Returns the parameter list passed by ascending order using the method 
        for this fast quicksort ordenation.
        
        Quicksort is a sorting algorithm that, on average, makes O(nlogn) 
        comparisons to sort n items. It is often faster in practice than 
        other O(nlogn) algorithms.
        
        First divides a large list into two smaller sub-lists: the low elements 
        and the high elements. Thus, can then recursively sort the sub-lists.
        
        The steps are:
        
           1. Pick an element, called a pivot, from the list.
           2. Reorder the list so that all elements with values less than the 
              pivot come before the pivot, while all elements with values 
              greater than the pivot come after it (equal values can go either
              way). After this partitioning, the pivot is in its final
              position. This is called the partition operation.
           3. Recursively sort the sub-list of lesser elements and the
              sub-list of greater elements.

        The base case of the recursion are lists of size zero or one, which
        never need to be sorted.
        
        In simple pseudocode, the algorithm might be expressed as this:

              >>>    function quicksort(list)
              ...     create empty lists less and greater
              ...     if length(list) <= 1
              ...         return list 
              ...         // an list of zero or one elements is already sorted
              ...         // select and remove a pivot value pivo' from list
              ...     for each x in list
              ...         if x <= pivot then append  to less
              ...         else append x to greater
              ...    return concatenate(quicksort(less), pivot, 
              ...                       quicksort(greater))

        @param lval: Is the list to be ordered. 
        @type lval: C{list}
        @param first: first element of the sublist
        @type first: C{number}
        @param last: last element of the sublist 
        @type last: C{number}        
        @return: Ordered list in ascending.
        @rtype: C{list}      
        """
        ivar = first
        jvar = last
        lpivot = []
        pivot = ((int(lval[first][int(self.xcolumn) - 1]) + 
                 int(lval[last][int(self.xcolumn) - 1])) / 2)
        lpivot.append(pivot)
        while ivar < jvar:
            while int(lval[ivar][int(self.xcolumn) - 1]) < pivot:
                ivar += 1
            while int(lval[jvar][int(self.xcolumn) - 1]) > pivot:
                jvar -= 1
            if ivar <= jvar:
                aux1 = int(lval[ivar][int(self.xcolumn) - 1])
                aux2 = int(lval[ivar][int(self.ycolumn) - 1])
                lval[ivar][int(self.xcolumn) - 1] = \
                lval[jvar][int(self.xcolumn) - 1]
                lval[ivar][int(self.ycolumn) - 1] = \
                lval[jvar][int(self.ycolumn) - 1]
                lval[jvar][int(self.xcolumn) - 1] = aux1
                lval[jvar][int(self.ycolumn) - 1] = aux2
                ivar += 1
                jvar -= 1
        if first < jvar:
            lval = self.ordenatewithquicksort(lval, first, jvar)
        if last > ivar:
            lval = self.ordenatewithquicksort(lval, ivar, last)
        return lval

    def printsvg(self):
        
        """
        This diagram is merely an extension of the scatter diagram which
        includes a line that connects all the dots.
        
        The steps to build this chart are basically the following:
        
            1. B{Check the maximum value of the input data on the y axis} for
               Y and Y2 component using the auxiliary function: 
               B{getmaxpoint(self, lval)}.
            2. B{Create the x and y axis} by a horizontal and vertical line
               respectively to the maximum value of each axis and include the
               numbering on them.
            3. B{Building the line connecting the points}. To do this you must:
                - I{Transform the coordinates into SVG coordinates} by the
                  function: B{transformtocoordenates(self.lval, ymaxpoint)}. 
                  The resulting value will be stored in a list called 
                  B{I{"lpoints"}}.
                - Sort the list of points previously obtained by the quicksort
                  algorithm in ascending. B{ordenatewithquicksort(lpoints, 0,
                  len(lpoints)-1)}. Store the resulting list in the variable
                  "lpointsordenate".
                - Finally insert two additional points on the list.
                    - Insert in the first position, a point whose x-coordinate
                      will be the first value in the list and whose
                      y-coordinate will be the y-axis maximum value.
                    - In the last position insert another point whose
                      coordinates x, y are the maximum values for each axis.
                      
                      >>> lpointsOrdenate.insert(0, [lpointsOrdenate[0][0],
                      ...                            ymaxaxis])
                      ... lpointsOrdenate.insert(int(len(lpointsOrdenate)),
                      ... [xmaxpoint, ymaxaxis])
                      
                - Once done, draw the dotted line by an element B{Linepath}
                
                     >>> Linepath(self.xorigin, self.yorigin, "regline",
                     ...          lpointsOrdenate, self.fillcolor,
                     ...          self.ptcolor)
                     
                  This element will be the same color as the fill color of the
                  points marked by the variable C{self.ptcolor}.
                
                  B{This process is repeated in case the Y2 component is 
                  specified.}
                  
            4. B{Draw the cloud of points} as explained in the dispersion
               diagram
            5. B{Include additional elements} such as labels on the coordinate
               axes, title and legend.
                    - xtext = Text(.....)
                    - ytext = Verticaltext(....)
                    - lineplottitle = Text(....)
               In this case, the legend is built differently from the other
               diagrams and will be drawn in the bottom of the chart. 
               We will create a line item, the color of the point cloud plus
               a text element.
               
               >>>  linelegend = Line(self.xorigin, 1.5 * self.yorigin + 
               ...                    ymaxaxis, self.xorigin + lineLegendsize, 
               ...                    1.5 * self.yorigin + ymaxaxis, "no",
               ...                    self.ptcolor)
               ...  textlegend = Text(self.xorigin + 2 * lineLegendsize, 
               ...                    1.5 *self.yorigin+ymaxaxis,
               ...                    fontsize, self.name)
              
        @return: SVG code for line graph.
        @rtype: C{string}        
              
        """
        
        #find the maximum value of x and y to determine the size of each axis
        fontsize = 10
        linelegendsize = 10
        try:
            self.ptsize = float(self.ptsize)  
            xmaxaxis, ymaxaxis = self.getmaxaxis(self.lval)             
            #draw lines axis
            vline = Line(self.xorigin, self.yorigin, self.xorigin,
                         self.yorigin + ymaxaxis, "no")
            hline = Line(self.xorigin, self.yorigin + ymaxaxis,
                         self.xorigin + xmaxaxis, 
                         self.yorigin + ymaxaxis, "no")
            string = vline.printsvg() + hline.printsvg()
            #Draw the axis
            cont = 0
            auxinc = int(self.yinc)
            while int(self.yinc) <= ymaxaxis:
                ylinetext = Linetext(self.xorigin, self.yorigin + ymaxaxis -
                                     int(self.yinc), fontsize, self.yinc)
                string += ylinetext.printsvg()
                self.yinc = auxinc * cont
                cont += 1
            cont = 0
            self.yinc = auxinc
            while int(self.yinc) <= xmaxaxis:
                linextext = Linetextvertical(self.xorigin + int(self.yinc),
                                             self.yorigin + ymaxaxis, fontsize, 
                                             self.yinc)
                string += linextext.printsvg()
                self.yinc = auxinc * cont
                cont += 1
            #create axes and the path defined by the dotted line
            lpoints = self.transformtocoordenates(self.lval, ymaxaxis)
            lpointsordenate = list(self.ordenatewithquicksort(lpoints, 
                              int(self.xcolumn) - 1, len(lpoints) - 1))
            #initial and end point of the path
            lpointsordenate.insert(0, [lpointsordenate[0][0], ymaxaxis])
            lpointsordenate.append([self.getmaxpoint(self.lval
                                    [int(self.xcolumn) - 1]), ymaxaxis])
            plotline = Linepath(self.xorigin, self.yorigin, "plotline",
                               lpointsordenate, self.fillcolor, self.ptcolor)
            string += plotline.printsvg() 
            
            if (len(self.lval) > int(self.xcolumn2)):
                lpoints2 = self.transformtocoordenates(self.lval[2:], ymaxaxis)
                lpointsordenate2 = list(self.ordenatewithquicksort(lpoints2,
                                   int(self.xcolumn) - 1, len(lpoints2) - 1))
                lpointsordenate2.insert(0, [lpointsordenate2[0][0], ymaxaxis])
                lpointsordenate2.append([self.getmaxpoint(self.lval
                                    [int(self.xcolumn2) - 1]), ymaxaxis])
                plotline2 = Linepath(self.xorigin, self.yorigin, "plotline2",
                                     lpointsordenate2, self.fillcolor2,
                                     self.pt2color)
                string += plotline2.printsvg()       
            #draw points
            for cont in range(len(self.lval[int(self.xcolumn) - 1])):
                xpoint = int(self.lval[int(self.xcolumn) - 1][cont]) \
                        + int(self.xorigin)
                ypoint = int(self.yorigin) + ymaxaxis \
                         - int(self.lval[int(self.ycolumn) - 1][cont])
                
                string += self.getsvgpoint(xpoint, ypoint, self.ptsym, 
                                           self.ptcolor, self.ptsize)

                if (len(self.lval) > int(self.xcolumn2)):
                    ycolumn2 = len(self.lval)
                    xpoint2 = int(self.lval[int(self.xcolumn2) - 1]
                                  [cont]) + int(self.xorigin)
                    ypoint2 = int(self.yorigin) + ymaxaxis - \
                              int(self.lval[int(ycolumn2) - 1][cont]) 
                    string += self.getsvgpoint(xpoint2, ypoint2, self.pt2sym,
                                               self.pt2color, self.ptsize)
    
            #draw the axis labels
            if self.xlabel != "":
                xtext = Text(self.xorigin + (xmaxaxis / 2), 1.5 * self.yorigin
                              + ymaxaxis, fontsize, self.xlabel)
                string += xtext.printsvg()
            if self.ylabel != "":
                ytext = Verticaltext(self.xorigin - self.xorigin / 2,
                                     self.yorigin + (ymaxaxis / 2),
                                     fontsize, self.ylabel, 0)
                string += ytext.printsvg()
                
            #draw the legend
            if self.legend:          
                linelegend = Line(self.xorigin, 1.75 * self.yorigin + ymaxaxis,
                                  self.xorigin + linelegendsize, 
                                1.75 * self.yorigin + ymaxaxis, "no",
                                  self.ptcolor)
                textlegend = Text(self.xorigin + 2 * linelegendsize,
                                  1.75 * self.yorigin + ymaxaxis, fontsize,
                                  self.name)
                if (len(self.lval) > int(self.xcolumn2)):
                    linelegend2 = Line(self.xorigin, 1.8 * self.yorigin +
                                       ymaxaxis + linelegendsize, self.xorigin
                                       + linelegendsize, 1.8 * self.yorigin + 
                                       ymaxaxis + linelegendsize, "no",
                                       self.pt2color)
                    textlegend2 = Text(self.xorigin + 2 * linelegendsize,
                                       1.8 * self.yorigin + ymaxaxis +
                                       linelegendsize, fontsize, self.name2)
                    string += linelegend.printsvg() + textlegend.printsvg() + \
                              linelegend2.printsvg() + textlegend2.printsvg()   
                else:
                    string += linelegend.printsvg() + textlegend.printsvg()
            if self.title != "":
                lineplottitle = Text((self.xorigin + xmaxaxis) / 2, 
                                     self.yorigin / 2, 12, self.title)
                string += lineplottitle.printsvg() 
            return string
        except IndexError:
            print "The number of columns in data file must be equal to the"\
            + " maximum value indicated by the parameters x, y, x2, y2"\
            + "\nPlease review the input data \nFor help use --help"\
            + "\npysvg 0.0.4-Oct2011\nCopyright (C) 2011 Isabel Rodriguez"\
            + "\nYou can see the full documentation at URL:"\
            + " \"http://www.pysvg/orgfree.com\""  
            sys.exit(2)
