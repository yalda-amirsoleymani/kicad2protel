import sexpdata
from pprint import pprint
import math

valid_layers = ['*.Cu', 'F.Cu', 'B.Cu', 'F.SilkS', 'B.SilkS', 'F.Mask', 'B.Mask', 'Edge.Cuts', 'MULTILAYER']
u = 5000
u2 = 39.3701
f = open('template.txt', 'r')
template = f.read()
def set_layer(l):
  if l == '*.Cu':
    l = 'MULTILAYER'
  if l == 'F.Cu':
    l = 'TOP'
  if l == 'B.Cu':
    l = 'BOTTOM'
  if l == 'F.SilkS':
    l = 'TOPOVERLAY'
  if l == 'B.SilkS':
    l = 'BOTTOMOVERLAY'
  if l == 'F.Mask':
    l = 'TOPSOLDER'
  if l == 'B.Mask':
    l = 'BOTTOMSOLDER'
  if l == 'F.Paste':
    l = 'TOPPASTE'
  if l == 'B.Paste':
    l = 'BOTTOMPASTE'
  if l == 'Edge.Cuts':
    l = 'KEEPOUT'
  return l

def kicad_line(l, x_reference, y_reference):
    line_argument = {}
    x_start = 0
    y_start = 0
    x_end = 0
    y_end = 0
    width = 0
    layer = ""
    for x in l:
        if isinstance(x, list):
            if x[0].value() == "start":
                x_start = (x[1] + x_reference) * u2
                y_start = u - ((x[2] + y_reference)) * u2
            if x[0].value() == "end":
                x_end = (x[1] + x_reference) * u2
                y_end = u - ((x[2] + y_reference)) * u2
            if x[0].value() == "layer":
                layer = x[1].value()
            if x[0].value() == "width":
                width = x[1] * u2
    line_argument.update(
        {
            "x_start": x_start,
            "y_start": y_start,
            "x_end": x_end,
            "y_end": y_end,
            "layer": layer,
            "width": width,
        }
    )

    if line_argument['layer'] in valid_layers:
      line_argument['layer'] = set_layer(line_argument['layer'])
      kicad_line_list.append(line_argument)


def kicad_via(v):
    via_argument = {}
    x_center = 0
    y_center = 0
    size = 0
    drill = 0
    ## *********layer barresi nashode****************
    for x in v:
        if isinstance(x, list):
            if x[0].value() == "at":
                x_center = x[1] * u2
                y_center = u - (x[2]) * u2
            if x[0].value() == "size":
                size = x[1] * u2
            if x[0].value() == "drill":
                drill = x[1] * u2
            if x[0].value() == "layers":
                x.pop(0)
                layers = []
                for a in x:
                  layers.append(a)
    via_argument.update(
        {"x_center": x_center, "y_center": y_center, "size": size, "drill": drill}
    )
    for v in layers:
      if v.value() in valid_layers:
        via_argument['layer'] = set_layer(v.value())
        kicad_via_list.append(via_argument)


def kicad_pad(p, x_reference, y_reference):
    pad_argument = {}
    x_center = 0
    y_center = 0
    x_size = 0
    y_size = 0
    drill = 0
    shape = ""
    ## *********layer barresi nashode****************
    for x in p:
        if isinstance(x, list):
            if x[0].value() == "at":
                x_center = (x[1] + x_reference) * u2
                y_center = u - (x[2] + y_reference) * u2
            if x[0].value() == "size":
                x_size = x[1] * u2
                y_size = x[2] * u2
            if x[0].value() == "drill":
                drill = x[1] * u2
            if x[0].value() == "layers":
                x.pop(0)
                layers = []
                for a in x:
                  layers.append(a)
        elif isinstance(x, int):
            continue
        elif isinstance(x, str):
            continue
        elif x.value() == "circle" or x.value() == "oval":
            shape = "circ"
        elif x.value() == "rect" or x.value() == "roundrect":
            shape = "rect"

    pad_argument.update(
        {
            "x_center": x_center,
            "y_center": y_center,
            "x_size": x_size,
            "y_size": y_size,
            "drill": drill,
            "shape": shape,
        }
    )
    for l in layers:
      if l.value() in valid_layers:
        pad_argument['layer'] = set_layer(l.value())
        kicad_pad_list.append(pad_argument)


