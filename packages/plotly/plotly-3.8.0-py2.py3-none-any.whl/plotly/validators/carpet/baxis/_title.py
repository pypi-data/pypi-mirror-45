import _plotly_utils.basevalidators


class TitleValidator(_plotly_utils.basevalidators.TitleValidator):

    def __init__(
        self, plotly_name='title', parent_name='carpet.baxis', **kwargs
    ):
        super(TitleValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            data_class_str=kwargs.pop('data_class_str', 'Title'),
            data_docs=kwargs.pop(
                'data_docs', """
            font
                Sets this axis' title font. Note that the
                title's font used to be set by the now
                deprecated `titlefont` attribute.
            offset
                An additional amount by which to offset the
                title from the tick labels, given in pixels.
                Note that this used to be set by the now
                deprecated `titleoffset` attribute.
            text
                Sets the title of this axis. Note that before
                the existence of `title.text`, the title's
                contents used to be defined as the `title`
                attribute itself. This behavior has been
                deprecated.
"""
            ),
            **kwargs
        )
