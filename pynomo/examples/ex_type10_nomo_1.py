"""
    ex_type10_nomo_1.py

    Simple nomogram of type 7: F1(u)+F2(v)*F3(w)+F4(w)=0
    This example plots: u+v*w+w=0

    Copyright (C) 2007-2008  Leif Roschier

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
sys.path.insert(0, "../..")
from pynomo.nomographer import *

N_params_1={
        'u_min':-10.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$u$',
        'tick_levels':3,
        'tick_text_levels':2,
                }

N_params_2={
        'u_min':-10.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$v$',
        'tick_levels':3,
        'tick_text_levels':2,
        'tick_side':'left',
                }

N_params_3={
        'u_min':0.5,
        'u_max':4.0,
        'function_3':lambda u:u,
        'function_4':lambda u:u,
        'title':r'$w$',
        'tick_levels':3,
        'tick_text_levels':1,
                }

block_1_params={
             'block_type':'type_10',
             'width':10.0,
             'height':10.0,
             'f1_params':N_params_1,
             'f2_params':N_params_2,
             'f3_params':N_params_3,
             }

main_params={
              'filename':'ex_type10_nomo_1.pdf',
              'paper_height':10.0,
              'paper_width':10.0,
              'block_params':[block_1_params],
              'transformations':[('rotate',0.01),('scale paper',)],
              'title_str':r'$u+vw+w=0$'
              }
Nomographer(main_params)
