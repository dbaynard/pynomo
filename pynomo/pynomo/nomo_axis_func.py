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

from math import *
from scipy import *
from numpy import *
import random

class Axis_Wrapper:
    """
    class to wrap axis functionalities. Grid_wrapper and other classes
    will be derived from this.
    """
    def __init__(self,f,g,start,stop,sections=350):
        self.sections=sections # how many sections are used for calculations
        self.f=f
        self.g=g
        self.start=start
        self.stop=stop
        # initial transformation coeffs
        self.set_transformation()
        self._calculate_points_()
        self.calc_length()
        self.calc_bound_box()

    def _calculate_points_(self):
        """
        calculates points and segments of the line
        """
        f=self.f
        g=self.g
        start=self.start
        stop=self.stop
        du=fabs(start-stop)*1e-12
        # approximate line length is found
        line_length_straigth=sqrt((f(start)-f(stop))**2+(g(start)-g(stop))**2)
        random.seed(0.1) # so that mistakes always the same
        for dummy in range(100):
            first=random.uniform(start,stop)
            second=random.uniform(start,stop)
            temp=sqrt((f(first)-f(second))**2+(g(first)-g(second))**2)
            if temp>line_length_straigth:
                line_length_straigth=temp
                #print "length: %f"%line_length_straigth
        sections=self.sections # about number of sections
        section_length=line_length_straigth/sections
        line = [(f(start), g(start))]
        line.append((f(start), g(start)))
        u=start
        count=1
        while True:
            if u<stop:
                dx=(f(u+du)-f(u))
                dy=(g(u+du)-g(u))
                dl=sqrt(dx**2+dy**2)
                delta_u=du*section_length/dl
                # let's calculate actual length
                # and iterate until length is in factor 2 from target
                while True:
                    delta_x=f(u+delta_u)-f(u)
                    delta_y=g(u+delta_u)-g(u)
                    delta_l=sqrt(delta_x**2+delta_y**2)
                    if delta_l>2.0*section_length:
                        delta_u=delta_u*0.999
                        #print "delta_u pienenee:%f"%delta_u
                    else:
                        if delta_l<section_length/2.0:
                            delta_u=delta_u*1.001
                            #print "delta_u kasvaa:%f"%delta_u
                    if delta_l<=2*section_length and delta_l>=0.5*section_length:
                        break

                u+=delta_u
                #print u,stop
                count=count+1
                line.append((f(u), g(u)))
            else:
                line.append((f(stop), g(stop)))
                #print count
                #print line
                break
        self.line=line
        # calculate sections
        sections=[]
        for index,(x,y) in enumerate(line):
            if index>1:
                sections.append((x,y,prev_x,prev_y))
            prev_x=x
            prev_y=y
        self.sections=sections

    def give_trafo_x(self,x,y):
        """
        transformed x-coordinate
        """
        return ((self.alpha1*x+self.beta1*y+self.gamma1)\
        /(self.alpha3*x+self.beta3*y+self.gamma3))

    def give_trafo_y(self,x,y):
        """
        transformed y-coordinate
        """
        return ((self.alpha2*x+self.beta2*y+self.gamma2)\
        /(self.alpha3*x+self.beta3*y+self.gamma3))

    def set_transformation(self,alpha1=1.0,beta1=0.0,gamma1=0.0,
                           alpha2=0.0,beta2=1.0,gamma2=0.0,
                           alpha3=0.0,beta3=0.0,gamma3=1.0):
        """
        sets the transformation for x,y points to be applied
        see funcs give_trafo_x and give_trafo_y for details
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

    def calc_length(self):
        """
        calculates length of the basic line
        """
        length=0
        for x1,y1,x2,y2 in self.sections:
            x1t=self.give_trafo_x(x1, y1)
            y1t=self.give_trafo_y(x1, y1)
            x2t=self.give_trafo_x(x2, y2)
            y2t=self.give_trafo_y(x2, y2)
            section=sqrt((x1t-x2t)**2+(y1t-y2t)**2)
            length=length+section
        #print length
        self.length=length
        return length

    def calc_bound_box(self):
        """
        calculates bounding box for axis
        """
        line=self.line
        (x_0,y_0)=line[0]
        x_left=self.give_trafo_x(x_0, y_0)
        y_top=self.give_trafo_y(x_0, y_0)
        x_right=self.give_trafo_x(x_0, y_0)
        y_bottom=self.give_trafo_y(x_0, y_0)
        for x,y in line:
            x_trafo=self.give_trafo_x(x, y)
            y_trafo=self.give_trafo_y(x, y)
            if x_trafo<x_left:
                x_left=x_trafo
            if x_trafo>x_right:
                x_right=x_trafo
            if y_trafo<y_bottom:
                y_bottom=y_trafo
            if y_trafo>y_top:
                y_top=y_trafo
        #print x_left,x_right,y_bottom,y_top
        self.x_left=x_left
        self.x_right=x_right
        self.y_top=y_top
        self.y_bottom=y_bottom
        return x_left,x_right,y_bottom,y_top





class Axes_Wrapper:
    """
    class to wrap axes group functionalities. For optimization of
    axes w.r.t. to paper
    """
    def __init__(self,paper_width=10.0,paper_height=10.0):
        self.paper_width=paper_width
        self.paper_height=paper_height
        self.paper_prop=paper_width/paper_height
        self.set_transformation()
        self.axes_list=[]

    def add_axis(self,axis):
        """
        adds axis to the list
        """
        self.axes_list.append(axis)

    def define_paper_size(self,paper_width=10.0,paper_height=10.0):
        """
        sets proportion of the paper
        """
        self.paper_width=paper_width
        self.paper_height=paper_height
        self.paper_prop=paper_width/paper_height

    def set_transformation(self,alpha1=1.0,beta1=0.0,gamma1=0.0,
                           alpha2=0.0,beta2=1.0,gamma2=0.0,
                           alpha3=0.0,beta3=0.0,gamma3=1.0):
        """
        sets the transformation for x,y points to be applied
        see funcs give_trafo_x and give_trafo_y for details
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

    def _set_transformation_to_all_axis_(self):
        """
        sets current transformation to all axes
        """
        for axis in self.axes_list:
            axis.set_transformation(alpha1=self.alpha1,beta1=self.beta1,gamma1=self.gamma1,
                           alpha2=self.alpha2,beta2=self.beta2,gamma2=self.gamma2,
                           alpha3=self.alpha3,beta3=self.beta3,gamma3=self.gamma3)

    def _calc_bounding_box_(self):
        """
        calculates bounding box for the axes
        """
        x_left,x_right,y_bottom,y_top=self.axes_list[0].calc_bound_box()
        for axis in self.axes_list:
            x_left0,x_right0,y_bottom0,y_top0=axis.calc_bound_box()
            if x_left0<x_left:
                x_left=x_left0
            if x_right0>x_right:
                x_right=x_right0
            if y_bottom0<y_bottom:
                y_bottom=y_bottom0
            if y_top0>y_top:
                y_top=y_top0
        self.x_left=x_left
        self.x_right=x_right
        self.y_top=y_top
        self.y_bottom=y_bottom
        self.Wt=self.x_right-self.x_left
        self.Ht=self.y_top-self.y_bottom
        return x_left,x_right,y_bottom,y_top

    def _calc_paper_area_(self):
        """
        calculates paper area needed to fit axes to
        given paper proportions
        """
        proportion=self.Wt/self.Ht
        if proportion>=self.paper_prop:
            W=self.Wt
            H=self.Wt/self.paper_prop
        else: #proportion<self.paper_prop
            W=self.Ht*self.paper_prop
            H=self.Ht
        self.paper_area=W*H

    def _calc_axes_length_sq_sum_(self):
        """
        calculates sum of axes squared lengths
        """
        length_sum_sq=0.0
        for axis in self.axes_list:
            length_sum_sq=length_sum_sq+(axis.calc_length())**2
        self.length_sum_sq=length_sum_sq
        return length_sum_sq

    def _set_params_to_trafo_(self,params):
        """
        sets transformation coeffs from optimization params
        """
        self.alpha1=params[0]
        self.beta1=params[1]
        self.gamma1=params[2]
        self.alpha2=params[3]
        self.beta2=params[4]
        self.gamma2=params[5]
        self.alpha3=params[6]
        self.beta3=params[7]
        self.gamma3=params[8]

    def _calc_min_func_(self,params):
        """
        calculates function to be minimized
        """
        print params
        self._set_params_to_trafo_(params) # sets tranformation parameters
        self._set_transformation_to_all_axis_() # applies trafo to every axis
        self._calc_bounding_box_()
        self._calc_paper_area_()
        self._calc_axes_length_sq_sum_()
        opt_value=self.paper_area/self.length_sum_sq
        return opt_value

    def optimize_transformation(self):
        """
        returns optimal transformation
        """
        x0=[1.0,0,0,0,1.0,0,0,0,1.0]
        optimize.fmin(self._calc_min_func_,x0,full_output=1)

    def _print_result_pdf_(self):
        """
        prints result pdf for debugging purposes
        """
        pass
        # print original
        # print transformed


if __name__=='__main__':
    """
    testing
    """
    def f1(L):
        return (2*(L*L-8*L-5)/(3*L*L+2*L+7))
    def g1(L):
        return 10*(8*L*L+12*L-8)/(3*L*L+2*L+7)

    def f2(L):
        return log10(L)
    def g2(L):
        return 10**(L)

    def f3(L):
        return 0.0
    def g3(L):
        return L

    def f4(L):
        return 3.0
    def g4(L):
        return L

    def f5(L):
        return 6.0
    def g5(L):
        return L

    test1_ax=Axis_Wrapper(f1,g1,0.5,1.0)
    test2_ax=Axis_Wrapper(f2,g2,0.5,1.0)
    test3_ax=Axis_Wrapper(f3,g3,0.0,1.0)
    test4_ax=Axis_Wrapper(f4,g4,0.0,2.0)
    test5_ax=Axis_Wrapper(f5,g5,0.0,3.0)
    test_wrap=Axes_Wrapper()
    test_wrap.add_axis(test3_ax)
    test_wrap.add_axis(test4_ax)
    test_wrap.add_axis(test5_ax)
    #test_wrap._calc_min_func_([3.0,0,0,0,2,0,0,0,1])
    test_wrap.optimize_transformation()