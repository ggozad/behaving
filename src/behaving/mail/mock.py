# encoding: utf-8

import argparse
import logging
import os
import sys
import time

from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Debugging

try:
    from pync import Notifier

    notifier = Notifier
except ImportError:
    notifier = None


def getUniqueFilename(recipient_dir, ext="tmp"):
    filename = time.strftime("%Y-%m-%d-%H%M%S", time.gmtime(time.time()))
    dest = os.path.join(recipient_dir, f"{filename}.{ext}")
    i = 0
    while os.path.isfile(dest):
        i += 1
        if i > 1000:
            raise IOError(f"Tried too many filenames like: {dest}")
        fname = filename + "_" + str(i)
        dest = os.path.join(recipient_dir, f"{fname}.{ext}")

    return dest


class DebuggingHandler(Debugging):
    def __init__(self, output_dir, log_to_stdout=True):
        self.path = output_dir
        self.log_to_stdout = log_to_stdout
        super().__init__(sys.stdout)

    async def handle_DATA(self, server, session, envelope):
        rcpttos = envelope.rcpt_tos
        data = envelope.content
        print(f"Received email with data {data}")
        if self.log_to_stdout:
            result = super().handle_DATA(server, session, envelope)
            sys.stdout.flush()
        else:
            result = '250 Message accepted for delivery'
        if self.path:
            for addr in rcpttos:
                path = os.path.join(self.path, addr)
                if not os.path.exists(path):
                    os.makedirs(path)
                dest = getUniqueFilename(path, "eml")
                with open(dest, "wb") as f:
                    f.write(data)

            if notifier:
                notifier.notify(data, title=rcpttos, execute="open -a TextEdit " + dest)

        print(f"Returning email result: {result}")
        return result


def main(args=sys.argv[1:]):
    """Main function called by `mailmock` command."""
    parser = argparse.ArgumentParser(description="Mail mock server")

    parser.add_argument("-p", "--port", default="8025", help="The port to use")

    parser.add_argument(
        "-o",
        "--output_dir",
        default=None,
        required=True,
        help="Directory where to dump the mail.",
    )
    parser.add_argument(
        "-n",
        "--no-stdout",
        dest="log_to_stdout",
        default=True,
        action="store_false",
        required=False,
        help="Don't log received mail to stdout",
    )
    options = parser.parse_args(args=args)

    if not os.path.exists(options.output_dir):
        try:
            os.mkdir(options.output_dir)
        except OSError:
            logging.error("Output directory could not be created")

    controller = Controller(DebuggingHandler(options.output_dir, options.log_to_stdout), hostname="0.0.0.0", port=int(options.port))
    controller.start()
    try:
        while True:
            time.sleep(999999999)
    except KeyboardInterrupt:
        print("Stopping mail mock...")
        controller.stop()


if __name__ == "__main__":
    main()
