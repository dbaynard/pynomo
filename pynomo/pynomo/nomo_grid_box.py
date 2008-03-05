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
    class to calculate "grid boxes" according to (East)-German nomographic tradition
    """
    def __init__(self,params={}):
        """
        params = definitions
        """
        params_default_values={'width':10.0,
                               'height':10.0,
                               'u_func':lambda u:u,
                               'v_func':lambda x,para:x+para,
                               'line_func':lambda x:x, # function for centerline assuming square
                               'draw_line':True,
                               'w_func':lambda x:x, # function for w axis
                               'w_func_inv':lambda x:x, # inverse function for w axis
                               'w_min':0.1,
                               'w_max':1.0,
                               'manual_w_scale':False,
                               'x_min':0.1,
                               'x_max':1.0,
                               'manual_x_scale':False, # if inital x_scale is set manually, use two values above
                               'u_values':[0.0,0.25*pi/2,0.5*pi/2,0.75*pi/2,1.0*pi/2],
                               'v_values':[0.0,0.25*pi/2,0.5*pi/2,0.75*pi/2,1.0*pi/2],
                               'wd_values':[],
                               'w_values':[],
                               'u_tag':'none', # manual labels
                               'w_tag':'none',
                               'wd_tag':'none',
                               'u_reference':False, # manual labels
                               'v_reference':False,
                               'w_reference':True,
                               'wd_reference':False,
                               'scale_type_u':'manual line',
                               'scale_type_w':'linear',
                               'scale_type_wd':'linear',
                               'u_title':'u',
                               'v_title':'v',
                               'w_title':'',
                               'wd_title':'',
                               'u_tick_side':'left',
                               'v_tick_side':'right',
                               'w_tick_side':'right',
                               'wd_tick_side':'left'
                               }
        self.params=params_default_values
        self.params.update(params)
        # initial guesses
        self.u_func=self.params['u_func']
        self.v_func=self.params['v_func']
        self._build_v_lines_(self.v_func)
        self._calc_bound_box_ini_()
        self._build_u_lines_(self.u_func)
        #debug by looking pdf
        self._draw_debug_ini_()
        # build scaled versions
        self._scale_()
        self._draw_debug_ini_('after.pdf')

        self.give_u_data()
        self.give_v_data()
        self.give_w_data()
        self.give_wd_data()

    def give_u_data(self):
        """
        gives F(u),G(u)-functions and other params (left coordinate)
        """
        # calc func
        u_func = self.u_func # defined in scaling
        u_manual_axis_data = {}
        for u_value in self.params['u_values']:
            u_manual_axis_data[u_value]='%f'%u_value
        self.params_u={
            'u_min':min(self.params['u_values']),
            'u_max':max(self.params['u_values']),
            'F':lambda u:self.x_left, # x-coordinate
            'G':u_func, # y-coordinate
            'title':self.params['u_title'],
            'scale_type':self.params['scale_type_u'], #'linear' 'log' 'manual point' 'manual line'
            'manual_axis_data':u_manual_axis_data,
            'tick_side':self.params['u_tick_side'],
            'tag':self.params['u_tag'], # for aligning block wrt others
            'reference':self.params['u_reference']
            }
        return self.params_u

    def give_v_data(self):
        """
        givesgives F(u),G(u)-functions and other params (top coordinate)
        function is linear and values are set manually to correct places
        """
        v_manual_axis_data = {}
        # let's go through all lines and find x-coordinate of top points.
        for idx1,v_line in enumerate(self.v_lines):
            x_max,y_max = v_line[0]
            for idx2,(x,y) in enumerate(v_line):
                if y>y_max:
                    x_max=x
                    y_max=y
            v_value=self.params['v_values'][idx1]
            v_manual_axis_data[v_value]='%f'%x_max

        self.params_v={
            'u_min':min(self.params['v_values']),
            'u_max':max(self.params['v_values']),
            'F':lambda u:u, # x-coordinate
            'G':lambda u:self.y_top, # y-coordinate
            'title':self.params['v_title'],
            'scale_type':'manual line', #this have to be hard coded
            'manual_axis_data':v_manual_axis_data,
            'tick_side':self.params['v_tick_side'],
            'tag':'none', # this axis should not be aligned
            'reference':self.params['v_reference']
            }
        return self.params_v

    def give_w_data(self):
        """
        gives x(w),y(w)-functions and w_min and w_max values.
        w = f2(f3(x))
        x = bottom coordinate of initial axes
        f3 = line func
        f2 = additional transformation
        """
        f3=self.params['line_func']
        f2=self.params['w_func']
        f2_inv=self.params['w_func_inv']
        w_manual_axis_data={}
        if self.params['scale_type_w']=='manual line':
            for w_value in self.params['w_values']:
                w_manual_axis_data[w_value]='%f'%w_value

        w_min=f2(f3(self.x_left_ini))
        w_max=f2(f3(self.x_right_ini))
        w_diff=w_max-w_min
        self.params_w={
            'u_min':w_min,  #this is w_min
            'u_max':w_max, # this is w_max
            'F':lambda w:self.x_right, # x-coordinate
            'G':lambda w:self.y_bottom+(f2_inv(w)-f2_inv(w_min))/(f2_inv(w_max)-f2_inv(w_min))\
                        *self.params['height'], # y-coordinate
            'title':self.params['w_title'],
            'scale_type':self.params['scale_type_w'],
            'manual_axis_data':w_manual_axis_data,
            'tick_side':self.params['w_tick_side'],
            'tag':self.params['w_tag'], # for aligning block wrt others
            'reference':self.params['w_reference']
            }
        return self.params_w

    def give_wd_data(self):
        """
        gives x(wd),y(wd)-functions and wd_min and wd_max values. (bottom coordinate)
        """
        wd_manual_axis_data={}
        if self.params['scale_type_wd']=='manual line':
            for wd_value in self.params['wd_values']:
                wd_manual_axis_data[wd_value]='%f'%wd_value
        self.params_wd={
            'u_min':self.x_left_ini,
            'u_max':self.x_right_ini,
            'F':lambda u:u*self.x_factor, # x-coordinate
            'G':lambda u:self.y_bottom, # y-coordinate
            'title':self.params['wd_title'],
            'scale_type':self.params['scale_type_wd'],
            'manual_axis_data':wd_manual_axis_data,
            'tick_side':self.params['wd_tick_side'],
            'tag':self.params['wd_tag'], # for aligning block wrt others
            'reference':self.params['wd_reference']
            }
        return self.params_wd

    def give_contours(self):
        """
        gives contours to be drawn
        """
        pass


    def _scale_(self):
        """
        scales everything to width and height
        """
        # scales lines
        y_factor=self.params['height']/self.BB_height_ini
        x_factor=self.params['width']/self.BB_width_ini
        for idx1,u_line in enumerate(self.u_lines):
            for idx2,(x,y) in enumerate(u_line):
                x_new=x*x_factor
                y_new=y*y_factor
                self.u_lines[idx1][idx2]=(x_new,y_new)
        for idx1,v_line in enumerate(self.v_lines):
            for idx2,(x,y) in enumerate(v_line):
                x_new=x*x_factor
                y_new=y*y_factor
                self.v_lines[idx1][idx2]=(x_new,y_new)
        # scale functions
        self.u_func=lambda u:self.params['u_func'](u)*y_factor
        self.v_func=lambda x,v:self.params['v_func'](x/x_factor,v)*y_factor
        self.x_left=self.x_left_ini*x_factor
        self.x_right=self.x_right_ini*x_factor
        self.y_bottom=self.y_bottom_ini*y_factor
        self.y_top=self.y_top_ini*y_factor
        self.x_factor=x_factor
        self.y_factor=y_factor

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

    def _build_u_lines_(self,u_func):
        """
        lines starting from u scale
        """
        self.u_lines=[]
        self.u_sections=[]
        #g=self.u_func
        g=u_func
        for u in self.params['u_values']:
            line = [(self.x_left_ini, g(u))]
            line.append((self.x_left_ini, g(u)))
            line.append((self.x_right_ini, g(u)))
            section=[(self.x_left_ini,g(u),self.x_right_ini,g(u))]
            self.u_lines.append(line)
            self.u_sections.append(section)

    def _build_v_lines_(self,v_func):
        """
        build lines starting from top scale
        """
        self.v_lines=[]
        self.v_sections=[]
        for p in self.params['v_values']:
            line,sections = self._build_v_line_(v_func=v_func,p=p)
            self.v_lines.append(line)
            self.v_sections.append(sections)

    def _build_v_line_(self,v_func,p=1.0):
        """
        line starting from x scale
        code copied originally form nomo_axis_func.py: _calculate_points_
        v_func is the functio(x,p)
        p is the parametric value of the top scale
        """
        # find top and bottom lines
        max_fu=self.u_func(self.params['u_values'][0])
        min_fu=max_fu
        for u in self.params['u_values']:
            fu=self.u_func(u)
            if fu>max_fu:
                max_fu=fu
            if fu<min_fu:
                min_fu=fu
        # functions to find x-values in paper
        func2=v_func
        func_top=lambda x:(func2(x,p)-max_fu)**2 # minimum at height
        func_bottom=lambda x:(func2(x,p)-min_fu)**2 # minimum at 0.0
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
        line_length_straigth=max_fu-min_fu
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
        if self.params['manual_x_scale']==True:
            self.x_left_ini=self.params['x_min']
            self.x_right_ini=self.params['x_max']
        else:
            self.x_left_ini=x_left
            self.x_right_ini=x_right
        self.y_top_ini=y_top
        self.y_bottom_ini=y_bottom
        self.BB_width_ini=x_right-x_left
        self.BB_height_ini=y_top-y_bottom
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

    def f1(x,u):
        return log(x/(x-u/100.0))/log(1+u/100.0)

    params={'width':10.0,
           'height':10.0,
           'u_func':lambda u:u,
           'v_func':f1,
           'u_values':[10.0,20.0,30.0,40.0,50.0,60.0],
           'v_values':[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0],
           'manual_axis_data':None # manual labels
           }
    tic = time.time()
    test=Nomo_Grid_Box(params=params)
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