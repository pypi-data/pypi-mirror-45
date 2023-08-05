from plotly.basedatatypes import BaseTraceHierarchyType
import copy


class Node(BaseTraceHierarchyType):

    # color
    # -----
    @property
    def color(self):
        """
        Sets the `node` color. It can be a single value, or an array
        for specifying color for each `node`. If `node.color` is
        omitted, then the default `Plotly` color palette will be cycled
        through to have a variety of colors. These defaults are not
        fully opaque, to allow some visibility of what is beneath the
        node.
    
        The 'color' property is a color and may be specified as:
          - A hex string (e.g. '#ff0000')
          - An rgb/rgba string (e.g. 'rgb(255,0,0)')
          - An hsl/hsla string (e.g. 'hsl(0,100%,50%)')
          - An hsv/hsva string (e.g. 'hsv(0,100%,100%)')
          - A named CSS color:
                aliceblue, antiquewhite, aqua, aquamarine, azure,
                beige, bisque, black, blanchedalmond, blue,
                blueviolet, brown, burlywood, cadetblue,
                chartreuse, chocolate, coral, cornflowerblue,
                cornsilk, crimson, cyan, darkblue, darkcyan,
                darkgoldenrod, darkgray, darkgrey, darkgreen,
                darkkhaki, darkmagenta, darkolivegreen, darkorange,
                darkorchid, darkred, darksalmon, darkseagreen,
                darkslateblue, darkslategray, darkslategrey,
                darkturquoise, darkviolet, deeppink, deepskyblue,
                dimgray, dimgrey, dodgerblue, firebrick,
                floralwhite, forestgreen, fuchsia, gainsboro,
                ghostwhite, gold, goldenrod, gray, grey, green,
                greenyellow, honeydew, hotpink, indianred, indigo,
                ivory, khaki, lavender, lavenderblush, lawngreen,
                lemonchiffon, lightblue, lightcoral, lightcyan,
                lightgoldenrodyellow, lightgray, lightgrey,
                lightgreen, lightpink, lightsalmon, lightseagreen,
                lightskyblue, lightslategray, lightslategrey,
                lightsteelblue, lightyellow, lime, limegreen,
                linen, magenta, maroon, mediumaquamarine,
                mediumblue, mediumorchid, mediumpurple,
                mediumseagreen, mediumslateblue, mediumspringgreen,
                mediumturquoise, mediumvioletred, midnightblue,
                mintcream, mistyrose, moccasin, navajowhite, navy,
                oldlace, olive, olivedrab, orange, orangered,
                orchid, palegoldenrod, palegreen, paleturquoise,
                palevioletred, papayawhip, peachpuff, peru, pink,
                plum, powderblue, purple, red, rosybrown,
                royalblue, saddlebrown, salmon, sandybrown,
                seagreen, seashell, sienna, silver, skyblue,
                slateblue, slategray, slategrey, snow, springgreen,
                steelblue, tan, teal, thistle, tomato, turquoise,
                violet, wheat, white, whitesmoke, yellow,
                yellowgreen
          - A list or array of any of the above

        Returns
        -------
        str|numpy.ndarray
        """
        return self['color']

    @color.setter
    def color(self, val):
        self['color'] = val

    # colorsrc
    # --------
    @property
    def colorsrc(self):
        """
        Sets the source reference on plot.ly for  color .
    
        The 'colorsrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        return self['colorsrc']

    @colorsrc.setter
    def colorsrc(self, val):
        self['colorsrc'] = val

    # groups
    # ------
    @property
    def groups(self):
        """
        Groups of nodes. Each group is defined by an array with the
        indices of the nodes it contains. Multiple groups can be
        specified.
    
        The 'groups' property is an info array that may be specified as:
        * a 2D list where:
          The 'groups[i][j]' property is a number and may be specified as:
          - An int or float

        Returns
        -------
        list
        """
        return self['groups']

    @groups.setter
    def groups(self, val):
        self['groups'] = val

    # hoverinfo
    # ---------
    @property
    def hoverinfo(self):
        """
        Determines which trace information appear when hovering nodes.
        If `none` or `skip` are set, no information is displayed upon
        hovering. But, if `none` is set, click and hover events are
        still fired.
    
        The 'hoverinfo' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['all', 'none', 'skip']

        Returns
        -------
        Any
        """
        return self['hoverinfo']

    @hoverinfo.setter
    def hoverinfo(self, val):
        self['hoverinfo'] = val

    # hoverlabel
    # ----------
    @property
    def hoverlabel(self):
        """
        The 'hoverlabel' property is an instance of Hoverlabel
        that may be specified as:
          - An instance of plotly.graph_objs.sankey.node.Hoverlabel
          - A dict of string/value properties that will be passed
            to the Hoverlabel constructor
    
            Supported dict properties:
                
                bgcolor
                    Sets the background color of the hover labels
                    for this trace
                bgcolorsrc
                    Sets the source reference on plot.ly for
                    bgcolor .
                bordercolor
                    Sets the border color of the hover labels for
                    this trace.
                bordercolorsrc
                    Sets the source reference on plot.ly for
                    bordercolor .
                font
                    Sets the font used in hover labels.
                namelength
                    Sets the length (in number of characters) of
                    the trace name in the hover labels for this
                    trace. -1 shows the whole name regardless of
                    length. 0-3 shows the first 0-3 characters, and
                    an integer >3 will show the whole name if it is
                    less than that many characters, but if it is
                    longer, will truncate to `namelength - 3`
                    characters and add an ellipsis.
                namelengthsrc
                    Sets the source reference on plot.ly for
                    namelength .

        Returns
        -------
        plotly.graph_objs.sankey.node.Hoverlabel
        """
        return self['hoverlabel']

    @hoverlabel.setter
    def hoverlabel(self, val):
        self['hoverlabel'] = val

    # hovertemplate
    # -------------
    @property
    def hovertemplate(self):
        """
        Template string used for rendering the information that appear
        on hover box. Note that this will override `hoverinfo`.
        Variables are inserted using %{variable}, for example "y:
        %{y}". Numbers are formatted using d3-format's syntax
        %{variable:d3-format}, for example "Price: %{y:$.2f}". See http
        s://github.com/d3/d3-format/blob/master/README.md#locale_format
        for details on the formatting syntax. The variables available
        in `hovertemplate` are the ones emitted as event data described
        at this link https://plot.ly/javascript/plotlyjs-events/#event-
        data. Additionally, every attributes that can be specified per-
        point (the ones that are `arrayOk: true`) are available.
        variables `value` and `label`. Anything contained in tag
        `<extra>` is displayed in the secondary box, for example
        "<extra>{fullData.name}</extra>".
    
        The 'hovertemplate' property is a string and must be specified as:
          - A string
          - A number that will be converted to a string
          - A tuple, list, or one-dimensional numpy array of the above

        Returns
        -------
        str|numpy.ndarray
        """
        return self['hovertemplate']

    @hovertemplate.setter
    def hovertemplate(self, val):
        self['hovertemplate'] = val

    # hovertemplatesrc
    # ----------------
    @property
    def hovertemplatesrc(self):
        """
        Sets the source reference on plot.ly for  hovertemplate .
    
        The 'hovertemplatesrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        return self['hovertemplatesrc']

    @hovertemplatesrc.setter
    def hovertemplatesrc(self, val):
        self['hovertemplatesrc'] = val

    # label
    # -----
    @property
    def label(self):
        """
        The shown name of the node.
    
        The 'label' property is an array that may be specified as a tuple,
        list, numpy array, or pandas Series

        Returns
        -------
        numpy.ndarray
        """
        return self['label']

    @label.setter
    def label(self, val):
        self['label'] = val

    # labelsrc
    # --------
    @property
    def labelsrc(self):
        """
        Sets the source reference on plot.ly for  label .
    
        The 'labelsrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        return self['labelsrc']

    @labelsrc.setter
    def labelsrc(self, val):
        self['labelsrc'] = val

    # line
    # ----
    @property
    def line(self):
        """
        The 'line' property is an instance of Line
        that may be specified as:
          - An instance of plotly.graph_objs.sankey.node.Line
          - A dict of string/value properties that will be passed
            to the Line constructor
    
            Supported dict properties:
                
                color
                    Sets the color of the `line` around each
                    `node`.
                colorsrc
                    Sets the source reference on plot.ly for  color
                    .
                width
                    Sets the width (in px) of the `line` around
                    each `node`.
                widthsrc
                    Sets the source reference on plot.ly for  width
                    .

        Returns
        -------
        plotly.graph_objs.sankey.node.Line
        """
        return self['line']

    @line.setter
    def line(self, val):
        self['line'] = val

    # pad
    # ---
    @property
    def pad(self):
        """
        Sets the padding (in px) between the `nodes`.
    
        The 'pad' property is a number and may be specified as:
          - An int or float in the interval [0, inf]

        Returns
        -------
        int|float
        """
        return self['pad']

    @pad.setter
    def pad(self, val):
        self['pad'] = val

    # thickness
    # ---------
    @property
    def thickness(self):
        """
        Sets the thickness (in px) of the `nodes`.
    
        The 'thickness' property is a number and may be specified as:
          - An int or float in the interval [1, inf]

        Returns
        -------
        int|float
        """
        return self['thickness']

    @thickness.setter
    def thickness(self, val):
        self['thickness'] = val

    # property parent name
    # --------------------
    @property
    def _parent_path_str(self):
        return 'sankey'

    # Self properties description
    # ---------------------------
    @property
    def _prop_descriptions(self):
        return """\
        color
            Sets the `node` color. It can be a single value, or an
            array for specifying color for each `node`. If
            `node.color` is omitted, then the default `Plotly`
            color palette will be cycled through to have a variety
            of colors. These defaults are not fully opaque, to
            allow some visibility of what is beneath the node.
        colorsrc
            Sets the source reference on plot.ly for  color .
        groups
            Groups of nodes. Each group is defined by an array with
            the indices of the nodes it contains. Multiple groups
            can be specified.
        hoverinfo
            Determines which trace information appear when hovering
            nodes. If `none` or `skip` are set, no information is
            displayed upon hovering. But, if `none` is set, click
            and hover events are still fired.
        hoverlabel
            plotly.graph_objs.sankey.node.Hoverlabel instance or
            dict with compatible properties
        hovertemplate
            Template string used for rendering the information that
            appear on hover box. Note that this will override
            `hoverinfo`. Variables are inserted using %{variable},
            for example "y: %{y}". Numbers are formatted using
            d3-format's syntax %{variable:d3-format}, for example
            "Price: %{y:$.2f}". See https://github.com/d3/d3-format
            /blob/master/README.md#locale_format for details on the
            formatting syntax. The variables available in
            `hovertemplate` are the ones emitted as event data
            described at this link
            https://plot.ly/javascript/plotlyjs-events/#event-data.
            Additionally, every attributes that can be specified
            per-point (the ones that are `arrayOk: true`) are
            available. variables `value` and `label`. Anything
            contained in tag `<extra>` is displayed in the
            secondary box, for example
            "<extra>{fullData.name}</extra>".
        hovertemplatesrc
            Sets the source reference on plot.ly for  hovertemplate
            .
        label
            The shown name of the node.
        labelsrc
            Sets the source reference on plot.ly for  label .
        line
            plotly.graph_objs.sankey.node.Line instance or dict
            with compatible properties
        pad
            Sets the padding (in px) between the `nodes`.
        thickness
            Sets the thickness (in px) of the `nodes`.
        """

    def __init__(
        self,
        arg=None,
        color=None,
        colorsrc=None,
        groups=None,
        hoverinfo=None,
        hoverlabel=None,
        hovertemplate=None,
        hovertemplatesrc=None,
        label=None,
        labelsrc=None,
        line=None,
        pad=None,
        thickness=None,
        **kwargs
    ):
        """
        Construct a new Node object
        
        The nodes of the Sankey plot.

        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of plotly.graph_objs.sankey.Node
        color
            Sets the `node` color. It can be a single value, or an
            array for specifying color for each `node`. If
            `node.color` is omitted, then the default `Plotly`
            color palette will be cycled through to have a variety
            of colors. These defaults are not fully opaque, to
            allow some visibility of what is beneath the node.
        colorsrc
            Sets the source reference on plot.ly for  color .
        groups
            Groups of nodes. Each group is defined by an array with
            the indices of the nodes it contains. Multiple groups
            can be specified.
        hoverinfo
            Determines which trace information appear when hovering
            nodes. If `none` or `skip` are set, no information is
            displayed upon hovering. But, if `none` is set, click
            and hover events are still fired.
        hoverlabel
            plotly.graph_objs.sankey.node.Hoverlabel instance or
            dict with compatible properties
        hovertemplate
            Template string used for rendering the information that
            appear on hover box. Note that this will override
            `hoverinfo`. Variables are inserted using %{variable},
            for example "y: %{y}". Numbers are formatted using
            d3-format's syntax %{variable:d3-format}, for example
            "Price: %{y:$.2f}". See https://github.com/d3/d3-format
            /blob/master/README.md#locale_format for details on the
            formatting syntax. The variables available in
            `hovertemplate` are the ones emitted as event data
            described at this link
            https://plot.ly/javascript/plotlyjs-events/#event-data.
            Additionally, every attributes that can be specified
            per-point (the ones that are `arrayOk: true`) are
            available. variables `value` and `label`. Anything
            contained in tag `<extra>` is displayed in the
            secondary box, for example
            "<extra>{fullData.name}</extra>".
        hovertemplatesrc
            Sets the source reference on plot.ly for  hovertemplate
            .
        label
            The shown name of the node.
        labelsrc
            Sets the source reference on plot.ly for  label .
        line
            plotly.graph_objs.sankey.node.Line instance or dict
            with compatible properties
        pad
            Sets the padding (in px) between the `nodes`.
        thickness
            Sets the thickness (in px) of the `nodes`.

        Returns
        -------
        Node
        """
        super(Node, self).__init__('node')

        # Validate arg
        # ------------
        if arg is None:
            arg = {}
        elif isinstance(arg, self.__class__):
            arg = arg.to_plotly_json()
        elif isinstance(arg, dict):
            arg = copy.copy(arg)
        else:
            raise ValueError(
                """\