def kicad_text(t, x_reference, y_reference, text):
    text_argument = {}
    x_pos = 0
    y_pos = 0
    height = 0
    width = 0
    layer = ""
    l = len(text)
    for x in t:
        if isinstance(x, list):
            if x[0].value() == "layer":
                layer = x[1].value()
            if x[0].value() == "at":
                x_pos = x[1] + x_reference
                y_pos = u -(x[2] + y_reference) * u2
            if x[0].value() == "effects":
                if x[1][1][0].value() == 'size':
                    w = x[1][1][1]
                    l = (l * w) /2
                if x[1][2][0].value() == 'thikness':
                    width = x[1][2][1] * u2 
                x = x[1][1]
                height = x[1] * u2
    x_pos = (x_pos - l) * u2
    text_argument.update(
        {
            "x_pos": x_pos,
            "y_pos": y_pos,
            "height": height,
            "width": width,
            "layer": layer,
            "text": text,
        }
    )
    if text_argument['layer'] in valid_layers:
      text_argument['layer'] = set_layer(text_argument['layer'])
      kicad_text_list.append(text_argument)


def arc_calculation(x_start, y_start, x_end, y_end, start_angle, angle):
    if y_end - y_start < 0 and x_end - x_start < 0 : start_angle = 180 - start_angle
    elif y_end - y_start > 0 and x_end - x_start < 0 : start_angle = 180 + start_angle
    elif y_end - y_start > 0 and x_end - x_start > 0 : start_angle = 360 - start_angle
    end_angle = angle + start_angle
    if end_angle > 360 : end_angle %= 360
    return start_angle, end_angle

def determine_area (x_start, y_start, x_center, y_center, start_angle):
    print('##')
    if y_start < y_center and x_start > x_center : 
        print("first_area")
    elif y_start < y_center and x_start < x_center: 
        print("second_area")
        start_angle = -start_angle - 180
    elif y_start > y_center and x_start > x_center : 
        print("fourth_area")
    elif y_start > y_center and x_start < x_center :
        print('third_area')
        start_angle = 180 - start_angle
    elif y_start == y_center and x_start < x_center :
        start_angle = 180
    elif y_start == y_center and x_start > x_center :
        start_angle = 0
    elif x_start == x_center and y_start < y_center :
        start_angle = 90
    elif x_start == x_center and y_start > y_center :
        start_angle = 270
    return start_angle
#    if end_angle > 360 : end_angle %= 360
#    return start_angle, end_angle
def arc_math(component, x_reference, y_reference, x_start, y_start, x_center, y_center, angle):
    delta_x = (x_start  - x_center)
    delta_y = (y_start  - y_center)
    radius = ((delta_x ** 2) + (delta_y ** 2)) ** 0.5
    x_loc = (x_center + x_reference) * u2
    y_loc = u - ((y_center + y_reference) * u2)
    start_angle = delta_y / radius
    start_angle = math.degrees(math.asin(start_angle))
    start_angle = determine_area (x_start, y_start, x_center, y_center, start_angle)
    end_angle = start_angle + angle
    print("start_angle:",start_angle,"end_angle:",start_angle)
    if start_angle < end_angle:
        x = start_angle
        start_angle = -end_angle
        end_angle = -x
    else :
        start_angle = - start_angle
        end_angle = - end_angle
    radius = radius * u2
    return (radius, x_loc, y_loc, start_angle, end_angle)


def kicad_arc(component, a, x_reference, y_reference):
    arc_argument = {}
    x_start = 0
    y_start = 0
    x_end = 0
    y_end = 0
    width = 0
    angle = 0
    layer = ""
    for x in a:
        if isinstance(x, list):
            if x[0].value() == "start":
                x_center = x[1]
                y_center = x[2]
                print("__________________")
                print('x_center:',x_center+x_reference,'y_center:',y_center+y_reference)
            if x[0].value() == "end":
                x_start = x[1]
                y_start = x[2]
                print('x_start:',x_start+x_reference,'y_start:',y_start+y_reference)
            if x[0].value() == "angle":
                angle = x[1]
            if x[0].value() == "layer":
                layer = x[1].value()
            if x[0].value() == "width":
                width = x[1]
    radius, x_loc, y_loc, start_angle, end_angle = arc_math(component, x_reference, y_reference, x_start, y_start, x_center, y_center, angle)
    arc_argument.update(
        {
            "x_loc": x_loc,
            "y_loc": y_loc,
            "radius": radius,
            "start_angle": start_angle,
            "layer": layer,
            "width": width,
            "end_angle": end_angle,
        }
    )
    if arc_argument['layer'] in valid_layers:
      arc_argument['layer'] = set_layer(arc_argument['layer'])
      kicad_arc_list.append(arc_argument)


def module(i):
    x_reference = 0
    y_reference = 0
    for x in i:
        if isinstance(x, list):
            if x[0].value() == "at":
                x_reference = x[1]
                y_reference = x[2]
            if x[0].value() == "fp_line":
                kicad_line(x, x_reference, y_reference)
            if x[0].value() == "fp_text":
                if x[1].value() == "reference":
                    text = x[2].value()
                    kicad_text(x, x_reference, y_reference, text)
            if x[0].value() == "pad":
                kicad_pad(x, x_reference, y_reference)
            if x[0].value() == "fp_arc":
                kicad_arc(True, x, x_reference, y_reference)
