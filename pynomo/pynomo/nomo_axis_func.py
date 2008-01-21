#
#    This file is part of PyNomo -
#    a program to create nomographs with Python (http://pynomo.sourceforge.net/)
#
#    Copyright (C) 2007-2008  Leif Roschier  <lefakkomies@users.sourceforge.net>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.



class Axis_Wrapper:
    """
    class to wrap axis functionalities. Grid_wrapper and other classes
    will be derived from this.
    """
    def __init__(self):
        pass

    def set_transformation(self):
        """
        sets the transformation for x,y points to be applied
        """
        pass

    def calc_length(self,transformation):
        """
        calculates length of the basic line
        """
        pass


class Axes_Wrapper:
    """
    class to wrap axes group functionalities. For optimization of
    axes w.r.t. to paper
    """
    def __init__(self):
        pass

    def add_axis(self):
        """
        sets the transformation for x,y points to be applied
        """
        pass

    def define_paper_size(self):
        """
        sets proportion of the paper
        """
        pass

    def optimize_tranformation(self):
        """
        returns optimal transformation
        """
        pass


