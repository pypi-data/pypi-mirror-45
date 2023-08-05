import _plotly_utils.basevalidators


class ThicknessmodeValidator(_plotly_utils.basevalidators.EnumeratedValidator):

    def __init__(
        self,
        plotly_name='thicknessmode',
        parent_name='parcats.line.colorbar',
        **kwargs
    ):
        super(ThicknessmodeValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'colorbars'),
            role=kwargs.pop('role', 'style'),
            values=kwargs.pop('values', ['fraction', 'pixels']),
            **kwargs
        )