The first argument to the plotly.graph_objs.sankey.Node 
constructor must be a dict or 
an instance of plotly.graph_objs.sankey.Node"""
            )

        # Handle skip_invalid
        # -------------------
        self._skip_invalid = kwargs.pop('skip_invalid', False)

        # Import validators
        # -----------------
        from plotly.validators.sankey import (node as v_node)

        # Initialize validators
        # ---------------------
        self._validators['color'] = v_node.ColorValidator()
        self._validators['colorsrc'] = v_node.ColorsrcValidator()
        self._validators['groups'] = v_node.GroupsValidator()
        self._validators['hoverinfo'] = v_node.HoverinfoValidator()
        self._validators['hoverlabel'] = v_node.HoverlabelValidator()
        self._validators['hovertemplate'] = v_node.HovertemplateValidator()
        self._validators['hovertemplatesrc'
                        ] = v_node.HovertemplatesrcValidator()
        self._validators['label'] = v_node.LabelValidator()
        self._validators['labelsrc'] = v_node.LabelsrcValidator()
        self._validators['line'] = v_node.LineValidator()
        self._validators['pad'] = v_node.PadValidator()
        self._validators['thickness'] = v_node.ThicknessValidator()

        # Populate data dict with properties
        # ----------------------------------
        _v = arg.pop('color', None)
        self['color'] = color if color is not None else _v
        _v = arg.pop('colorsrc', None)
        self['colorsrc'] = colorsrc if colorsrc is not None else _v
        _v = arg.pop('groups', None)
        self['groups'] = groups if groups is not None else _v
        _v = arg.pop('hoverinfo', None)
        self['hoverinfo'] = hoverinfo if hoverinfo is not None else _v
        _v = arg.pop('hoverlabel', None)
        self['hoverlabel'] = hoverlabel if hoverlabel is not None else _v
        _v = arg.pop('hovertemplate', None)
        self['hovertemplate'
            ] = hovertemplate if hovertemplate is not None else _v
        _v = arg.pop('hovertemplatesrc', None)
        self['hovertemplatesrc'
            ] = hovertemplatesrc if hovertemplatesrc is not None else _v
        _v = arg.pop('label', None)
        self['label'] = label if label is not None else _v
        _v = arg.pop('labelsrc', None)
        self['labelsrc'] = labelsrc if labelsrc is not None else _v
        _v = arg.pop('line', None)
        self['line'] = line if line is not None else _v
        _v = arg.pop('pad', None)
        self['pad'] = pad if pad is not None else _v
        _v = arg.pop('thickness', None)
        self['thickness'] = thickness if thickness is not None else _v

        # Process unknown kwargs
        # ----------------------
        self._process_kwargs(**dict(arg, **kwargs))

        # Reset skip_invalid
        # ------------------
        self._skip_invalid = False
