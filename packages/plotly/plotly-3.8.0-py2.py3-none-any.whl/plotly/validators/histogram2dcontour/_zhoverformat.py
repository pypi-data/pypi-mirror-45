import _plotly_utils.basevalidators


class ZhoverformatValidator(_plotly_utils.basevalidators.StringValidator):

    def __init__(
        self,
        plotly_name='zhoverformat',
        parent_name='histogram2dcontour',
        **kwargs
    ):
        super(ZhoverformatValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'none'),
            role=kwargs.pop('role', 'style'),
            **kwargs
        )
