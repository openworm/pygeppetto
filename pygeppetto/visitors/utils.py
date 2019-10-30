import json
import requests

def stream_requests(url, params, method="GET", chunk_size=8192):
    processed_output = []
    kwargs = { "url": url, "stream": True }

    if method == "POST":
        method = requests.post
        kwargs["json"] = params

    elif method == "GET":
        method = requests.get
        kwargs["params"] = params

    with method(**kwargs) as r:
        for chunk in r.iter_lines(chunk_size=chunk_size, delimiter=b'\n'):
            if chunk:
                processed_output.append(chunk.decode("utf-8"))

    return processed_output