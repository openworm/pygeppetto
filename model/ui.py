import StringIO

def getSVG(fig):
    if isinstance(fig, list):
        svgs = []
        for f in fig:
            svgs.append(getSingleSVG(f))
        return svgs
    return getSingleSVG(fig)

def getSingleSVG(fig):
    imgdata = StringIO.StringIO()
    fig.savefig(imgdata, format='svg', transparent=True)
    imgdata.seek(0)  # rewind the data
    svg_dta = imgdata.buf  # this is svg data
    return svg_dta