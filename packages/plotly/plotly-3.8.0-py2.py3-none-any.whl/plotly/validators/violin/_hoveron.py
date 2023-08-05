import _plotly_utils.basevalidators


class HoveronValidator(_plotly_utils.basevalidators.FlaglistValidator):

    def __init__(self, plotly_name='hoveron', parent_name='violin', **kwargs):
        super(HoveronValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'style'),
            extras=kwargs.pop('extras', ['all']),
            flags=kwargs.pop('flags', ['violins', 'points', 'kde']),
            role=kwargs.pop('role', 'info'),
            **kwargs
        )
