import os
import smtpd
import sys
import time
import argparse
import logging
import asyncore

output_dir = None


class DebuggingServer(smtpd.DebuggingServer):
    def __init__(self, localaddr, remoteaddr):
        global output_dir
        self.path = output_dir
        smtpd.DebuggingServer.__init__(self, localaddr, remoteaddr)

    def process_message(self, peer, mailfrom, rcpttos, data):
        smtpd.DebuggingServer.process_message(self,
                                              peer,
                                              mailfrom,
                                              rcpttos,
                                              data)
        sys.stdout.flush()
        if self.path is None:
            return
        filename = time.strftime("%Y-%m-%d-%H%M%S", time.gmtime(time.time()))
        for addr in rcpttos:
            path = os.path.join(self.path, addr)
            if not os.path.exists(path):
                os.makedirs(path)
            dest = os.path.join(path, "%s.eml" % filename)
            index = 1
            while os.path.exists(dest):
                if index > 1000:
                    raise IOError("Tried too many filenames like: %s" % dest)
                dest = os.path.join(path, "%s-%s.eml" % (filename, index))
                index = index + 1
            with open(dest, "w") as f:
                f.write(data)


def main(args=sys.argv[1:]):
    """Main function called by `mailmock` command.
    """
    parser = argparse.ArgumentParser(description='Mail mock server')

    parser.add_argument('-p', '--port',
                        default='8025',
                        help='The port to use')

    parser.add_argument('-o', '--output_dir',
                        default=None,
                        required=True,
                        help='Directory where to dump the mail.')

    options = parser.parse_args(args=args)

    if not os.path.exists(options.output_dir):
        try:
            os.mkdir(options.output_dir)
        except OSError:
            logging.error('Output directory could not be created')
    global output_dir
    output_dir = options.output_dir

    smtpd = DebuggingServer(('localhost', int(options.port)), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        smtpd.close()

if __name__ == '__main__':
    main()
