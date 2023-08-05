from lcapy.schematic import Schematic
sch = Schematic()
sch.add('V1 1 2 dc 1; down')
sch.add('R1 1 3; right')
sch.draw()

# horiz  cnodes 1:2 3:1 2:2  i.e. nodes 1, 2 have the same x value
