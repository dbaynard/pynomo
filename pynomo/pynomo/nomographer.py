#    PyNomo - nomographs with Python
#    Copyright (C) 2007-2008  Leif Roschier
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
from nomo_wrapper import *
from math import *

class Nomographer:
    """
    Top-level class to build nomographs
    """
    def __init__(self,params):
        """
        params hold all information to build the nomograph
        """
        self._check_params_(params) # sets default values for missing keys
        wrapper=Nomo_Wrapper(paper_width=params['paper_width'],
                             paper_height=params['paper_height'],
                             filename=params['filename'])
        blocks=[]
        for block_para in params['block_params']:
            # TYPE 1
            if block_para['block_type']=='type_1':
                self._check_block_type_1_params_(block_para)
                blocks.append(Nomo_Block_Type_1(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                self._check_axis_params_(block_para['f1_params'])
                self._check_axis_params_(block_para['f2_params'])
                self._check_axis_params_(block_para['f3_params'])
                blocks[-1].define_F1(block_para['f1_params'])
                blocks[-1].define_F2(block_para['f2_params'])
                blocks[-1].define_F3(block_para['f3_params'])
                blocks[-1].set_block(width=block_para['width'],
                                     height=block_para['height'],
                                     proportion=block_para['proportion'])
                wrapper.add_block(blocks[-1])
            # TYPE 2
            if block_para['block_type']=='type_2':
                self._check_block_type_2_params_(block_para)
                blocks.append(Nomo_Block_Type_2(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                self._check_axis_params_(block_para['f1_params'])
                self._check_axis_params_(block_para['f2_params'])
                self._check_axis_params_(block_para['f3_params'])
                blocks[-1].define_F1(block_para['f1_params'])
                blocks[-1].define_F2(block_para['f2_params'])
                blocks[-1].define_F3(block_para['f3_params'])
                blocks[-1].set_block(width=block_para['width'],
                                     height=block_para['height'])
                wrapper.add_block(blocks[-1])
            # TYPE 3
            if block_para['block_type']=='type_3':
                self._check_block_type_3_params_(block_para)
                blocks.append(Nomo_Block_Type_3(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                for axis_params in block_para['f_params']:
                    self._check_axis_params_(axis_params)
                    blocks[-1].add_F(axis_params)
                blocks[-1].set_block(width=block_para['width'],
                                     height=block_para['height'])
                wrapper.add_block(blocks[-1])
            # TYPE 7
            if block_para['block_type']=='type_7':
                self._check_block_type_7_params_(block_para)
                blocks.append(Nomo_Block_Type_7(mirror_x=block_para['mirror_x'],
                                                mirror_y=block_para['mirror_y']))
                self._check_axis_params_(block_para['f1_params'])
                self._check_axis_params_(block_para['f2_params'])
                self._check_axis_params_(block_para['f3_params'])
                blocks[-1].define_F1(block_para['f1_params'])
                blocks[-1].define_F2(block_para['f2_params'])
                blocks[-1].define_F3(block_para['f3_params'])
                blocks[-1].set_block(width_1=block_para['width_1'],
                                     angle_u=block_para['angle_u'],
                                     angle_v=block_para['angle_v'])
                wrapper.add_block(blocks[-1])

        wrapper.align_blocks()
        wrapper.build_axes_wrapper() # build structure for transformations
        for trafo in params['transformations']:
            if len(trafo)>1:
                wrapper.do_transformation(method=trafo[0],params=trafo[1])
            else:
                wrapper.do_transformation(method=trafo[0])
        c=canvas.canvas()
        wrapper.draw_nomogram(c)

    def _check_params_(self,params):
        """
        checks if main params ok and adds default values
        """
        params_default={
                      'filename':'pynomo_default.pdf',
                      'paper_height':20.0,
                      'paper_width':20.0,
                      #'block_params':[test1_block1_params,test1_block2_params],
                      'transformations':[('rotate',0.01),('scale paper',)]
                      }
        for key in params_default:
            if not params.has_key(key):
                params[key]=params_default[key]

    def _check_block_type_1_params_(self,params):
        """
        checks if block type 1 params ok and adds default values
        """
        params_default={
                         'mirror_x':False,
                         'mirror_y':False,
                         'width':10.0,
                         'height':10.0}
        for key in params_default:
            if not params.has_key(key):
                params[key]=params_default[key]

    def _check_block_type_2_params_(self,params):
        """
        checks if block type 2 params ok and adds default values
        """
        params_default={
                         'mirror_x':False,
                         'mirror_y':False,
                         'width':10.0,
                         'height':10.0}
        for key in params_default:
            if not params.has_key(key):
                params[key]=params_default[key]

    def _check_block_type_3_params_(self,params):
        """
        checks if block type 2 params ok and adds default values
        """
        params_default={
                         'mirror_x':False,
                         'mirror_y':False,
                         'width':10.0,
                         'height':10.0}
        for key in params_default:
            if not params.has_key(key):
                params[key]=params_default[key]

    def _check_block_type_7_params_(self,params):
        """
        checks if block type 1 params ok and adds default values
        """
        params_default={
                         'mirror_x':False,
                         'mirror_y':False,
                         'width_1':10.0,
                         'angle_u':45.0,
                         'angle_v':45.0}
        for key in params_default:
            if not params.has_key(key):
                params[key]=params_default[key]

    def _check_axis_params_(self,params):
        """
        checks (TODO: if axis params ok) and adds default values
        """
        params_default={
            'ID':'none', # to identify the axis
            'tag':'none', # for aligning block wrt others
            #'u_min':0.1,
            #'u_max':1.0,
            #'F':lambda u:u, # x-coordinate
            #'G':lambda u:u, # y-coordinate
            'title':'',
            'title_x_shift':0.0,
            'title_y_shift':0.25,
            'scale_type':'linear', #'linear' 'log' 'manual point' 'manual line'
            'tick_levels':4,
            'tick_text_levels':3,
            'tick_side':'right',
            'reference':False,
            'reference padding': 0.20, # fraction of reference line over other lines
            'manual_axis_data':{},
            'title_distance_center':0.5,
            'title_opposite_tick':True,
            'title_draw_center':False
            }
        for key in params_default:
            if not params.has_key(key):
                params[key]=params_default[key]

if __name__=='__main__':
    """
    tests
    """
    test1=True
    if test1:
        test1_f1_para={
                'u_min':1.0,
                'u_max':10.0,
                'function':lambda u:u,
                'title':'F1',
                'tick_levels':3,
                'tick_text_levels':2,
                }
        test1_f2_para={
                'u_min':0.0,
                'u_max':10.0,
                'function':lambda u:u,
                'title':'F2',
                'tick_levels':3,
                'tick_text_levels':2,
                        }
        test1_f3_para={
                'u_min':1.0,
                'u_max':10.0,
                #'function':lambda u:u*12.0,
                'function':lambda u:u,
                'title':'F3',
                'tag':'A',
                'tick_side':'right'
                        }
        test1_f4_para={
                'u_min':-10.0,
                'u_max':10.0,
                'function':lambda u:u,
                'title':'F2',
                'tick_levels':3,
                'tick_text_levels':2,
                        }
        test1_block1_params={
                             'block_type':'type_1',
                             'width':10.0,
                             'height':10.0,
                             'proportion':0.5,
                             'f1_params':test1_f1_para,
                             'f2_params':test1_f2_para,
                             'f3_params':test1_f3_para}

        test1_block7_params={
                             'block_type':'type_7',
                             'width_1':10.0,
                             'angle_u':60.0,
                             'angle_v':60.0,
                             'f1_params':test1_f1_para,
                             'f2_params':test1_f2_para,
                             'f3_params':test1_f3_para}

        test1_params={
                      'filename':'test1.pdf',
                      'paper_height':20.0,
                      'paper_width':20.0,
                      'block_params':[test1_block1_params,test1_block7_params],
                      'transformations':[('rotate',0.01),('scale paper',)]
                      }
        Nomographer(test1_params)

        test2_block2_params={
                             'block_type':'type_2',
                             'width':10.0,
                             'height':10.0,
                             'proportion':0.5,
                             'f1_params':test1_f1_para,
                             'f2_params':test1_f2_para,
                             'f3_params':test1_f3_para}

        test2_params={
                      'filename':'test2.pdf',
                      'paper_height':20.0,
                      'paper_width':20.0,
                      'block_params':[test2_block2_params],
                      'transformations':[('rotate',0.01),('scale paper',)]
                      }
        Nomographer(test2_params)

        test3_block3_params={
                             'block_type':'type_3',
                             'width':10.0,
                             'height':10.0,
                             'f_params':[test1_f1_para,test1_f1_para,
                                         test1_f1_para,test1_f1_para,test1_f4_para]
                             }

        test3_params={
                      'filename':'test3.pdf',
                      'paper_height':20.0,
                      'paper_width':20.0,
                      'block_params':[test3_block3_params],
                      'transformations':[('rotate',0.01),('scale paper',)]
                      }
        Nomographer(test3_params)


