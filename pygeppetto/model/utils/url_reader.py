""" generated source for class URLReader """
SERVER_ROOT_TOKEN = "SERVER_ROOT"
from multimethod import multidispatch


# 
# 	 * @param urlString
# 	 * @param baseURL
# 	 * @return
#
@multidispatch
def getURL(urlString, baseURL):
    """ generated source for method getURL """
    url = urlString

    if baseURL != None:
        if not urlString.startsWith("http://") and not urlString.startsWith(
                "https://") and not urlString.startsWith(SERVER_ROOT_TOKEN):
            url = baseURL + urlString
    if urlString.startsWith("file:"):
        urlString.replace("file:", "")
    return getURL(url)


# 
# 	 * @param urlString
# 	 * @return
#
@getURL.register(object, str)
def getURL_0(urlString):
    """ generated source for method getURL_0 """
    url = None
    if urlString.startsWith("https://") or urlString.startsWith("http://"):
        url = urlString
    elif urlString.startsWith(SERVER_ROOT_TOKEN):
        url = urlString.replace(SERVER_ROOT_TOKEN, "")
    return url
