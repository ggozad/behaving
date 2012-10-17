import argparse
import sys

import SimpleHTTPServer
import SocketServer
import urlparse


class SMSServer(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_length)
        params = urlparse.parse_qs(post_body)
        fr = params.get('from')
        to = params.get('to')
        body = params.get('body')
        if not (fr and to and body):
            self.send_response(400)
            self.end_headers()
            return
        self.send_response(200)
        self.end_headers()
        print fr, to, body


def main(args=sys.argv[1:]):
    """Main function called by `smsmock` command.
    """
    parser = argparse.ArgumentParser(description='SMS mock server')
    parser.add_argument('-p', '--port',
                        default='8099',
                        help='The port to use')

    options = parser.parse_args(args=args)
    httpd = SocketServer.TCPServer(("", int(options.port)), SMSServer)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