#            if x[0].value == 'fp_circle':
#              circule(x, x_reference, y_reference)

def protel_text(kicad_txt_list):
    for x in kicad_txt_list:
        t = (
            "|RECORD=TEXT|SELECTION=FALSE|LAYER={}|LOCKED=FALSE|"
            "POLYGONOUTLINE=FALSE|USERROUTED=TRUE|X={}mil|Y= {}mil|HEIGHT={}mil|"
            "FONT=DEFAULT|ROTATION=0.000|MIRROR=FALSE|TEXT={}|WIDTH={}mil".format(
                x["layer"], x["x_pos"], x["y_pos"], x["height"], x["text"], x["width"]
            )
        )
        protel_text_list.append(t)


def protel_line(kicad_line_list):
    for x in kicad_line_list:
        l = (
            "|RECORD=Track|INDEXFORSAVE=0|SELECTION=FALSE|LAYER={}|LOCKED=FALSE|"
            "POLYGONOUTLINE=FALSE|USERROUTED=TRUE|UNIONINDEX=0|"
            "SOLDERMASKEXPANSIONMODE=None|PASTEMASKEXPANSIONMODE=None|"
            "X1={}mil|Y1={}mil|X2={}mil|Y2={}mil|WIDTH={}mil|SUBPOLYINDEX=0".format(
                x["layer"],
                x["x_start"],
                x["y_start"],
                x["x_end"],
                x["y_end"],
                x["width"],
            )
        )
        protel_line_list.append(l)


def protel_arc(kicad_arc_list):
    for x in kicad_arc_list:
        a = ("|RECORD=Arc|INDEXFORSAVE=0|SELECTION=TRUE|LAYER={}|LOCKED=FALSE|"
             "POLYGONOUTLINE=FALSE|USERROUTED=TRUE|UNIONINDEX=0|"
             "SOLDERMASKEXPANSIONMODE=None|PASTEMASKEXPANSIONMODE=None|"
             "LOCATION.X={}mil|LOCATION.Y={}mil|RADIUS={}mil|STARTANGLE= {}|"
             "ENDANGLE= {}|WIDTH={}mil|SUBPOLYINDEX=0"
             .format(
                x["layer"],
                x["x_loc"],
                x["y_loc"],
                x["radius"],
                x["start_angle"],
                x["end_angle"],
                x["width"],
            )
        )
        protel_arc_list.append(a)

def protel_pad(kicad_pad_list):
    for x in kicad_pad_list:
        p = (
            "|RECORD=Pad|INDEXFORSAVE=1|SELECTION=FALSE|LAYER={}|"
            "LOCKED=FALSE|POLYGONOUTLINE=FALSE|USERROUTED=TRUE|UNIONINDEX=0|"
            "SOLDERMASKEXPANSIONMODE=Rule|PASTEMASKEXPANSIONMODE=Rule|NAME=4|"
            "X={}mil|Y={}mil|XSIZE={}mil|YSIZE={}mil|SHAPE={}|HOLESIZE={}mil|"
            "ROTATION= 0.00000000000000E+0000|PLATED=TRUE|DAISYCHAIN=Load|"
            "CCSV=0|CPLV=0|CCWV=1|CENV=1|CAGV=1|CPEV=1|CSEV=1|CPCV=1|CPRV=1|"
            "CCW=10mil|CEN=4|CAG=10mil|CPE=0mil|CSE=4mil|CPC=20mil|CPR=20mil|"
            "PADMODE=0|SWAPID_PAD=|SWAPID_GATE=|&|0|SWAPPEDPADNAME=|GATEID=0|"
            "OVERRIDEWITHV6_6SHAPES=FALSE|DRILLTYPE=0|HOLETYPE=0|"
            "HOLEWIDTH=0mil|HOLEROTATION= 0.00000000000000E+0000|"
            "PADXOFFSET0=0mil|PADYOFFSET0=0mil|PADXOFFSET1=0mil|PADYOFFSET1=0mil|"
            "PADXOFFSET2=0mil|PADYOFFSET2=0mil|PADXOFFSET3=0mil|"
            "PADYOFFSET3=0mil|PADXOFFSET4=0mil|PADYOFFSET4=0mil|PADXOFFSET5=0mil|"
            "PADYOFFSET5=0mil|PADXOFFSET6=0mil|PADYOFFSET6=0mil|PADXOFFSET7=0mil|"
            "PADYOFFSET7=0mil|PADXOFFSET8=0mil|PADYOFFSET8=0mil|PADXOFFSET9=0mil|"
            "PADYOFFSET9=0mil|PADXOFFSET10=0mil|PADYOFFSET10=0mil|"
            "PADXOFFSET11=0mil|PADYOFFSET11=0mil|PADXOFFSET12=0mil|PADYOFFSET12=0mil|"
            "PADXOFFSET13=0mil|PADYOFFSET13=0mil|PADXOFFSET14=0mil|PADYOFFSET14=0mil|PADXOFFSET15=0mil|"
            "PADYOFFSET15=0mil|PADXOFFSET16=0mil|PADYOFFSET16=0mil|PADXOFFSET17=0mil|PADYOFFSET17=0mil|"
            "PADXOFFSET18=0mil|PADYOFFSET18=0mil|PADXOFFSET19=0mil|PADYOFFSET19=0mil|PADXOFFSET20=0mil|"
            "PADYOFFSET20=0mil|PADXOFFSET21=0mil|PADYOFFSET21=0mil|PADXOFFSET22=0mil|PADYOFFSET22=0mil|"
            "PADXOFFSET23=0mil|PADYOFFSET23=0mil|PADXOFFSET24=0mil|PADYOFFSET24=0mil|PADXOFFSET25=0mil|"
            "PADYOFFSET25=0mil|PADXOFFSET26=0mil|PADYOFFSET26=0mil|PADXOFFSET27=0mil|PADYOFFSET27=0mil|"
            "PADXOFFSET28=0mil|PADYOFFSET28=0mil|PADXOFFSET29=0mil|PADYOFFSET29=0mil|PADXOFFSET30=0mil|"
            "PADYOFFSET30=0mil|PADXOFFSET31=0mil|PADYOFFSET31=0mil|PADJUMPERID=0".format(
                x["layer"],
                x["x_center"],
                x["y_center"],
                x["x_size"],
                x["y_size"],
                x["shape"],
                x["drill"],
            )
        )
        protel_pad_list.append(p)
