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
This module will be responsible for carrying out the
processing operations of the data file input and output.
"""
__docformat__ = 'epytext en'


###############################################################################
## Imports
###############################################################################


import sys


###############################################################################
## Functions
###############################################################################


def readinputfile(path):
    """
        Returns a list of column data input file.
        @param path: It is the path to the input data file
        @type path: C{string}
        @return: list of column data input file.
        @rtype: C{list}
    """

    cad = []
    finalcad = []
    try:
        datafile = open(path, "r")
    except IOError:
        print "Inputfile= " + str(path) + "\nNo such file or directory"
        print "For help use --help or -h"
        print "pysvg 0.0.4-Nov2011\nCopyright (C) 2011 Isabel Rodriguez"
        print "You can see the full documentation at URL:" + \
        "\"http://www.pysvg/orgfree.com\""
        sys.exit(2)
    fileline = datafile.readline()
    while fileline != "":
        cad1 = fileline.split()
        cad.append(cad1)
        fileline = datafile.readline()
    datafile.close()
    try:
        for poscad1 in range(len(cad1)):
            auxcad = []
            for poscad in range(len(cad)):
                auxcad.append(cad[poscad][poscad1])
            finalcad.append(auxcad)
    except IndexError:
        print "The number of values of the parameters x, x2, y or y2 must" + \
        "be equal," + " please review the input data \nFor help use --help"
        sys.exit(2)
    return finalcad


def writesvgfile(path, outstring):
    """
    Write to the file whose path is passed as parameter the value
    stored in the variable C{"outstring"}
    @param path: It is the path to the input data file
    @type path: C{string}
    @param outstring: It is the SVG document code of each graph
    @type outstring: C{string}
    @rtype: C{file.svg}
    """
    datafile = open(path, "w")
    datafile.write(outstring)
    datafile.close()
    print "Done: outputFile=" + str(path)
    print "pysvg 0.0.4-Nov2011\nCopyright (C) 2011 Isabel Rodriguez"
    print "You can see the full documentation at URL:" + \
    "\"http://www.pysvg/orgfree.com\""
