"""
    ex_temp_convert.py

    Celcius-Fahrenheit converter

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
sys.path.insert(0, "..")
from pynomo.nomographer import *
F_start=-40.0
F_stop=90.0
C_start=-40.0
C_stop=30.0

def celcius(fahrenheit):
    return (fahrenheit-32.0)/1.8

F_para={
        'tag':'A',
        'u_min':F_start,
        'u_max':F_stop,
        'function':lambda u:celcius(u),
        'title':r'$^\circ$ F',
        'tick_levels':4,
        'tick_text_levels':3,
        'align_func':celcius,
        'title_x_shift':0.5
        }

C_para={
        'tag':'A',
        'u_min':C_start,
        'u_max':C_stop,
        'function':lambda u:u,
        'title':r'$^\circ$ C',
        'tick_levels':5,
        'tick_text_levels':3,
        'scale_type':'linear',
        'tick_side':'left',
        'title_x_shift':-0.5
}

C_block={
         'block_type':'type_8',
            'f_params':C_para
         }
F_block={
         'block_type':'type_8',
            'f_params':F_para
            }

main_params={
              'filename':'ex_temp_converter.pdf',
              'paper_height':20.0,
              'paper_width':2.0,
              'block_params':[C_block,F_block],
              'transformations':[('scale paper',)]
              }
Nomographer(main_params)