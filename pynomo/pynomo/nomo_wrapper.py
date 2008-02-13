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

from numpy import *

class Nomo_Wrapper:
    """
    class for building nomographs consisting of many blocks (pieces connected by
    a line)
    """
    def __init__(self,params={},paper_width=10.0,paper_height=10.0,filename='dummy.pdf'):
                # default parameters
        self.params_default={
            'title_str':'',
            'title_x': paper_width/2.0,
            'title_y': paper_height,
            'title_box_width': paper_width/2.2}
        self.params=self.params_default
        self.params.update(params)
        self.block_stack=[]
        self.filename=filename

    def add_block(self,nomo_block):
        """
        adds nomograph (Nomo_Block) to the wrapper
        """
        self.block_stack.append(nomo_block)
        # TODO: calculate transformation according to tag

    def _calc_trafo_(self,x1,y1,x2,y2,x3,y3,x1d,y1d,x2d,y2d,x3d,y3d):
        """
        transforms three points to three points via rotation and scaling
        and transformation
        xd = alpha1*x+beta1*y+gamma1
        yd = alpha2*x+beta2*y+gamma2
        alpha3=0, beta3=0, gamma3=0
        """
        mat=array([[x1,y1,1.0,0.0,0.0,0.0],
                   [0,0,0,x1,y1,1],
                   [x2,y2,1,0,0,0],
                   [0,0,0,x2,y2,1],
                   [x3,y3,1,0,0,0],
                   [0,0,0,x3,y3,1]])
        #print rank(mat)
        inverse=linalg.inv(mat)
        vec=dot(inverse,[x1d,y1d,x2d,y2d,x3d,y3d])
        alpha1=vec[0]
        beta1=vec[1]
        gamma1=vec[2]
        alpha2=vec[3]
        beta2=vec[4]
        gamma2=vec[5]
        alpha3=0.0
        beta3=0.0
        gamma3=1.0
        return alpha1,beta1,gamma1,alpha2,beta2,gamma2,alpha3,beta3,gamma3

    def find_total_trafo(self,method=None):
        """
        Finds transformation according to given method
        uses class Axis_Wrapper in nomo_axis_func.py
        """
        pass

    def draw_nomogram(self,canvas):
        """
        draws the nomogram = draws blocks, titles, etc.
        """
        for block in block_stack:
            block.draw(canvas)
        c.writePDFfile(self.filename)


class Nomo_Block:
    """
    class to hold separate nomograph blocks connected by a single line in
    order to build the whole nomograph consisting of multiple blocks
    """
    def __init__(self,mirror=False):
        """
        if mirror=True the transformation wrt to other blocks is mirrored
        """

        """
        Idea is that block has one own tranformation that aligns it with respect to other
        blocks and one overall transformation that optimizes axes w.r.t. paper size.
        Overall transformation is calculated using class Axis_Wrapper in nomo_axis_func.py
        in wrapper class Nomo_Wrapper.
        """
        # initial transformation
        self.trafo_stack=[] # stack for transformation matrices for block
        self.add_transformation() # adds initial unit transformation
        self.atom_stack=[] # atoms

    def add_atom(self,atom):
        """
        adds atom to the block
        """
        self.atom_stack.append(atom)

    def add_transformation(self,alpha1=1.0,beta1=0.0,gamma1=0.0,
                             alpha2=0.0,beta2=1.0,gamma2=0.0,
                             alpha3=0.0,beta3=0.0,gamma3=1.0):
        """
        adds transformation to be applied as a basis.
        all transformation matrices are multiplied together
        """
        trafo_mat = array([[alpha1,beta1,gamma1],
                          [alpha2,beta2,gamma2],
                          [alpha3,beta3,gamma3]])
        self.trafo_stack.append(trafo_mat)
        self._calculate_total_trafo_mat_() # update coeffs

    def _calculate_total_trafo_mat_(self):
        """
        calculates total transformation matrix and
        master coeffs self.alpha1,self.beta1,...
        """
        stack_copy=copy(self.trafo_stack)
        stack_copy.reverse()
        trafo_mat=stack_copy.pop()
        for matrix in stack_copy:
            trafo_mat=dot(trafo_mat,matrix) # matrix multiplication
        self.alpha1=trafo_mat[0][0]
        self.beta1=trafo_mat[0][1]
        self.gamma1=trafo_mat[0][2]
        self.alpha2=trafo_mat[1][0]
        self.beta2=trafo_mat[1][1]
        self.gamma2=trafo_mat[1][2]
        self.alpha3=trafo_mat[2][0]
        self.beta3=trafo_mat[2][1]
        self.gamma3=trafo_mat[2][2]
        self._set_trafo_to_atoms()

    def _set_trafo_to_atoms(self):
        """
        sets overall transformation to all atoms
        """
        for atom in atom_stack:
            atom.set_trafo(alpha1=self.alpha1,beta1=self.beta1,gamma1=self.gamma1,
                           alpha2=self.alpha2,beta2=self.beta2,gamma2=self.gamma2,
                           alpha3=self.gamma3,beta3=self.beta3,gamma3=self.gamma3)

#    Maybe not needed
#
#    def give_trafo_x(self,x,y):
#        """
#        transformed x-coordinate
#        """
#        return ((self.alpha1*x+self.beta1*y+self.gamma1)\
#        /(self.alpha3*x+self.beta3*y+self.gamma3))
#
#    def give_trafo_y(self,x,y):
#        """
#        transformed y-coordinate
#        """
#        return ((self.alpha2*x+self.beta2*y+self.gamma2)\
#        /(self.alpha3*x+self.beta3*y+self.gamma3))


    def draw(self,canvas):
        """
        draws the Atoms of block
        """
        for atom in atom_stack:
            atom.draw(canvas)

