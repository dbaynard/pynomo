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
import math
from pyx import *

class Isopleth_Wrapper(object):
    """
    class to hold all isopleths and control everything related to them
    """
    def __init__(self):
        self.isopleth_list=[] # list of isopleth objects
        self.solutions=[] # list of dictionaries (solutions)
    def add_isopleth_block(self,block):
        """
        Add block of type derived from Isopleth_Block
        """
        self.isopleth_list.append(block)

    def draw(self,canvas):
        """
        solves isopleths and draws them
        """
        for isopleth in self.isopleth_list:
            isopleth.calc_atoms()
        self._solve_()
        for isopleth in self.isopleth_list:
            isopleth.draw(canvas)

    def _solve_(self):
        """
        solves unknown values
        """
        for isopleth in self.isopleth_list:
            isopleth.solve(self.solutions)



class Isopleth_Block(object):
    """
    parent class for isopleth generation for blocks.
    Isopleths should be instanced once Atoms have final transformations
    """
    def __init__(self,block,params):
        """
        params is for example:
        {
        'isopleth_values':[['x1',0.1,0.2]],
        }
        if x1 is found outside this implementation, 'x1' is replaced
        by tuple (x,y) of the coordinate pair
        """
        self.params=params
        self.block=block
        self.isopleth_values=params['isopleth_values']
        self.atom_stack=block.atom_stack
        self.draw_coordinates=[] # coordinates [[x1,y1,x2,y2,x3,y3],...] to be drawn

    def calc_atoms(self):
        """
        calculates coordinates for atoms
        """
        for atom in self.atom_stack:
            # calculates lines (list of coordinates)
            atom.calc_line_and_sections()

    def _replace_found_values_(self,found_dict={}):
        """
        replaces found variables with the coordinates
        found_dict is of form (for example)
        {
        'x1':(1.0,2.0),
        'y2':(3.4,2.1)
        }
        """
        for key in found_dict.keys():
            if self.params['points'].count(key)>0:
                idx=self.params['points'].index(key)
                self.params['points'][idx]=found_dict[key]

    def _calc_distance_(self,x0,y0,x1,y1,x2,y2):
        """
        Calculates distance of point (x0,y0) from line passing
        through points (x1,y1), (x2,y2)
        """
        return abs((x2-x1)*(y1-y0)-(x1-x0)*(y2-y1))/math.sqrt((x2-x1)**2+(y2-y1)**2)

    def _calc_distance_points_(self,x1,y1,x2,y2):
        """
        calcs distance between two points
        """
        return math.sqrt((x1-x2)**2+(y1-y2)**2)

    def _find_closest_point_(self,line,x1,y1,x2,y2):
        """
        finds closest point of isopleth and axis (scale)
        """
        x=line[0][0]
        y=line[0][1]
        distances=[]
        smallest_distance=self._calc_distance_(x,y,x1,y1,x2,y2)
        distances.append(smallest_distance)
        smallest_idx=0
        for idx,(x,y) in enumerate(line):
            distance=self._calc_distance_(x,y,x1,y1,x2,y2)
            distances.append(distance)
            if distance<smallest_distance:
                smallest_distance=distance
                smallest_idx=0
        if idx==0:
            idx2=1
        if idx==len(distances):
            idx2=len(distances)-1
        if idx>0 and idx<len(distances):
            if distances[idx-1]<distances[idx+1]:
                idx2=idx-1
            else:
                idx2=idx+1
        sum_distance=distances[idx]+distances[idx2]
        middle_x=distances[idx]/sum_distance*line[idx][0]+\
                 distances[idx2]/sum_distance*line[idx2][0]
        middle_y=distances[idx]/sum_distance*line[idx][1]+\
                 distances[idx2]/sum_distance*line[idx2][1]
        return middle_x,middle_y

    def collinear(self,x1,y1,x2,y2,x3,y3):
        determinant=x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2)
        if abs(determinant)<1e-3:
            return True
        else:
            return False

    def find_farthest_pair(self,x1,y1,x2,y2,x3,y3):
        """
        finds farthest two points of three
        """
        dist_12=self._calc_distance_points_(x1,y1,x2,y2)
        dist_13=self._calc_distance_points_(x1,y1,x3,y3)
        dist_23=self._calc_distance_points_(x2,y2,x3,y3)
        if dist_12>=dist_13 and dist_12>=dist_23:
            return x1,y1,x2,y2
        if dist_13>=dist_23 and dist_13>=dist_12:
            return x1,y1,x3,y3
        if dist_23>=dist_13 and dist_23>=dist_12:
            return x2,y2,x3,y3


    def draw(self,canvas):
        """
        draws the isopleth
        """
        for (x1,y1,x2,y2,x3,y3) in self.draw_coordinates:
            xx1,yy1,xx2,yy2=self.find_farthest_pair(x1,y1,x2,y2,x3,y3)
            print xx1,yy1,xx2,yy2
            # check for collinearity
