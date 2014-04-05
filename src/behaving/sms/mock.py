import argparse
import logging
import os
import sys
try:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    import SocketServer
    from urlparse import parse_qs
except ImportError:
    from http.server import SimpleHTTPRequestHandler
    import socketserver as SocketServer
    from urllib.parse import parse_qs
import time

output_dir = None


class SMSServer(SimpleHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers.get('content-length'))
        post_body = self.rfile.read(content_length)
        params = parse_qs(post_body)
        fr = params.get(b'from')
        to = params.get(b'to')
        body = params.get(b'text')
        if not (fr and to and body):
            self.send_response(400)
            self.end_headers()
            return
        if sys.version_info[0] >= 3:
            fr = fr[0].decode('utf-8')
            to = to[0].decode('utf-8')
            body = body[0].decode('utf-8')
        else:
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
                logging.error('Phone directory could not be created')
                return

        filename = time.strftime("%Y-%m-%d-%H%M%S", time.gmtime(time.time()))
        dest = os.path.join(phone_dir, "%s.sms" % filename)
        with open(dest, "w") as f:
            f.write(body)


def main(args=sys.argv[1:]):
    """Main function called by `smsmock` command.
    """
    parser = argparse.ArgumentParser(description='SMS mock server')
    parser.add_argument('-p', '--port',
                        default='8099',
                        help='The port to use')

    parser.add_argument('-o', '--output_dir',
                        default=None,
                        required=True,
                        help='Directory where to dump the SMSs')

    options = parser.parse_args(args=args)

    if not os.path.exists(options.output_dir):
        try:
            os.mkdir(options.output_dir)
        except OSError:
            logging.error('Output directory could not be created')
    global output_dir
    output_dir = options.output_dir

    httpd = SocketServer.TCPServer(("", int(options.port)), SMSServer)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
