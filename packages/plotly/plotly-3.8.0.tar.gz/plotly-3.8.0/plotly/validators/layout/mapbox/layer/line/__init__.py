

import _plotly_utils.basevalidators


class WidthValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self,
        plotly_name='width',
        parent_name='layout.mapbox.layer.line',
        **kwargs
    ):
        super(WidthValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'plot'),
            role=kwargs.pop('role', 'style'),
            **kwargs
        )


import _plotly_utils.basevalidators


class DashsrcValidator(_plotly_utils.basevalidators.SrcValidator):

    def __init__(
        self,
        plotly_name='dashsrc',
        parent_name='layout.mapbox.layer.line',
        **kwargs
    ):
        super(DashsrcValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'none'),
            role=kwargs.pop('role', 'info'),
            **kwargs
        )


import _plotly_utils.basevalidators


class DashValidator(_plotly_utils.basevalidators.DataArrayValidator):

    def __init__(
        self,
        plotly_name='dash',
        parent_name='layout.mapbox.layer.line',
        **kwargs
    ):
        super(DashValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'plot'),
            role=kwargs.pop('role', 'data'),
            **kwargs
        )
