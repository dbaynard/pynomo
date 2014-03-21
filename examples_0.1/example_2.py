#    PyNomo - nomographs with Python
#    Copyright (C) 2007  Leif Roschier
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
from pynomo import *
"""
Example nomograph z=y/x or y=x*z
"""
nomo_type='F2(v)=F3(w)/F1(u)'
functions1={ 'filename':'nomogram2.pdf',
        'F2':lambda z:z,
        'v_start':2.0,
        'v_stop':0.5,
        'v_title':'z',
        'F1':lambda x:x,
        'u_start':1.0,
        'u_stop':5.0,
        'u_title':'x',
        'F3':lambda y:y,
        'w_start':5.0,
        'w_stop':1.0,
        'w_title':'y'}
nomograph.Nomograph(nomo_type=nomo_type,functions=functions1)
