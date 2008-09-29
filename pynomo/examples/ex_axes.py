"""
    ex_axes.py

    Examples of axes parameters

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

# Ex 1
N_params={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':'u',
        }

block_params={
              'block_type':'type_8',
              'f_params':N_params,
              'width':5.0,
              'height':15.0,
                     }

main_params={
              'filename':'ex_axes_1.pdf',
              'paper_height':15.0,
              'paper_width':5.0,
              'block_params':[block_params],
              'transformations':[('scale paper',)]
              }

Nomographer(main_params)

# Ex 2
N_params={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':'u',
        'tick_levels':3,
        'tick_text_levels':2,
        'tick_side':'left',
        }
block_params={
              'block_type':'type_8',
              'f_params':N_params,
              'width':5.0,
              'height':10.0,
                     }
main_params={
              'filename':'ex_axes_2.pdf',
              'paper_height':10.0,
              'paper_width':5.0,
              'block_params':[block_params],
              'transformations':[('scale paper',)]
              }
Nomographer(main_params)

# Ex 3
N_params={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':'u',
        'tick_levels':3,
        'tick_text_levels':2,
        'tick_side':'left',
        'title_x_shift':-1.0,
        'title_y_shift':0.5
        }
block_params={
              'block_type':'type_8',
              'f_params':N_params,
              'width':5.0,
              'height':10.0,
                     }
main_params={
              'filename':'ex_axes_3.pdf',
              'paper_height':10.0,
              'paper_width':5.0,
              'block_params':[block_params],
              'transformations':[('scale paper',)]
              }
Nomographer(main_params)

# Ex 4
N_params={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':'title',
        'tick_levels':2,
        'tick_text_levels':1,
        'tick_side':'left',
        'title_draw_center':True,
        'extra_params':[{
                        'u_min':5.0,
                        'u_max':10.0,
                        'tick_levels':3,
                        'tick_text_levels':2,
                        },
                        {
                        'u_min':9.0,
                        'u_max':10.0,
                        'tick_levels':4,
                        'tick_text_levels':2,
                        }
                        ]
        }
block_params={
              'block_type':'type_8',
              'f_params':N_params,
              'width':5.0,
              'height':10.0,
                     }
main_params={
              'filename':'ex_axes_4.pdf',
              'paper_height':10.0,
              'paper_width':5.0,
              'block_params':[block_params],
              'transformations':[('scale paper',)]
              }
Nomographer(main_params)

# Ex 5
N_params={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':'title',
        'tick_levels':2,
        'tick_text_levels':1,
        'tick_side':'left',
        'title_draw_center':True,
        'scale_type':'manual point',
        'manual_axis_data': {1.0:'one',
                     2.0:'two',
                     3.0:'three',
                     3.1415:r'$\pi$',
                     4.0:'four',
                     5.0:'five',
                     6.0:'six',
                     7.0:'seven',
                     8.0:'eight',
                     9.0:'nine',
                     10.0:'ten'}
        }
block_params={
              'block_type':'type_8',
              'f_params':N_params,
              'width':5.0,
              'height':10.0,
                     }
main_params={
              'filename':'ex_axes_5.pdf',
              'paper_height':10.0,
              'paper_width':5.0,
              'block_params':[block_params],
              'transformations':[('scale paper',)]
              }
Nomographer(main_params)

# Ex 6
N_params={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':'title',
        'tick_levels':2,
        'tick_text_levels':1,
        'tick_side':'left',
        'title_draw_center':True,
        'scale_type':'manual line',
        'manual_axis_data': {1.0:'one',
                     2.0:'two',
                     3.0:'three',
                     3.1415:r'$\pi$',
                     4.0:'four',
                     5.0:'five',
                     6.0:'six',
                     7.0:'seven',
                     8.0:'eight',
                     9.0:'nine',
                     10.0:'ten'}

        }
block_params={
              'block_type':'type_8',
              'f_params':N_params,
              'width':5.0,
              'height':10.0,
                     }
main_params={
              'filename':'ex_axes_6.pdf',
              'paper_height':10.0,
              'paper_width':5.0,
              'block_params':[block_params],
              'transformations':[('scale paper',)]
              }
Nomographer(main_params)

# Ex 7
N_params={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':'title',
        'tick_levels':2,
        'tick_text_levels':1,
        'tick_side':'left',
        'scale_type':'manual line',
        'manual_axis_data': {1.0:'one',
                     2.0:'two',
                     3.0:'three',
                     3.1415:r'$\pi$',
                     4.0:'four',
                     5.0:'five',
                     6.0:'six',
                     7.0:'seven',
                     8.0:'eight',
                     9.0:'nine',
                     10.0:'ten'},
        'extra_params':[{
                        'u_min':1.0,
                        'u_max':10.0,
                        'scale_type':'linear',
                        'tick_levels':3,
                        'tick_text_levels':2,
                        'tick_side':'right',
                        }]
        }
block_params={
              'block_type':'type_8',
              'f_params':N_params,
              'width':5.0,
              'height':10.0,
                     }
main_params={
              'filename':'ex_axes_7.pdf',
              'paper_height':10.0,
              'paper_width':5.0,
              'block_params':[block_params],
              'transformations':[('scale paper',)]
              }
Nomographer(main_params)

# Ex 8
N_params={
        'u_min':0.0,
        'u_max':300.0,
        'function_x':lambda u:3*sin(u/180.0*pi),
        'function_y':lambda u:3*cos(u/180.0*pi),
        'title':'u',
        'tick_levels':3,
        'tick_text_levels':1,
        'title_x_shift':-0.5,
        }

block_params={
              'block_type':'type_8',
              'f_params':N_params,
              'width':5.0,
              'height':15.0,
                     }

main_params={
              'filename':'ex_axes_8.pdf',
              'paper_height':10.0,
              'paper_width':10.0,
              'block_params':[block_params],
              'transformations':[('scale paper',)]
              }

Nomographer(main_params)

# Ex 9
N_params={
        'u_min':1.0,
        'u_max':10000.0,
        'function':lambda u:log(u),
        'title':'u',
        'scale_type':'log',
        }

block_params={
              'block_type':'type_8',
              'f_params':N_params,
              'width':5.0,
              'height':15.0,
                     }

main_params={
              'filename':'ex_axes_9.pdf',
              'paper_height':15.0,
              'paper_width':5.0,
              'block_params':[block_params],
              'transformations':[('scale paper',)]
              }

Nomographer(main_params)