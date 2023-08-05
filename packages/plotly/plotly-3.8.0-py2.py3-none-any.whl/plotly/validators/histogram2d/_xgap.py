import _plotly_utils.basevalidators


class XgapValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self, plotly_name='xgap', parent_name='histogram2d', **kwargs
    ):
        super(XgapValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'plot'),
            min=kwargs.pop('min', 0),
            role=kwargs.pop('role', 'style'),
            **kwargs
        )
