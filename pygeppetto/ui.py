
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
    svg_dta = imgdata.getvalue()  # this is svg data
    return svg_dta

