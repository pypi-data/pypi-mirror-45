    def _schemdraw_draw_TF(self, elt, drw, label_values):

        import SchemDraw.elements as e

        n1, n2, n3, n4 = elt.nodes

        pos1 = self.coords[n1] * self.node_spacing
        pos2 = self.coords[n2] * self.node_spacing
        pos3 = self.coords[n3] * self.node_spacing
        pos4 = self.coords[n4] * self.node_spacing

        drw.add(e.INDUCTOR2, xy=pos4.xy, to=pos3.xy)
        drw.add(e.INDUCTOR2, xy=pos2.xy, to=pos1.xy,
                label=elt.tex_label.replace('\\,', ' '))

    def _schemdraw_draw_TP(self, elt, drw, label_values):

        # TODO
        pass

    def _schemdraw_draw_cpt(self, elt, drw, label_values, draw_nodes):

        import SchemDraw.elements as e

        cpt_type_map2 = {'R': e.RES, 'C': e.CAP, 'L': e.INDUCTOR2,
                         'Vac': e.SOURCE_SIN, 'Vdc': e.SOURCE_V,
                         'Iac': e.SOURCE_SIN, 'Idc': e.SOURCE_I,
                         'Vstep': e.SOURCE_V, 'Vdelta': e.SOURCE_V,
                         'Istep': e.SOURCE_I, 'Idelta': e.SOURCE_I,
                         'V': e.SOURCE_V, 'I': e.SOURCE_I,
                         'Vs': e.SOURCE_V, 'Is': e.SOURCE_I,
                         'v': e.SOURCE_V, 'i': e.SOURCE_I,
                         'P': e.GAP_LABEL, 'port': e.GAP_LABEL,
                         'W': e.LINE, 'wire': e.LINE,
                         'Y': e.RBOX, 'Z': e.RBOX}

        cpt_type = cpt_type_map2[elt.cpt_type]

        n1, n2 = elt.nodes[0:2]

        pos1 = self.coords[n1] * self.node_spacing
        pos2 = self.coords[n2] * self.node_spacing

        if label_values:
            drw.add(cpt_type, xy=pos2.xy, to=pos1.xy,
                    label=elt.tex_label.replace('\\,', ' '))
        else:
            drw.add(cpt_type, xy=pos2.xy, to=pos1.xy)

    def _schemdraw_draw_opamp(self, elt, label_values):

        # TODO
        pass

    def _schemdraw_draw_K(self, elt, label_values):

        # TODO
        pass

    def schemdraw_draw(self, label_values=True, draw_nodes=True,
                       label_nodes=True, filename=None, args=None):

        from SchemDraw import Drawing
        import SchemDraw.elements as e

        # Preamble
        if args is None:
            args = ''

        drw = Drawing()

        # Update element positions
        self.coords

        draw = {'TF': self._schemdraw_draw_TF,
                'TP': self._schemdraw_draw_TP,
                'K': self._schemdraw_draw_K,
                'opamp': self._schemdraw_draw_opamp}

        # Draw components
        for m, elt in enumerate(self.elements.values()):

            if elt.cpt_type in draw:
                draw[elt.cpt_type](elt, drw, label_values)
            else:
                self._schemdraw_draw_cpt(elt, drw, label_values, draw_nodes)

        if draw_nodes:
            for m, node in enumerate(self.nodes.values()):
                label_str = node.name if label_values and node.primary else ''
                if node.port:
                    drw.add(e.DOT_OPEN,
                            xy=self.coords[node.name].xy * self.node_spacing,
                            label=label_str)
                elif node.primary:
                    drw.add(e.DOT,
                            xy=self.coords[node.name].xy * self.node_spacing,
                            label=label_str)

        drw.draw()
        if filename is not None:
            drw.save(filename)


            return self.schemdraw_draw(filename=filename, **kwargs)
