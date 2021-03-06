import sys

from dingus.ast_printer import AstPrinter
from dingus.error_handler import ErrorHandler
from dingus.parser import Parser
from dingus.scanner import Scanner

EX_OK = 0  # successful termination
EX__BASE = 64  # base value for error messages
EX_USAGE = 64  # command line usage error
EX_DATAERR = 65  # data format error
EX_NOINPUT = 66  # cannot open input
EX_NOUSER = 67  # addressee unknown
EX_NOHOST = 68  # host name unknown
EX_UNAVAILABLE = 69  # service unavailable
EX_SOFTWARE = 70  # internal software error
EX_OSERR = 71  # system error (e.g., can't fork)
EX_OSFILE = 72  # critical OS file missing
EX_CANTCREAT = 73  # can't create (user) output file
EX_IOERR = 74  # input/output error
EX_TEMPFAIL = 75  # temp failure; user is invited to retry
EX_PROTOCOL = 76  # remote error in protocol
EX_NOPERM = 77  # permission denied
EX_CONFIG = 78  # configuration error
EX__MA = 78  # maximum listed value


def run_file(path):
    with open(path, 'r') as lf:
        data = lf.read()
    error = ErrorHandler()
    scanner = Scanner(data, error)
    tokens = scanner.scan_tokens()

    if error.warning_count > 0 or error.error_count > 0:
        ec = error.error_count
        wc = error.warning_count
        print(f'{ec} error(s) and {wc} warning(s) occurred')

    if error.had_error:
        sys.exit(EX_DATAERR)

    parser = Parser(tokens, error)
    ast = parser.parse()

    if error.warning_count > 0 or error.error_count > 0:
        ec = error.error_count
        wc = error.warning_count
        print(f'{ec} error(s) and {wc} warning(s) occurred')

    if error.had_error:
        sys.exit(EX_DATAERR)

    print(AstPrinter().print(ast))


if len(sys.argv) != 2:
    print('Usage: dingus [script]')
    sys.exit(EX_USAGE)
elif len(sys.argv) == 2:
    run_file(sys.argv[1])
