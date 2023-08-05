import _plotly_utils.basevalidators


class ZerolineValidator(_plotly_utils.basevalidators.BooleanValidator):

    def __init__(
        self, plotly_name='zeroline', parent_name='layout.xaxis', **kwargs
    ):
        super(ZerolineValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'ticks'),
            role=kwargs.pop('role', 'style'),
            **kwargs
        )
