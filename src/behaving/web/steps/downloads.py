import os

from behave import then

from behaving.web.steps.basic import _retry


@then(
    'the file "{filename}" containing "{text}" should have been downloaded within {timeout:d} seconds'
)
def verify_download_contents(context, filename, text, timeout):
    path = os.path.join(context.download_dir, filename)

    def check():
        return os.path.exists(path)

    assert _retry(check, timeout), f"File {filename} could not be downloaded"
    with open(path, "rb") as f:
        contents = f.read()

    assert text.encode() in contents, f'Text "{text}" not found in {filename}'


@then('the file "{filename}" should have been downloaded within {timeout:d} seconds')
def verify_download(context, filename, timeout):
    path = os.path.join(context.download_dir, filename)

    def check():
        return os.path.exists(path)

    assert _retry(check, timeout), f"File {filename} has not been downloaded"
