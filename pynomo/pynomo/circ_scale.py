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
                             'tick_direction':'inner', # or 'outer'
                             'scale_type':'linear',
                             'text_distance_4':1.0/4,
                             'grid_length':0.1,
                             'grid_length_0':0.5/4,
                             'grid_length_1':0.5/4,
                             'grid_length_2':0.5/4,
                             'grid_length_3':0.3/4,
                             'grid_length_4':0.3/4,
                             'text_size': text.size.scriptsize,
                             'text_size_0': text.size.small,
                             'text_size_1': text.size.scriptsize,
                             'text_size_2': text.size.tiny,
                             'text_size_3': text.size.tiny,
                             'text_size_4': text.size.tiny,
                             'text_size_log_0': text.size.small,
                             'text_size_log_1': text.size.tiny,
                             'text_size_log_2': text.size.tiny,
                             'text_size_manual': text.size.small,
                             'title_distance_center':0.5,
                             'title_opposite_tick':True,
                             'title_draw_center':False,
                             'text_format':"$%3.1f$",
                             'full_angle':True,
                             'extra_angle':90.0,
                             'text_horizontal_align_center':True,
                             'manual_axis_data':{}}
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
        scaling=(angle_max-angle_min)/(func(u_max)-func(u_min))*math.pi/180.0
        offset=-u_min*scaling+angle_min*math.pi/180.0
        self.func_f = lambda u:radius*math.cos(u*scaling+offset)
        self.func_g = lambda u:radius*math.sin(u*scaling+offset)
        if self.circ_appear['tick_direction']=='inner':
            self.side='left'
        else:
            self.side='right'


if __name__=='__main__':
    c = canvas.canvas()
    appear={
           'angle_min':45.0,
           'angle_max':270.0,}
    circ_scale=Circ_Scale(canvas=c,circ_appear=appear)
    circ_scale.draw()
    c.writePDFfile("test_circ")
