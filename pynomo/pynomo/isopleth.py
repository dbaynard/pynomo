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
import copy

class Isopleth_Wrapper(object):
    """
    class to hold all isopleths and control everything related to them
    """
    def __init__(self):
        self.isopleth_list=[] # list of isopleth objects
        self.solutions=[] # list of dictionaries (solutions)
        self.ref_tag_number=1 # to separate type 3 ref scales

    def add_isopleth_block(self,block,block_para):
        """
        Add block of type derived from Isopleth_Block
        """
        if block_para['block_type']=='type_1':
            iso_block=Isopleth_Block_Type_1(block.atom_stack,block_para)
            self.isopleth_list.append(iso_block)
        if block_para['block_type']=='type_2':
            iso_block=Isopleth_Block_Type_2(block.atom_stack,block_para)
            self.isopleth_list.append(iso_block)
        if block_para['block_type']=='type_7':
            iso_block=Isopleth_Block_Type_7(block.atom_stack,block_para)
            self.isopleth_list.append(iso_block)
        if block_para['block_type']=='type_10':
            iso_block=Isopleth_Block_Type_10(block.atom_stack,block_para)
            self.isopleth_list.append(iso_block)
        if block_para['block_type']=='type_3':
            # handle type 3 as multiple type 1
            N=block.N
            ref_N=N-3
            ref_atoms=block.atom_stack[N:(N+ref_N)]
            # set ref axes
            for idx,ref_atom in enumerate(ref_atoms):
                ref_atom.params['tag']='ref'+`idx`+`self.ref_tag_number`
            self.ref_tag_number=self.ref_tag_number+1
            atoms=block.atom_stack[:N]
            atom_stack_start=[atoms[0],atoms[1],ref_atoms[0]]
            atom_stack_stop=[ref_atoms[-1],atoms[-2],atoms[-1]]
            center_atom_stack=[]
            for idx in range(2,N-2):
                center_atom_stack.append([ref_atoms[idx-2],atoms[idx],ref_atoms[idx-1]])
            # make block params
            # start
            block_para_start=copy.deepcopy(block_para)
            block_para_start['isopleth_values']=[]
            for idx,isopleth_values in enumerate(block_para['isopleth_values']):
                block_para_start['isopleth_values'].append([block_para['isopleth_values'][idx][0],\
                                                            block_para['isopleth_values'][idx][1],'x'])
            # stop
            block_para_stop=copy.deepcopy(block_para)
            block_para_stop['isopleth_values']=[]
            for idx,isopleth_values in enumerate(block_para['isopleth_values']):
                block_para_stop['isopleth_values'].append(['x',block_para['isopleth_values'][idx][-2],\
                                                            block_para['isopleth_values'][idx][-1]])
            # middle
            block_para_middles=[]
            for idx in range(3,N-1):
                block_para_middles.append(copy.deepcopy(block_para))
                block_para_middles[-1]['isopleth_values']=[]
                for idx1,isopleth_values in enumerate(block_para['isopleth_values']):
                    block_para_middles[-1]['isopleth_values'].append(['x',block_para['isopleth_values'][idx1][idx-1],'x'])
            # do the list
            self.isopleth_list.append(Isopleth_Block_Type_1(atom_stack_start,block_para_start))
            for idx,atom_stack in enumerate(center_atom_stack):
                self.isopleth_list.append(Isopleth_Block_Type_1(atom_stack,block_para_middles[idx]))
            self.isopleth_list.append(Isopleth_Block_Type_1(atom_stack_stop,block_para_stop))
        # type 4
        if block_para['block_type']=='type_4':
            atoms=block.atom_stack
            atom_stack_12=[atoms[0],atoms[1],atoms[4]] # 4 = ref line
            atom_stack_34=[atoms[2],atoms[3],atoms[4]]
            # tag the reference line
            atoms[4].params['tag']='ref_type4'+`self.ref_tag_number`
            self.ref_tag_number=self.ref_tag_number+1
            # make blocks
            block_para_12=copy.deepcopy(block_para)
            block_para_12['isopleth_values']=[]
            for idx,isopleth_values in enumerate(block_para['isopleth_values']):
                block_para_12['isopleth_values'].append([block_para['isopleth_values'][idx][0],\
                                                            block_para['isopleth_values'][idx][1],'x'])
            block_para_34=copy.deepcopy(block_para)
            block_para_34['isopleth_values']=[]
            for idx,isopleth_values in enumerate(block_para['isopleth_values']):
                block_para_34['isopleth_values'].append([block_para['isopleth_values'][idx][2],\
                                                            block_para['isopleth_values'][idx][3],'x'])
            self.isopleth_list.append(Isopleth_Block_Type_1(atom_stack_12,block_para_12))
            self.isopleth_list.append(Isopleth_Block_Type_1(atom_stack_34,block_para_34))
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
        solutions_updated=True
        while solutions_updated:
            for idx,isopleth in enumerate(self.isopleth_list):
                isopleth.solve(self.solutions)
                # take initial values (they are most correct)
                isopleth.find_initial_solutions(self.solutions)
            # updates solutions
            solutions_updated=False
            for idx,isopleth in enumerate(self.isopleth_list):
                update=isopleth.update_solutions(self.solutions)
                if update==True:
                    solutions_updated=True
        # check for error
        for idx,isopleth in enumerate(self.isopleth_list):
            isopleth.check_if_all_solutions_found(self.solutions)


