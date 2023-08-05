import warnings
import functools

_future_flags = set()


def _assert_plotly_not_imported():
    import sys
    if 'plotly' in sys.modules:
        raise ImportError("""\
The _plotly_future_ module must be imported before the plotly module""")


warnings.filterwarnings(
    'default',
    '.*?is deprecated, please use chart_studio*',
    DeprecationWarning
)


def _chart_studio_warning(submodule):
    if 'extract_chart_studio' in _future_flags:
        warnings.warn(
            'The plotly.{submodule} module is deprecated, '
            'please use chart_studio.{submodule} instead'
                .format(submodule=submodule),
            DeprecationWarning,
            stacklevel=2)


def _chart_studio_deprecation(fn):

    fn_name = fn.__name__
    fn_module = fn.__module__
    plotly_name = '.'.join(
        ['plotly'] + fn_module.split('.')[1:] + [fn_name])
    chart_studio_name = '.'.join(
        ['chart_studio'] + fn_module.split('.')[1:] + [fn_name])

    msg = """\
{plotly_name} is deprecated, please use {chart_studio_name}\
""".format(plotly_name=plotly_name, chart_studio_name=chart_studio_name)

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if 'extract_chart_studio' in _future_flags:
            warnings.warn(
                msg,
                DeprecationWarning,
                stacklevel=2)

        return fn(*args, **kwargs)

    return wrapper


__all__ = ['_future_flags', '_chart_studio_warning']
