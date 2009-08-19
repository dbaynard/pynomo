#
#    This file is part of PyNomo -
#    a program to create nomographs with Python (http://pynomo.sourceforge.net/)
#
#    Copyright (C) 2007-2009  Leif Roschier  <lefakkomies@users.sourceforge.net>
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

class Isopleth(object):
    """
    parent class for isopleth generation for blocks
    """
    def __init__(self,params,atom_stack):
        self.params=params
        self.atom_stack=atom_stack

class Isopleth_Block_Type_1(Isopleth,params,atom_stack,solution_dict):
    """
    type F1+F2+F3=0 isopleth
    atom stack is the stack of scales
    solution_dict is a dictionary of found solutions
    """
    def __init__(self,params,atom_stack):
        super(Isopleth_Block_Type_1,self).__init__(params,atom_stack,solution_dict)

    def _check_if_enough_params_(self):
        """
        checks if enough numbers given to find solution
        """
        numbers=self.params['numbers']
        given=0
        for number in numbers:
            if isintance(number,(int,float)):
                         given=given+1
        if given<2:
            return False # isopleth not solvable (right now)
        else:
            return True # isopleth solvable
