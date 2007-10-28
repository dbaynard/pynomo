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
Example nomograph of body-mass index BMI = weight (kg)/(height^2(m^2))
BMI = W/H^2
"""
nomo_type='F2(v)=F3(w)/F1(u)'
functions1={ 'filename':'BMI.pdf',
        'F2':lambda BMI:BMI,
        'v_start':15.0,
        'v_stop':45.0,
        'v_title':r'BMI',
        'v_scale_type':'linear',
        'v_title_x_shift':-3.0,
        'v_title_y_shift':0.5,
        'F1':lambda H:H**2,
        'u_start':1.4,
        'u_stop':2.2,
        'u_title':'Height (m)',
        'u_scale_type':'linear',
        'F3':lambda W:W,
        'w_start':200,
        'w_stop':30.0,
        'w_title':r'Weight (kg)',
        'w_scale_type':'linear',
        'title_str':r"Body mass index $BMI=W($kg$)/H($m$)^2$"
        }
nomo_bmi=nomograph.Nomograph(nomo_type=nomo_type,functions=functions1)
# lets add additional scales for demonstration
def feet2meter(feet):
    return feet*0.3048

def pound2kg(pound):
    return pound*0.45359237

nomo_axis.Nomo_Axis(func_f=(lambda h: nomo_bmi.nomo.give_x1(feet2meter(h))-0),
          func_g=(lambda h: nomo_bmi.nomo.give_y1(feet2meter(h))),
          start=4.6,stop=7.2,turn=-1,title='Height (ft)',
          title_x_shift=-2,
          canvas=nomo_bmi.canvas,type='linear')
nomo_axis.Nomo_Axis(func_f=(lambda h: nomo_bmi.nomo.give_x3(pound2kg(h))+0),
          func_g=(lambda h: nomo_bmi.nomo.give_y3(pound2kg(h))),
          start=70.0,stop=440.0,turn=1,title='Weight (lb)',
          title_x_shift=-2,
          canvas=nomo_bmi.canvas,type='linear')
nomo_bmi.canvas.writePDFfile('BMI1.pdf')