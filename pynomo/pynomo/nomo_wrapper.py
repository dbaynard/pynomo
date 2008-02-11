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
    def __init__(self,params={},paper_width=10.0,paper_height=10.0):
                # default parameters
        self.params_default={
            'title_str':'',
            'title_x': paper_width/2.0,
            'title_y': paper_height,
            'title_box_width': paper_width/2.2}
        self.params=self.params_default
        self.params.update(params)
        self.nomo_blocks=[]

    def add_nomo(self,nomo_block):
        """
        adds nomograph (Nomo_Block) to the wrapper
        """
        self.nomo_blocks.append(nomo_block)

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


class Nomo_Block:
    """
    class to hold separate nomograhs connected by a single line in
    order to build the whole paper
    """
    def __init__(self,params={}):
        """
        type: N,III,...
        parameters: dict with parameters
        """
        # default parameters
        self.params_default={
            'u_title':'f(u)',
            'u_title_x_shift':0.0,
            'u_title_y_shift':0.25,
            'u_scale_type':'linear',
            'u_tick_levels':10,
            'u_tick_text_levels':10,
            'u_tick_dir':-1,
            'u_tag':'A',
            'v_title':'f(v)',
            'v_title_x_shift':0.0,
            'v_title_y_shift':0.25,
            'v_scale_type':'linear',
            'v_tick_levels':10,
            'v_tick_text_levels':10,
            'v_tick_dir':1,
            'v_tag':'B',
            'w_title':'f(w)',
            'w_title_x_shift':0.0,
            'w_title_y_shift':0.25,
            'w_scale_type':'linear',
            'w_tick_levels':10,
            'w_tick_text_levels':10,
            'w_tick_dir':-1,
            'w_tag':'C'}
        self.params=self.params_default
        self.params.update(params)


if __name__=='__main__':
    """
    testing
    """
    test=Nomo_Wrapper()
    print test._calc_trafo_(1,0,1,1,2,0,1,0,1,1,2,0)
    print test._calc_trafo_(1,0,1,1,2,0,4,1,4,2,5,1)