def protel_via(kicad_via_list):
    for x in kicad_via_list:
        v = (
            "|RECORD=Via|INDEXFORSAVE=0|SELECTION=TRUE|LAYER=MULTILAYER|LOCKED=FALSE|"
            "POLYGONOUTLINE=FALSE|USERROUTED=TRUE|UNIONINDEX=0|SOLDERMASKEXPANSIONMODE=Rule|"
            "PASTEMASKEXPANSIONMODE=None|X={}mil|Y={}mil|DIAMETER={}mil|HOLESIZE={}mil|"
            "STARTLAYER=TOP|ENDLAYER=BOTTOM|CCSV=0|CPLV=0|CCWV=0|CENV=0|CAGV=0|"
            "CPEV=0|CSEV=1|CPCV=0|CPRV=0|CSE=4mil".format(
            x["x_center"], x["y_center"], x["size"], x["drill"]
            )
        )
        protel_via_list.append(v)


kicad_arc_list = []
kicad_line_list = []
kicad_pad_list = []
kicad_via_list = []
kicad_text_list = []
protel_arc_list = []
protel_line_list = []
protel_pad_list = []
protel_via_list = []
protel_text_list = []
with open("1.kicad_pcb", "r") as f:
    inp = f.read()
    stmt = sexpdata.loads(inp)
for i in stmt:
    if isinstance(i, list):
        if i[0].value() == "module":
            module(i)
        if i[0].value() == "gr_arc":
            kicad_arc(False, i, 0, 0)
        if i[0].value() == "segment":
            kicad_line(i, 0, 0)
        if i[0].value() == "gr_text":
            text = i[1]
            kicad_text(i, 0, 0, text)
        if i[0].value() == "via":
            kicad_via(i)
#        if i[0].value() == 'zone':
#            for x in i:
#                if isinstance(x, list):
#                    if x[0].value() == 'filled_polygon':
#                        x = x[1]
#                        for i in x:
#                            if isinstance(i, list):
#                                if i[0].value() == 'xy':
#                                    print(i[1]*u2,' ',i[2]*u2)


# if arc_list:
#  protel_arc(kicad_arc_list)
if kicad_via_list:
    protel_via(kicad_via_list)
if kicad_pad_list:
    protel_pad(kicad_pad_list)
if kicad_text_list:
    protel_text(kicad_text_list)
if kicad_line_list:
    protel_line(kicad_line_list)
if kicad_arc_list:
    protel_arc(kicad_arc_list)

#print("ARC: ", kicad_arc_list)
for x in protel_pad_list:
  template = template + x + '\n'
for x in protel_via_list:
  template = template + x + '\n'
for x in protel_line_list:
  template = template + x + '\n'
for x in protel_text_list:
  template = template + x + '\n'
for x in protel_arc_list:
  template = template + x + '\n'
f = open('1.PcbDoc', 'w+')
f.write(template)
