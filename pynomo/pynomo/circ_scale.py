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

from nomo_axis import *

class Circ_Scale:
    """
    class for primitive circular scales
    """
    def __init__(self,canvas,circ_appear={}):
        circ_appear_default_values={
                             'function':lambda u:u,
                             'u_min':1.0,
                             'u_max':10.0,
                             'angle_min':0.0,
                             'angle_max':180.0,
                             'radius':12,
                             'angle_tick_direction':'inner', # or 'outer'
                             'tick_levels':4,
                             'tick_text_levels':2,
                             'scale_type':'linear',
                             'text_distance_4':1.0/4,
                             'grid_length':0.1,
                             'grid_length_0':0.5/4,
                             'grid_length_1':0.5/4,
                             'grid_length_2':0.5/4,
                             'grid_length_3':0.4/4,
                             'grid_length_4':0.3/4,
                             'text_size': text.size.scriptsize,
                             'text_size_0': text.size.tiny,
                             'text_size_1': text.size.tiny,
                             'text_size_2': text.size.tiny,
                             'text_size_3': text.size.tiny,
                             'text_size_4': text.size.tiny,
                             'text_size_log_0': text.size.tiny,
                             'text_size_log_1': text.size.tiny,
                             'text_size_log_2': text.size.tiny,
                             'text_size_manual': text.size.tiny,
                             'text_distance_0':1.0/4,
                             'text_distance_1':1.0/4,
                             'text_distance_2':1.0/4,
                             'text_distance_3':1.0/4,
                             'text_distance_4':1.0/4,
                             'title_distance_center':0.5,
                             'title_opposite_tick':True,
                             'title_draw_center':False,
                             'text_format':"$%3.1f$",
                             'full_angle':True,
                             'extra_angle':90.0,
                             'text_horizontal_align_center':True,
                             'manual_axis_data':{},
                             'circ_scaling':None}
        self.circ_appear=circ_appear_default_values
        self.circ_appear.update(circ_appear)
        self.canvas=canvas
        self._make_f_and_g_func_()

    def draw(self):
        """
        draws the circular scale
        """
        Nomo_Axis(func_f=self.func_f,func_g=self.func_g,
                  start=self.circ_appear['u_min'],stop=self.circ_appear['u_max'],
                  turn=-1,title='circ',
                  tick_levels=self.circ_appear['tick_levels'],
                  tick_text_levels=self.circ_appear['tick_text_levels'],
                  canvas=self.canvas,type=self.circ_appear['scale_type'],
                  manual_axis_data=self.circ_appear['manual_axis_data'],
                  side=self.side,axis_appear=self.circ_appear)

    def _make_f_and_g_func_(self):
        """
        defines f and g functions. Assumes monotonic functions.
        """
        func=self.circ_appear['function']
        radius=self.circ_appear['radius']
        u_min=self.circ_appear['u_min']
        u_max=self.circ_appear['u_max']
        angle_min=self.circ_appear['angle_min']
        angle_max=self.circ_appear['angle_max']
        if self.circ_appear['circ_scaling']==None:
            scaling=(angle_max-angle_min)/(func(u_max)-func(u_min))*math.pi/180.0
        else:
            scaling=self.circ_appear['circ_scaling']
        offset=-func(u_min)*scaling+angle_min*math.pi/180.0
        self.func_f = lambda u:radius*math.cos(func(u)*scaling+offset)
        self.func_g = lambda u:radius*math.sin(func(u)*scaling+offset)
        if self.circ_appear['angle_tick_direction']=='inner':
            self.side='left'
        else:
            self.side='right'



class Circ_Block(object):
    """
    basic class for circle objects
    """
    def __init__(self):
        self.circ_scale_stack=[] # for sirc scales

    def _calculate_scaling_offset_(self,params):
        """
        calculates scalings for given params
        """
        func=lambda u:params['circ_sign']*params['function'](u)
        u_min=params['u_min']
        u_max=params['u_max']
        angle_min=params['angle_min']
        angle_max=params['angle_max']
        scaling=(angle_max-angle_min)/(abs(func(u_max)-func(u_min)))*math.pi/180.0
        if func(u_min)<func(u_max):
            offset=-func(u_min)*scaling+angle_min*math.pi/180.0
        else:
            offset=-func(u_max)*scaling+angle_max*math.pi/180.0
        return scaling,offset

    def _calculate_offset_(self,params):
        """
        assumes scaling is given
        """
        func=lambda u:params['circ_sign']*params['function'](u)
        u_value=params['angle_offset_u_value']
        angle_offset=params['angle_offset_angle_value']
        scaling=params['circ_scaling']
        offset=-func(u_value)*scaling+angle_offset*math.pi/180.0
