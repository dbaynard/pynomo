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

from pyx import *
from math import *
from scipy import *
from numpy import *
from nomo_axis import *
import time


class Nomo_Grid_Box(object):
    """
    class to draw "grid boxes" according to (East)-German nomographies
    """
    def __init__(self,params={}):
        """
        params = definitions
        """
        params_default_values={'width':10.0,
                               'height':10.0,
                               'u_start':0.0,
                               'u_stop':1.0,
                               'u_func':lambda u:u,
                               'v_start':0.0,
                               'v_stop':1.0*pi/2,
                               'v_func':lambda x,para:x+para,
                               'u_values':[0.0,0.25*pi/2,0.5*pi/2,0.75*pi/2,1.0*pi/2],
                               'v_values':[0.0,0.25*pi/2,0.5*pi/2,0.75*pi/2,1.0*pi/2],
                               'manual_axis_data':None # manual labels
                               }
        self.params=params_default_values
        self.params.update(params)
        self.u_func=self.params['u_func']
        self.v_func=self.params['v_func']
        #testing
        #self.line,self.sections=self._build_x_line(p=1.0)
        self._scale_funcs_vertical_()
        self._build_v_lines_()
        self._calc_bound_box_ini_()
        self._build_u_lines_()

#        v_func_temp=self.v_func
#        self.v_func=lambda x,v:v_func_temp((x-self.x_left_ini)/\
#                                           (self.x_right_ini-self.x_left_ini)*\
#                                           self.params['width'],v)
#        self._scale_funcs_vertical_()
#        self._build_v_lines_()
#        self._calc_bound_box_ini_()
#        self._build_u_lines_()

        self._draw_debug_ini_()

    def _scale_ini_to_width_height_(self):
        """
        scales initial coordinates to width and to height
        """
        # bounding box initial have to still ok
        pass

    def _scale_funcs_vertical_(self):
        """
        scales functions such that maximum value gives 1.0 and minimum 0.0
        """
        max_fu=self.u_func(self.params['u_values'][0])
        min_fu=max_fu
        for u in self.params['u_values']:
            fu=self.u_func(u)
            if fu>max_fu:
                max_fu=fu
            if fu<min_fu:
                min_fu=fu
        self.u_func = lambda u:(self.params['u_func'](u)-min_fu)/(max_fu-min_fu)*self.params['height']
        self.v_func = lambda x,v:(self.params['v_func'](x,v)-min_fu)/(max_fu-min_fu)*self.params['height']

    def _build_u_scale_(self):
        """
        vertical scale on the left
        """
        pass

    def _build_v_scale_(self):
        """
        horizontal scale on the top
        """
        pass

    def _build_u_lines_(self):
        """
        lines starting from u scale
        """
        self.u_lines=[]
        self.u_sections=[]
        g=self.u_func
        for u in self.params['u_values']:
            line = [(self.x_left_ini, g(u))]
            line.append((self.x_left_ini, g(u)))
            line.append((self.x_right_ini, g(u)))
            section=[(self.x_left_ini,g(u),self.x_right_ini,g(u))]
            self.u_lines.append(line)
            self.u_sections.append(section)

    def _build_v_lines_(self):
        """
        build lines starting from top scale
        """
        self.v_lines=[]
        self.v_sections=[]
        for p in self.params['v_values']:
            line,sections = self._build_v_line_(p)
            self.v_lines.append(line)
            self.v_sections.append(sections)

    def _build_v_line_(self,p=1.0):
        """
        line starting from x scale
        code copied originally form nomo_axis_func.py: _calculate_points_
        p is the parametric value of the top scale
        """
        #func2=self.params['v_func']
        func2=self.v_func
        func_top=lambda x:(func2(x,p)-self.params['height'])**2 # minimum at height
        func_bottom=lambda x:(func2(x,p))**2 # minimum at 0.0
        f=lambda x:x
        g=lambda x:func2(x,p)
        # find point of scale to meet point 1.0
        x_top=optimize.fmin(func_top,[1.0],disp=0,ftol=1e-5,xtol=1e-5)[0]
        x_bottom=optimize.fmin(func_bottom,[1.0],disp=0,ftol=1e-5,xtol=1e-5)[0]
        print "x_top %f"%x_top
        print "x_bottom %f" % x_bottom
        print "g(x_top) %f"%g(x_top)
        print "g(x_bottom) %f" %g(x_bottom)

        start=min(x_top,x_bottom)
        stop=max(x_top,x_bottom)
        du=fabs(stop-start)*1e-12
        # approximate line length is found
        line_length_straigth=1.0
        sections=200.0 # number of sections
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
                if u<stop:
                    line.append((f(u), g(u)))
                #print "count %f"%count
            else:
                line.append((f(stop), g(stop)))
                print count
                #print line
                break
        # calculate sections
        sections=[]
        for index,(x,y) in enumerate(line):
            if index>1:
                sections.append((x,y,prev_x,prev_y))
            prev_x=x
            prev_y=y
        return line,sections

    def _calc_bound_box_ini_(self):
        """
        calculates bounding inital bounding box
        """
        (x_0,y_0)=self.v_lines[0][0]
        x_left=x_0
        y_top=y_0
        x_right=x_0
        y_bottom=y_0
        for line in self.v_lines:
            for x,y in line:
                if x<x_left:
                    x_left=x
                if x>x_right:
                    x_right=x
                if y<y_bottom:
                    y_bottom=y
                if y>y_top:
                    y_top=y
                    #print "y_top %f"%y_top
        #print x_left,x_right,y_bottom,y_top
        self.x_left_ini=x_left
        self.x_right_ini=x_right
        self.y_top_ini=y_top
        self.y_bottom_ini=y_bottom
        return x_left,x_right,y_bottom,y_top


    def _build_box_(self):
        """
        box around structure
        """
        pass

    def _build_diagonal_line(self):
        """
        diagonal line to make 90 degree angle
        """
        pass

    def _draw_debug_ini_(self,filename='nomo_grid_test_debug.pdf'):
        """
        draws lines for debugging purposes, initial figure
        """
        cc=canvas.canvas()
        x00,y00=self.u_lines[0][0]
        line = path.path(path.moveto(x00, y00))
        for u_line in self.u_lines:
            x0,y0=u_line[0]
            line.append(path.moveto(x0, y0))
            for x,y in u_line:
                line.append(path.lineto(x, y))
        for v_line in self.v_lines:
            x0,y0=v_line[0]
            line.append(path.moveto(x0, y0))
            for x,y in v_line:
                line.append(path.lineto(x, y))

        cc.stroke(line, [style.linewidth.normal])
        cc.writePDFfile(filename)

if __name__=='__main__':
    tic = time.time()
    test=Nomo_Grid_Box()
    toc = time.time()
    print toc-tic,' has elapsed'



    manual_axis_data={1.0:'first',
                     2.0:'second',
                     3.0:'third',
                     3.1415:r'$\pi$',
                     4.0:'fourth',
                     5.0:'fifth',
                     6.0:'sixth',
                     7.0:'seventh',
                     8.0:'eigth',
                     9.0:'nineth',
                     10.0:'tenth'}