import _plotly_utils.basevalidators


class CategoryarraysrcValidator(_plotly_utils.basevalidators.SrcValidator):

    def __init__(
        self,
        plotly_name='categoryarraysrc',
        parent_name='layout.yaxis',
        **kwargs
    ):
        super(CategoryarraysrcValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'none'),
            role=kwargs.pop('role', 'info'),
            **kwargs
        )