#        u_min=params['u_min']
#        u_max=params['u_max']
#        angle_min=params['angle_min']
#        angle_max=params['angle_max']
#        if func(u_min)<func(u_max):
#            offset=-func(u_min)*scaling+angle_min*math.pi/180.0
#        else:
#            offset=-func(u_max)*scaling+angle_min*math.pi/180.0
        return offset

    def _draw_(self,params,f,g,canvas):
        """
        draws the circular scale
        """
        increase=params['circ_sign']*params['function'](params['u_max'])-params['circ_sign']*params['function'](params['u_min'])
        if params['angle_tick_direction']=='inner' and increase>0:
            side='left'
        if params['angle_tick_direction']=='inner' and increase<0:
            side='right'
        if params['angle_tick_direction']=='outer' and increase>0:
            side='right'
        if params['angle_tick_direction']=='outer' and increase<0:
            side='left'
        Nomo_Axis(func_f=f,func_g=g,
                  start=params['u_min'],stop=params['u_max'],
                  turn=-1,title=params['title'],
                  tick_levels=params['tick_levels'],
                  tick_text_levels=params['tick_text_levels'],
                  canvas=canvas,type=params['scale_type'],
                  manual_axis_data=params['manual_axis_data'],
                  side=side,axis_appear=params)
    def _draw_arrow_(self,F,G,ccanvas):
        """
        draws an arrow, F amd G are constant functions
        """
        ccanvas.stroke(path.line(0.8*F(0), 0.8*G(0), 0.99*F(0), 0.99*G(0)),
         [style.linewidth.thick, color.rgb.black,
          deco.earrow([deco.stroked([color.rgb.black]),
                       deco.filled([color.rgb.black])], size=0.3)])

    def _draw_circle_(self,radius,ccanvas):
        """
        draws circle
        """
        ccanvas.stroke(path.circle(0, 0, radius), [style.linewidth.thin])

    def _draw_center_circle_(self,radius,ccanvas):
        """
        draws circle
        """
        ccanvas.stroke(path.circle(0, 0, radius), [style.linewidth.thin])
        ccanvas.stroke(path.line(-radius, 0,radius,0), [style.linewidth.thin])
        ccanvas.stroke(path.line(0,-radius, 0,radius), [style.linewidth.thin])

    def _draw_title_ends_(self,params):
        """
        draws title to the ends
        """

class Circ_Block_Type_1(Circ_Block):
    """
    type F1+F2+F3=0 circular slide rule
    scaling comes from F1
    offsets can be set for F2 and F3
    """
    def __init__(self):
        super(Circ_Block_Type_1,self).__init__()

    def set_block(self,block_params):
        """
        sets the block
        """
        self.f1_params=block_params['f1_params']
        self.f2_params=block_params['f2_params']
        self.f3_params=block_params['f3_params']
        self._check_initial_values_()
        self.block_params=block_params
        self.scaling,self.offset_f1=self._calculate_scaling_offset_(self.f1_params)
        self.f1_params['circ_scaling']=self.scaling
        self.f2_params['circ_scaling']=self.scaling
        self.f3_params['circ_scaling']=self.scaling
        self.offset_f2=self._calculate_offset_(self.f2_params)
        self.offset_f3=self._calculate_offset_(self.f3_params)
        self._calculate_funcs_()
