from scrapy.http import HtmlResponse, Request, TextResponse


def file_response(file_name, url=None):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_name: The relative filename from the tests directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.

    Based on https://stackoverflow.com/a/12741030, a nice bit of hacking.
    """
    if not url:
        url = "http://www.example.com"

    request = Request(url=url)
    with open(file_name, "r", encoding="utf-8") as f:
        file_content = f.read()

    if file_name[-5:] == ".json":
        body = file_content
        return TextResponse(url=url, body=body, encoding="utf-8")

    body = str.encode(file_content)
    return HtmlResponse(url=url, request=request, body=body)
