import argparse
import asyncore
import logging
import os
import smtpd
import sys
import time

try:
    from pync import Notifier
    notifier = Notifier
except ImportError:
    notifier = None

output_dir = None


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


class DebuggingServer(smtpd.DebuggingServer):
    def __init__(self, localaddr, remoteaddr, log_to_stdout=True):
        global output_dir
        self.path = output_dir
        self.log_to_stdout = log_to_stdout
        smtpd.DebuggingServer.__init__(self, localaddr, remoteaddr)

    def process_message(
        self, peer, mailfrom, rcpttos, data, mail_options=[], rcpt_options=[]
    ):
        if self.log_to_stdout:
            smtpd.DebuggingServer.process_message(self, peer, mailfrom, rcpttos, data)
            sys.stdout.flush()
        if self.path is None:
            return
        for addr in rcpttos:
            path = os.path.join(self.path, addr)
            if not os.path.exists(path):
                os.makedirs(path)
            dest = getUniqueFilename(path, "eml")
            with open(dest, "wb") as f:
                f.write(data)

        if notifier:
            notifier.notify(data, title=rcpttos, execute="open -a TextEdit " + dest)


def main(args=sys.argv[1:]):
    """Main function called by `mailmock` command.
    """
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
    global output_dir
    output_dir = options.output_dir

    smtpd = DebuggingServer(("0.0.0.0", int(options.port)), None, options.log_to_stdout)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        smtpd.close()


if __name__ == "__main__":
    main()
