"""
    ex_retaining_wall.py

    Retaining wall.

          -----------------------------------------
          | 2*(u*u-1) | 3*u*(u+1) | -u*(u-1.0)    |
          -----------------------------------------
          |      v    |     1     |    -v*v       | = 0
          -----------------------------------------
          | 2*(2*w+1) | 3*(w+1)   |-(w+1)*(2*w+1) |
          -----------------------------------------


    Copyright (C) 2007-2009  Leif Roschier

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
sys.path.insert(0, "..")
from pynomo.nomographer import *
N_params_1={
        'u_min':0.5,
        'u_max':1.0,
        'u_min_trafo':0.5,
        'u_max_trafo':1.0,
        'f':lambda u:2*(u*u-1.0),
        'g':lambda u:3*u*(u+1.0),
        'h':lambda u:(-u*(u-1.0)),
        'title':'p',
        'tick_side':'left',
        'tick_levels':4,
        'tick_text_levels':2,
        }
N_params_2={
        'u_min':1.0,
        'u_max':0.75,
        'f':lambda v:v,
        'g':lambda v:1.0,
        'h':lambda v:(-v*v),
        'title':'h',
        'tick_side':'right',
        'tick_levels':3,
        'tick_text_levels':2
        }
N_params_3={
        'u_min':1.0,
        'u_max':0.5,
        'u_min_trafo':1.0,
        'u_max_trafo':0.5,
        'f':lambda w:2.0*(2.0*w+1.0),
        'g':lambda w:3.0*(w+1.0),
        'h':lambda w:(-(w+1.0)*(2.0*w+1.0)),
        'title':'L',
        'tick_side':'left',
        'tick_levels':4,
        'tick_text_levels':2
        }
block_params={
                     'block_type':'type_9',
                     'f1_params':N_params_1,
                     'f2_params':N_params_2,
                     'f3_params':N_params_3,
                     'transform_ini':True,
                     'isopleth_values':[[0.8,'x',0.7]]
                     }

main_params={
              'filename':'ex_retaining_wall.pdf',
              'paper_height':10.0,
              'paper_width':10.0,
              'block_params':[block_params],
              'transformations':[('scale paper',)]
              }
Nomographer(main_params)