#            if not self.collinear(x1, y1, x2, y2, x3, y3):
#                print "found points not collinear in isopleth..."
            canvas.stroke(path.line(xx1,yy1,xx2,yy2),[color.cmyk.Black,
                                                    style.linewidth.thick,
                                                    style.linestyle.dashed])

    def solve(self,solutions):
        """
        parent class to be overriden, solves coordinates
        """
        pass

    def _check_if_enough_params_(self,idx):
        """
        parent class to be overriden, checks if enough params to solve
        """
        pass

class Isopleth_Block_Type_1(Isopleth_Block):
    """
    type F1+F2+F3=0 isopleth
    atom stack is the stack of scales
    solution_dict is a dictionary of found solutions
    """
    def __init__(self,block,params):
        super(Isopleth_Block_Type_1,self).__init__(block,params)

    def _check_if_enough_params_(self,idx):
        """
        checks if enough numbers given to find solution
        """
        numbers=self.isopleth_values[idx]
        given=0
        for number in numbers:
            if isinstance(number,(int,float)):
                         given=given+1
        if given<2:
            return False # isopleth not solvable (right now)
        else:
            return True # isopleth solvable

    def solve(self,solutions):
        """
        solves coordinates
        solutions is list of dicts of found solutions
        """
        for idx,isopleth_values_single in enumerate(self.isopleth_values):
            if len(self.draw_coordinates)<(idx+1):
                self.draw_coordinates.append([]) # dummy expansion of matrix
            if self._check_if_enough_params_(idx):
                if len(solutions)<(idx+1):
                    solutions.append({})
                x0,y0,x1,y1,x2,y2=self.solve_single(solutions[idx],
                                                    isopleth_values_single)
                self.draw_coordinates[idx]=[x0,y0,x1,y1,x2,y2]


    def solve_single(self,solution,isopleth_values):
        """
        solves single isopleth
        solution = dict with values of found solutions
        isopleth_values = list of values and coordinates
        """
        atom_stack=self.atom_stack
        f1_known=False
        f2_known=False
        f3_known=False
        # f1 known
        if isinstance(isopleth_values[0],(int,float)):
            x0=atom_stack[0].give_x(isopleth_values[0])
            y0=atom_stack[0].give_y(isopleth_values[0])
            f1_known=True
        # f2 known
        if isinstance(isopleth_values[1],(int,float)):
            x1=atom_stack[1].give_x(isopleth_values[1])
            y1=atom_stack[1].give_y(isopleth_values[1])
            f2_known=True
        # f3 known
        if isinstance(isopleth_values[2],(int,float)):
            x2=atom_stack[2].give_x(isopleth_values[2])
            y2=atom_stack[2].give_y(isopleth_values[2])
            f3_known=True
        if not f1_known:
            line=self.atom_stack[0].line
            x0,y0=self._find_closest_point_(line,x1,y1,x2,y2)
            solution[isopleth_values[0]]=(x0,y0)
            isopleth_values[0]=(x0,y0)
        if not f2_known:
            line=self.atom_stack[1].line
            x1,y1=self._find_closest_point_(line,x0,y0,x2,y2)
            solution[isopleth_values[1]]=(x1,y1)
            isopleth_values[1]=(x1,y1)
        if not f3_known:
            line=self.atom_stack[2].line
            x2,y2=self._find_closest_point_(line,x0,y0,x1,y1)
            solution[isopleth_values[2]]=(x2,y2)
            isopleth_values[2]=(x2,y2)
        return x0,y0,x1,y1,x2,y2
