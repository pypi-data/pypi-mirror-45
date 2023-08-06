2a98cb28 (Michael Hayes 2016-01-05 00:15:49 +1300    1) """
2a98cb28 (Michael Hayes 2016-01-05 00:15:49 +1300    2) This module defines and draws the schematic components using
2a98cb28 (Michael Hayes 2016-01-05 00:15:49 +1300    3) circuitikz.   The components are defined at the bottom of this file.
2a98cb28 (Michael Hayes 2016-01-05 00:15:49 +1300    4) 
2a98cb28 (Michael Hayes 2016-01-05 00:15:49 +1300    5) Copyright 2015, 2016 Michael Hayes, UCECE
2a98cb28 (Michael Hayes 2016-01-05 00:15:49 +1300    6) """
2a98cb28 (Michael Hayes 2016-01-05 00:15:49 +1300    7) 
2a98cb28 (Michael Hayes 2016-01-05 00:15:49 +1300    8) 
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300    9) from __future__ import print_function
577895d5 (Michael Hayes 2016-01-25 16:29:50 +1300   10) from lcapy.latex import latex_str, format_label
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300   11) from lcapy.schemmisc import Pos, Opts
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300   12) import numpy as np
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300   13) import sys
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300   14) 
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300   15) module = sys.modules[__name__]
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300   16) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200   17) # There are two types of component (Cpt).
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200   18) #
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200   19) # 1. The stretchable components (such as resistors and capacitors) have
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200   20) # wires that can be stretched.  The size attribute controls the
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200   21) # spacing between the nodes but does not affect the component size.
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200   22) # The component size can be changed with the scale attribute (this changes
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200   23) # the dipole length).  The aspect ratio is not easy to change (need to use
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200   24) # dipole/resistor/height).
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200   25) #
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200   26) # 2.  The fixed components (such as ICs) do not have wires and cannot
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200   27) # be stretched.  The (unrotated) width is set by the size attribute and
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200   28) # the (unrotated) height is set by the aspect attribute.  The scale attribute
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200   29) # is not used.
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200   30) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   31) # There are two paradigms used for specifying node coordinates:
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   32) #
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   33) # 1.  The old model.  required_node_names returns subset of
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   34) # explicit_node_names as a list.
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   35) #
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   36) # 2.  The new model.  node_map specifies the subset of required nodes.
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   37) 
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300   38) 
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300   39) class Cpt(object):
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300   40) 
3e01a748 (Michael Hayes 2016-01-29 11:18:56 +1300   41)     voltage_keys = ('v', 'v_', 'v^', 'v_>', 'v_<', 'v^>', 'v^<',
3e01a748 (Michael Hayes 2016-01-29 11:18:56 +1300   42)                     'v<', 'v>')
257682e8 (Michael Hayes 2016-01-25 17:02:46 +1300   43)     current_keys = ('i', 'i_', 'i^', 'i_>',  'i_<', 'i^>', 'i^<',
d8a54694 (Michael Hayes 2016-01-29 10:25:43 +1300   44)                     'i>_', 'i<_', 'i>^', 'i<^', 'i>', 'i<')
f287b641 (Michael Hayes 2017-08-09 16:02:20 +1200   45)     flow_keys = ('f', 'f_', 'f^', 'f_>',  'f_<', 'f^>', 'f^<',
f287b641 (Michael Hayes 2017-08-09 16:02:20 +1200   46)                     'f>_', 'f<_', 'f>^', 'f<^', 'f>', 'f<')    
257682e8 (Michael Hayes 2016-01-25 17:02:46 +1300   47)     label_keys = ('l', 'l_', 'l^')
ba5b24f0 (Michael Hayes 2016-01-31 00:12:51 +1300   48)     implicit_keys =  ('implicit', 'ground', 'sground', 'rground')
cc22aab4 (Michael Hayes 2016-01-27 17:11:35 +1300   49)     # The following keys do not get passed through to circuitikz.
cc22aab4 (Michael Hayes 2016-01-27 17:11:35 +1300   50)     misc_keys = ('left', 'right', 'up', 'down', 'rotate', 'size',
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300   51)                  'mirror', 'scale', 'invisible', 'variable', 'fixed',
48bf8c60 (Michael Hayes 2017-09-20 18:43:32 +1200   52)                  'aspect', 'pins', 'image', 'offset')
257682e8 (Michael Hayes 2016-01-25 17:02:46 +1300   53) 
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300   54)     can_rotate = True
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300   55)     can_scale = False
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300   56)     can_mirror = False
3e3729df (Michael Hayes 2016-02-12 10:32:19 +1300   57)     can_stretch = True
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200   58)     default_width = 1.0
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200   59)     default_aspect = 1.0
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   60)     node_map = ()
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   61)     required_anchors = ()
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   62)     anchors = {}
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300   63) 
cf47f9a8 (Michael Hayes 2016-03-24 17:39:32 +1300   64)     @property
cf47f9a8 (Michael Hayes 2016-03-24 17:39:32 +1300   65)     def s(self):
cf47f9a8 (Michael Hayes 2016-03-24 17:39:32 +1300   66)         """Sanitised name"""
cf47f9a8 (Michael Hayes 2016-03-24 17:39:32 +1300   67)         return self.name.replace('.', '@')
cf47f9a8 (Michael Hayes 2016-03-24 17:39:32 +1300   68) 
a3b74280 (Michael Hayes 2016-03-26 23:35:10 +1300   69)     def __init__(self, sch, name, cpt_type, cpt_id, string,
ad105941 (Michael Hayes 2017-01-21 21:57:32 +1300   70)                  opts_string, node_names, keyword, *args):
e10ebcc8 (Michael Hayes 2016-01-07 12:35:58 +1300   71) 
e10ebcc8 (Michael Hayes 2016-01-07 12:35:58 +1300   72)         self.sch = sch
e10ebcc8 (Michael Hayes 2016-01-07 12:35:58 +1300   73)         self.type = cpt_type
e10ebcc8 (Michael Hayes 2016-01-07 12:35:58 +1300   74)         self.id = cpt_id
a3b74280 (Michael Hayes 2016-03-26 23:35:10 +1300   75)         self.name = name
e10ebcc8 (Michael Hayes 2016-01-07 12:35:58 +1300   76) 
02b5e379 (Michael Hayes 2016-01-09 21:47:13 +1300   77)         self.net = string.split(';')[0]
e10ebcc8 (Michael Hayes 2016-01-07 12:35:58 +1300   78)         self.opts_string = opts_string
680b2526 (Michael Hayes 2016-12-12 21:05:09 +1300   79) 
e10ebcc8 (Michael Hayes 2016-01-07 12:35:58 +1300   80)         self.args = args
e10ebcc8 (Michael Hayes 2016-01-07 12:35:58 +1300   81)         self.classname = self.__class__.__name__
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300   82) 
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300   83)         # Drawing hints
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300   84)         self.opts = Opts(opts_string)
e10ebcc8 (Michael Hayes 2016-01-07 12:35:58 +1300   85) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   86)         self.explicit_node_names = node_names
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   87) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   88)         extra_node_names = []
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   89)         for anchor in self.required_anchors:
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   90)             extra_node_names.append(name + '.' + anchor)
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   91)         self.extra_node_names = tuple(extra_node_names)
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   92)         
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   93)         anchor_node_names = []
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   94)         for anchor in self.anchors.keys():
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   95)             anchor_node_names.append(name + '.' + anchor)
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   96)         self.anchor_node_names = tuple(anchor_node_names)
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   97) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   98)         self.node_names = self.required_node_names + self.anchor_node_names
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300   99) 
e10ebcc8 (Michael Hayes 2016-01-07 12:35:58 +1300  100)     def __repr__(self):
0eb885d9 (Michael Hayes 2016-01-09 21:18:59 +1300  101)         return self.__str__()
e10ebcc8 (Michael Hayes 2016-01-07 12:35:58 +1300  102) 
0eb885d9 (Michael Hayes 2016-01-09 21:18:59 +1300  103)     def __str__(self):
0eb885d9 (Michael Hayes 2016-01-09 21:18:59 +1300  104) 
0eb885d9 (Michael Hayes 2016-01-09 21:18:59 +1300  105)         if self.opts == {}:
0eb885d9 (Michael Hayes 2016-01-09 21:18:59 +1300  106)             return self.net
0eb885d9 (Michael Hayes 2016-01-09 21:18:59 +1300  107)         return self.net + '; ' + str(self.opts)
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  108) 
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  109)     @property
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  110)     def size(self):
63f41b4f (Michael Hayes 2016-01-28 16:13:08 +1300  111)         """Component size between its nodes"""
784e2ed3 (Michael Hayes 2016-02-01 09:51:45 +1300  112)         if 'size' in self.opts:
784e2ed3 (Michael Hayes 2016-02-01 09:51:45 +1300  113)             val = self.opts['size']
784e2ed3 (Michael Hayes 2016-02-01 09:51:45 +1300  114)         elif self.right:
784e2ed3 (Michael Hayes 2016-02-01 09:51:45 +1300  115)             val = self.opts['right']
784e2ed3 (Michael Hayes 2016-02-01 09:51:45 +1300  116)         elif self.down:
784e2ed3 (Michael Hayes 2016-02-01 09:51:45 +1300  117)             val = self.opts['down']
784e2ed3 (Michael Hayes 2016-02-01 09:51:45 +1300  118)         elif self.left:
784e2ed3 (Michael Hayes 2016-02-01 09:51:45 +1300  119)             val = self.opts['left']
784e2ed3 (Michael Hayes 2016-02-01 09:51:45 +1300  120)         elif self.up:
784e2ed3 (Michael Hayes 2016-02-01 09:51:45 +1300  121)             val = self.opts['up']
784e2ed3 (Michael Hayes 2016-02-01 09:51:45 +1300  122)         else:
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  123)             val = self.default_width
784e2ed3 (Michael Hayes 2016-02-01 09:51:45 +1300  124)         if val == '':
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  125)             val = self.default_width
784e2ed3 (Michael Hayes 2016-02-01 09:51:45 +1300  126)         return float(val)
cc22aab4 (Michael Hayes 2016-01-27 17:11:35 +1300  127) 
cc22aab4 (Michael Hayes 2016-01-27 17:11:35 +1300  128)     @property
cc22aab4 (Michael Hayes 2016-01-27 17:11:35 +1300  129)     def scale(self):
cc22aab4 (Michael Hayes 2016-01-27 17:11:35 +1300  130)         return float(self.opts.get('scale', 1.0))
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  131) 
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  132)     @property
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  133)     def down(self):
9796abb5 (Michael Hayes 2016-02-01 09:26:25 +1300  134)         return 'down' in self.opts
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  135) 
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  136)     @property
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  137)     def up(self):
9796abb5 (Michael Hayes 2016-02-01 09:26:25 +1300  138)         return 'up' in self.opts
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  139) 
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  140)     @property
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  141)     def left(self):
9796abb5 (Michael Hayes 2016-02-01 09:26:25 +1300  142)         return 'left' in self.opts
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  143) 
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  144)     @property
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  145)     def right(self):
9796abb5 (Michael Hayes 2016-02-01 09:26:25 +1300  146)         return 'right' in self.opts
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  147) 
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  148)     @property
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  149)     def horizontal(self):
9796abb5 (Michael Hayes 2016-02-01 09:26:25 +1300  150)         return self.left or self.right
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  151) 
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  152)     @property
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  153)     def vertical(self):
9796abb5 (Michael Hayes 2016-02-01 09:26:25 +1300  154)         return self.up or self.down
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  155) 
784e2ed3 (Michael Hayes 2016-02-01 09:51:45 +1300  156)     def boolattr(self, opt):
92cb37dc (Michael Hayes 2016-01-31 10:46:28 +1300  157) 
92cb37dc (Michael Hayes 2016-01-31 10:46:28 +1300  158)         if opt not in self.opts:
92cb37dc (Michael Hayes 2016-01-31 10:46:28 +1300  159)             return False
92cb37dc (Michael Hayes 2016-01-31 10:46:28 +1300  160)         if self.opts[opt] == '':
92cb37dc (Michael Hayes 2016-01-31 10:46:28 +1300  161)             return True
92cb37dc (Michael Hayes 2016-01-31 10:46:28 +1300  162)         return self.opts[opt]
92cb37dc (Michael Hayes 2016-01-31 10:46:28 +1300  163) 
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  164)     @property
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  165)     def mirror(self):
784e2ed3 (Michael Hayes 2016-02-01 09:51:45 +1300  166)         return self.boolattr('mirror')
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300  167) 
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300  168)     @property
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300  169)     def invisible(self):
784e2ed3 (Michael Hayes 2016-02-01 09:51:45 +1300  170)         return self.boolattr('invisible')
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  171) 
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  172)     @property
f3d69499 (Michael Hayes 2016-01-30 22:53:19 +1300  173)     def variable(self):
784e2ed3 (Michael Hayes 2016-02-01 09:51:45 +1300  174)         return self.boolattr('variable')
f3d69499 (Michael Hayes 2016-01-30 22:53:19 +1300  175) 
f3d69499 (Michael Hayes 2016-01-30 22:53:19 +1300  176)     @property
22ec4c2f (Michael Hayes 2016-03-08 08:31:19 +1300  177)     def fixed(self):
22ec4c2f (Michael Hayes 2016-03-08 08:31:19 +1300  178)         return self.boolattr('fixed')
22ec4c2f (Michael Hayes 2016-03-08 08:31:19 +1300  179) 
22ec4c2f (Michael Hayes 2016-03-08 08:31:19 +1300  180)     @property
22ec4c2f (Michael Hayes 2016-03-08 08:31:19 +1300  181)     def stretch(self):
22ec4c2f (Michael Hayes 2016-03-08 08:31:19 +1300  182)         return self.can_stretch and not self.fixed
22ec4c2f (Michael Hayes 2016-03-08 08:31:19 +1300  183) 
22ec4c2f (Michael Hayes 2016-03-08 08:31:19 +1300  184)     @property
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  185)     def angle(self):
2a98cb28 (Michael Hayes 2016-01-05 00:15:49 +1300  186)         """Return rotation angle"""
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  187)         if self.right:
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  188)             angle = 0   
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  189)         elif self.down:
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  190)             angle = -90
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  191)         elif self.left:
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  192)             angle = 180
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  193)         elif self.up:
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  194)             angle = 90
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  195)         else:
39e2338a (Michael Hayes 2017-01-23 21:54:42 +1300  196)             angle = -90 if self.type in ('P', ) else 0
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  197)         
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  198)         if 'rotate' in self.opts:
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  199)             angle += float(self.opts['rotate'])
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  200)         return angle
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  201) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  202)     @property
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  203)     def w(self):
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  204)         """Normalised width"""
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  205)         return 1.0
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  206) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  207)     @property
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  208)     def h(self):
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  209)         """Normalised height"""
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  210)         return self.w / self.aspect
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  211) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  212)     @property
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  213)     def aspect(self):
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  214)         return float(self.opts.get('aspect', self.default_aspect))
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  215) 
48bf8c60 (Michael Hayes 2017-09-20 18:43:32 +1200  216)     @property
48bf8c60 (Michael Hayes 2017-09-20 18:43:32 +1200  217)     def offset(self):
48bf8c60 (Michael Hayes 2017-09-20 18:43:32 +1200  218)         return float(self.opts.get('offset', 0))
48bf8c60 (Michael Hayes 2017-09-20 18:43:32 +1200  219) 
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  220)     def R(self, angle_offset=0):
2a98cb28 (Michael Hayes 2016-01-05 00:15:49 +1300  221)         """Return rotation matrix"""
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  222)         angle = self.angle + angle_offset
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  223)         
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  224)         Rdict = {0: ((1, 0), (0, 1)),
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  225)                  90: ((0, 1), (-1, 0)),
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  226)                  180: ((-1, 0), (0, -1)),
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  227)                  -180: ((-1, 0), (0, -1)),
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  228)                  -90: ((0, -1), (1, 0))}
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  229)         if angle in Rdict:
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  230)             return np.array(Rdict[angle])
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  231)         
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  232)         t = angle / 180.0 * np.pi
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  233)         return np.array(((np.cos(t), np.sin(t)),
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  234)                          (-np.sin(t), np.cos(t))))
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  235) 
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  236)     @property
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  237)     def required_node_names(self):
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  238)         """Subset of explicit_node_names"""
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  239) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  240)         # Old model.   The number of node names in the list
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  241)         # must match the number of entries in coords.
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  242)         if self.node_map == ():
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  243)             return self.explicit_node_names
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  244) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  245)         # New model.
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  246)         node_names = []
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  247)         for anchor, node_name in zip(self.node_map, self.explicit_node_names):
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  248)             if anchor != '':
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  249)                 node_names.append(node_name)
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  250)         return tuple(node_names)
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  251) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  252)     def node(self, anchor):
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  253)         """Return node by anchor"""
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  254) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  255)         if anchor in self.node_map:
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  256)             index = self.node_map.index(anchor)
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  257)             node_name = self.explicit_node_names[index]
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  258)         else:
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  259)             node_name = self.name + '.' + anchor
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  260)         for node in self.nodes:
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  261)             if node.name == node_name:
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  262)                 return node
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  263)         raise ValueError('Unknown anchor %s for %s' % (anchor, self))
e8246268 (Michael Hayes 2016-01-03 21:23:21 +1300  264) 
e8246268 (Michael Hayes 2016-01-03 21:23:21 +1300  265)     @property
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  266)     def nodes(self):
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  267)         """Nodes used to draw the current element."""
14054b4d (Michael Hayes 2016-11-13 11:28:33 +1300  268) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  269)         if hasattr(self, '_nodes'):
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  270)             return self._nodes
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  271) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  272)         # Perhaps determine coords here as well and cache them?
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  273)         
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  274)         node_names = self.required_node_names + self.extra_node_names + self.anchor_node_names
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  275)         
14054b4d (Michael Hayes 2016-11-13 11:28:33 +1300  276)         rnodes = []
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  277)         for n in node_names:
14054b4d (Michael Hayes 2016-11-13 11:28:33 +1300  278)             if n in self.sch.nodes:
14054b4d (Michael Hayes 2016-11-13 11:28:33 +1300  279)                 rnodes.append(self.sch.nodes[n])
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  280)         self._nodes = rnodes
14054b4d (Michael Hayes 2016-11-13 11:28:33 +1300  281)         return rnodes
e10ebcc8 (Michael Hayes 2016-01-07 12:35:58 +1300  282) 
e10ebcc8 (Michael Hayes 2016-01-07 12:35:58 +1300  283)     @property
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  284)     def drawn_nodes(self):
14054b4d (Michael Hayes 2016-11-13 11:28:33 +1300  285)         """Nodes that are drawn"""
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  286)         return self.nodes
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  287) 
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  288)     @property
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  289)     def coords(self):
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  290) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  291)         # Determine the required coords.
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  292)         rcoords = []
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  293)         for node in self.nodes:
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  294)             node_name = node.name
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  295)             if node_name in self.explicit_node_names:
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  296)                 index = self.explicit_node_names.index(node_name)
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  297)                 anchor = self.node_map[index]
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  298)             elif node_name in self.sch.nodes:
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  299)                 anchor = node_name.split('.')[-1]
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  300)             else:
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  301)                 raise ValueError('Unknown node %s' % node_name)
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  302) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  303)             if anchor != '':
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  304)                 rcoords.append(self.anchors[anchor])
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  305)         return rcoords
34f0380f (Michael Hayes 2016-01-03 18:24:34 +1300  306) 
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  307)     @property
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  308)     def scoords(self):
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  309)         """Scaled coordinates for each of the nodes"""
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  310) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  311)         c = np.array(self.coords)
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  312)         S = np.array(((self.w, self.h),) * c.shape[0])
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  313)         return c * S
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  314) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  315)     @property
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  316)     def tcoords(self):
2a98cb28 (Michael Hayes 2016-01-05 00:15:49 +1300  317)         """Transformed coordinates for each of the nodes"""
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  318)         if hasattr(self, '_tcoords'):
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  319)             return self._tcoords
34f0380f (Michael Hayes 2016-01-03 18:24:34 +1300  320) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  321)         self._tcoords = np.dot(self.scoords, self.R())
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  322)         return self._tcoords
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  323) 
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  324)     @property
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  325)     def xvals(self):
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  326)         return self.tcoords[:, 0]
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  327) 
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  328)     @property
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  329)     def yvals(self):
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  330)         return self.tcoords[:, 1]
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  331) 
5f32fd4c (Michael Hayes 2016-01-03 19:54:50 +1300  332)     def xlink(self, graphs):
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  333) 
34f0380f (Michael Hayes 2016-01-03 18:24:34 +1300  334)         xvals = self.xvals
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  335)         for m1, n1 in enumerate(self.nodes):
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  336)             for m2, n2 in enumerate(self.nodes[m1 + 1:], m1 + 1):
34f0380f (Michael Hayes 2016-01-03 18:24:34 +1300  337)                 if xvals[m2] == xvals[m1]:
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300  338)                     graphs.link(n1.name, n2.name)
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  339) 
5f32fd4c (Michael Hayes 2016-01-03 19:54:50 +1300  340)     def ylink(self, graphs):
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  341) 
34f0380f (Michael Hayes 2016-01-03 18:24:34 +1300  342)         yvals = self.yvals
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  343)         for m1, n1 in enumerate(self.nodes):
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  344)             for m2, n2 in enumerate(self.nodes[m1 + 1:], m1 + 1):
34f0380f (Michael Hayes 2016-01-03 18:24:34 +1300  345)                 if yvals[m2] == yvals[m1]:
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300  346)                     graphs.link(n1.name, n2.name)
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  347) 
bd68d386 (Michael Hayes 2016-03-01 22:20:49 +1300  348)     def place(self, graphs, vals):
aa8778c7 (Michael Hayes 2017-09-20 20:34:52 +1200  349) 
aa8778c7 (Michael Hayes 2017-09-20 20:34:52 +1200  350)         if self.offset != 0:
aa8778c7 (Michael Hayes 2017-09-20 20:34:52 +1200  351)             print('TODO: offset %s by %f' % (self, self.offset))
bd68d386 (Michael Hayes 2016-03-01 22:20:49 +1300  352)         
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300  353)         size = self.size
bd68d386 (Michael Hayes 2016-03-01 22:20:49 +1300  354)         idx = np.argsort(vals)[::-1]
bd68d386 (Michael Hayes 2016-03-01 22:20:49 +1300  355)         for i in range(len(idx) - 1):
bd68d386 (Michael Hayes 2016-03-01 22:20:49 +1300  356)             m1 = idx[i]
bd68d386 (Michael Hayes 2016-03-01 22:20:49 +1300  357)             m2 = idx[i + 1]
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  358)             n1 = self.nodes[m1]
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  359)             n2 = self.nodes[m2]
bd68d386 (Michael Hayes 2016-03-01 22:20:49 +1300  360)             value = (vals[m2] - vals[m1]) * size
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300  361)             graphs.add(self, n1.name, n2.name, value, self.stretch)
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  362) 
bd68d386 (Michael Hayes 2016-03-01 22:20:49 +1300  363)     def xplace(self, graphs):
bd68d386 (Michael Hayes 2016-03-01 22:20:49 +1300  364)         self.place(graphs, self.xvals)
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  365) 
bd68d386 (Michael Hayes 2016-03-01 22:20:49 +1300  366)     def yplace(self, graphs):
bd68d386 (Michael Hayes 2016-03-01 22:20:49 +1300  367)         self.place(graphs, self.yvals)
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  368) 
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300  369)     def midpoint(self, node1, node2):
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300  370)         return (node1.pos + node2.pos) * 0.5
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300  371) 
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300  372)     def _node_str(self, node1, **kwargs):
02b5e379 (Michael Hayes 2016-01-09 21:47:13 +1300  373) 
02b5e379 (Michael Hayes 2016-01-09 21:47:13 +1300  374)         draw_nodes = kwargs.get('draw_nodes', True)
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  375) 
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300  376)         s = ''
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300  377)         if node1.visible(draw_nodes) and not node1.pin:
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300  378)             s = 'o' if node1.port else '*'
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300  379)         return s
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  380) 
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300  381)     def _node_pair_str(self, node1, node2, **kwargs):
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  382) 
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300  383)         # Create o-o o-* *-* etc.
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300  384)         s = self._node_str(node1, **kwargs)
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300  385)         s += '-'
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300  386)         s += self._node_str(node2, **kwargs)
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  387) 
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300  388)         if s == '-':
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300  389)             s = ''
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  390)         
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300  391)         return s
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  392) 
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  393)     def draw_node(self, n, **kwargs):
02b5e379 (Michael Hayes 2016-01-09 21:47:13 +1300  394) 
02b5e379 (Michael Hayes 2016-01-09 21:47:13 +1300  395)         draw_nodes = kwargs.get('draw_nodes', True)        
02b5e379 (Michael Hayes 2016-01-09 21:47:13 +1300  396) 
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  397)         s = ''
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  398)         if not draw_nodes:
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  399)             return s
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  400) 
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300  401)         if not n.visible(draw_nodes) or n.pin:
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  402)             return s
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  403) 
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300  404)         if n.port:
cf47f9a8 (Michael Hayes 2016-03-24 17:39:32 +1300  405)             s = r'  \draw (%s) node[ocirc] {};''\n' % n.s
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  406)         else:
cf47f9a8 (Michael Hayes 2016-03-24 17:39:32 +1300  407)             s = r'  \draw (%s) node[circ] {};''\n' % n.s
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  408) 
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  409)         return s
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  410) 
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  411)     def draw_nodes(self, **kwargs):
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  412) 
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  413)         s = ''
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  414)         for n in self.drawn_nodes:
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  415)             s += self.draw_node(n, **kwargs)
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  416)         return s
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  417) 
5ad52862 (Michael Hayes 2016-01-07 12:53:31 +1300  418)     def draw(self, **kwargs):
4e875e49 (Michael Hayes 2016-01-06 11:13:03 +1300  419)         raise NotImplementedError('draw method not implemented for %s' % self)
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  420) 
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300  421) 
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300  422)     def opts_str_list(self, choices):
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300  423)         """Format voltage, current, or label string as a key-value pair
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300  424)         and return list of strings"""
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  425) 
577895d5 (Michael Hayes 2016-01-25 16:29:50 +1300  426)         def fmt(key, val):
2cb46971 (Michael Hayes 2016-09-24 14:28:37 +1200  427)             label = format_label(val)
2cb46971 (Michael Hayes 2016-09-24 14:28:37 +1200  428)             if label == '':
2cb46971 (Michael Hayes 2016-09-24 14:28:37 +1200  429)                 label = '{}'
2cb46971 (Michael Hayes 2016-09-24 14:28:37 +1200  430)             if not (label[0] == '{' and label[-1] == '}'):
2cb46971 (Michael Hayes 2016-09-24 14:28:37 +1200  431)                 label = '{' + label + '}'
2cb46971 (Michael Hayes 2016-09-24 14:28:37 +1200  432) 
2cb46971 (Michael Hayes 2016-09-24 14:28:37 +1200  433)             return '%s=%s' % (key, label)
577895d5 (Michael Hayes 2016-01-25 16:29:50 +1300  434) 
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300  435)         return [fmt(key, val) for key, val in self.opts.items()
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300  436)                 if key in choices]
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300  437) 
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300  438)     def opts_str(self, choices):
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300  439)         """Format voltage, current, or label string as a key-value pair"""
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300  440) 
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300  441)         return ','.join(self.opts_str_list(choices))
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  442) 
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  443)     @property
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  444)     def voltage_str(self):
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  445) 
257682e8 (Michael Hayes 2016-01-25 17:02:46 +1300  446)         return self.opts_str(self.voltage_keys)
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  447) 
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  448)     @property
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  449)     def current_str(self):
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  450) 
257682e8 (Michael Hayes 2016-01-25 17:02:46 +1300  451)         return self.opts_str(self.current_keys)
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  452) 
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  453)     @property
f287b641 (Michael Hayes 2017-08-09 16:02:20 +1200  454)     def flow_str(self):
f287b641 (Michael Hayes 2017-08-09 16:02:20 +1200  455) 
f287b641 (Michael Hayes 2017-08-09 16:02:20 +1200  456)         return self.opts_str(self.flow_keys)    
f287b641 (Michael Hayes 2017-08-09 16:02:20 +1200  457) 
f287b641 (Michael Hayes 2017-08-09 16:02:20 +1200  458)     @property
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  459)     def label_str(self):
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  460) 
257682e8 (Michael Hayes 2016-01-25 17:02:46 +1300  461)         return self.opts_str(self.label_keys)
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  462) 
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  463)     @property
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300  464)     def label_str_list(self):
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300  465) 
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300  466)         return self.opts_str_list(self.label_keys)
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300  467) 
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300  468)     @property
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  469)     def args_str(self):
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  470) 
257682e8 (Michael Hayes 2016-01-25 17:02:46 +1300  471)         def fmt(key, val):
257682e8 (Michael Hayes 2016-01-25 17:02:46 +1300  472)             return '%s=%s' % (key, format_label(val))
257682e8 (Michael Hayes 2016-01-25 17:02:46 +1300  473) 
257682e8 (Michael Hayes 2016-01-25 17:02:46 +1300  474)         return ','.join([fmt(key, val) 
257682e8 (Michael Hayes 2016-01-25 17:02:46 +1300  475)                          for key, val in self.opts.items()
f287b641 (Michael Hayes 2017-08-09 16:02:20 +1200  476)                          if key not in self.voltage_keys + self.current_keys + self.flow_keys + self.label_keys + self.misc_keys + self.implicit_keys])
257682e8 (Michael Hayes 2016-01-25 17:02:46 +1300  477) 
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  478)     def label(self, **kwargs):
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  479) 
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  480)         label_values = kwargs.get('label_values', True)
39e2338a (Michael Hayes 2017-01-23 21:54:42 +1300  481)         label_ids = kwargs.get('label_ids', True)        
39e2338a (Michael Hayes 2017-01-23 21:54:42 +1300  482) 
39e2338a (Michael Hayes 2017-01-23 21:54:42 +1300  483)         label_str = ''
39e2338a (Michael Hayes 2017-01-23 21:54:42 +1300  484)         if label_ids:
39e2338a (Michael Hayes 2017-01-23 21:54:42 +1300  485)             label_str = self.id_label
39e2338a (Michael Hayes 2017-01-23 21:54:42 +1300  486)         if label_values and self.value_label != '':
39e2338a (Michael Hayes 2017-01-23 21:54:42 +1300  487)             label_str = self.value_label        
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  488) 
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  489)         # Override label if specified.  There are no placement options.
39e2338a (Michael Hayes 2017-01-23 21:54:42 +1300  490)         string =  ','.join([format_label(val)
39e2338a (Michael Hayes 2017-01-23 21:54:42 +1300  491)                             for key, val in self.opts.items()
39e2338a (Michael Hayes 2017-01-23 21:54:42 +1300  492)                             if key in ('l', )])
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  493) 
39e2338a (Michael Hayes 2017-01-23 21:54:42 +1300  494)         if string != '':
39e2338a (Michael Hayes 2017-01-23 21:54:42 +1300  495)             label_str = string
d5ac0001 (Michael Hayes 2017-01-30 16:39:53 +1300  496)         # Remove curly braces.
d5ac0001 (Michael Hayes 2017-01-30 16:39:53 +1300  497)         if len(label_str) > 1 and label_str[0] == '{' and label_str[-1] == '}':
d5ac0001 (Michael Hayes 2017-01-30 16:39:53 +1300  498)             label_str = label_str[1:-1]
a8c45a35 (Michael Hayes 2016-01-25 14:29:31 +1300  499)         return label_str
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  500) 
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  501)     def label_make(self, label_pos='', **kwargs):
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  502) 
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  503)         # TODO merge with label
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  504) 
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  505)         label_values = kwargs.get('label_values', True)
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  506)         label_ids = kwargs.get('label_ids', True)
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  507) 
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  508)         # Generate default label.
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  509)         if (label_ids and label_values and self.id_label != '' 
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  510)             and self.value_label and self.id_label != self.value_label):
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  511)             label_str = r'l%s={%s}{=%s}' % (label_pos, self.id_label,
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  512)                                             self.value_label)
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  513)         elif label_ids and self.id_label != '':
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  514)             label_str = r'l%s=%s' % (label_pos, self.id_label)
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  515)         elif label_values and self.value_label != '':
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  516)             label_str = r'l%s=%s' % (label_pos, self.value_label)
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  517)         else:
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  518)             label_str = ''
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  519) 
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  520)         # Override label if specified.
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  521)         if self.label_str != '':
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  522)             label_str = self.label_str
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  523)         return label_str
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300  524) 
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  525)     def check(self):
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300  526)         """Check schematic options and return True if component is to be drawn"""
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  527) 
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  528)         if not self.can_rotate and self.angle != 0:
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  529)             raise ValueError('Cannot rotate component %s' % self.name)
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  530) 
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  531)         if not self.can_scale and self.scale != 1:
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  532)             raise ValueError('Cannot scale component %s' % self.name)
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  533) 
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  534)         if not self.can_mirror and self.mirror:
f3d69499 (Michael Hayes 2016-01-30 22:53:19 +1300  535)             raise ValueError('Cannot mirror component %s' % self.name)
9796abb5 (Michael Hayes 2016-02-01 09:26:25 +1300  536) 
9796abb5 (Michael Hayes 2016-02-01 09:26:25 +1300  537)         if self.left + self.right + self.up + self.down > 1:
9796abb5 (Michael Hayes 2016-02-01 09:26:25 +1300  538)             raise ValueError('Mutually exclusive drawing directions for %s' % self.name)
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300  539)         
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300  540)         return not self.invisible
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  541) 
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  542)     def tf(self, centre, offset, angle_offset=0.0):
92cb37dc (Michael Hayes 2016-01-31 10:46:28 +1300  543)         """Transform coordinate"""
92cb37dc (Michael Hayes 2016-01-31 10:46:28 +1300  544) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  545)         raise NotImplementedError('tf method not implemented for %s' % self)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  546) 
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200  547)     def draw_path(self, points, style='', join='--', closed=False):
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  548) 
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200  549)         path = (' %s ' % join).join(['(%s)' % point for point in points])
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200  550)         if closed:
77ce381c (Michael Hayes 2016-04-04 08:48:35 +1200  551)             path += ' %s cycle' % join
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200  552) 
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  553)         args_str = self.args_str
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  554)         if style == '':
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  555)             s = args_str
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  556)         elif args_str == '':
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  557)             s = style
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  558)         else:
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  559)             s = style + ', ' + args_str
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  560)         if s != '':
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  561)             s = '[%s]' % s
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  562) 
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  563)         return r'  \draw%s %s;''\n' % (s, path)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  564) 
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  565)     def draw_label(self, pos, **kwargs):
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  566) 
fcabf8cd (Michael Hayes 2017-01-30 16:47:03 +1300  567)         return r'  \draw[%s] (%s) node[] {%s};''\n'% (
fcabf8cd (Michael Hayes 2017-01-30 16:47:03 +1300  568)             self.args_str, pos, self.label(**kwargs))
9226ff89 (Michael Hayes 2016-01-31 11:00:12 +1300  569) 
9226ff89 (Michael Hayes 2016-01-31 11:00:12 +1300  570) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  571) class StretchyCpt(Cpt):
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  572) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  573)     can_stretch = True
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  574) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  575)     def xtf(self, centre, offset, angle_offset=0.0):
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  576)         """Transform coordinate."""
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  577) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  578)         # Note the size attribute is not used.   This only scales the x coords.
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  579)         if isinstance(offset[0], tuple):
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  580)             return [self.xtf(centre, offset1, angle_offset) for offset1 in offset]
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  581) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  582)         return centre + np.dot((offset[0] * self.w * self.scale, offset[1] * self.h), self.R(angle_offset)) * self.sch.node_spacing
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  583) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  584) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  585)     def tf(self, centre, offset, angle_offset=0.0):
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  586)         """Transform coordinate."""
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  587) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  588)         # Note the size attribute is not used.
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  589)         if isinstance(offset[0], tuple):
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  590)             return [self.tf(centre, offset1, angle_offset) for offset1 in offset]
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  591) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  592)         return centre + np.dot((offset[0] * self.w, offset[1] * self.h), self.R(angle_offset)) * self.scale * self.sch.node_spacing
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  593) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  594) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  595) class FixedCpt(Cpt):
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  596) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  597)     can_stretch = False
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  598) 
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  599)     @property
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  600)     def centre(self):
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  601)         if hasattr(self, 'anchors'):
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  602)             # Look for centre anchor.
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  603)             for node in self.nodes:
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  604)                 if node.name.split('.')[-1] == 'mid':
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  605)                     return node.pos
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  606)         
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  607)         N = len(self.nodes)
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  608)         return self.midpoint(self.nodes[0], self.nodes[N // 2])
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  609) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  610)     def tf(self, centre, offset, angle_offset=0.0):
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  611)         """Transform coordinate."""
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  612) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  613)         if isinstance(offset[0], tuple):
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  614)             return [self.tf(centre, offset1, angle_offset) for offset1 in offset]
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  615) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  616)         return centre + np.dot((offset[0] * self.w, offset[1] * self.h), self.R(angle_offset)) * self.size * self.scale * self.sch.node_spacing
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  617) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  618) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  619) class Transistor(FixedCpt):
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  620)     """Transistor"""
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  621)     
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  622)     npos = ((1, 1.5), (0, 0.75), (1, 0))
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  623)     ppos = ((1, 0), (0, 0.75), (1, 1.5))
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  624) 
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  625)     can_mirror = True
eea2a110 (Michael Hayes 2016-03-08 08:54:01 +1300  626)     can_scale = True
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  627) 
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  628)     @property
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  629)     def coords(self):
43739ecb (Michael Hayes 2016-01-04 14:48:02 +1300  630)         if self.classname in ('Qpnp', 'Mpmos', 'Jpjf'):
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  631)             return self.npos if self.mirror else self.ppos
43739ecb (Michael Hayes 2016-01-04 14:48:02 +1300  632)         else:
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  633)             return self.ppos if self.mirror else self.npos
43739ecb (Michael Hayes 2016-01-04 14:48:02 +1300  634) 
5ad52862 (Michael Hayes 2016-01-07 12:53:31 +1300  635)     def draw(self, **kwargs):
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  636) 
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300  637)         if not self.check():
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300  638)             return ''
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  639) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  640)         n1, n2, n3 = self.nodes
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300  641)         centre = (n1.pos + n3.pos) * 0.5
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  642) 
eea2a110 (Michael Hayes 2016-03-08 08:54:01 +1300  643)         s = r'  \draw (%s) node[%s, %s, scale=%s, rotate=%d] (%s) {};''\n' % (
eea2a110 (Michael Hayes 2016-03-08 08:54:01 +1300  644)             centre, self.tikz_cpt, self.args_str, 2 * self.scale,
cf47f9a8 (Michael Hayes 2016-03-24 17:39:32 +1300  645)             self.angle, self.s)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  646)         s += self.draw_label(centre, **kwargs)
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  647) 
67a9db8d (Michael Hayes 2016-03-08 22:18:08 +1300  648)         # Add additional wires.  These help to compensate for the
67a9db8d (Michael Hayes 2016-03-08 22:18:08 +1300  649)         # slight differences in sizes of the different transistors.
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300  650)         if self.tikz_cpt in ('pnp', 'npn'):
67a9db8d (Michael Hayes 2016-03-08 22:18:08 +1300  651)             s += r'  \draw (%s.C) -- (%s) (%s.B) -- (%s) (%s.E) -- (%s);''\n' % (
cf47f9a8 (Michael Hayes 2016-03-24 17:39:32 +1300  652)                 self.s, n1.s, self.s, n2.s, self.s, n3.s)
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  653)         else:
67a9db8d (Michael Hayes 2016-03-08 22:18:08 +1300  654)             s += r'  \draw (%s.D) -- (%s) (%s.G) -- (%s) (%s.S) -- (%s);''\n' % (
cf47f9a8 (Michael Hayes 2016-03-24 17:39:32 +1300  655)                 self.s, n1.s, self.s, n2.s, self.s, n3.s)
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  656) 
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  657)         s += self.draw_nodes(**kwargs)
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  658)         return s
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  659) 
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  660) 
e5bf56bd (Michael Hayes 2016-01-04 15:11:14 +1300  661) class JFET(Transistor):
e5bf56bd (Michael Hayes 2016-01-04 15:11:14 +1300  662)     """Transistor"""
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  663) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  664)     #node_map = ('c', 'b', 'e')
e5bf56bd (Michael Hayes 2016-01-04 15:11:14 +1300  665)     npos = ((1, 1.5), (0, 0.48), (1, 0))
e5bf56bd (Michael Hayes 2016-01-04 15:11:14 +1300  666)     ppos = ((1, 0), (0, 1.02), (1, 1.5))
e5bf56bd (Michael Hayes 2016-01-04 15:11:14 +1300  667) 
e5bf56bd (Michael Hayes 2016-01-04 15:11:14 +1300  668) 
e5bf56bd (Michael Hayes 2016-01-04 15:11:14 +1300  669) class MOSFET(Transistor):
e5bf56bd (Michael Hayes 2016-01-04 15:11:14 +1300  670)     """Transistor"""
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  671) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  672)     #node_map = ('d', 'g', 's')    
257682e8 (Michael Hayes 2016-01-25 17:02:46 +1300  673)     npos = ((0.85, 1.52), (-0.25, 0.76), (0.85, 0))
257682e8 (Michael Hayes 2016-01-25 17:02:46 +1300  674)     ppos = ((0.85, 0), (-0.25, 0.76), (0.85, 1.52))
e5bf56bd (Michael Hayes 2016-01-04 15:11:14 +1300  675) 
e5bf56bd (Michael Hayes 2016-01-04 15:11:14 +1300  676) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  677) class TwoPort(FixedCpt):
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  678)     """Two-port"""
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  679) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  680)     # TODO
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  681)     can_rotate = False
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  682) 
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  683)     @property
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300  684)     def coords(self):
7bb91a86 (Michael Hayes 2016-03-26 14:54:04 +1300  685)         return ((1.5, 1), (1.5, 0), (0, 1), (0, 0))
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  686) 
5ad52862 (Michael Hayes 2016-01-07 12:53:31 +1300  687)     def draw(self, **kwargs):
7244ad0b (Michael Hayes 2016-01-03 22:20:08 +1300  688) 
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300  689)         if not self.check():
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300  690)             return ''
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  691) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  692)         n1, n2, n3, n4 = self.nodes
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300  693)         width = n2.pos.x - n4.pos.x
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300  694)         centre = (n1.pos + n2.pos + n3.pos + n4.pos) * 0.25
7244ad0b (Michael Hayes 2016-01-03 22:20:08 +1300  695) 
7bb91a86 (Michael Hayes 2016-03-26 14:54:04 +1300  696)         q = self.tf(centre, ((-1.5, -1.5), (-1.5, 1.5), (1.5, 1.5), (1.5, -1.5),
7bb91a86 (Michael Hayes 2016-03-26 14:54:04 +1300  697)                              (0, 1.15)))
7bb91a86 (Michael Hayes 2016-03-26 14:54:04 +1300  698) 
7bb91a86 (Michael Hayes 2016-03-26 14:54:04 +1300  699)         top = q[4]
7bb91a86 (Michael Hayes 2016-03-26 14:54:04 +1300  700) 
7bb91a86 (Michael Hayes 2016-03-26 14:54:04 +1300  701)         titlestr = ''
7bb91a86 (Michael Hayes 2016-03-26 14:54:04 +1300  702)         if len(self.args) > 0:
7bb91a86 (Michael Hayes 2016-03-26 14:54:04 +1300  703)             titlestr = "%s-parameter two-port" % self.args[0]
7244ad0b (Michael Hayes 2016-01-03 22:20:08 +1300  704) 
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200  705)         s = self.draw_path(q[0:4], closed=True)
1839042c (Michael Hayes 2016-03-27 10:28:02 +1300  706)         s += r'  \draw (%s) node[text width=%.1fcm, align=center] (%s) {%s};''\n' % (
cf47f9a8 (Michael Hayes 2016-03-24 17:39:32 +1300  707)             centre, width, titlestr, self.s)
1839042c (Michael Hayes 2016-03-27 10:28:02 +1300  708)         s += r'  \draw (%s) node[text width=%.1fcm, align=center, %s] {%s};''\n' % (
1839042c (Michael Hayes 2016-03-27 10:28:02 +1300  709)             top, width, self.args_str, self.label(**kwargs))
7244ad0b (Michael Hayes 2016-01-03 22:20:08 +1300  710) 
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  711)         s += self.draw_nodes(**kwargs)
7244ad0b (Michael Hayes 2016-01-03 22:20:08 +1300  712)         return s
7244ad0b (Michael Hayes 2016-01-03 22:20:08 +1300  713) 
7244ad0b (Michael Hayes 2016-01-03 22:20:08 +1300  714) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  715) class MX(FixedCpt):
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  716)     """Mixer"""
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  717) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  718)     # Dubious
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  719)     can_scale = True
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  720) 
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  721)     @property
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  722)     def coords(self):
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  723)         return ((0.25, 0.25), (-0.25, 0.25), (0, 0))
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  724) 
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  725)     def draw(self, **kwargs):
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  726) 
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  727)         if not self.check():
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  728)             return ''
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  729) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  730)         n1, n2, n3 = self.nodes
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  731) 
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  732)         centre = (n1.pos + n2.pos) * 0.5
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  733)         q = self.tf(centre, ((0, 0.35)))
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  734) 
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  735)         s = r'  \draw (%s) node[mixer,xscale=%s] {};''\n' % (
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  736)             centre, self.scale * self.size)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  737)         s += self.draw_label(q, **kwargs)
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  738)         return s
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  739) 
5ca0969f (Michael Hayes 2016-03-26 15:44:51 +1300  740) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  741) class SP(FixedCpt):
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  742)     """Summing point"""
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  743) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  744)     # Dubious
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  745)     can_scale = True
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  746)     can_mirror = True
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  747) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  748)     @property
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  749)     def coords(self):
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  750)         if self.mirror:
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  751)             return ((-0.25, 0), (0, 0.25), (0.25, 0), (0, -0.25))
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  752)         return ((-0.25, 0), (0, -0.25), (0.25, 0), (0, 0.25))
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  753) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  754)     def draw(self, **kwargs):
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  755) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  756)         if not self.check():
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  757)             return ''
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  758) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  759)         n = self.nodes
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  760) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  761)         centre = (n[0].pos + n[2].pos) * 0.5
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  762)         q = self.tf(centre, ((0.3, 0.3), (-0.125, 0), (0, -0.125),
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  763)                              (0, 0.125), (0, 0.125)))
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  764)         xscale = self.scale * self.size
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  765)         yscale = self.scale * self.size       
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  766)         if self.mirror:
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  767)             yscale = -yscale
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  768) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  769)         s = r'  \draw (%s) node[mixer, xscale=%s, yscale=%s, rotate=%s] {};''\n' % (
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  770)             centre, xscale, yscale, self.angle)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  771)         s += self.draw_label(q[0], **kwargs)
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  772)         s += r'  \draw (%s) node[] {$%s$};''\n'% (q[1], self.labels[0])
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  773) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  774)         if self.mirror:
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  775)             s += r'  \draw (%s) node[] {$%s$};''\n'% (q[4], self.labels[0])
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  776)         else:
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  777)             s += r'  \draw (%s) node[] {$%s$};''\n'% (q[2], self.labels[1])
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  778)         if len(self.labels) > 2:
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  779)             s += r'  \draw (%s) node[] {$%s$};''\n'% (q[3], self.labels[2])
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  780)         return s
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  781) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  782) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  783) class SP3(SP):
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  784)     """Summing point"""
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  785) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  786)     @property
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  787)     def coords(self):
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  788)         if self.mirror:
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  789)             return ((-0.25, 0), (0, 0.25), (0.25, 0))
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  790)         return ((-0.25, 0), (0, -0.25), (0.25, 0))
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  791) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  792) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  793) class SPpp(SP3):
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  794)     """Summing point"""
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  795) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  796)     labels = '++'
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  797) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  798) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  799) class SPpm(SP3):
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  800)     """Summing point"""
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  801) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  802)     labels = '+-'
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  803) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  804) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  805) class SPppp(SP):
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  806)     """Summing point"""
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  807) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  808)     labels = '+++'
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  809) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  810) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  811) class SPpmm(SP):
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  812)     """Summing point"""
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  813) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  814)     labels = '+--'
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  815) 
731fd1c5 (Michael Hayes 2016-03-28 12:50:37 +1300  816) 
3a7a7023 (Michael Hayes 2016-03-29 21:19:41 +1300  817) class SPppm(SP):
3a7a7023 (Michael Hayes 2016-03-29 21:19:41 +1300  818)     """Summing point"""
3a7a7023 (Michael Hayes 2016-03-29 21:19:41 +1300  819) 
3a7a7023 (Michael Hayes 2016-03-29 21:19:41 +1300  820)     labels = '++-'
3a7a7023 (Michael Hayes 2016-03-29 21:19:41 +1300  821) 
3a7a7023 (Michael Hayes 2016-03-29 21:19:41 +1300  822) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  823) class TL(StretchyCpt):
3e01a748 (Michael Hayes 2016-01-29 11:18:56 +1300  824)     """Transmission line"""
3e01a748 (Michael Hayes 2016-01-29 11:18:56 +1300  825) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  826)     # Dubious.  Perhaps should stretch this component in proportion to size?
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  827)     can_scale = True
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  828) 
3e01a748 (Michael Hayes 2016-01-29 11:18:56 +1300  829)     @property
3e01a748 (Michael Hayes 2016-01-29 11:18:56 +1300  830)     def coords(self):
3e01a748 (Michael Hayes 2016-01-29 11:18:56 +1300  831)         return ((1.25, 0.5), (1.25, 0), (0, 0.5), (0, 0))
3e01a748 (Michael Hayes 2016-01-29 11:18:56 +1300  832) 
3e01a748 (Michael Hayes 2016-01-29 11:18:56 +1300  833)     def draw(self, **kwargs):
3e01a748 (Michael Hayes 2016-01-29 11:18:56 +1300  834) 
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300  835)         if not self.check():
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300  836)             return ''
3e01a748 (Michael Hayes 2016-01-29 11:18:56 +1300  837) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  838)         n1, n2, n3, n4 = self.nodes
3c7394e8 (Michael Hayes 2016-01-29 12:29:52 +1300  839) 
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300  840)         centre = (n1.pos + n3.pos) * 0.5
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  841)         q = self.xtf(centre, ((0.32, 0),
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  842)                               (0.27, -0.145),
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  843)                               (-0.35, 0),
68dde2c2 (Michael Hayes 2016-04-05 23:14:49 +1200  844)                               (-0.35, -0.145),
68dde2c2 (Michael Hayes 2016-04-05 23:14:49 +1200  845)                               (-0.65, 0)))
9226ff89 (Michael Hayes 2016-01-31 11:00:12 +1300  846) 
9226ff89 (Michael Hayes 2016-01-31 11:00:12 +1300  847)         # Rotation creates an ellipse!
68dde2c2 (Michael Hayes 2016-04-05 23:14:49 +1200  848)         s = r'  \draw (%s) node[tlinestub, xscale=%s, rotate=%s] {};''\n' % (
68dde2c2 (Michael Hayes 2016-04-05 23:14:49 +1200  849)             q[4], self.scale, self.angle)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  850)         s += self.draw_label(centre, **kwargs)
48d76392 (Michael Hayes 2016-04-06 09:09:27 +1200  851) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  852)         s += self.draw_path((q[0], n1.s))
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  853)         s += self.draw_path((q[1], n2.s), join='|-')
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  854)         s += self.draw_path((q[2], n3.s))
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  855)         s += self.draw_path((q[3], n4.s), join='|-')
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  856)         s += self.draw_nodes(**kwargs)
3e01a748 (Michael Hayes 2016-01-29 11:18:56 +1300  857)         return s
3e01a748 (Michael Hayes 2016-01-29 11:18:56 +1300  858) 
3e01a748 (Michael Hayes 2016-01-29 11:18:56 +1300  859) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  860) class TF1(FixedCpt):
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  861)     """Transformer"""
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  862) 
142fed89 (Michael Hayes 2016-02-05 11:54:46 +1300  863)     @property
142fed89 (Michael Hayes 2016-02-05 11:54:46 +1300  864)     def coords(self):
142fed89 (Michael Hayes 2016-02-05 11:54:46 +1300  865)         return ((0.5, 1), (0.5, 0), (0, 1), (0, 0))
142fed89 (Michael Hayes 2016-02-05 11:54:46 +1300  866) 
5ad52862 (Michael Hayes 2016-01-07 12:53:31 +1300  867)     def draw(self, **kwargs):
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  868) 
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300  869)         if not self.check():
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300  870)             return ''
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300  871) 
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  872)         link = kwargs.get('link', True)
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  873) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  874)         p = [node.pos for node in self.nodes]
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  875) 
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  876)         centre = (p[0] + p[1] + p[2] + p[3]) * 0.25
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  877)         q = self.tf(centre, ((-0.35, 0.3), (0.35, 0.3), (0, 0.375)))
62640edd (Michael Hayes 2016-03-16 23:05:45 +1300  878)         primary_dot = q[0]
62640edd (Michael Hayes 2016-03-16 23:05:45 +1300  879)         secondary_dot = q[1]
62640edd (Michael Hayes 2016-03-16 23:05:45 +1300  880)         labelpos = q[2]
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  881) 
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  882)         s = r'  \draw (%s) node[circ] {};''\n' % primary_dot
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  883)         s += r'  \draw (%s) node[circ] {};''\n' % secondary_dot
f85233fc (Michael Hayes 2016-01-24 23:36:30 +1300  884)         s += r'  \draw (%s) node[minimum width=%.1f] (%s) {%s};''\n' % (
cf47f9a8 (Michael Hayes 2016-03-24 17:39:32 +1300  885)             labelpos, 0.5, self.s, self.label(**kwargs))
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  886) 
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  887)         if link:
62640edd (Michael Hayes 2016-03-16 23:05:45 +1300  888)             # TODO: allow for rotation
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  889)             width = p[0].x - p[2].x
338f042a (Michael Hayes 2016-03-29 21:29:55 +1300  890)             arcpos = Pos((p[0].x + p[2].x) / 2, secondary_dot.y - width / 2 + 0.3)
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  891) 
a91378a1 (Michael Hayes 2016-01-26 09:26:59 +1300  892)             s += r'  \draw [<->] ([shift=(45:%.2f)]%s) arc(45:135:%.2f);''\n' % (
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  893)                 width / 2, arcpos, width / 2)
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  894) 
f0791e8a (Michael Hayes 2016-03-17 11:40:04 +1300  895)         if self.classname in ('TFcore', 'TFtapcore'):
62640edd (Michael Hayes 2016-03-16 23:05:45 +1300  896)             # Draw core
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  897)             q = self.tf(centre, ((-0.05, -0.2), (-0.05, 0.2),
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  898)                                  (0.05, -0.2), (0.05, 0.2)))
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  899)             s += self.draw_path(q[0:2], style='thick')
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  900)             s += self.draw_path(q[2:4], style='thick')
62640edd (Michael Hayes 2016-03-16 23:05:45 +1300  901) 
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  902)         return s
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  903) 
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  904) 
62640edd (Michael Hayes 2016-03-16 23:05:45 +1300  905) class Transformer(TF1):
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  906)     """Transformer"""
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  907) 
5ad52862 (Michael Hayes 2016-01-07 12:53:31 +1300  908)     def draw(self, **kwargs):
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  909) 
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300  910)         if not self.check():
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300  911)             return ''
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300  912) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  913)         n1, n2, n3, n4 = self.nodes
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  914) 
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300  915)         s = r'  \draw (%s) to [inductor] (%s);''\n' % (n3.s, n4.s)
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300  916)         s += r'  \draw (%s) to [inductor] (%s);''\n' % (n2.s, n1.s)
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  917) 
62640edd (Michael Hayes 2016-03-16 23:05:45 +1300  918)         s += super(Transformer, self).draw(link=False, **kwargs)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  919)         s += self.draw_nodes(**kwargs)
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  920)         return s
27874514 (Michael Hayes 2016-01-03 22:15:09 +1300  921) 
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  922) 
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  923) class TFtap(TF1):
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  924)     """Transformer"""
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  925) 
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  926)     @property
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  927)     def coords(self):
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  928)         return ((0.5, 1), (0.5, 0), (0, 1), (0, 0), (-0.125, 0.55), (0.625, 0.55))
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  929) 
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  930)     @property
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  931)     def drawn_nodes(self):
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  932)         # Do not draw the taps.
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  933)         return self.nodes[0:4]
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  934) 
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  935)     def draw(self, **kwargs):
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  936) 
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  937)         if not self.check():
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  938)             return ''
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  939) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  940)         n1, n2, n3, n4, n5, n6 = self.nodes
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  941) 
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300  942)         s = r'  \draw (%s) to [inductor] (%s);''\n' % (n3.s, n4.s)
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300  943)         s += r'  \draw (%s) to [inductor] (%s);''\n' % (n2.s, n1.s)
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  944) 
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  945)         s += super(TFtap, self).draw(link=False, **kwargs)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200  946)         s += self.draw_nodes(**kwargs)
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  947)         return s
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  948) 
b66f61a9 (Michael Hayes 2016-02-29 22:05:27 +1300  949) 
2479f554 (Michael Hayes 2016-01-03 23:40:02 +1300  950) class K(TF1):
2479f554 (Michael Hayes 2016-01-03 23:40:02 +1300  951)     """Mutual coupling"""
2479f554 (Michael Hayes 2016-01-03 23:40:02 +1300  952) 
a3b74280 (Michael Hayes 2016-03-26 23:35:10 +1300  953)     def __init__(self, sch, name, cpt_type, cpt_id, string,
ad105941 (Michael Hayes 2017-01-21 21:57:32 +1300  954)                  opts_string, node_names, keyword, *args):
4e875e49 (Michael Hayes 2016-01-06 11:13:03 +1300  955) 
4e875e49 (Michael Hayes 2016-01-06 11:13:03 +1300  956)         self.Lname1 = args[0]
4e875e49 (Michael Hayes 2016-01-06 11:13:03 +1300  957)         self.Lname2 = args[1]
a3b74280 (Michael Hayes 2016-03-26 23:35:10 +1300  958)         super (K, self).__init__(sch, name, cpt_type, cpt_id, string,
ad105941 (Michael Hayes 2017-01-21 21:57:32 +1300  959)                                  opts_string, node_names, keyword, *args[2:])
4e875e49 (Michael Hayes 2016-01-06 11:13:03 +1300  960) 
e10ebcc8 (Michael Hayes 2016-01-07 12:35:58 +1300  961)     @property
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  962)     def nodes(self):
2479f554 (Michael Hayes 2016-01-03 23:40:02 +1300  963) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  964)         # CHECKME
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  965)         
e10ebcc8 (Michael Hayes 2016-01-07 12:35:58 +1300  966)         # L1 and L2 need to be previously defined so we can find their nodes.
e10ebcc8 (Michael Hayes 2016-01-07 12:35:58 +1300  967)         L1 = self.sch.elements[self.Lname1]
e10ebcc8 (Michael Hayes 2016-01-07 12:35:58 +1300  968)         L2 = self.sch.elements[self.Lname2]
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300  969)         return [self.sch.nodes[n] for n in L1.node_names + L2.node_names]
2479f554 (Michael Hayes 2016-01-03 23:40:02 +1300  970) 
2479f554 (Michael Hayes 2016-01-03 23:40:02 +1300  971) 
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  972) class Gyrator(FixedCpt):
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  973)     """Gyrator"""
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  974) 
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  975)     @property
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  976)     def coords(self):
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  977)         return ((1, 1), (1, 0), (0, 1), (0, 0))
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  978)     
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  979)     def draw(self, **kwargs):
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  980) 
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  981)         if not self.check():
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  982)             return ''
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  983) 
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  984)         yscale = self.scale
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  985)         if not self.mirror:
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  986)             yscale = -yscale
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  987) 
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  988)         s = r'  \draw (%s) node[gyrator, %s, xscale=%.3f, yscale=%.3f, rotate=%d] (%s) {};''\n' % (
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  989)             self.midpoint(self.nodes[1], self.nodes[3]),
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  990)             self.args_str, 0.95 * self.scale, 0.89 * yscale,
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  991)             -self.angle, self.s)        
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  992) 
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  993)         s += self.draw_label(self.centre, **kwargs)
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  994)         s += self.draw_nodes(**kwargs)        
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  995)         return s
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  996) 
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300  997)     
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200  998) class OnePort(StretchyCpt):
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300  999)     """OnePort"""
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1000) 
b9e6697e (Michael Hayes 2016-01-30 23:01:33 +1300 1001)     can_mirror = True
a8f763dd (Michael Hayes 2016-02-02 22:18:01 +1300 1002)     can_scale = True
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300 1003) 
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300 1004)     @property
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300 1005)     def coords(self):
07a0ef3a (Michael Hayes 2016-01-04 23:38:44 +1300 1006)         return ((0, 0), (1, 0))
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1007) 
5ad52862 (Michael Hayes 2016-01-07 12:53:31 +1300 1008)     def draw(self, **kwargs):
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1009) 
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300 1010)         if not self.check():
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300 1011)             return ''
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300 1012) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1013)         n1, n2 = self.nodes
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1014) 
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1015)         tikz_cpt = self.tikz_cpt
f3d69499 (Michael Hayes 2016-01-30 22:53:19 +1300 1016)         if self.variable:
f3d69499 (Michael Hayes 2016-01-30 22:53:19 +1300 1017)             if self.type in ('C', 'R', 'L'):
f3d69499 (Michael Hayes 2016-01-30 22:53:19 +1300 1018)                 tikz_cpt = 'v' + tikz_cpt
f3d69499 (Michael Hayes 2016-01-30 22:53:19 +1300 1019)             else:
f3d69499 (Michael Hayes 2016-01-30 22:53:19 +1300 1020)                 raise Error('Component %s not variable' % self.name)
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1021) 
e658523b (Michael Hayes 2016-01-26 15:04:56 +1300 1022)         label_pos = '_'
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1023)         voltage_pos = '^'
faa532a4 (Michael Hayes 2017-08-09 14:13:45 +1200 1024)         if ((self.type in ('V', 'I', 'E', 'F', 'G', 'H', 'BAT')
faa532a4 (Michael Hayes 2017-08-09 14:13:45 +1200 1025)              and self.sch.circuitikz_version < '2016/01/01')
09e80731 (Michael Hayes 2017-08-09 14:41:54 +1200 1026)             or (self.type in ('I', 'F', 'G')
e974c549 (Michael Hayes 2018-08-19 18:40:46 +1200 1027)                 and self.sch.circuitikz_version >= '2018/05/28')):
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1028) 
d9a76b08 (Michael Hayes 2016-08-20 18:28:18 +1200 1029)             # Old versions of circuitikz expects the positive node
d9a76b08 (Michael Hayes 2016-08-20 18:28:18 +1200 1030)             # first, except for voltage and current sources!  So
d9a76b08 (Michael Hayes 2016-08-20 18:28:18 +1200 1031)             # swap the nodes otherwise they are drawn the wrong
d9a76b08 (Michael Hayes 2016-08-20 18:28:18 +1200 1032)             # way around.
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1033)             n1, n2 = n2, n1
d9a76b08 (Michael Hayes 2016-08-20 18:28:18 +1200 1034)                 
6c0f2ae6 (Michael Hayes 2016-02-12 15:23:02 +1300 1035)             if self.right or self.up:
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1036)                 # Draw label on LHS for vertical cpt and below
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1037)                 # for horizontal cpt.
e658523b (Michael Hayes 2016-01-26 15:04:56 +1300 1038)                 label_pos = '^'
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1039)                 voltage_pos = '_'
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1040)         else:
6c0f2ae6 (Michael Hayes 2016-02-12 15:23:02 +1300 1041)             if self.left or self.down:
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1042)                 # Draw label on LHS for vertical cpt and below
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1043)                 # for horizontal cpt.
e658523b (Michael Hayes 2016-01-26 15:04:56 +1300 1044)                 label_pos = '^'
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1045)                 voltage_pos = '_'
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1046) 
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1047)         # Add modifier to place voltage label on other side
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1048)         # from component identifier label.
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1049)         if 'v' in self.opts:
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1050)             self.opts['v' + voltage_pos] = self.opts.pop('v')
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1051) 
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1052)         # Reversed voltage.
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1053)         if 'vr' in self.opts:
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1054)             self.opts['v' + voltage_pos + '>'] = self.opts.pop('vr')
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1055) 
e658523b (Michael Hayes 2016-01-26 15:04:56 +1300 1056)         current_pos = label_pos
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1057)         # Add modifier to place current label on other side
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1058)         # from voltage marks.
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1059)         if 'i' in self.opts:
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1060)             self.opts['i' + current_pos] = self.opts.pop('i')
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1061) 
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1062)         # Reversed current.
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1063)         if 'ir' in self.opts:
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1064)             self.opts['i' + current_pos + '<'] = self.opts.pop('ir')
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1065) 
e658523b (Michael Hayes 2016-01-26 15:04:56 +1300 1066)         if 'l' in self.opts:
e658523b (Michael Hayes 2016-01-26 15:04:56 +1300 1067)             self.opts['l' + label_pos] = self.opts.pop('l')
e658523b (Michael Hayes 2016-01-26 15:04:56 +1300 1068) 
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300 1069)         node_pair_str = self._node_pair_str(n1, n2, **kwargs)
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1070) 
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1071)         args_str = self.args_str
f287b641 (Michael Hayes 2017-08-09 16:02:20 +1200 1072)         args_str2 = ','.join([self.voltage_str, self.current_str, self.flow_str])
f0791e8a (Michael Hayes 2016-03-17 11:40:04 +1300 1073) 
b9e6697e (Michael Hayes 2016-01-30 23:01:33 +1300 1074)         if self.mirror:
b9e6697e (Michael Hayes 2016-01-30 23:01:33 +1300 1075)             args_str += ',mirror'
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1076) 
a8f763dd (Michael Hayes 2016-02-02 22:18:01 +1300 1077)         if self.scale != 1.0:
f0791e8a (Michael Hayes 2016-03-17 11:40:04 +1300 1078)             args_str2 += ',bipoles/length=%scm' % (self.sch.cpt_size * self.scale)
a8f763dd (Michael Hayes 2016-02-02 22:18:01 +1300 1079) 
48cd7671 (Michael Hayes 2016-10-27 11:52:26 +1300 1080)         label_str = self.label_make(label_pos, **kwargs)
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1081)             
d866a23e (Michael Hayes 2016-03-21 20:34:15 +1300 1082)         s = r'  \draw[%s] (%s) to [%s,%s,%s,%s,n=%s] (%s);''\n' % (
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1083)             args_str, n1.s, tikz_cpt, label_str, args_str2,
cf47f9a8 (Michael Hayes 2016-03-24 17:39:32 +1300 1084)             node_pair_str, self.s, n2.s)
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1085)         return s
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1086) 
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1087) 
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1088) class VCS(OnePort):
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1089)     """Voltage controlled source"""
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1090) 
e8246268 (Michael Hayes 2016-01-03 21:23:21 +1300 1091)     @property
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1092)     def required_node_names(self):
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1093)         return self.explicit_node_names[0:2]
e8246268 (Michael Hayes 2016-01-03 21:23:21 +1300 1094) 
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1095) 
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1096) class CCS(OnePort):
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1097)     """Current controlled source"""
09e80731 (Michael Hayes 2017-08-09 14:41:54 +1200 1098) 
09e80731 (Michael Hayes 2017-08-09 14:41:54 +1200 1099)     @property
09e80731 (Michael Hayes 2017-08-09 14:41:54 +1200 1100)     def required_node_names(self):
09e80731 (Michael Hayes 2017-08-09 14:41:54 +1200 1101)         return self.explicit_node_names[0:2]    
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300 1102) 
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1103) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1104) class Opamp(FixedCpt):
2479f554 (Michael Hayes 2016-01-03 23:40:02 +1300 1105) 
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300 1106)     can_scale = True
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300 1107)     can_mirror = True
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300 1108) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1109)     required_anchors = ('mid', )
5ac80187 (Michael Hayes 2016-01-03 22:53:27 +1300 1110) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1111)     # The Nm node is not used (ground).
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1112)     node_map = ('out', '', '+', '-')
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1113)     
1d95e096 (Michael Hayes 2017-08-12 18:23:06 +1200 1114)     panchors = {'out' : (2.5, 0.0),
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1115)                 '+' : (0.0, 0.5),
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1116)                 '-' : (0.0, -0.5),
1d95e096 (Michael Hayes 2017-08-12 18:23:06 +1200 1117)                 'mid' : (1.25, 0.0),
1d95e096 (Michael Hayes 2017-08-12 18:23:06 +1200 1118)                 'vdd' : (1.25, 0.5),
4313abd2 (Michael Hayes 2016-12-17 18:57:38 +1300 1119)                 'vdd2' : (0.8, 0.745),
4313abd2 (Michael Hayes 2016-12-17 18:57:38 +1300 1120)                 'vss2' : (0.8, -0.745),
1d95e096 (Michael Hayes 2017-08-12 18:23:06 +1200 1121)                 'vss' : (1.25, -0.5),
1d95e096 (Michael Hayes 2017-08-12 18:23:06 +1200 1122)                 'ref' : (1.7, -0.255),
c183c6f5 (Michael Hayes 2016-12-13 17:06:34 +1300 1123)                 'r+' : (0.35, 0.25),
c183c6f5 (Michael Hayes 2016-12-13 17:06:34 +1300 1124)                 'r-' : (0.35, -0.25)}
8b237a4b (Michael Hayes 2016-12-13 21:33:42 +1300 1125)     
1d95e096 (Michael Hayes 2017-08-12 18:23:06 +1200 1126)     nanchors = {'out' : (2.5, 0.0),
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1127)                 '+' : (0.0, -0.5),
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1128)                 '-' : (0.0, 0.5),
1d95e096 (Michael Hayes 2017-08-12 18:23:06 +1200 1129)                 'mid' : (1.25, 0.0),
1d95e096 (Michael Hayes 2017-08-12 18:23:06 +1200 1130)                 'vdd' : (1.25, 0.5),
4313abd2 (Michael Hayes 2016-12-17 18:57:38 +1300 1131)                 'vdd2' : (0.8, 0.745),
4313abd2 (Michael Hayes 2016-12-17 18:57:38 +1300 1132)                 'vss2' : (0.8, -0.745),
1d95e096 (Michael Hayes 2017-08-12 18:23:06 +1200 1133)                 'vss' : (1.25, -0.5),
1d95e096 (Michael Hayes 2017-08-12 18:23:06 +1200 1134)                 'ref' : (1.7, -0.255),
c183c6f5 (Michael Hayes 2016-12-13 17:06:34 +1300 1135)                 'r+' : (0.35, 0.25),
c183c6f5 (Michael Hayes 2016-12-13 17:06:34 +1300 1136)                 'r-' : (0.35, -0.25)}
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1137) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1138)     @property
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1139)     def anchors(self):
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1140)         return self.nanchors if self.mirror else self.panchors
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1141)     
5ad52862 (Michael Hayes 2016-01-07 12:53:31 +1300 1142)     def draw(self, **kwargs):
5ac80187 (Michael Hayes 2016-01-03 22:53:27 +1300 1143) 
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300 1144)         if not self.check():
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300 1145)             return ''
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300 1146) 
1d95e096 (Michael Hayes 2017-08-12 18:23:06 +1200 1147)         yscale = 2 * 0.95 * self.scale        
63f41b4f (Michael Hayes 2016-01-28 16:13:08 +1300 1148)         if not self.mirror:
63f41b4f (Michael Hayes 2016-01-28 16:13:08 +1300 1149)             yscale = -yscale
63f41b4f (Michael Hayes 2016-01-28 16:13:08 +1300 1150) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1151)         centre = self.node('mid')
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1152) 
5855c4c2 (Michael Hayes 2016-01-28 11:54:26 +1300 1153)         # Note, scale scales by area, xscale and yscale scale by length.
cc22aab4 (Michael Hayes 2016-01-27 17:11:35 +1300 1154)         s = r'  \draw (%s) node[op amp, %s, xscale=%.3f, yscale=%.3f, rotate=%d] (%s) {};''\n' % (
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1155)             centre.s,
b24388f4 (Michael Hayes 2018-08-18 11:42:49 +1200 1156)             self.args_str, 2 * self.scale * 0.95, yscale,
cf47f9a8 (Michael Hayes 2016-03-24 17:39:32 +1300 1157)             -self.angle, self.s)
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1158)         s += r'  \draw (%s.out) |- (%s);''\n' % (self.s, self.node('out').s)
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1159)         s += r'  \draw (%s.+) |- (%s);''\n' % (self.s, self.node('+').s)
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1160)         s += r'  \draw (%s.-) |- (%s);''\n' % (self.s, self.node('-').s)
79fbb970 (Michael Hayes 2017-07-08 12:34:02 +1200 1161)         s += self.draw_label(centre.s, **kwargs)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1162)         s += self.draw_nodes(**kwargs)
2479f554 (Michael Hayes 2016-01-03 23:40:02 +1300 1163)         return s
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1164) 
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1165) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1166) class FDOpamp(FixedCpt):
f3ac4194 (Michael Hayes 2016-01-04 11:30:23 +1300 1167) 
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300 1168)     can_scale = True
0511a032 (Michael Hayes 2016-01-30 09:37:30 +1300 1169)     can_mirror = True
63f41b4f (Michael Hayes 2016-01-28 16:13:08 +1300 1170) 
6e6cc8a2 (Michael Hayes 2016-12-13 18:29:37 +1300 1171)     required_anchors = ('mid', )
6e6cc8a2 (Michael Hayes 2016-12-13 18:29:37 +1300 1172) 
6e6cc8a2 (Michael Hayes 2016-12-13 18:29:37 +1300 1173)     node_map = ('out+', 'out-', '+', '-')
6e6cc8a2 (Michael Hayes 2016-12-13 18:29:37 +1300 1174)     
05bdb0b6 (Michael Hayes 2018-08-18 11:55:46 +1200 1175)     panchors = {'out+' : (2.1, -0.5),
05bdb0b6 (Michael Hayes 2018-08-18 11:55:46 +1200 1176)                 'out-' : (2.1, 0.5),                
6e6cc8a2 (Michael Hayes 2016-12-13 18:29:37 +1300 1177)                 '+' : (0.0, 0.5),
6e6cc8a2 (Michael Hayes 2016-12-13 18:29:37 +1300 1178)                 '-' : (0.0, -0.5),
1d95e096 (Michael Hayes 2017-08-12 18:23:06 +1200 1179)                 'mid' : (1.25, 0.0),
b24388f4 (Michael Hayes 2018-08-18 11:42:49 +1200 1180)                 'vdd' : (1.0, 0.645),
b24388f4 (Michael Hayes 2018-08-18 11:42:49 +1200 1181)                 'vss' : (1.0, -0.645),
b24388f4 (Michael Hayes 2018-08-18 11:42:49 +1200 1182)                 'r+' : (0.4, 0.25),
b24388f4 (Michael Hayes 2018-08-18 11:42:49 +1200 1183)                 'r-' : (0.4, -0.25)}
8b237a4b (Michael Hayes 2016-12-13 21:33:42 +1300 1184)     
05bdb0b6 (Michael Hayes 2018-08-18 11:55:46 +1200 1185)     nanchors = {'out+' : (2.1, 0.5),
05bdb0b6 (Michael Hayes 2018-08-18 11:55:46 +1200 1186)                 'out-' : (2.1, -0.5),
6e6cc8a2 (Michael Hayes 2016-12-13 18:29:37 +1300 1187)                 '+' : (0.0, -0.5),
6e6cc8a2 (Michael Hayes 2016-12-13 18:29:37 +1300 1188)                 '-' : (0.0, 0.5),
1d95e096 (Michael Hayes 2017-08-12 18:23:06 +1200 1189)                 'mid' : (1.25, 0.0),
b24388f4 (Michael Hayes 2018-08-18 11:42:49 +1200 1190)                 'vdd' : (1.0, 0.645),
b24388f4 (Michael Hayes 2018-08-18 11:42:49 +1200 1191)                 'vss' : (1.0, -0.645),
b24388f4 (Michael Hayes 2018-08-18 11:42:49 +1200 1192)                 'r+' : (0.4, 0.25),
b24388f4 (Michael Hayes 2018-08-18 11:42:49 +1200 1193)                 'r-' : (0.4, -0.25)}
f3ac4194 (Michael Hayes 2016-01-04 11:30:23 +1300 1194) 
6e6cc8a2 (Michael Hayes 2016-12-13 18:29:37 +1300 1195)     @property
6e6cc8a2 (Michael Hayes 2016-12-13 18:29:37 +1300 1196)     def anchors(self):
6e6cc8a2 (Michael Hayes 2016-12-13 18:29:37 +1300 1197)         return self.nanchors if self.mirror else self.panchors
6e6cc8a2 (Michael Hayes 2016-12-13 18:29:37 +1300 1198)     
5ad52862 (Michael Hayes 2016-01-07 12:53:31 +1300 1199)     def draw(self, **kwargs):
f3ac4194 (Michael Hayes 2016-01-04 11:30:23 +1300 1200) 
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300 1201)         if not self.check():
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300 1202)             return ''
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300 1203) 
6e6cc8a2 (Michael Hayes 2016-12-13 18:29:37 +1300 1204)         centre = self.node('mid')
f3ac4194 (Michael Hayes 2016-01-04 11:30:23 +1300 1205) 
b24388f4 (Michael Hayes 2018-08-18 11:42:49 +1200 1206)         yscale = 2 * 0.952 * self.scale
63f41b4f (Michael Hayes 2016-01-28 16:13:08 +1300 1207)         if not self.mirror:
63f41b4f (Michael Hayes 2016-01-28 16:13:08 +1300 1208)             yscale = -yscale
63f41b4f (Michael Hayes 2016-01-28 16:13:08 +1300 1209) 
cc22aab4 (Michael Hayes 2016-01-27 17:11:35 +1300 1210)         s = r'  \draw (%s) node[fd op amp, %s, xscale=%.3f, yscale=%.3f, rotate=%d] (%s) {};''\n' % (
b24388f4 (Michael Hayes 2018-08-18 11:42:49 +1200 1211)             centre.s, self.args_str, 2 * self.scale * 0.95, yscale,
cf47f9a8 (Michael Hayes 2016-03-24 17:39:32 +1300 1212)             -self.angle, self.s)
79fbb970 (Michael Hayes 2017-07-08 12:34:02 +1200 1213)         s += r'  \draw (%s.out +) |- (%s);''\n' % (self.s, self.node('out+').s)
79fbb970 (Michael Hayes 2017-07-08 12:34:02 +1200 1214)         s += r'  \draw (%s.out -) |- (%s);''\n' % (self.s, self.node('out-').s)
79fbb970 (Michael Hayes 2017-07-08 12:34:02 +1200 1215)         s += r'  \draw (%s.+) |- (%s);''\n' % (self.s, self.node('+').s)
79fbb970 (Michael Hayes 2017-07-08 12:34:02 +1200 1216)         s += r'  \draw (%s.-) |- (%s);''\n' % (self.s, self.node('-').s)
79fbb970 (Michael Hayes 2017-07-08 12:34:02 +1200 1217)         s += self.draw_label(centre.s, **kwargs)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1218)         s += self.draw_nodes(**kwargs)
f3ac4194 (Michael Hayes 2016-01-04 11:30:23 +1300 1219)         return s
f3ac4194 (Michael Hayes 2016-01-04 11:30:23 +1300 1220) 
f3ac4194 (Michael Hayes 2016-01-04 11:30:23 +1300 1221) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1222) class SPDT(StretchyCpt):
a91378a1 (Michael Hayes 2016-01-26 09:26:59 +1300 1223)     """SPDT switch"""
a91378a1 (Michael Hayes 2016-01-26 09:26:59 +1300 1224) 
a91378a1 (Michael Hayes 2016-01-26 09:26:59 +1300 1225)     @property
a91378a1 (Michael Hayes 2016-01-26 09:26:59 +1300 1226)     def coords(self):
33808401 (Michael Hayes 2016-03-05 15:16:24 +1300 1227)         return ((0, 0.1565), (0.59, 0.313), (0.59, 0))
a91378a1 (Michael Hayes 2016-01-26 09:26:59 +1300 1228) 
a91378a1 (Michael Hayes 2016-01-26 09:26:59 +1300 1229)     def draw(self, **kwargs):
a91378a1 (Michael Hayes 2016-01-26 09:26:59 +1300 1230) 
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300 1231)         if not self.check():
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300 1232)             return ''
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300 1233) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1234)         n1, n2, n3 = self.nodes
a91378a1 (Michael Hayes 2016-01-26 09:26:59 +1300 1235) 
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300 1236)         centre = n1.pos * 0.5 + (n2.pos + n3.pos) * 0.25
a91378a1 (Michael Hayes 2016-01-26 09:26:59 +1300 1237)         s = r'  \draw (%s) node[spdt, %s, rotate=%d] (%s) {};''\n' % (
cf47f9a8 (Michael Hayes 2016-03-24 17:39:32 +1300 1238)             centre, self.args_str, self.angle, self.s)
a91378a1 (Michael Hayes 2016-01-26 09:26:59 +1300 1239)         
a91378a1 (Michael Hayes 2016-01-26 09:26:59 +1300 1240)         # TODO, fix label position.
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300 1241)         centre = (n1.pos + n3.pos) * 0.5 + Pos(0, -0.5)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1242)         s += self.draw_label(centre, **kwargs)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1243)         s += self.draw_nodes(**kwargs)
a91378a1 (Michael Hayes 2016-01-26 09:26:59 +1300 1244)         return s
a91378a1 (Michael Hayes 2016-01-26 09:26:59 +1300 1245) 
a91378a1 (Michael Hayes 2016-01-26 09:26:59 +1300 1246) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1247) class Shape(FixedCpt):
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1248)     """General purpose shape"""
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1249) 
19b65731 (Michael Hayes 2016-03-28 23:02:59 +1300 1250)     default_aspect = 1.0
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1251)     can_mirror = True
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1252) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1253) 
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1254)     @property
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1255)     def width(self):
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1256)         return self.w * self.size * self.sch.node_spacing
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1257) 
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1258)     @property
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1259)     def height(self):
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1260)         return self.h * self.size * self.sch.node_spacing
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1261) 
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1262)     def draw(self, **kwargs):
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1263) 
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1264)         if not self.check():
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1265)             return ''
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1266) 
770e1d4c (Michael Hayes 2016-11-04 16:55:21 +1300 1267)         label = self.label(**kwargs)
770e1d4c (Michael Hayes 2016-11-04 16:55:21 +1300 1268)         if 'image' in self.opts:
3cd21f10 (Michael Hayes 2016-11-04 20:43:19 +1300 1269)             # Override label with image
3cd21f10 (Michael Hayes 2016-11-04 20:43:19 +1300 1270)             label = r'\includegraphics[width=%scm]{%s}' % (self.width - 0.5,
3cd21f10 (Michael Hayes 2016-11-04 20:43:19 +1300 1271)                                                            self.opts['image'])
770e1d4c (Michael Hayes 2016-11-04 16:55:21 +1300 1272) 
5f5aed56 (Michael Hayes 2016-11-14 16:30:01 +1300 1273)         text_width = self.width * 0.8
5f5aed56 (Michael Hayes 2016-11-14 16:30:01 +1300 1274) 
5c5382d3 (Michael Hayes 2016-03-29 20:16:52 +1300 1275)         # shape border rotate rotates the box but not the text
b0564ffe (Michael Hayes 2016-09-04 18:15:17 +1200 1276)         s = r'  \draw (%s) node[%s, thick, inner sep=0pt, minimum width=%scm, minimum height=%scm, text width=%scm, align=center, shape border rotate=%s, draw, %s] (%s) {%s};''\n'% (
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1277)             self.centre, self.shape, self.width, self.height, 
5f5aed56 (Michael Hayes 2016-11-14 16:30:01 +1300 1278)             text_width, self.angle, self.args_str, self.s, label)
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1279) 
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1280)         return s
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1281) 
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1282) 
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1283) class Box2(Shape):
32c8c2e9 (Michael Hayes 2017-01-30 16:28:57 +1300 1284)     """Square box,  A rectangle is created by defining aspect."""
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1285) 
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1286)     shape = 'rectangle'
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1287) 
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1288)     @property
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1289)     def coords(self):
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1290)         return ((-0.5, 0), (0.5, 0))
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1291) 
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1292) 
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1293) class Box4(Shape):
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1294)     """Box4"""
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1295) 
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1296)     shape = 'rectangle'
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1297) 
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1298)     @property
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1299)     def coords(self):
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1300)         return ((-0.5, 0), (0, -0.5), (0.5, 0), (0, 0.5))
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1301) 
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1302) 
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1303) class Box12(Shape):
1e62920b (Michael Hayes 2016-10-04 11:37:50 +1300 1304)     """Box12"""
1e62920b (Michael Hayes 2016-10-04 11:37:50 +1300 1305) 
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1306)     shape = 'rectangle'
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1307) 
1e62920b (Michael Hayes 2016-10-04 11:37:50 +1300 1308)     @property
1e62920b (Michael Hayes 2016-10-04 11:37:50 +1300 1309)     def coords(self):
1e62920b (Michael Hayes 2016-10-04 11:37:50 +1300 1310)         return ((-0.5, 0.25), (-0.5, 0), (-0.5, -0.25),
1e62920b (Michael Hayes 2016-10-04 11:37:50 +1300 1311)                 (-0.25, -0.5), (0, -0.5), (0.25, -0.5),
1e62920b (Michael Hayes 2016-10-04 11:37:50 +1300 1312)                 (0.5, -0.25), (0.5, 0), (0.5, 0.25),
1e62920b (Michael Hayes 2016-10-04 11:37:50 +1300 1313)                 (0.25, 0.5), (0, 0.5), (-0.25, 0.5))
1e62920b (Michael Hayes 2016-10-04 11:37:50 +1300 1314) 
1e62920b (Michael Hayes 2016-10-04 11:37:50 +1300 1315) 
6e6cc8a2 (Michael Hayes 2016-12-13 18:29:37 +1300 1316) class Box(Shape):
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1317)     """Box"""
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1318) 
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1319)     shape = 'rectangle'    
8379e461 (Michael Hayes 2016-12-12 21:10:09 +1300 1320)     anchors = {'nw' : (-0.5, 0.5), 'wnw' : (-0.5, 0.25),
8379e461 (Michael Hayes 2016-12-12 21:10:09 +1300 1321)                'w' : (-0.5, 0), 'wsw' : (-0.5, -0.25), 
8379e461 (Michael Hayes 2016-12-12 21:10:09 +1300 1322)                'sw' : (-0.5, -0.5), 'ssw' : (-0.25, -0.5),
8379e461 (Michael Hayes 2016-12-12 21:10:09 +1300 1323)                's' : (0, -0.5), 'sse' : (0.25, -0.5),
8379e461 (Michael Hayes 2016-12-12 21:10:09 +1300 1324)                'se' : (0.5, -0.5), 'ese' : (0.5, -0.25),
8379e461 (Michael Hayes 2016-12-12 21:10:09 +1300 1325)                'e' : (0.5, 0), 'ene' : (0.5, 0.25),
8379e461 (Michael Hayes 2016-12-12 21:10:09 +1300 1326)                'ne' : (0.5, 0.5), 'nne' : (0.25, 0.5),
8379e461 (Michael Hayes 2016-12-12 21:10:09 +1300 1327)                'n' : (0, 0.5), 'nnw' : (-0.25, 0.5),
23c940f8 (Michael Hayes 2017-12-03 09:16:14 +1300 1328)                'c' : (0.0, 0.0),
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1329)                'mid' : (0.0, 0.0)}
8b237a4b (Michael Hayes 2016-12-13 21:33:42 +1300 1330)     required_anchors = ('mid', )    
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1331) 
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1332) 
32c8c2e9 (Michael Hayes 2017-01-30 16:28:57 +1300 1333) class Ellipse(Shape):
32c8c2e9 (Michael Hayes 2017-01-30 16:28:57 +1300 1334)     """Ellipse"""
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1335) 
32c8c2e9 (Michael Hayes 2017-01-30 16:28:57 +1300 1336)     # Ellipse needs the tikz shapes library.
32c8c2e9 (Michael Hayes 2017-01-30 16:28:57 +1300 1337)     shape = 'ellipse'
8379e461 (Michael Hayes 2016-12-12 21:10:09 +1300 1338)     anchors = {'nw' : (-0.3536, 0.3536), 'wnw' : (-0.4619, 0.1913),
8379e461 (Michael Hayes 2016-12-12 21:10:09 +1300 1339)                'w' : (-0.5, 0), 'wsw' : (-0.4619, -0.1913), 
8379e461 (Michael Hayes 2016-12-12 21:10:09 +1300 1340)                'sw' : (-0.3536, -0.3536), 'ssw' : (-0.1913, -0.4619),
8379e461 (Michael Hayes 2016-12-12 21:10:09 +1300 1341)                's' : (0, -0.5), 'sse' : (0.1913, -0.4619),
8379e461 (Michael Hayes 2016-12-12 21:10:09 +1300 1342)                'se' : (0.3536, -0.3536), 'ese' : (0.4619, -0.1913),
8379e461 (Michael Hayes 2016-12-12 21:10:09 +1300 1343)                'e' : (0.5, 0), 'ene' : (0.4619, 0.1913),
8379e461 (Michael Hayes 2016-12-12 21:10:09 +1300 1344)                'ne' : (0.3536, 0.35365), 'nne' : (0.1913, 0.4619),
8379e461 (Michael Hayes 2016-12-12 21:10:09 +1300 1345)                'n' : (0, 0.5), 'nnw' : (-0.1913, 0.4619),
23c940f8 (Michael Hayes 2017-12-03 09:16:14 +1300 1346)                'c' : (0.0, 0.0),               
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1347)                'mid' : (0.0, 0.0)}
8b237a4b (Michael Hayes 2016-12-13 21:33:42 +1300 1348)     required_anchors = ('mid', )
14054b4d (Michael Hayes 2016-11-13 11:28:33 +1300 1349) 
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1350) 
32c8c2e9 (Michael Hayes 2017-01-30 16:28:57 +1300 1351) class Circle(Ellipse):
32c8c2e9 (Michael Hayes 2017-01-30 16:28:57 +1300 1352)     """Circle"""
32c8c2e9 (Michael Hayes 2017-01-30 16:28:57 +1300 1353) 
32c8c2e9 (Michael Hayes 2017-01-30 16:28:57 +1300 1354)     shape = 'circle'
32c8c2e9 (Michael Hayes 2017-01-30 16:28:57 +1300 1355) 
32c8c2e9 (Michael Hayes 2017-01-30 16:28:57 +1300 1356) 
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1357) class Circle2(Shape):
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1358)     """Circle"""
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1359) 
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1360)     shape = 'circle'
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1361) 
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1362)     @property
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1363)     def coords(self):
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1364)         return ((-0.5, 0), (0.5, 0))
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1365) 
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1366) 
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1367) class Circle4(Shape):
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1368)     """Circle4"""
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1369) 
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1370)     shape = 'circle'
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1371) 
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1372)     @property
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1373)     def coords(self):
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1374)         return ((-0.5, 0), (0, -0.5), (0.5, 0), (0, 0.5))
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1375) 
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1376) 
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1377) class Triangle(Shape):
32c8c2e9 (Michael Hayes 2017-01-30 16:28:57 +1300 1378)     """Equilateral triangle, The triangle shape can be altered by defining
97710898 (Michael Hayes 2017-08-03 13:47:53 +1200 1379)     aspect."""    
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1380) 
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1381)     shape = 'triangle'
c3543bb9 (Michael Hayes 2017-02-02 17:20:11 +1300 1382)     # 1 / sqrt(3) approx 0.5774, 1 / (2 * sqrt(3)) approx 0.2887
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1383)     anchors = {'c1' : (0.0, 0.5774),
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1384)                'c2' : (-0.5, -0.2887),
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1385)                'c3' : (0.5, -0.2887),
97710898 (Michael Hayes 2017-08-03 13:47:53 +1200 1386)                'n' : (0.0, 0.5774),
f420046a (Michael Hayes 2018-08-21 18:21:12 +1200 1387)                'ne' : (0.25, 0.14435),
f420046a (Michael Hayes 2018-08-21 18:21:12 +1200 1388)                'nw' : (-0.25, 0.14435),
97710898 (Michael Hayes 2017-08-03 13:47:53 +1200 1389)                'w' : (-0.5, -0.2887),
97710898 (Michael Hayes 2017-08-03 13:47:53 +1200 1390)                'e' : (0.5, -0.2887),
e7d00003 (Michael Hayes 2017-08-07 17:35:02 +1200 1391)                's' : (0.0, -0.2887),
f420046a (Michael Hayes 2018-08-21 18:21:12 +1200 1392)                'se' : (0.25, -0.2887),
f420046a (Michael Hayes 2018-08-21 18:21:12 +1200 1393)                'sw' : (-0.25, -0.2887),
f420046a (Michael Hayes 2018-08-21 18:21:12 +1200 1394)                'ssw' : (-0.125, -0.2887),
f420046a (Michael Hayes 2018-08-21 18:21:12 +1200 1395)                'sse' : (0.125, -0.2887),
f420046a (Michael Hayes 2018-08-21 18:21:12 +1200 1396)                'nne' : (0.125, 0.355),
f420046a (Michael Hayes 2018-08-21 18:21:12 +1200 1397)                'nnw' : (-0.125, 0.355),
f420046a (Michael Hayes 2018-08-21 18:21:12 +1200 1398)                'wsw' : (-0.375, -0.2887),
f420046a (Michael Hayes 2018-08-21 18:21:12 +1200 1399)                'ese' : (0.375, -0.2887),
f420046a (Michael Hayes 2018-08-21 18:21:12 +1200 1400)                'ene' : (0.375, -0.075),
f420046a (Michael Hayes 2018-08-21 18:21:12 +1200 1401)                'wnw' : (-0.375, -0.075),                              
23c940f8 (Michael Hayes 2017-12-03 09:16:14 +1300 1402)                'c' : (0.0, 0.0),               
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1403)                'mid' : (0.0, 0.0)}
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1404)     required_anchors = ('mid', 'c1', 'c2', 'c3')
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1405) 
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1406)     def draw(self, **kwargs):
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1407) 
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1408)         if not self.check():
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1409)             return ''
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1410) 
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1411)         s = self.draw_path([self.node('c1').pos, self.node('c2').pos,
e7d00003 (Michael Hayes 2017-08-07 17:35:02 +1200 1412)                             self.node('c3').pos], closed=True, style='thick')
97710898 (Michael Hayes 2017-08-03 13:47:53 +1200 1413)         s += self.draw_label(self.node('mid').pos, **kwargs)
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1414) 
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1415)         return s
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1416) 
680b2526 (Michael Hayes 2016-12-12 21:05:09 +1300 1417) class TR(Box2):
19b65731 (Michael Hayes 2016-03-28 23:02:59 +1300 1418)     """Transfer function"""
19b65731 (Michael Hayes 2016-03-28 23:02:59 +1300 1419) 
19b65731 (Michael Hayes 2016-03-28 23:02:59 +1300 1420)     default_width = 1.5
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1421)     default_aspect = 1.5
19b65731 (Michael Hayes 2016-03-28 23:02:59 +1300 1422) 
19b65731 (Michael Hayes 2016-03-28 23:02:59 +1300 1423) 
58b9f1a9 (Michael Hayes 2016-04-05 09:05:55 +1200 1424) class Chip(Shape):
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300 1425)     """General purpose chip"""
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300 1426) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1427)     default_width = 2.0
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1428) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1429)     # Could allow can_scale but not a lot of point since nodes
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1430)     # will not be on the boundary of the chip.
40de0a25 (Michael Hayes 2016-02-09 10:44:57 +1300 1431) 
05c73218 (Michael Hayes 2016-02-12 08:23:30 +1300 1432)     # TODO, tweak coord if pin name ends in \ using pinpos to
05c73218 (Michael Hayes 2016-02-12 08:23:30 +1300 1433)     # accomodate inverting circle.  This will require stripping of the
05c73218 (Michael Hayes 2016-02-12 08:23:30 +1300 1434)     # \ from the label. Alternatively, do not use inverting circle and
05c73218 (Michael Hayes 2016-02-12 08:23:30 +1300 1435)     # add overline to symbol name when printing.
05c73218 (Michael Hayes 2016-02-12 08:23:30 +1300 1436) 
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1437)     @property
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1438)     def path(self):
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1439)         return ((-0.5, 0.5), (0.5, 0.5), (0.5, -0.5), (-0.5, -0.5))
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1440) 
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1441)     def pinmap(self, pos):
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1442) 
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1443)         pinmap = ['l', 't', 'r', 'b']
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1444)         if pos not in pinmap:
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1445)             return pos
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1446)             
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1447)         index = pinmap.index(pos)
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1448)         angle = int(self.angle)
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1449)         if angle < 0:
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1450)             angle += 360
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1451) 
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1452)         angles = (0, 90, 180, 270)
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1453)         if angle not in angles:
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1454)             raise ValueError('Cannot rotate pinpos %s by %s' % (pos, self.angle))
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1455) 
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1456)         index += angles.index(angle)
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1457)         pos = pinmap[index % len(pinmap)]
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1458)         return pos
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1459) 
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200 1460)     def name_pins(self):
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300 1461) 
3bef8cdf (Michael Hayes 2016-03-29 14:39:42 +1300 1462)         pins = self.opts.get('pins', '')
3a7a7023 (Michael Hayes 2016-03-29 21:19:41 +1300 1463)         if pins != '' and pins != 'auto':
3bef8cdf (Michael Hayes 2016-03-29 14:39:42 +1300 1464)             if pins[0] != '{':
3bef8cdf (Michael Hayes 2016-03-29 14:39:42 +1300 1465)                 raise ValueError('Expecting { for pins in %s' % self)
3bef8cdf (Michael Hayes 2016-03-29 14:39:42 +1300 1466)             if pins[-1] != '}':
3bef8cdf (Michael Hayes 2016-03-29 14:39:42 +1300 1467)                 raise ValueError('Expecting } for pins in %s' % self)
3bef8cdf (Michael Hayes 2016-03-29 14:39:42 +1300 1468)             pins = pins[1:-1]
3bef8cdf (Michael Hayes 2016-03-29 14:39:42 +1300 1469)                 
3bef8cdf (Michael Hayes 2016-03-29 14:39:42 +1300 1470)             pins = pins.split(',')
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1471)             if len(pins) != len(self.nodes):
3bef8cdf (Michael Hayes 2016-03-29 14:39:42 +1300 1472)                 raise ValueError('Expecting %d pin names, got %s in %s' % (
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1473)                     len(self.nodes), len(pins), self))
3bef8cdf (Michael Hayes 2016-03-29 14:39:42 +1300 1474) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1475)         for m, n in enumerate(self.nodes):
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1476)             n.pinpos = self.pinmap(self.pinpos[m])
3a7a7023 (Michael Hayes 2016-03-29 21:19:41 +1300 1477)             label = ''
3a7a7023 (Michael Hayes 2016-03-29 21:19:41 +1300 1478)             if pins == 'auto':
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1479)                 label = n.name.split('.')[-1]
3bef8cdf (Michael Hayes 2016-03-29 14:39:42 +1300 1480)                 if label[0] == '_':
3bef8cdf (Michael Hayes 2016-03-29 14:39:42 +1300 1481)                     label = ''
3a7a7023 (Michael Hayes 2016-03-29 21:19:41 +1300 1482)             elif pins != '':
3a7a7023 (Michael Hayes 2016-03-29 21:19:41 +1300 1483)                 label = pins[m].strip()
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300 1484) 
2738ef50 (Michael Hayes 2016-04-04 20:00:04 +1200 1485)             n.clock = label != '' and label[0] == '>'
2738ef50 (Michael Hayes 2016-04-04 20:00:04 +1200 1486)             if n.clock:
2738ef50 (Michael Hayes 2016-04-04 20:00:04 +1200 1487)                 # Remove clock designator
2738ef50 (Michael Hayes 2016-04-04 20:00:04 +1200 1488)                 label = label[1:]
2738ef50 (Michael Hayes 2016-04-04 20:00:04 +1200 1489) 
2738ef50 (Michael Hayes 2016-04-04 20:00:04 +1200 1490)             n.label = label
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200 1491) 
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200 1492)     def draw(self, **kwargs):
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200 1493) 
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200 1494)         if not self.check():
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200 1495)             return ''
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200 1496) 
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200 1497)         self.name_pins()
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200 1498)             
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300 1499)         centre = self.centre
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1500)         q = self.tf(centre, self.path)
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300 1501) 
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1502)         s = self.draw_path(q, closed=True, style='thick')
1839042c (Michael Hayes 2016-03-27 10:28:02 +1300 1503)         s += r'  \draw (%s) node[text width=%scm, align=center, %s] {%s};''\n'% (
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1504)             centre, self.width - 0.5, self.args_str, self.label(**kwargs))
2738ef50 (Michael Hayes 2016-04-04 20:00:04 +1200 1505) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1506)         for m, n in enumerate(self.nodes):
2738ef50 (Michael Hayes 2016-04-04 20:00:04 +1200 1507)             if n.clock:
2738ef50 (Michael Hayes 2016-04-04 20:00:04 +1200 1508)                 # TODO, tweak for pinpos
b4242fd1 (Michael Hayes 2016-04-14 08:50:21 +1200 1509)                 q = self.tf(n.pos, ((0, 0.125 * 0.707), (0.125, 0), 
b4242fd1 (Michael Hayes 2016-04-14 08:50:21 +1200 1510)                                     (0, -0.125 * 0.707)))
2738ef50 (Michael Hayes 2016-04-04 20:00:04 +1200 1511)                 s += self.draw_path(q[0:3], style='thick')
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1512)                 
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300 1513)         return s
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300 1514) 
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300 1515) 
705155bc (Michael Hayes 2016-04-04 15:20:26 +1200 1516) class Uchip1310(Chip):
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300 1517)     """Chip of size 1 3 1 0"""
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300 1518) 
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1519)     default_aspect = 4.0 / 3.0
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300 1520)     pinpos = ('l', 'b', 'b', 'b', 'r')
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300 1521) 
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300 1522)     @property
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300 1523)     def centre(self):
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1524)         return self.midpoint(self.nodes[0], self.nodes[4])
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300 1525) 
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300 1526)     @property
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300 1527)     def coords(self):
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1528)         return ((0, 0), (0.25, -0.5), (0.5, -0.5), (0.75, -0.5), (1, 0))
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300 1529) 
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300 1530) 
705155bc (Michael Hayes 2016-04-04 15:20:26 +1200 1531) class Uchip2121(Chip):
0c5ea67d (Michael Hayes 2016-02-05 14:01:55 +1300 1532)     """Chip of size 2 1 2 1"""
0c5ea67d (Michael Hayes 2016-02-05 14:01:55 +1300 1533) 
0c5ea67d (Michael Hayes 2016-02-05 14:01:55 +1300 1534)     pinpos = ('l', 'l', 'b', 'r', 'r', 't')
0c5ea67d (Michael Hayes 2016-02-05 14:01:55 +1300 1535) 
0c5ea67d (Michael Hayes 2016-02-05 14:01:55 +1300 1536)     @property
0c5ea67d (Michael Hayes 2016-02-05 14:01:55 +1300 1537)     def coords(self):
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1538)         return ((0, 0.25), (0, -0.25),
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1539)                 (0.5, -0.5), 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1540)                 (1.0, -0.25), (1.0, 0.25),
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1541)                 (0.5, 0.5))
4a19b985 (Michael Hayes 2016-02-05 15:19:05 +1300 1542) 
4a19b985 (Michael Hayes 2016-02-05 15:19:05 +1300 1543) 
705155bc (Michael Hayes 2016-04-04 15:20:26 +1200 1544) class Uchip3131(Chip):
4a19b985 (Michael Hayes 2016-02-05 15:19:05 +1300 1545)     """Chip of size 3 1 3 1"""
4a19b985 (Michael Hayes 2016-02-05 15:19:05 +1300 1546) 
705155bc (Michael Hayes 2016-04-04 15:20:26 +1200 1547)     pinpos = ('l', 'l', 'l', 'b', 'r', 'r', 'r', 't')
705155bc (Michael Hayes 2016-04-04 15:20:26 +1200 1548) 
705155bc (Michael Hayes 2016-04-04 15:20:26 +1200 1549)     @property
705155bc (Michael Hayes 2016-04-04 15:20:26 +1200 1550)     def coords(self):
bdc78606 (Michael Hayes 2017-08-12 18:51:43 +1200 1551)         return ((-0.5, 0.25), (-0.5, 0), (-0.5, -0.25), (0.0, -0.375), 
bdc78606 (Michael Hayes 2017-08-12 18:51:43 +1200 1552)                 (0.5, -0.25), (0.5, 0), (0.5, 0.25), (0.0, 0.375))
705155bc (Michael Hayes 2016-04-04 15:20:26 +1200 1553) 
b4242fd1 (Michael Hayes 2016-04-14 08:50:21 +1200 1554)     @property
b4242fd1 (Michael Hayes 2016-04-14 08:50:21 +1200 1555)     def path(self):
b4242fd1 (Michael Hayes 2016-04-14 08:50:21 +1200 1556)         return ((-0.5, 0.375), (0.5, 0.375), (0.5, -0.375), (-0.5, -0.375))
b4242fd1 (Michael Hayes 2016-04-14 08:50:21 +1200 1557) 
705155bc (Michael Hayes 2016-04-04 15:20:26 +1200 1558) 
705155bc (Michael Hayes 2016-04-04 15:20:26 +1200 1559) class Uchip4141(Chip):
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300 1560)     """Chip of size 4 1 4 1"""
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300 1561) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1562)     default_width = 2
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1563)     default_aspect = 0.5
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300 1564)     pinpos = ('l', 'l', 'l', 'l', 'b', 'r', 'r', 'r', 'r', 't')
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300 1565) 
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300 1566)     @property
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300 1567)     def coords(self):
15d67942 (Michael Hayes 2016-04-08 22:39:47 +1200 1568)         return ((-0.5, 0.375), (-0.5, 0.125), (-0.5, -0.125), (-0.5, -0.375),
15d67942 (Michael Hayes 2016-04-08 22:39:47 +1200 1569)                 (0.0, -0.5), 
15d67942 (Michael Hayes 2016-04-08 22:39:47 +1200 1570)                 (0.5, -0.375), (0.5, -0.125), (0.5, 0.125), (0.5, 0.375),
15d67942 (Michael Hayes 2016-04-08 22:39:47 +1200 1571)                 (0, 0.5))
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300 1572) 
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300 1573) 
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1574) class Uadc(Chip):
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1575)     """ADC"""
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1576) 
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1577)     # in, vref, vss, clk, data, fs, vdd, vref
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1578)     pinpos = ('l', 'b', 'b', 'r', 'r', 'r', 't', 't')
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1579) 
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1580)     @property
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1581)     def coords(self):
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1582)         return ((0, 0.0), (0.5, -0.5), (0.75, -0.5), 
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1583)                 (1.0, -0.25), (1.0, 0), (1.0, 0.25), (0.75, 0.5), (0.5, 0.5))
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1584) 
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1585)     @property
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1586)     def path(self):
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1587)         return ((-0.5, 0.0), (-0.25, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.25, 0.5))
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1588) 
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1589)     @property
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1590)     def centre(self):
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1591)         return self.midpoint(self.nodes[0], self.nodes[4])
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1592) 
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1593) 
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1594) class Udac(Chip):
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1595)     """DAC"""
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1596) 
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1597)     # fs, data, clk, vss, out, vdd, vref
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1598)     pinpos = ('l', 'l', 'l', 'b', 'b', 'r', 't', 't')
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1599) 
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1600)     @property
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1601)     def coords(self):
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1602)         return ((0, 0.25), (0, 0), (0, -0.25), (0.25, -0.5), (0.5, -0.5),
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1603)                 (1.0, 0), (0.5, 0.5), (0.25, 0.5))
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1604) 
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1605)     @property
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1606)     def path(self):
8d9c91a3 (Michael Hayes 2016-04-08 21:24:09 +1200 1607)         return ((-0.5, -0.5), (0.25, -0.5), (0.5, 0), (0.25, 0.5), (-0.5, 0.5))
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1608) 
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1609)     @property
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1610)     def centre(self):
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1611)         return self.midpoint(self.nodes[1], self.nodes[5])
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1612) 
eaca488b (Michael Hayes 2016-04-08 15:08:51 +1200 1613) 
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1614) class Udiffamp(Chip):
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1615)     """Amplifier"""
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1616) 
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1617)     default_width = 1.0
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1618)     pinpos = ('l', 'l', 'b', 'r', 't')
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1619) 
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1620)     @property
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1621)     def coords(self):
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1622)         return ((-0.5, 0.25), (-0.5, -0.25), (0.0, -0.25), (0.5, 0), (0.0, 0.25))
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1623) 
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1624)     @property
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1625)     def path(self):
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1626)         return ((-0.5, 0.5), (-0.5, -0.5), (0.5, 0))
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1627) 
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1628)     @property
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1629)     def centre(self):
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1630)         n1, n2, n3, n4, n5 = self.nodes
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1631)         return (n1.pos + n2.pos) * 0.25 + n4.pos * 0.5
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1632) 
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1633) 
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1634) class Ubuffer(Chip):
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1635)     """Buffer with power supplies"""
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1636) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1637)     default_width = 1.0
cd2efbf2 (Michael Hayes 2016-03-07 23:02:37 +1300 1638)     pinpos = ('l', 'b', 'r', 't')
cd2efbf2 (Michael Hayes 2016-03-07 23:02:37 +1300 1639) 
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1640)     @property
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1641)     def coords(self):
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1642)         return ((0, 0), (0.5, -0.25), (1.0, 0), (0.5, 0.25))
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1643) 
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1644)     @property
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1645)     def path(self):
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1646)         return ((-0.5, 0.5), (0.5, 0), (-0.5, -0.5))
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1647) 
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1648)     def draw(self, **kwargs):
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1649) 
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1650)         if not self.check():
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1651)             return ''
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1652) 
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200 1653)         self.name_pins()
cd2efbf2 (Michael Hayes 2016-03-07 23:02:37 +1300 1654) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1655)         n1, n2, n3, n4 = self.nodes
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300 1656)         centre = (n1.pos + n3.pos) * 0.5
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1657) 
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1658)         q = self.tf(centre, self.path)
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200 1659)         s = self.draw_path(q[0:3], closed=True, style='thick')
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1660)         s += self.draw_label(centre, **kwargs)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1661)         s += self.draw_nodes(**kwargs)
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1662)         return s
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1663) 
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200 1664) 
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1665) class Uinverter(Chip):
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1666)     """Inverter with power supplies"""
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1667) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1668)     default_width = 1.0
cd2efbf2 (Michael Hayes 2016-03-07 23:02:37 +1300 1669)     pinpos = ('l', 'b', 'r', 't')
cd2efbf2 (Michael Hayes 2016-03-07 23:02:37 +1300 1670) 
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1671)     @property
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1672)     def coords(self):
cd2efbf2 (Michael Hayes 2016-03-07 23:02:37 +1300 1673)         return ((0, 0), (0.5, -0.22), (1.0, 0), (0.5, 0.22))
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1674) 
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1675)     @property
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1676)     def path(self):
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1677)         w = 0.05
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1678)         return ((-0.5, 0.5), (0.5 -2 * w, 0), (-0.5, -0.5), (0.5 - w, 0))
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1679) 
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1680)     def draw(self, **kwargs):
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1681) 
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1682)         if not self.check():
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1683)             return ''
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1684) 
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200 1685)         self.name_pins()
cd2efbf2 (Michael Hayes 2016-03-07 23:02:37 +1300 1686) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1687)         n1, n2, n3, n4 = self.nodes
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300 1688)         centre = (n1.pos + n3.pos) * 0.5
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1689) 
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1690)         q = self.tf(centre, self.path)
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200 1691)         s = self.draw_path(q[0:3], closed=True, style='thick')
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1692)         s += r'  \draw[thick] (%s) node[ocirc, scale=%s] {};''\n' % (
40b7e038 (Michael Hayes 2016-04-08 22:21:15 +1200 1693)             q[3], 1.8 * self.size * self.scale)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1694)         s += self.draw_label(centre, **kwargs)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1695)         s += self.draw_nodes(**kwargs)
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1696)         return s
b7339475 (Michael Hayes 2016-02-05 09:54:21 +1300 1697) 
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200 1698) 
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1699) class Wire(OnePort):
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1700) 
a3b74280 (Michael Hayes 2016-03-26 23:35:10 +1300 1701)     def __init__(self, sch, name, cpt_type, cpt_id, string,
ad105941 (Michael Hayes 2017-01-21 21:57:32 +1300 1702)                  opts_string, node_names, keyword, *args):
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300 1703) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1704)         implicit = False
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1705)         for key in self.implicit_keys:
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1706)             if key in opts_string:
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1707)                 implicit = True
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1708)                 break
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300 1709) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1710)         if implicit:
edd24fe5 (Michael Hayes 2016-02-05 23:46:28 +1300 1711)             # Rename second node since this is spatially different from
ff20231e (Michael Hayes 2016-02-07 09:42:44 +1300 1712)             # other nodes of the same name.  Add underscore so node
ff20231e (Michael Hayes 2016-02-07 09:42:44 +1300 1713)             # not drawn.
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1714)             node_names = (node_names[0], name + '@_' + node_names[1])
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1715)         
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1716)         super (Wire, self).__init__(sch, name, cpt_type, cpt_id, string,
ad105941 (Michael Hayes 2017-01-21 21:57:32 +1300 1717)                                     opts_string, node_names, keyword, *args)
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1718)         self.implicit = implicit
e2538348 (Michael Hayes 2016-01-31 00:09:09 +1300 1719) 
e2538348 (Michael Hayes 2016-01-31 00:09:09 +1300 1720)     @property
e95aaee1 (Michael Hayes 2016-01-05 12:05:54 +1300 1721)     def coords(self):
e95aaee1 (Michael Hayes 2016-01-05 12:05:54 +1300 1722)         return ((0, 0), (1, 0))
e95aaee1 (Michael Hayes 2016-01-05 12:05:54 +1300 1723) 
5ad52862 (Michael Hayes 2016-01-07 12:53:31 +1300 1724)     def draw_implicit(self, **kwargs):
c3062cd9 (Michael Hayes 2017-03-23 21:54:34 +1300 1725)         """Draw implicit wires, i.e., connections to ground, etc."""
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1726) 
ba5b24f0 (Michael Hayes 2016-01-31 00:12:51 +1300 1727)         kind = None
ba5b24f0 (Michael Hayes 2016-01-31 00:12:51 +1300 1728)         for key in self.implicit_keys:
ba5b24f0 (Michael Hayes 2016-01-31 00:12:51 +1300 1729)             if key in self.opts:
ba5b24f0 (Michael Hayes 2016-01-31 00:12:51 +1300 1730)                 kind = key
ba5b24f0 (Michael Hayes 2016-01-31 00:12:51 +1300 1731)                 break;
ba5b24f0 (Michael Hayes 2016-01-31 00:12:51 +1300 1732) 
e2538348 (Michael Hayes 2016-01-31 00:09:09 +1300 1733)         # I like the sground symbol for power supplies but rground symbol
e2538348 (Michael Hayes 2016-01-31 00:09:09 +1300 1734)         # is also common.
c3062cd9 (Michael Hayes 2017-03-23 21:54:34 +1300 1735)         if (kind is None) or (kind == 'implicit'):
ba5b24f0 (Michael Hayes 2016-01-31 00:12:51 +1300 1736)             kind = 'sground'
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1737)         anchor = 'south west'
81f59d54 (Michael Hayes 2016-01-04 12:43:26 +1300 1738)         if self.down:
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1739)             anchor = 'north west'
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1740) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1741)         n1, n2 = self.nodes
c3062cd9 (Michael Hayes 2017-03-23 21:54:34 +1300 1742)         s = self.draw_path((n1.s, n2.s))
c3062cd9 (Michael Hayes 2017-03-23 21:54:34 +1300 1743)         s += r'  \draw (%s) node[%s, scale=0.5, rotate=%d] {};''\n' % (
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300 1744)             n2.s, kind, self.angle + 90)
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1745) 
8ae6d8c0 (Michael Hayes 2016-01-02 23:37:54 +1300 1746)         if 'l' in self.opts:
48d76392 (Michael Hayes 2016-04-06 09:09:27 +1200 1747)             lpos = self.tf(n2.pos, (0.125, 0))
cc22aab4 (Michael Hayes 2016-01-27 17:11:35 +1300 1748)             s += r'  \draw [anchor=%s] (%s) node {%s};''\n' % (
577895d5 (Michael Hayes 2016-01-25 16:29:50 +1300 1749)                 anchor, lpos, self.label(**kwargs))
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1750)         return s
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1751) 
5ad52862 (Michael Hayes 2016-01-07 12:53:31 +1300 1752)     def draw(self, **kwargs):
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1753) 
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300 1754)         if not self.check():
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300 1755)             return ''
465a2e97 (Michael Hayes 2016-01-30 17:51:33 +1300 1756) 
e2538348 (Michael Hayes 2016-01-31 00:09:09 +1300 1757)         if self.implicit:
5ad52862 (Michael Hayes 2016-01-07 12:53:31 +1300 1758)             return self.draw_implicit(**kwargs)
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1759)             
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1760)         def arrow_map(name):
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1761) 
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1762)             try:
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1763)                 return {'tee': '|', 'otri' : 'open triangle 60',
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1764)                         'tri' : 'triangle 60'}[name]
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1765)             except:
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1766)                 return name
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1767) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1768)         n1, n2 = self.nodes
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1769) 
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1770)         # W 1 2; up, arrow=tri, l=V_{dd}
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1771)         # W 1 3; right, arrow=otri
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1772)         # W 1 4; down, arrow=tee, l=0V
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1773)         # W 1 5; left, startarrow=tri, endarrow=open triangle 90, bus=8
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1774) 
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1775)         startarrow = self.opts.pop('startarrow', '')
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1776)         endarrow = self.opts.pop('arrow', '')
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1777)         endarrow = self.opts.pop('endarrow', endarrow)
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1778) 
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1779)         bus = self.opts.pop('bus', False)
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1780)         style = ''
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1781)         if bus:
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1782)             # TODO if bus has numeric arg, indicate number of lines with slash.
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1783)             style = 'ultra thick'
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1784) 
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1785)         # TODO, add arrow shapes for earth symbol.
c04e028c (Michael Hayes 2016-03-07 22:32:33 +1300 1786) 
8c071858 (Michael Hayes 2016-03-07 23:05:54 +1300 1787)         s = r'  \draw[%s-%s, %s, %s] (%s) to (%s);''\n' % (
7577c358 (Michael Hayes 2016-03-19 22:20:32 +1300 1788)             arrow_map(startarrow), arrow_map(endarrow), style,
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300 1789)             self.args_str, n1.s, n2.s)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1790)         s += self.draw_nodes(**kwargs)
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1791) 
7577c358 (Michael Hayes 2016-03-19 22:20:32 +1300 1792)         if self.voltage_str != '':
7577c358 (Michael Hayes 2016-03-19 22:20:32 +1300 1793)             print('There is no voltage drop across an ideal wire!')
7577c358 (Michael Hayes 2016-03-19 22:20:32 +1300 1794) 
874f6eb8 (Michael Hayes 2016-10-04 08:11:08 +1300 1795)         if self.current_str != '' or self.label_str != '':
7577c358 (Michael Hayes 2016-03-19 22:20:32 +1300 1796)             # FIXME, we don't really want the wire drawn since this
7577c358 (Michael Hayes 2016-03-19 22:20:32 +1300 1797)             # can clobber the arrow.  We just want the current
d866a23e (Michael Hayes 2016-03-21 20:34:15 +1300 1798)             # annotation and/or the label.
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300 1799) 
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300 1800)             # To handle multiple labels, we need to draw separate wires.
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300 1801)             for label_str in self.label_str_list:
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300 1802)                 s += r'  \draw[%s] (%s) [short, %s, %s] to (%s);''\n' % (
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300 1803)                     self.args_str, n1.s, self.current_str, label_str, n2.s)
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300 1804)             if self.label_str_list == []:
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300 1805)                 s += r'  \draw[%s] (%s) [short, %s] to (%s);''\n' % (
896dca89 (Michael Hayes 2016-10-04 11:52:12 +1300 1806)                     self.args_str, n1.s, self.current_str, n2.s)
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1807)         return s
2496cbd5 (Michael Hayes 2016-03-06 22:04:42 +1300 1808) 
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1809) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1810) class FB(StretchyCpt):
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1811)     """Ferrite bead"""
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1812) 
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1813)     can_scale = True
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1814) 
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1815)     @property
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1816)     def coords(self):
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1817)         return ((-0.5, 0), (0.5, 0))
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1818) 
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1819)     def draw(self, **kwargs):
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1820) 
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1821)         if not self.check():
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1822)             return ''
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1823) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1824)         n1, n2 = self.nodes
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1825) 
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1826)         centre = (n1.pos + n2.pos) * 0.5
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1827)         w = 0.125
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1828)         h = 0.4
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1829)         
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1830)         q = self.tf(centre, ((-0.5 * w, -0.5 * h), (-0.5 * w, 0.5 * h),
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1831)                              (0.5 * w, 0.5 * h), (0.5 * w, -0.5 * h),
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1832)                              (0, h)), -30)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1833)         q2 = self.tf(centre, ((-0.53 * w, 0), (0.53 * w, 0), (0, h)))
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1834) 
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200 1835)         s = self.draw_path(q[0:4], closed=True, style='thick')
77ce381c (Michael Hayes 2016-04-04 08:48:35 +1200 1836)         s += self.draw_path((n1.s, q2[0]))
77ce381c (Michael Hayes 2016-04-04 08:48:35 +1200 1837)         s += self.draw_path((q2[1], n2.s))
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1838)         s += self.draw_label(q[4], **kwargs)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1839)         s += self.draw_nodes(**kwargs)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1840)         return s
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1841) 
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1842) 
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1843) class XT(StretchyCpt):
4b480c5b (Michael Hayes 2016-01-31 17:51:51 +1300 1844)     """Crystal"""
4b480c5b (Michael Hayes 2016-01-31 17:51:51 +1300 1845) 
4b480c5b (Michael Hayes 2016-01-31 17:51:51 +1300 1846)     can_scale = True
4b480c5b (Michael Hayes 2016-01-31 17:51:51 +1300 1847) 
4b480c5b (Michael Hayes 2016-01-31 17:51:51 +1300 1848)     @property
4b480c5b (Michael Hayes 2016-01-31 17:51:51 +1300 1849)     def coords(self):
4b480c5b (Michael Hayes 2016-01-31 17:51:51 +1300 1850)         return ((-0.5, 0), (0.5, 0))
4b480c5b (Michael Hayes 2016-01-31 17:51:51 +1300 1851) 
4b480c5b (Michael Hayes 2016-01-31 17:51:51 +1300 1852)     def draw(self, **kwargs):
4b480c5b (Michael Hayes 2016-01-31 17:51:51 +1300 1853) 
4b480c5b (Michael Hayes 2016-01-31 17:51:51 +1300 1854)         if not self.check():
4b480c5b (Michael Hayes 2016-01-31 17:51:51 +1300 1855)             return ''
4b480c5b (Michael Hayes 2016-01-31 17:51:51 +1300 1856) 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1857)         n1, n2 = self.nodes
4b480c5b (Michael Hayes 2016-01-31 17:51:51 +1300 1858) 
51e479a1 (Michael Hayes 2016-03-24 11:13:19 +1300 1859)         centre = (n1.pos + n2.pos) * 0.5
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1860)         q = self.tf(centre, ((-0.15, 0), (-0.15, 0.15), (-0.15, -0.15),
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1861)                              (0.15, 0), (0.15, 0.15), (0.15, -0.15),
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1862)                              (-0.06, 0.15), (0.06, 0.15),
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1863)                              (0.06, -0.15), (-0.06, -0.15),
ee9a8970 (Michael Hayes 2016-04-05 23:01:42 +1200 1864)                              (0.0, -0.3)))
4b480c5b (Michael Hayes 2016-01-31 17:51:51 +1300 1865) 
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1866)         s = self.draw_path((q[1], q[2]), style='thick')
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1867)         s += self.draw_path((q[4], q[5]), style='thick')
7fb94a5c (Michael Hayes 2016-04-04 11:08:01 +1200 1868)         s += self.draw_path(q[6:10], closed=True, style='thick')
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1869)         s += self.draw_path((q[0], n1.s), style='thick')
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1870)         s += self.draw_path((q[3], n2.s), style='thick')
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1871)         s += self.draw_label(q[10], **kwargs)
ef82ed99 (Michael Hayes 2016-04-03 20:54:45 +1200 1872)         s += self.draw_nodes(**kwargs)
4b480c5b (Michael Hayes 2016-01-31 17:51:51 +1300 1873)         return s
4b480c5b (Michael Hayes 2016-01-31 17:51:51 +1300 1874) 
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1875) 
e5a76352 (Michael Hayes 2016-01-02 13:45:21 +1300 1876) classes = {}
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1877) 
43739ecb (Michael Hayes 2016-01-04 14:48:02 +1300 1878) def defcpt(name, base, docstring, cpt=None):
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1879)     
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1880)     if isinstance(base, str):
e5a76352 (Michael Hayes 2016-01-02 13:45:21 +1300 1881)         base = classes[base]
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1882) 
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1883)     newclass = type(name, (base, ), {'__doc__': docstring})
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1884) 
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1885)     if cpt is not None:
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1886)         newclass.tikz_cpt = cpt
e5a76352 (Michael Hayes 2016-01-02 13:45:21 +1300 1887)     classes[name] = newclass
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1888) 
e95aaee1 (Michael Hayes 2016-01-05 12:05:54 +1300 1889) 
a3b74280 (Michael Hayes 2016-03-26 23:35:10 +1300 1890) def make(classname, parent, name, cpt_type, cpt_id,
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1891)          string, opts_string, node_names, *args):
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300 1892) 
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300 1893)     # Create instance of component object
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300 1894)     try:
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300 1895)         newclass = getattr(module, classname)
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300 1896)     except:
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300 1897)         newclass = classes[classname]
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300 1898) 
a3b74280 (Michael Hayes 2016-03-26 23:35:10 +1300 1899)     cpt = newclass(parent, name, cpt_type, cpt_id, string, opts_string, 
510fd9fd (Michael Hayes 2016-12-13 16:51:57 +1300 1900)                    node_names, *args)
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300 1901)     # Add named attributes for the args?   Lname1, etc.
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300 1902)         
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300 1903)     return cpt
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300 1904) 
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1905) # Dynamically create classes.
c35cf09a (Michael Hayes 2016-03-17 08:00:39 +1300 1906) defcpt('AM', OnePort, 'Ammeter', 'ammeter')
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1907) 
825571af (Michael Hayes 2016-03-17 08:25:32 +1300 1908) defcpt('BAT', OnePort, 'Battery', 'battery')
825571af (Michael Hayes 2016-03-17 08:25:32 +1300 1909) 
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1910) defcpt('C', OnePort, 'Capacitor', 'C')
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1911) 
59e9da13 (Michael Hayes 2016-01-03 21:10:04 +1300 1912) defcpt('D', OnePort, 'Diode', 'D')
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1913) defcpt('Dled', 'D', 'LED', 'leD')
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1914) defcpt('Dphoto', 'D', 'Photo diode', 'pD')
4a80c6b1 (Michael Hayes 2016-01-03 21:12:11 +1300 1915) defcpt('Dschottky', 'D', 'Schottky diode', 'zD')
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1916) defcpt('Dtunnel', 'D', 'Tunnel diode', 'tD')
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1917) defcpt('Dzener', 'D', 'Zener diode', 'zD')
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1918) 
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1919) defcpt('E', VCS, 'VCVS', 'american controlled voltage source')
f3ac4194 (Michael Hayes 2016-01-04 11:30:23 +1300 1920) defcpt('Eopamp', Opamp, 'Opamp')
f3ac4194 (Michael Hayes 2016-01-04 11:30:23 +1300 1921) defcpt('Efdopamp', FDOpamp, 'Fully differential opamp')
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300 1922) defcpt('F', VCS, 'CCCS', 'american controlled current source')
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300 1923) defcpt('G', CCS, 'VCCS', 'american controlled current source')
7b092de6 (Michael Hayes 2016-01-08 17:33:17 +1300 1924) defcpt('H', CCS, 'CCVS', 'american controlled voltage source')
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1925) 
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300 1926) defcpt('GY', Gyrator, 'Gyrator', 'gyrator')
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300 1927) 
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1928) defcpt('I', OnePort, 'Current source', 'I')
f2297edf (Michael Hayes 2016-01-09 13:19:39 +1300 1929) defcpt('sI', OnePort, 'Current source', 'I')
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1930) defcpt('Isin', 'I', 'Sinusoidal current source', 'sI')
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1931) defcpt('Idc', 'I', 'DC current source', 'I')
11cae929 (Michael Hayes 2016-10-23 19:28:30 +1300 1932) defcpt('Istep', 'I', 'Step current source', 'I')
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1933) defcpt('Iac', 'I', 'AC current source', 'sI')
abbcea01 (Michael Hayes 2016-12-22 21:57:39 +1300 1934) defcpt('Inoise', 'I', 'Noise current source', 'sI')
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1935) 
43739ecb (Michael Hayes 2016-01-04 14:48:02 +1300 1936) defcpt('J', JFET, 'N JFET transistor', 'njfet')
3652143d (Michael Hayes 2016-01-03 23:57:47 +1300 1937) defcpt('Jnjf', 'J', 'N JFET transistor', 'njfet')
43739ecb (Michael Hayes 2016-01-04 14:48:02 +1300 1938) defcpt('Jpjf', 'J', 'P JFET transistor', 'pjfet')
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1939) 
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1940) defcpt('L', OnePort, 'Inductor', 'L')
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1941) 
e5bf56bd (Michael Hayes 2016-01-04 15:11:14 +1300 1942) defcpt('M', MOSFET, 'N MOSJFET transistor', 'nmos')
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1943) defcpt('Mnmos', 'M', 'N channel MOSJFET transistor', 'nmos')
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1944) defcpt('Mpmos', 'M', 'P channel MOSJFET transistor', 'pmos')
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1945) 
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1946) defcpt('O', OnePort, 'Open circuit', 'open')
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1947) defcpt('P', OnePort, 'Port', 'open')
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1948) 
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1949) defcpt('Q', Transistor, 'NPN transistor', 'npn')
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1950) defcpt('Qpnp', 'Q', 'PNP transistor', 'pnp')
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1951) defcpt('Qnpn', 'Q', 'NPN transistor', 'npn')
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1952) 
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1953) defcpt('R', OnePort, 'Resistor', 'R')
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1954) 
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1955) defcpt('Sbox', Box, 'Box shape')
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1956) defcpt('Scircle', Circle, 'Circle shape')
32c8c2e9 (Michael Hayes 2017-01-30 16:28:57 +1300 1957) defcpt('Sellipse', Ellipse, 'Ellipse shape')
53b708eb (Michael Hayes 2017-01-30 14:08:47 +1300 1958) defcpt('Striangle', Triangle, 'Triangle shape')
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1959) 
3e2c3bd9 (Michael Hayes 2016-01-26 11:30:27 +1300 1960) defcpt('SW', OnePort, 'Switch', 'closing switch')
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1961) defcpt('SWno', 'SW', 'Normally open switch', 'closing switch')
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1962) defcpt('SWnc', 'SW', 'Normally closed switch', 'opening switch')
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1963) defcpt('SWpush', 'SW', 'Pushbutton switch', 'push button')
a91378a1 (Michael Hayes 2016-01-26 09:26:59 +1300 1964) defcpt('SWspdt', SPDT, 'SPDT switch', 'spdt')
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1965) 
b1f075e8 (Michael Hayes 2018-03-06 08:49:53 +1300 1966) defcpt('TF', Transformer, 'Transformer', 'ideal transformer')
62640edd (Michael Hayes 2016-03-16 23:05:45 +1300 1967) defcpt('TFcore', Transformer, 'Transformer with core', 'transformer core')
f0791e8a (Michael Hayes 2016-03-17 11:40:04 +1300 1968) defcpt('TFtapcore', TFtap, 'Tapped transformer with core', 'transformer core')
7244ad0b (Michael Hayes 2016-01-03 22:20:08 +1300 1969) defcpt('TP', TwoPort, 'Two port', '')
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1970) 
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1971) defcpt('Ubox', Box2, 'Box')
021b3fc4 (Michael Hayes 2016-11-08 14:49:46 +1300 1972) defcpt('Ucircle', Circle2, 'Circle')
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1973) defcpt('Ubox4', Box4, 'Box')
1e62920b (Michael Hayes 2016-10-04 11:37:50 +1300 1974) defcpt('Ubox12', Box12, 'Box')
b1a63bb4 (Michael Hayes 2016-03-27 20:45:40 +1300 1975) defcpt('Ucircle4', Circle4, 'Circle')
705155bc (Michael Hayes 2016-04-04 15:20:26 +1200 1976) 
3e2c3bd9 (Michael Hayes 2016-01-26 11:30:27 +1300 1977) 
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1978) defcpt('V', OnePort, 'Voltage source', 'V')
f2297edf (Michael Hayes 2016-01-09 13:19:39 +1300 1979) defcpt('sV', OnePort, 'Voltage source', 'V')
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1980) defcpt('Vsin', 'V', 'Sinusoidal voltage source', 'sV')
362c1d5c (Michael Hayes 2016-01-01 19:55:59 +1300 1981) defcpt('Vdc', 'V', 'DC voltage source', 'V')
345f48f5 (Michael Hayes 2016-01-05 16:57:51 +1300 1982) defcpt('Vstep', 'V', 'Step voltage source', 'V')
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1983) defcpt('Vac', 'V', 'AC voltage source', 'sV')
abbcea01 (Michael Hayes 2016-12-22 21:57:39 +1300 1984) defcpt('Vnoise', 'V', 'Noise voltage source', 'sV')
10627a7e (Michael Hayes 2015-12-28 17:34:16 +1300 1985) 
c35cf09a (Michael Hayes 2016-03-17 08:00:39 +1300 1986) defcpt('VM', OnePort, 'Voltmeter', 'voltmeter')
c35cf09a (Michael Hayes 2016-03-17 08:00:39 +1300 1987) 
e95aaee1 (Michael Hayes 2016-01-05 12:05:54 +1300 1988) defcpt('W', Wire, 'Wire', 'short')
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1989) defcpt('Y', OnePort, 'Admittance', 'european resistor')
cbcd7bc2 (Michael Hayes 2016-01-02 17:17:48 +1300 1990) defcpt('Z', OnePort, 'Impedance', 'european resistor')
99b96e87 (Michael Hayes 2015-12-28 18:09:30 +1300 1991) 
99b96e87 (Michael Hayes 2015-12-28 18:09:30 +1300 1992) # Perhaps AM for ammeter, VM for voltmeter, VR for variable resistor?
99b96e87 (Michael Hayes 2015-12-28 18:09:30 +1300 1993) # Currently, a variable resistor is supported with the variable
99b96e87 (Michael Hayes 2015-12-28 18:09:30 +1300 1994) # option.