class Nomo_Atom:
    """
    class for single axis or equivalent.
    """
    def __init__(self,params,f=lambda u:u,g=lambda v:v):
        # default parameters
        self.params_default={
            'u_min':0.1,
            'u_max':1.0,
            'title':'f1',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear', #'linear' 'log' 'manual point' 'manual line'
            'tick_levels':10,
            'tick_text_levels':10,
            'tick_side':'right',
            'tag':'A'} # for aligning block wrt others
        self.params=self.params_default
        self.params.update(params)
        set_trafo() # initialize
        self.f = f # x-coord func
        self.g = g # y-coord func

    def set_trafo(self,alpha1=1.0,beta1=0.0,gamma1=0.0,
                           alpha2=0.0,beta2=1.0,gamma2=0.0,
                           alpha3=0.0,beta3=0.0,gamma3=1.0):
        """
        sets the transformation for x,y points to be applied
        """
        self.alpha1=alpha1
        self.beta1=beta1
        self.gamma1=gamma1
        self.alpha2=alpha2
        self.beta2=beta2
        self.gamma2=gamma2
        self.alpha3=alpha3
        self.beta3=beta3
        self.gamma3=gamma3

    def give_x(self,u):
        """
        x-function
        """
        value=(self.alpha1*self.f(u)+self.beta1*self.g(u)+self.gamma1)/\
        (self.alpha3*self.f(u)+self.beta3*self.g(u)+self.gamma3)
        return value[0]

    def give_y(self,u):
        """
        y-function
        """
        value=(self.alpha2*self.f(u)+self.beta2*self.g(u)+self.gamma2)/\
        (self.alpha3*self.f(u)+self.beta3*self.g(u)+self.gamma3)
        return value[0]

    def draw(self,canvas):
        """
        draws the axis
        """
        p=self.params
        Nomo_Axis(func_f=self.give_x,func_g=self.give_y,
                  start=p['u_min'][2],stop=p['u_max'],
                  turn=-1,title=p['title'],canvas=canvas,type=p['scale_type'],
                  tick_levels=p['tick_levels'],tick_text_levels=p['tick_text_levels'])


if __name__=='__main__':
    """
    testing
    """
    test=Nomo_Wrapper()
    print test._calc_trafo_(1,0,1,1,2,0,1,0,1,1,2,0)
    print test._calc_trafo_(1,0,1,1,2,0,4,1,4,2,5,1)
    """
    0. build definitions of atoms
    1. build block1
    2. build block2
    3. build nomowrapper
    4. add block1 and block2
    5. optimize transformation
    6. draw nomogram in nomowrapper
    """

    # build atoms
    block1_atom1_para={
            'u_min':0.0,
            'u_max':1.0,
            'title':'b1 a1',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear',
            'tick_levels':10,
            'tick_text_levels':10,
            'tick_side':'right',
            'tag':'A'}
    b1_atom1=Nomo_Atom(params=block1_atom1_para,f=lambda u:0, g=lambda u:u)

    block1_atom2_para={
            'u_min':0.0,
            'u_max':1.0,
            'title':'b1 a1',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear',
            'tick_levels':10,
            'tick_text_levels':10,
            'tick_side':'right',
            'tag':'A'}
    b1_atom2=Nomo_Atom(params=block1_atom2_para,f=lambda u:1.0, g=lambda u:u)

    block1_atom3_para={
            'u_min':0.0,
            'u_max':1.0,
            'title':'b1 a1',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear',
            'tick_levels':10,
            'tick_text_levels':10,
            'tick_side':'right',
            'tag':'A'}

    b1_atom3=Nomo_Atom(params=block1_atom3_para,f=lambda u:2.0, g=lambda u:u)

    # block 2
    block2_atom1_para={
            'u_min':0.0,
            'u_max':1.0,
            'title':'b1 a1',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear',
            'tick_levels':10,
            'tick_text_levels':10,
            'tick_side':'right',
            'tag':'A'}
    b2_atom1=Nomo_Atom(params=block1_atom1_para,f=lambda u:u, g=lambda u:0.0)

    block1_atom2_para={
            'u_min':0.0,
            'u_max':1.0,
            'title':'b1 a1',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear',
            'tick_levels':10,
            'tick_text_levels':10,
            'tick_side':'right',
            'tag':'A'}
    b2_atom2=Nomo_Atom(params=block2_atom2_para,f=lambda u:u, g=lambda u:1.0)

    block1_atom3_para={
            'u_min':0.0,
            'u_max':1.0,
            'title':'b1 a1',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear',
            'tick_levels':10,
            'tick_text_levels':10,
            'tick_side':'right',
            'tag':'A'}

    b2_atom3=Nomo_Atom(params=block2_atom3_para,f=lambda u:u, g=lambda u:2.0)

    block1=Nomo_Block()
    block1.add_atom(b1_atom1)
    block1.add_atom(b1_atom2)
    block1.add_atom(b1_atom3)

    block2=Nomo_Block()
    block2.add_atom(b2_atom1)
    block2.add_atom(b2_atom2)
    block2.add_atom(b2_atom3)

    wrapper=Nomo_Wrapper()
    wrapper.add_block(block1)
    wrapper.add_block(block2)
    c=canvas.canvas()
    wrapper.draw_nomogram(c)