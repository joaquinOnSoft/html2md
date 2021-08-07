import socket

socket.setdefaulttimeout(4000)
#https://github.com/googleapis/google-api-python-client/issues/563#issuecomment-738363829
import getopt
import logging
import os
import sys

from html2md.HTML2md import HTML2md


def print_help():
    print('Convert an HTML file or folder (and its content) in a Markdown file')
    print('\nExecution:')
    print('\tHTML2mdCLI.py -s <input_file_or_folder> -d <destination_path>')
    print('where:')
    print('\t-h, --help: Print this help')
    print('\t-s, --source <source_path>: (Mandatory) source file or folder')
    print('\t-d, --dest <dest_path>: (Mandatory) destination file or folder')
    print('\t-u, --url: (Optional) Use the page title, header of level 1 or the last section of the '
          'URL as URL description (only when URL link a description are the same). NOTE: This option can be slow.')
    print('\t-t, --timeout <seconds>: (Optional) Timeout, in seconds, to use in link validation connections, '
          'e.g. "2" seconds. By default is unlimited')
    print('\t-m, --multiline : (Optional) Support for multiline content in table cells. (WARNING: Google Sites may '
          'use internal tables in HTML which may not seem tables for the user. Use under your own risk!)')


def main(argv):
    source = None
    destination = None
    url = False
    timeout = -1
    multiline = False

    # Initialize logging component
    # SEE: https://docs.python.org/3/howto/logging.html
    logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(lineno)d]%(filename)s: %(message)s',
                        filename='HTML2md.log',
                        filemode='w',
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('Started')

    try:
        opts, args = getopt.getopt(argv, "hs:d:t:um",
                                   ["help", "source=", "dest=", "timeout=", "url", "multiline"])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
        elif opt in ("-s", "--source"):
            source = arg
        elif opt in ("-d", "--dest"):
            destination = arg
        elif opt in ("-u", "--url"):
            url = True
        elif opt in ("-t", "--timeout"):
            if arg.isdigit():
                timeout = int(arg)
            else:
                print_help()
                sys.exit(f"Invalid timeout value: {arg}")

    if source and destination:
        if os.path.isfile(source) or \
                (os.path.isdir(source) and
                 os.path.isdir(destination)):

            parser = HTML2md()
            parser.process(source, destination, url, timeout, multiline)
        else:
            print("\nWARNING: Source and Destination must be both files or both folders\n")
            sys.exit(2)
    else:
        print_help()


if __name__ == "__main__":
    main(sys.argv[1:])
