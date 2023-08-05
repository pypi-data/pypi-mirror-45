from __future__ import print_function
import numpy as np
import re
from lcapy.latex import latex_str
from os import system, path, remove, mkdir, chdir, getcwd
from schemcpts import make_cpt
from schemmisc import *
import math

__all__ = ('Schematic', )


class SchematicOpts(Opts):

    def __init__(self):

        super (SchematicOpts, self).__init__(
            {'draw_nodes': 'primary',
             'label_values': True,
             'label_ids': True,
             'label_nodes': 'primary',
             'scale' : 1,
             'stretch' : 1,
             'style' : 'american'})


class Node(object):

    def __init__(self, name):

        self.name = name
        self._port = False
        self._count = 0
        parts = name.split('_')
        self.rootname = parts[0] if name[0] != '_' else name
        self.primary = len(parts) == 1
        self.list = []

    def append(self, elt):
        """Add new element to the node"""

        if isinstance(elt, Port):
            self._port = True

        self.list.append(elt)
        if not isinstance(elt, Open):
            self._count += 1

    @property
    def count(self):
        """Number of elements (including wires but not open-circuits)
        connected to the node"""

        return self._count

    def visible(self, draw_nodes):
        """Return true if node drawn"""

        if self.port:
            return True

        if draw_nodes in ('none', None, False):
            return False
        
        if draw_nodes == 'all':
            return True

        if draw_nodes == 'connections':
            return self.count > 2

        return self.name.find('_') == -1

    @property
    def port(self):
        """Return true if node is a port"""

        return self._port or self.count == 1


class Schematic(object):

    def __init__(self, filename=None, **kwargs):

        self.elements = {}
        self.nodes = {}
        # Shared nodes (with same voltage)
        self.snodes = {}
        self.hints = False

        if filename is not None:
            self.netfile_add(filename)

    def __getitem__(self, name):
        """Return component by name"""
        try:
            return self.elements[name]
        except KeyError:
            raise AttributeError('Unknown component %s' % name)

    def netfile_add(self, filename):
        """Add the nets from file with specified filename"""

        file = open(filename, 'r')

        lines = file.readlines()

        for line in lines:
            self.add(line)

    def netlist(self):
        """Return the current netlist"""

        return '\n'.join([elt.__str__() for elt in self.elements.values()])

    def _invalidate(self):

        for attr in ('_xnodes', '_ynodes', '_coords'):
            if hasattr(self, attr):
                delattr(self, attr)

    def _node_add(self, node, elt):

        if node not in self.nodes:
            self.nodes[node] = Node(node)
        self.nodes[node].append(elt)

        vnode = self.nodes[node].rootname

        if vnode not in self.snodes:
            self.snodes[vnode] = []

        if node not in self.snodes[vnode]:
            self.snodes[vnode].append(node)

    def _elt_add(self, elt):

        self._invalidate()

        if elt.name in self.elements:
            print('Overriding component %s' % elt.name)
            # Need to search lists and update component.

        self.elements[elt.name] = elt

        # Ignore nodes for mutual inductance.
        if elt.cpt_type == 'K':
            return

        nodes = elt.nodes
        # The controlling nodes are not drawn.
        if elt.cpt_type in ('E', 'G'):
            nodes = nodes[0:2]

        for node in nodes:
            self._node_add(node, elt)

    def add(self, string):
        """The general form is: 'Name Np Nm symbol'
        where Np is the positive nose and Nm is the negative node.

        A positive current is defined to flow from the positive node
        to the negative node.
        """

        # Ignore comments
        string = string.strip()
        if string == '' or string[0] in ('#', '%'):
            return

        if '\n' in string:
            lines = string.split('\n')
            for line in lines:
                self.add(line)
            return

        fields = string.split(';')
        string = fields[1].strip() if len(fields) > 1 else ''

        if string != '':
            self.hints = True

        opts = Opts(string)

        args = ()
        net = fields[0].strip()
        if net[-1] == '"':
            quote_pos = net[:-1].rfind('"')
            if quote_pos == -1:
                raise ValueError('Missing " in net: ' + net)
            args = (net[quote_pos + 1:-1], ) + args
            net = net[:quote_pos - 1]

        parts = tuple(re.split(r'[,]*[\s]+', net))

        elt = make_cpt(*(parts + args), **opts)

        self._elt_add(elt)

    
    #     c
    # b    
    #     e

    # Need to special case K since nodes are inductor names...

    def _xlink(self, cpt, cnodes):

        for n1 in cpt.nodes:
            for n2 in cpt.nodes:
                if n1 == n2:
                    continue
                if cpt.xvals[n2] == cpt.xvals[n1]:
                    print('TODO link xpos for node %d with %d' % (n1, n2))

    def _ylink(self, cpt, cnodes):

        for n1 in cpt.nodes:
            for n2 in cpt.nodes:
                if n1 == n2:
                    continue
                if cpt.yvals[n2] == cpt.yvals[n1]:
                    print('TODO link ypos for node %d with %d' % (n1, n2))

    def _xplace(self, cpt, graphs, size=1):

        for n1 in cpt.nodes:
            for n2 in cpt.nodes:
                if n1 == n2:
                    continue
                value = (cpt.xvals[n2] - cpt.xvals[1]) * cpt.xscale * size
                graphs.add(nodes[int(n1) - 1], nodes[int(n2) - 1], value)

    def _yplace(self, cpt, graphs, size=1):

        for n1 in cpt.nodes:
            for n2 in cpt.nodes:
                if n1 == n2:
                    continue
                value = (cpt.yvals[n2] - cpt.yvals[1]) * cpt.yscale * size
                graphs.add(nodes[int(n1) - 1], nodes[int(n2) - 1], value)


