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
    Top-level class to build nomgraphs
    """
    def __init__(self,params):
        """
        params hold all information to build the nomograph
        """
        wrapper=Nomo_Wrapper(paper_width=params['paper_width'],
                             paper_height=params['paper_height'],
                             filename=params['filename'])
        blocks=[]
        for block_para in params['block_params']:
            if block_para['block_type']=='type_1':
                blocks.append(Nomo_Block_Type_1())
                blocks[-1].define_F1(block_para['f1_params'])
                blocks[-1].define_F2(block_para['f2_params'])
                blocks[-1].define_F3(block_para['f3_params'])
                blocks[-1].set_block(width=block_para['width'],
                                     height=block_para['height'],
                                     proportion=block_para['proportion'])
                wrapper.add_block(blocks[-1])

            if block_para['block_type']=='type_7':
                blocks.append(Nomo_Block_Type_7())
                blocks[-1].define_F1(block_para['f1_params'])
                blocks[-1].define_F2(block_para['f2_params'])
                blocks[-1].define_F3(block_para['f3_params'])
                blocks[-1].set_block(width_1=block_para['width_1'],
                                     angle_u=block_para['angle_u'],
                                     angle_v=block_para['angle_v'])
                wrapper.add_block(blocks[-1])

        wrapper.align_blocks()
        wrapper.build_axes_wrapper() # build structure for optimization
        for trafo in params['transformations']:
            if len(trafo)>1:
                wrapper.do_transformation(method=trafo[0],params=trafo[1])
            else:
                wrapper.do_transformation(method=trafo[0])
        c=canvas.canvas()
        wrapper.draw_nomogram(c)

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
                'tag':'none',
                'tick_side':'left',
                'tick_levels':3,
                'tick_text_levels':2,
                'title_draw_center':True
                }
        test1_f2_para={
                'u_min':1.0,
                'u_max':10.0,
                'function':lambda u:u,
                'title':'F2',
                'tag':'none',
                'tick_side':'right',
                'tick_levels':3,
                'tick_text_levels':2,
                'title_draw_center':True
                        }
        test1_f3_para={
                'u_min':1.0,
                'u_max':10.0,
                #'function':lambda u:u*12.0,
                'function':lambda u:u,
                'title':'F3',
                'tag':'A',
                'tick_side':'right',
                'tick_levels':3,
                'tick_text_levels':2,
                'title_draw_center':True
                        }
        test1_block1_params={
                             'block_type':'type_7',
                             'mirror_x':True,
                             'mirror_y':False,
                             'width_1':10.0,
                             'angle_u':45.0,
                             'angle_v':45.0,
                             'f1_params':test1_f1_para,
                             'f2_params':test1_f2_para,
                             'f3_params':test1_f3_para}

        test1_block2_params={
                             'block_type':'type_1',
                             'mirror_x':False,
                             'mirror_y':False,
                             'width':10.0,
                             'height':10.0,
                             'proportion':0.2,
                             'f1_params':test1_f1_para,
                             'f2_params':test1_f2_para,
                             'f3_params':test1_f3_para}

        test1_params={
                      'filename':'test1.pdf',
                      'paper_height':20.0,
                      'paper_width':20.0,
                      'block_params':[test1_block1_params,test1_block2_params],
                      'transformations':[('rotate',0.01),('scale paper',)]
                      }
        Nomographer(test1_params)



