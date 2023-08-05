

import _plotly_utils.basevalidators


class WidthValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self,
        plotly_name='width',
        parent_name='waterfall.decreasing.marker.line',
        **kwargs
    ):
        super(WidthValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            anim=kwargs.pop('anim', True),
            array_ok=kwargs.pop('array_ok', False),
            edit_type=kwargs.pop('edit_type', 'style'),
            min=kwargs.pop('min', 0),
            role=kwargs.pop('role', 'style'),
            **kwargs
        )


import _plotly_utils.basevalidators


class ColorValidator(_plotly_utils.basevalidators.ColorValidator):

    def __init__(
        self,
        plotly_name='color',
        parent_name='waterfall.decreasing.marker.line',
        **kwargs
    ):
        super(ColorValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            array_ok=kwargs.pop('array_ok', False),
            edit_type=kwargs.pop('edit_type', 'style'),
            role=kwargs.pop('role', 'style'),
            **kwargs
        )