# Transformer
#   n4      n2
#
#   n3      n1
#
# For horiz. node layout want to make (n3, n4) and (n1, n2) in same cnodes
# For vert. node layout want to make (n2, n4) and (n1, n3) in same cnodes

    def _make_graphs(self, dirs):

        # Use components in orthogonal directions as constraints.  The
        # nodes of orthogonal components get combined into a
        # common node.

        cnodes = Cnodes(self.nodes)

        if dirs[0] == 'right':
            for m, elt in enumerate(self.elements.values()):
                self._xlink(elt, cnodes)                
        else:
            for m, elt in enumerate(self.elements.values()):
                self._ylink(elt, cnodes)                

        # Now form forward and reverse directed graphs using components
        # in the desired directions.
        graphs = Graphs(cnodes.size, 
                        'vertical' if dirs[0] == 'up' else 'horizontal')

        if dirs[0] == 'right':
            for m, elt in enumerate(self.elements.values()):
                self._xplace(elt, graphs, cnodes)                
        else:
            for m, elt in enumerate(self.elements.values()):
                self._yplace(elt, graphs, cnodes)                

        graphs.add_start_nodes()

        if False:
            print(graphs.fwd)
            print(graphs.rev)
            print(cnodes.node_map)
            import pdb
            pdb.set_trace()

        # Find longest path through the graphs.
        length, node, memo = graphs.fwd.longest_path()
        length, node, memor = graphs.rev.longest_path()

        pos = {}
        posr = {}
        posa = {}
        for cnode in graphs.fwd.keys():
            if cnode == 0:
                continue

            for node in cnodes.nodes[cnode]:
                pos[node] = length - memo[cnode]
                posr[node] = memor[cnode]
                posa[node] = 0.5 * (pos[node] + posr[node])

        if False:
            print(pos)
            print(posr)
        return posa, cnodes.nodes, length

    def _positions_calculate(self):

        # The x and y positions of a component node are determined
        # independently.  The principle is that each component has a
        # minimum size (usually 1 but changeable with the size option)
        # but its wires can be stretched.

        # When solving the x position, first nodes that must be
        # vertically aligned (with the up or down option) are combined
        # into a set.  Then the left and right options are used to
        # form a graph.  This graph is traversed to find the longest
        # path and in the process each node gets assigned the longest
        # distance from the root of the graph.  To centre components,
        # a reverse graph is created and the distances are averaged.

        xpos, self._xnodes, self.width = self._make_graphs(('right', 'left'))
        ypos, self._ynodes, self.height = self._make_graphs(('up', 'down'))

        coords = {}
        for node in xpos.keys():
            coords[node] = Pos(xpos[node], ypos[node])

        self._coords = coords

    @property
    def xnodes(self):

        if not hasattr(self, '_xnodes'):
            self._positions_calculate()
        return self._xnodes

    @property
    def ynodes(self):

        if not hasattr(self, '_ynodes'):
            self._positions_calculate()
        return self._ynodes

    @property
    def coords(self):
        """Directory of position tuples indexed by node name"""

        if not hasattr(self, '_coords'):
            self._positions_calculate()
        return self._coords

    def _make_wires1(self, snode_list):

        num_wires = len(snode_list) - 1
        if num_wires == 0:
            return []

        wires = []

        # TODO: remove overdrawn wires...
        for n in range(num_wires):
            n1 = snode_list[n]
            n2 = snode_list[n + 1]

            wires.append(NetElement('W_', n1, n2))

        return wires

    def _make_wires(self):
        """Create implict wires between common nodes."""

        wires = []

        snode_dir = self.snodes

        for m, snode_list in enumerate(snode_dir.values()):
            wires.extend(self._make_wires1(snode_list))

        return wires

    def _node_str(self, n1, n2, draw_nodes=True):

        node1, node2 = self.nodes[n1], self.nodes[n2]

        node_str = ''
        if node1.visible(draw_nodes):
            node_str = 'o' if node1.port else '*'

        node_str += '-'

        if node2.visible(draw_nodes):
            node_str += 'o' if node2.port else '*'

        if node_str == '-':
            node_str = ''
        
        return node_str


    def _tikz_draw(self, style_args='', label_values=True, 
                   draw_nodes=True, label_ids=True,
                   label_nodes='primary'):

        opts = r'scale=%.2f,/tikz/circuitikz/bipoles/length=%.1fcm,%s' % (
            self.node_spacing, self.cpt_size, style_args)
        s = r'\begin{tikzpicture}[%s]''\n' % opts

        # Write coordinates
        for coord in self.coords.keys():
            s += r'  \coordinate (%s) at (%s);''\n' % (
                coord, self.coords[coord])

        # Draw components
        for m, elt in enumerate(self.elements.values()):
            s += elt.draw(label_values, draw_nodes)

        wires = self._make_wires()

        if False:
            # Draw implict wires
            for wire in wires:
                n1, n2 = wire.nodes

                node_str = self._node_str(n1, n2, draw_nodes)
                s += r'  \draw (%s) to [short, %s] (%s);''\n' % (
                    n1, node_str, n2)

        # Label primary nodes
        if label_nodes:
            for m, node in enumerate(self.nodes.values()):
                if label_nodes == 'primary' and not node.primary:
                    continue
                s += r'  \draw {[anchor=south east] (%s) node {%s}};''\n' % (
                    node.name, node.name.replace('_', r'\_'))

        s += r'\end{tikzpicture}''\n'

        return s

    def _tmpfilename(self, suffix=''):

        from tempfile import gettempdir, NamedTemporaryFile

        # Searches using TMPDIR, TEMP, TMP environment variables
        tempdir = gettempdir()
        
        filename = NamedTemporaryFile(suffix=suffix, dir=tempdir, 
                                      delete=False).name
        return filename

    def _convert_pdf_svg(self, pdf_filename, svg_filename):

        system('pdf2svg %s %s' % (pdf_filename, svg_filename))
        if not path.exists(svg_filename):
            raise RuntimeError('Could not generate %s with pdf2svg' % 
                               svg_filename)

    def _convert_pdf_png(self, pdf_filename, png_filename, oversample=1):

        system('convert -density %d %s %s' %
               (oversample * 100, pdf_filename, png_filename))
        if path.exists(png_filename):
            return

        # Windows has a program called convert, try im-convert
        # for image magick convert.
        system('im-convert -density %d %s %s' %
               (oversample * 100, pdf_filename, png_filename))
        if path.exists(png_filename):
            return

        raise RuntimeError('Could not generate %s with convert' % 
                           png_filename)

    def tikz_draw(self, filename, **kwargs):

        root, ext = path.splitext(filename)

        debug = kwargs.pop('debug', False)
        oversample = float(kwargs.pop('oversample', 2))
        style = kwargs.pop('style', 'american')
        stretch = float(kwargs.pop('stretch', 1.0))
        scale = float(kwargs.pop('scale', 1.0))

        self.node_spacing = 2 * stretch * scale
        self.cpt_size = 1.5 * scale
        self.scale = scale

        if style == 'american':
            style_args = 'american currents,american voltages'
        elif style == 'british':
            style_args = 'american currents, european voltages'
        elif style == 'european':
            style_args = 'european currents, european voltages'
        else:
            raise ValueError('Unknown style %s' % style)

        content = self._tikz_draw(style_args, **kwargs)

        if debug:
            print('width = %d, height = %d, oversample = %d, stretch = %.2f, scale = %.2f'
                  % (self.width, self.height, oversample, stretch, scale))

        if ext == '.pytex':
            open(filename, 'w').write(content)
            return

        template = ('\\documentclass[a4paper]{standalone}\n'
                    '\\usepackage{circuitikz}\n'
                    '\\begin{document}\n%s\\end{document}')
        content = template % content

        texfilename = filename.replace(ext, '.tex')
        open(texfilename, 'w').write(content)

        if ext == '.tex':
            return

        dirname = path.dirname(texfilename)
        baseroot = path.basename(root)
        cwd = getcwd()
        if dirname != '':
            chdir(path.abspath(dirname))

        system('pdflatex -interaction batchmode %s.tex' % baseroot)

        if dirname != '':
            chdir(cwd)            

        if not debug:
            try:
                remove(root + '.aux')
                remove(root + '.log')
                remove(root + '.tex')
            except:
                pass

        pdf_filename = root + '.pdf'
        if not path.exists(pdf_filename):
            raise RuntimeError('Could not generate %s with pdflatex' % 
                               pdf_filename)

        if ext == '.pdf':
            return

        if ext == '.svg':
            self._convert_pdf_svg(pdf_filename, root + '.svg')
            if not debug:
                remove(pdf_filename)
            return

        if ext == '.png':
            self._convert_pdf_png(pdf_filename, root + '.png', oversample)
            if not debug:
                remove(pdf_filename)
            return

        raise ValueError('Cannot create file of type %s' % ext)

    def draw(self, filename=None, opts={}, **kwargs):

        for key, val in opts.iteritems():
            if key not in kwargs or kwargs[key] is None:
                kwargs[key] = val

        def in_ipynb():
            try:
                ip = get_ipython()
                cfg = ip.config

                kernapp = cfg['IPKernelApp']

                # Check if processing ipynb file.
                if 'connection_file' in kernapp:
                    return True
                elif kernapp and kernapp['parent_appname'] == 'ipython-notebook':
                    return True
                else:
                    return False
            except (NameError, KeyError):
                return False

        if not self.hints:
            raise RuntimeWarning('No schematic drawing hints provided!')

        png = 'png' in kwargs and kwargs.pop('png')
        svg = 'svg' in kwargs and kwargs.pop('svg')

        if not png and not svg:
            png = True

        if in_ipynb() and filename is None:

            if png:
                from IPython.display import Image, display_png

                pngfilename = self._tmpfilename('.png')
                self.tikz_draw(pngfilename, **kwargs)

                # Create and display PNG image object.
                # There are two problems:
                # 1. The image metadata (width, height) is ignored
                #    when the ipynb file is loaded.
                # 2. The image metadata (width, height) is not stored
                #    when the ipynb file is written non-interactively.
                display_png(Image(filename=pngfilename,
                                  width=self.width * 100, 
                                  height=self.height * 100))
                return

            if svg:
                from IPython.display import SVG, display_svg

                svgfilename = self._tmpfilename('.svg')
                self.tikz_draw(svgfilename, **kwargs)

                # Create and display SVG image object.
                # Note, there is a problem displaying multiple SVG
                # files since the later ones inherit the namespace of
                # the first ones.
                display_svg(SVG(filename=pngfilename, 
                                width=self.width * 100, height=self.height * 100))
                return

        display = False
        if filename is None:
            filename = self._tmpfilename('.png')
            display = True

        self.tikz_draw(filename=filename, **kwargs)
        
        if display:
            # TODO display as SVG so have scaled fonts...

            from matplotlib.pyplot import figure
            from matplotlib.image import imread

            img = imread(filename)

            fig = figure()
            ax = fig.add_subplot(111)
            ax.imshow(img)
            ax.axis('equal')
            ax.axis('off')

def test():

    sch = Schematic()

    sch.add('P1 1 0.1')
    sch.add('R1 1 3; right')
    sch.add('L1 3 2; right')
    sch.add('C1 3 0; down')
    sch.add('P2 2 0.2')
    sch.add('W 0.1 0; right')
    sch.add('W 0 0.2; right')

    sch.draw()
    return sch
