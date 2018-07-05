import holoviews as hv

hv.extension('bokeh')

import uuid

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def getSVG(fig):
    if isinstance(fig, list):
        svgs = []
        for f in fig:
            svgs.append(getSingleSVG(f))
        return svgs
        # Could be written:
        # return [getSingleSVG(f) for f in fig]
    return getSingleSVG(fig)


def getSingleSVG(fig):
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg', transparent=True)
    imgdata.seek(0)  # rewind the data
    svg_dta = imgdata.buf  # this is svg data
    return svg_dta


def get_url(obj, path):
    """Saves obj in path and returns an object with the url."""
    uuid_plot = path + str(uuid.uuid4())
    try:
        hv.renderer('bokeh').save(obj, uuid_plot)
        data = {'url': '/' + uuid_plot + ".html"}
    except:
        data = {'url': ''}
    return data

