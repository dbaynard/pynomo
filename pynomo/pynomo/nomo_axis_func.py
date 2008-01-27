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
                print count
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
        print length
        self.length=length
        return length

    def calc_bound_box(self):
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
        print x_left,x_right,y_bottom,y_top



class Axes_Wrapper:
    """
    class to wrap axes group functionalities. For optimization of
    axes w.r.t. to paper
    """
    def __init__(self):
        pass


    def add_axis(self):
        """
        adds axis to the list
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

    def _calc_bounding_box_(self):
        """
        calculates bounding box for the axes
        """
        pass

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

    def f2(L):
        return 0.0
    def g2(L):
        return L


    test1_ax=Axis_Wrapper(f1,g1,0.5,1.0)
    test2_ax=Axis_Wrapper(f2,g2,0.5,1.0)
    test3_ax=Axis_Wrapper(f2,g2,0.0,1.0)