def red(text):
    return color(text, 1)


def color(text, value=0):
    return '\u001b[38;5;%im%s\u001b[0m' % (value, text)


def green(text):
    return color(text, 3)


def blue(text):
    return color(text, 69)


def yellow(text):
    return color(text, 226)


class ErrorHandler(object):

    def __init__(self) -> None:
        self.had_error = False
        self.had_runtime_error = False
        self.warning_count = 0
        self.error_count = 0

    def scanner_error(self, line, message):
        self._report(line, '', message, False)

    # def token_error(self, token, message, warning=False, after=False):
    #     if token.type == TokenType.EOF:
    #         self._report(token.line, " at end", message, warning)
    #     elif after:
    #         self._report(token.line, f' after \'{token.lexeme}\'', message, warning)
    #     else:
    #         self._report(token.line, f' at \'{token.lexeme}\'', message, warning)
    #
    # def prompt_error(self, token, message):
    #     self.had_error = True
    #
    # def runtime_error(self, error):
    #     print(red(f'[RuntimeError at line {error.token.line}] {error.message}'))
    #     self.had_runtime_error = True

    def _report(self, line, where, message, warning):
        level = 'Error'
        color_func = red
        if warning:
            level = 'Warning'
            color_func = yellow
        print(color_func(f'[line {line}] {level}{where}: {message}'))
        if not warning:
            self.had_error = True
            self.error_count += 1
        else:
            self.warning_count += 1