#        print "offset f1 %f"%self.offset_f1
#        print "offset f2 %f"%self.offset_f2
#        print "offset f3 %f"%self.offset_f3

    def _check_initial_values_(self):
        """
        parameters for the block
        """
        general_default={
                             'function':lambda u:u,
                             'u_min':1.0,
                             'u_max':10.0,
                             'angle_min':0.0,
                             'angle_max':180.0,
                             'radius':12,
                             'angle_tick_direction':'inner', # or 'outer'
                             'tick_levels':4,
                             'tick_text_levels':2,
                             'scale_type':'linear',
                             'text_distance_4':1.0/4,
                             'grid_length':0.1,
                             'grid_length_0':0.5/4,
                             'grid_length_1':0.5/4,
                             'grid_length_2':0.4/4,
                             'grid_length_3':0.3/4,
                             'grid_length_4':0.2/4,
                             'text_size': text.size.scriptsize,
                             'text_size_0': text.size.tiny,
                             'text_size_1': text.size.tiny,
                             'text_size_2': text.size.tiny,
                             'text_size_3': text.size.tiny,
                             'text_size_4': text.size.tiny,
                             'text_size_log_0': text.size.tiny,
                             'text_size_log_1': text.size.tiny,
                             'text_size_log_2': text.size.tiny,
                             'text_size_manual': text.size.small,
                             'text_distance_0':1.0/4,
                             'text_distance_1':1.0/4,
                             'text_distance_2':1.0/4,
                             'text_distance_3':1.0/4,
                             'text_distance_4':1.0/4,
                             'title_distance_center':0.7,
                             'title_opposite_tick':True,
                             'title_draw_center':True,
                             'text_format':"$%3.1f$",
                             'full_angle':True,
                             'extra_angle':90.0,
                             'text_horizontal_align_center':True,
                             'manual_axis_data':{},
                             'circ_scaling':None,
                             'title':'',
                             'angle_offset_u_value':1,
                             'angle_offset_angle_value':1,
                             'turn_relative':True}
        ##############################################################
        # F1
        params_default_f1=general_default
        params_default_f1_0={
                         'radius':4,
                         'angle_tick_direction':'outer',
                         'circ_sign':1,
                         }
        params_default_f1.update(params_default_f1_0)
        for key in params_default_f1:
            if not self.f1_params.has_key(key):
                self.f1_params[key]=params_default_f1[key]
#        if self.f1_params['angle_tick_direction']=='inner':
#            self.side_f1='left'
#        else:
#            self.side_f1='right'
        ##############################################################
        # F2
        params_default_f2=general_default
        params_default_f2_0={
                         'radius':4,
                         'angle_tick_direction':'inner',
                         'circ_sign':-1,
                         }
        params_default_f2.update(params_default_f2_0)
        for key in params_default_f2:
            if not self.f2_params.has_key(key):
                self.f2_params[key]=params_default_f2[key]
#        if self.f2_params['angle_tick_direction']=='inner':
#            self.side_f2='left'
#        else:
#            self.side_f2='right'
        ##############################################################
        # F3
        params_default_f3=general_default
        params_default_f3_0={
                         'radius':3,
                         'angle_tick_direction':'outer',
                         'circ_sign':-1,
                         }
        params_default_f3.update(params_default_f3_0)
        for key in params_default_f3:
            if not self.f3_params.has_key(key):
                self.f3_params[key]=params_default_f3[key]