class Isopleth_Block(object):
    """
    parent class for isopleth generation for blocks.
    Isopleths should be instanced once Atoms have final transformations
    """
    def __init__(self,atom_stack,params):
        """
        params is for example:
        {
        'isopleth_values':[['x',0.1,0.2]],
        }
        if x is found outside this implementation, 'x' is replaced
        by tuple (x,y) of the coordinate pair
        """
        self.params=params
        #self.block=block
        self.isopleth_values=params['isopleth_values']
        self.atom_stack=atom_stack
        self.draw_coordinates=[] # coordinates [[x1,y1,x2,y2,x3,y3],...] to be drawn
        self.other_points=[] # list of list of additional solution coordinates

    def calc_atoms(self):
        """
        calculates coordinates for atoms
        """
        for atom in self.atom_stack:
            # calculates lines (list of coordinates)
            atom.calc_line_and_sections()

#    def _replace_found_values_(self,found_dict={}):
#        """
#        replaces found variables with the coordinates
#        found_dict is of form (for example)
#        {
#        'x1':(1.0,2.0),
#        'y2':(3.4,2.1)
#        }
#        """
#        for key in found_dict.keys():
#            if self.params['points'].count(key)>0:
#                idx=self.params['points'].index(key)
#                self.params['points'][idx]=found_dict[key]

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

    def _find_closest_point_old_(self,line,x1,y1,x2,y2):
        """
        finds closest point(S) of isopleth and axis (scale)
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
                smallest_idx=idx
        if smallest_idx==0:
            idx2=1
        if smallest_idx==len(line):
            idx2=len(line)-1
        if smallest_idx>0 and smallest_idx<len(line):
            if distances[smallest_idx-1]<distances[smallest_idx+1]:
                idx2=smallest_idx-1
            else:
                idx2=smallest_idx+1

#        sum_distance=distances[smallest_idx]+distances[idx2]
#        middle_x=distances[smallest_idx]/sum_distance*line[smallest_idx][0]+\
#                 distances[idx2]/sum_distance*line[idx2][0]
#        middle_y=distances[smallest_idx]/sum_distance*line[smallest_idx][1]+\
#                 distances[idx2]/sum_distance*line[idx2][1]
        # a better
        middle_x,middle_y=self._two_line_intersection_(line[smallest_idx][0],line[smallest_idx][1],
                                                        line[idx2][0], line[idx2][1],
                                                        x1,y1,x2,y2)
        return middle_x,middle_y

    def _find_closest_point_(self,sections,x1,y1,x2,y2):
        """
        finds closest point(S) of isopleth and axis (scale)
        """
        f=1.0 # factor to reduce double hits
        interps=[]
        for idx,(x1s,y1s,x2s,y2s) in enumerate(sections):
            x_inter,y_inter=self._two_line_intersection_(x1s,y1s,x2s*f,y2s*f,x1,y1,x2,y2)
            # check if instersection
            if (min(x1s,x2s*f)<=x_inter<=max(x1s,x2s*f)) and (min(y1s,y2s*f)<=y_inter<=max(y1s,y2s*f)):
                interps.append((x_inter,y_inter))
        if len(interps)<1:
            interps.append((-10,-10)) # dummy point
        return interps[0][0],interps[0][1]

    def _find_closest_other_points_(self,sections,x1,y1,x2,y2,x_found,y_found):
        """
        finds closest point(S) of isopleth and axis (scale)
        x_found, y_found are found already before
        """
        f=1-1e-12 # factor to reduce double hits
        interps=[]
        for idx,(x1s,y1s,x2s,y2s) in enumerate(sections):
            x_inter,y_inter=self._two_line_intersection_(x1s,y1s,x2s*f,y2s*f,x1,y1,x2,y2)
            # check if instersection
            if (min(x1s,x2s*f)<=x_inter<=max(x1s,x2*f)) and (min(y1s,y2s*f)<=y_inter<=max(y1s,y2s*f)):
                if not x_found==x_inter and not y_found==y_inter:
                    interps.append((x_inter,y_inter))
        return interps


    def collinear(self,x1,y1,x2,y2,x3,y3):
        determinant=x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2)
        if abs(determinant)<1e-3:
            return True
        else:
            return False

    def find_farthest_pair_extra(self,x1,y1,x2,y2,x3,y3,idx):
        """
        finds farthest pair including extra points
        """
        xf1,yf1,xf2,yf2=self.find_farthest_pair(x1,y1,x2,y2,x3,y3)
        for points in self.other_points[idx]:
            for (x,y) in points:
                xf1,yf1,xf2,yf2=self.find_farthest_pair(xf1,yf1,xf2,yf2,x,y)
        return xf1,yf1,xf2,yf2

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
        for idx,(x1,y1,x2,y2,x3,y3) in enumerate(self.draw_coordinates):
            xx1,yy1,xx2,yy2=self.find_farthest_pair_extra(x1,y1,x2,y2,x3,y3,idx)
            #print xx1,yy1,xx2,yy2
            # check for collinearity
#            if not self.collinear(x1, y1, x2, y2, x3, y3):
#                print "found points not collinear in isopleth..."
            canvas.stroke(path.line(xx1,yy1,xx2,yy2),[color.cmyk.Black,
                                                    style.linewidth.thick,
                                                    style.linestyle.dashed])
            self._draw_circle_(canvas,x1,y1,0.05)
            self._draw_circle_(canvas,x2,y2,0.05)
            self._draw_circle_(canvas,x3,y3,0.05)
        for line_points in self.other_points:
            for points in line_points:
                for (x,y) in points:
                    self._draw_circle_(canvas,x,y,0.05)

    def _draw_circle_(self,canvas,x,y,r):
        """
        draws marker circle
        """
        canvas.fill(path.circle(x, y, r), [color.rgb.white])
        canvas.stroke(path.circle(x,y,r))

    def solve(self,solutions):
        """
        parent class to be overriden, solves coordinates
        """
        pass

    def check_if_all_solutions_found(self,solutions):
        all_found=True
        for atom_idx,atom in enumerate(self.atom_stack):
            for idx,dummy in enumerate(solutions):
                if not isinstance(self.isopleth_values[idx][atom_idx],(int,float,tuple)):
                    print "not all isopleths solvable?"


    def find_initial_solutions(self,solutions):
        """
        Finds initial solutions
        """
        for atom_idx,atom in enumerate(self.atom_stack):
            if not atom.params['tag']=='none':
                for idx,dummy in enumerate(solutions):
                    if isinstance(self.isopleth_values[idx][atom_idx],(int,float,tuple)):
                        solutions[idx][atom.params['tag']]=self.isopleth_values[idx][atom_idx]


    def update_solutions(self,solutions):
        """
        Updates solutions
        """
        solutions_updated=False
        for idx,solution in enumerate(solutions):
            for key in solution.keys():
                for atom_idx,atom in enumerate(self.atom_stack):
                    if atom.params['tag']==key:
                        if isinstance(self.isopleth_values[idx][atom_idx],str):
                            self.isopleth_values[idx][atom_idx]=solution[key]
                            solutions_updated=True
        return solutions_updated



    def _check_if_enough_params_(self,idx):
        """
        parent class to be overriden, checks if enough params to solve
        """
        pass

    def _two_line_intersection_(self,x1,y1,x2,y2,x3,y3,x4,y4):
        """
        intersection of lines (x1,y1)-(x2,y2) and (x3,y3)-(x4,y4)
        """
        x=self._det_(self._det_(x1,y1,x2,y2),(x1-x2),self._det_(x3,y3,x4,y4),(x3-x4))/\
        self._det_(x1-x2,y1-y2,x3-x4,y3-y4)
        y=self._det_(self._det_(x1,y1,x2,y2),(y1-y2),self._det_(x3,y3,x4,y4),(y3-y4))/\
        self._det_(x1-x2,y1-y2,x3-x4,y3-y4)
        return x,y

    def _det_(self,a,b,c,d):
        return a*d-c*b

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
            if isinstance(number,(int,float,tuple)):
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
            if len(solutions)<(idx+1):
                solutions.append({})
            if len(self.other_points)<(idx+1):
                self.other_points.append([])
            if self._check_if_enough_params_(idx):
                x0,y0,x1,y1,x2,y2=self.solve_single(solutions[idx],
                                                    isopleth_values_single,idx)
                self.draw_coordinates[idx]=[x0,y0,x1,y1,x2,y2]


    def solve_single(self,solution,isopleth_values,idx):
        """
        solves single isopleth
        solution = dict with values of found solutions
        isopleth_values = list of values and coordinates
        idx = # of isopleth line
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
        if isinstance(isopleth_values[0],tuple):
            x0=isopleth_values[0][0]
            y0=isopleth_values[0][1]
            f1_known=True
        # f2 known
        if isinstance(isopleth_values[1],(int,float)):
            x1=atom_stack[1].give_x(isopleth_values[1])
            y1=atom_stack[1].give_y(isopleth_values[1])
            f2_known=True
        if isinstance(isopleth_values[1],tuple):
            x1=isopleth_values[1][0]
            y1=isopleth_values[1][1]
            f2_known=True
        # f3 known
        if isinstance(isopleth_values[2],(int,float)):
            x2=atom_stack[2].give_x(isopleth_values[2])
            y2=atom_stack[2].give_y(isopleth_values[2])
            f3_known=True
        if isinstance(isopleth_values[2],tuple):
            x2=isopleth_values[2][0]
            y2=isopleth_values[2][1]
            f3_known=True
        if not f1_known:
            #line=self.atom_stack[0].line
            x0,y0=self._find_closest_point_(self.atom_stack[0].sections,x1,y1,x2,y2)
            other_points=self._find_closest_other_points_(self.atom_stack[0].sections,x1,y1,x2,y2,x0,y0)
            #solution[isopleth_values[0]]=(x0,y0)
            if not self.atom_stack[0].params['tag']=='none':
                solution[self.atom_stack[0].params['tag']]=(x0,y0)
            isopleth_values[0]=(x0,y0)
            self.other_points[idx].append(other_points)
        if not f2_known:
            #line=self.atom_stack[1].line
            x1,y1=self._find_closest_point_(self.atom_stack[1].sections,x0,y0,x2,y2)
            other_points=self._find_closest_other_points_(self.atom_stack[1].sections,x0,y0,x2,y2,x1,y1)
            #solution[isopleth_values[1]]=(x1,y1)
            if not self.atom_stack[1].params['tag']=='none':
                solution[self.atom_stack[1].params['tag']]=(x1,y1)
            isopleth_values[1]=(x1,y1)
            self.other_points[idx].append(other_points)
        if not f3_known:
            #line=self.atom_stack[2].line
            x2,y2=self._find_closest_point_(self.atom_stack[2].sections,x0,y0,x1,y1)
            other_points=self._find_closest_other_points_(self.atom_stack[2].sections,x0,y0,x1,y1,x2,y2)
            #solution[isopleth_values[2]]=(x2,y2)
            if not self.atom_stack[2].params['tag']=='none':
                solution[self.atom_stack[2].params['tag']]=(x2,y2)
            isopleth_values[2]=(x2,y2)
            self.other_points[idx].append(other_points)
        return x0,y0,x1,y1,x2,y2

class Isopleth_Block_Type_2(Isopleth_Block_Type_1):
    """
    type F1=F2*F3 isopleth
    atom stack is the stack of scales
    solution_dict is a dictionary of found solutions
    """
    def __init__(self,block,params):
        super(Isopleth_Block_Type_2,self).__init__(block,params)

class Isopleth_Block_Type_7(Isopleth_Block_Type_1):
    """
    type 1/F1+1/F2=1/F3 isopleth
    atom stack is the stack of scales
    solution_dict is a dictionary of found solutions
    """
    def __init__(self,block,params):
        super(Isopleth_Block_Type_7,self).__init__(block,params)


class Isopleth_Block_Type_10(Isopleth_Block_Type_1):
    """
    type F1(u)+F2(v)*F3(w)+F4(w)=0
    atom stack is the stack of scales
    solution_dict is a dictionary of found solutions
    """
    def __init__(self,block,params):
        super(Isopleth_Block_Type_10,self).__init__(block,params)