import os

from behave import step
from behaving.web.steps.basic import _retry


@step(
    u'the file "{filename}" containing "{text}" should have been downloaded within {timeout:d} seconds'
)
def verify_download_contents(context, filename, text, timeout):
    path = os.path.join(context.download_dir, filename)

    def check():
        return os.path.exists(path)

    assert _retry(check, timeout), u"File has not been downloaded"
    with open(path, "rb") as f:
        contents = f.read()

    assert text.encode() in contents, u"Text not found in file"


@step(u'the file "{filename}" should have been downloaded within {timeout:d} seconds')
def verify_download(context, filename, timeout):
    path = os.path.join(context.download_dir, filename)

    def check():
        return os.path.exists(path)

    assert _retry(check, timeout), u"File has not been downloaded"
