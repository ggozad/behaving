import argparse
import logging
import os
import subprocess
import sys

try:
    import SocketServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from urlparse import parse_qs
except ImportError:
    import socketserver as SocketServer
    from http.server import SimpleHTTPRequestHandler
    from urllib.parse import parse_qs

try:
    from pync import Notifier

    notifier = Notifier
except ImportError:
    notifier = None

from behaving.mail.mock import getUniqueFilename

output_dir = None


class SMSServer(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("content-length"))
        post_body = self.rfile.read(content_length)
        if isinstance(post_body, bytes):
            post_body = post_body.decode("utf-8")
        params = parse_qs(post_body)
        fr = params.get("from")
        to = params.get("to")
        body = params.get("text")
        if not (fr and to and body):
            self.send_response(400)
            self.end_headers()
            return
        fr = fr[0]
        to = to[0]
        body = body[0]

        self.send_response(200)
        self.send_header("Content-type:", "text/json")
        self.end_headers()
        self.wfile.write(b'{"messages":[{"status":"0"}]}')
        global output_dir
        phone_dir = os.path.join(output_dir, to)
        if not os.path.exists(phone_dir):
            try:
                os.makedirs(phone_dir)
            except OSError:
                logging.error("Phone directory could not be created")
                return

        dest = getUniqueFilename(phone_dir, "sms")
        with open(dest, "w") as f:
            f.write(body)

        if sys.platform == "darwin":
            code = body.split(None)[-1]
            p = subprocess.Popen("pbcopy", stdin=subprocess.PIPE)
            p.communicate(code.encode("utf-8"))
            body = f"{body} and has been copied to the clipboard"
        if notifier:
            notifier.notify(body, title=to)


def main(args=sys.argv[1:]):
    """Main function called by `smsmock` command.
    """
    parser = argparse.ArgumentParser(description="SMS mock server")
    parser.add_argument("-p", "--port", default="8199", help="The port to use")

    parser.add_argument(
        "-o",
        "--output_dir",
        default=None,
        required=True,
        help="Directory where to dump the SMSs",
    )

    options = parser.parse_args(args=args)

    if not os.path.exists(options.output_dir):
        try:
            os.mkdir(options.output_dir)
        except OSError:
            logging.error("Output directory could not be created")
    global output_dir
    output_dir = options.output_dir

    httpd = SocketServer.TCPServer(("", int(options.port)), SMSServer)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
