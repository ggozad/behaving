import argparse
import json
import logging
import os
import socketserver as SocketServer
import sys
from http.server import SimpleHTTPRequestHandler

from behaving.mail.mock import getUniqueFilename

output_dir = None


class GCMServer(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("content-length"))
        body = self.rfile.read(content_length).decode("utf-8")

        try:
            message = json.loads(body)
        except json.JSONDecodeError:
            self.send_error(400, "JSON not parsable")
            return

        if "registration_ids" in message:
            recipients = message["registration_ids"]
            del message["registration_ids"]

        if "to" in message:
            to = message["to"]
            del message["to"]
            recipients = [to]

        if not recipients:
            self.send_error(400, "No recipients")
            return

        global output_dir
        for recipient in recipients:
            recipient = str(recipient)
            recipient_dir = os.path.join(output_dir, recipient)
            if not os.path.exists(recipient_dir):
                try:
                    os.makedirs(recipient_dir)
                except OSError:
                    self.send_error(
                        400,
                        f"Device directory [{recipient_dir}] could not be created",
                    )
                    return

            try:
                dest = getUniqueFilename(recipient_dir, "gcm")
            except IOError as e:
                self.send_error(400, e.message)
                return

            with open(dest, "w") as f:
                json.dump(message, f, ensure_ascii=False)

        response = json.dumps({"failure": 0, "canonical_ids": 0})
        self.send_response(200)
        self.end_headers()
        self.wfile.write(response.encode("utf8"))


def main(args=sys.argv[1:]):
    """Main function called by `gcmmock` command."""
    parser = argparse.ArgumentParser(description="GCM mock server")
    parser.add_argument("-p", "--port", default="8200", help="The port to use")

    parser.add_argument(
        "-o",
        "--output_dir",
        default=None,
        required=True,
        help="Directory where to dump the GCMs",
    )

    options = parser.parse_args(args=args)

    if not os.path.exists(options.output_dir):
        try:
            os.mkdir(options.output_dir)
        except OSError:
            logging.error("Output directory could not be created")
    global output_dir
    output_dir = options.output_dir

    httpd = SocketServer.TCPServer(("", int(options.port)), GCMServer)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