#        if self.f3_params['angle_tick_direction']=='inner':
#            self.side_f3='left'
#        else:
#            self.side_f3='right'

    def _calculate_funcs_(self):
        """
        makes the real funcs
        """
        self.func_F1 = lambda u:self.f1_params['radius']*math.cos(self.f1_params['circ_sign']*self.f1_params['function'](u)*self.scaling+self.offset_f1)
        self.func_G1 = lambda u:self.f1_params['radius']*math.sin(self.f1_params['circ_sign']*self.f1_params['function'](u)*self.scaling+self.offset_f1)
        self.func_F2 = lambda u:self.f2_params['radius']*math.cos(self.f2_params['circ_sign']*self.f2_params['function'](u)*self.scaling+self.offset_f2)
        self.func_G2 = lambda u:self.f2_params['radius']*math.sin(self.f2_params['circ_sign']*self.f2_params['function'](u)*self.scaling+self.offset_f2)
        self.func_F3 = lambda u:self.f3_params['radius']*math.cos(self.f3_params['circ_sign']*self.f3_params['function'](u)*self.scaling+self.offset_f3)
        self.func_G3 = lambda u:self.f3_params['radius']*math.sin(self.f3_params['circ_sign']*self.f3_params['function'](u)*self.scaling+self.offset_f3)
        self.arrow_F = lambda u:self.f3_params['radius']*math.cos(self.offset_f2+self.offset_f3)
        self.arrow_G = lambda u:self.f3_params['radius']*math.sin(self.offset_f2+self.offset_f3)

    def draw(self,ccanvas,rot_angle=0.0):
        """
        draws the scales
        """
        rotating_canvas = canvas.canvas()
        self._draw_(self.f1_params,self.func_F1,self.func_G1,ccanvas)
        self._draw_(self.f2_params,self.func_F2,self.func_G2,rotating_canvas)
        self._draw_(self.f3_params,self.func_F3,self.func_G3,ccanvas)
        self._draw_arrow_(self.arrow_F,self.arrow_G,rotating_canvas)
        self._draw_circle_(self.f1_params['radius']+1,ccanvas)
        self._draw_center_circle_(0.2,ccanvas)
        # insert subcanvas into canvas
        ccanvas.insert(rotating_canvas, [trafo.rotate(rot_angle)])

    def draw_slide(self,ccanvas,rot_angle=0.0):
        """
        draws the rotating (transparent)
        """
        rotating_canvas = canvas.canvas()
        self._draw_(self.f2_params,self.func_F2,self.func_G2,rotating_canvas)
        self._draw_arrow_(self.arrow_F,self.arrow_G,rotating_canvas)
        self._draw_circle_(self.f1_params['radius']+1,ccanvas)
        self._draw_center_circle_(0.2,ccanvas)
        # insert subcanvas into canvas
        ccanvas.insert(rotating_canvas, [trafo.rotate(rot_angle)])

    def draw_background(self,ccanvas,rot_angle=0.0):
        """
        draws the background
        """
        rotating_canvas = canvas.canvas()
        self._draw_(self.f1_params,self.func_F1,self.func_G1,ccanvas)
        self._draw_(self.f3_params,self.func_F3,self.func_G3,ccanvas)
        self._draw_circle_(self.f1_params['radius']+1,ccanvas)
        self._draw_center_circle_(0.2,ccanvas)

if __name__=='__main__':
    c = canvas.canvas()
    appear={
           'function':lambda u:u,
           'u_min':1.0,
           'u_max':12.0,
           'radius':4,
           'angle_min':75.0,
           'angle_max':270.0,
           'scale_max':10.0,
           'tick_levels':4,
           'text_format':"$%3.1f$",
           'tick_text_levels':2,
           'extra_angle':90.0,
}
    appear_1={
           'function':lambda u:u,
           'u_min':1.0,
           'u_max':9.0,
           'radius':4,
           'angle_min':0.0,
           'angle_max':360.0,
           'scale_max':10.0,
           'tick_levels':5,
           'text_format':"$%3.1f$",
           'tick_text_levels':2,
           'extra_angle':90.0,
           'angle_tick_direction':'outer',
}
    circ_scale=Circ_Scale(canvas=c,circ_appear=appear)
    circ_scale.draw()
    circ_scale_1=Circ_Scale(canvas=c,circ_appear=appear_1)
    circ_scale_1.draw()
    c.writePDFfile("test_circ")

    cc=canvas.canvas()
    cc_slide=canvas.canvas()
    cc_bg=canvas.canvas()
    para_1={'function':lambda u:3*u,
            'title':'F1',
            'radius':8,
            'u_min':0.0,
           'u_max':10.0,
           'angle_min':0.0,
           'angle_max':270.0}
    para_2={#'function':lambda u:10*math.log10(u),
            'function':lambda u:u,
            'title':'F2',
            'radius':8,
            'u_min':1.0,
           'u_max':10.0,
           'angle_offset_u_value':1.0,
           'angle_offset_angle_value':10.0,
           'scale_type':'linear'}
    para_3={'function':lambda u:-u,
            'title':'F3',
            'radius':6,
            'u_min':-15.0,
           'u_max':15.0,
           'angle_offset_u_value':0.0,
           'angle_offset_angle_value':180.0,
           'extra_angle':0,
           'title_distance_center':1.2,
           'text_horizontal_align_center':False}
    block_params={'f1_params':para_1,
                 'f2_params':para_2,
                 'f3_params':para_3}

    circle_test=Circ_Block_Type_1()
    circle_test.set_block(block_params)
    circle_test.draw(cc,45.0)
    circle_test.draw_slide(cc_slide,0.0)
    circle_test.draw_background(cc_bg,0.0)
    cc.writePDFfile("test_circ_combined.pdf")
    cc_slide.writePDFfile("test_circ_slide.pdf")
    cc_bg.writePDFfile("test_circ_bg.pdf")