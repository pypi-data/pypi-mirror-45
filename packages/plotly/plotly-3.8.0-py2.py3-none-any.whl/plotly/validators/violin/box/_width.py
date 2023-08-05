import _plotly_utils.basevalidators


class WidthValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self, plotly_name='width', parent_name='violin.box', **kwargs
    ):
        super(WidthValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'plot'),
            max=kwargs.pop('max', 1),
            min=kwargs.pop('min', 0),
            role=kwargs.pop('role', 'info'),
            **kwargs
        )
