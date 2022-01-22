class Error:
    def __init__(self, ctx, message):
        self.ctx = ctx
        self.message = message

    def extract_error_details(self):
        token_source = self.ctx.start.getTokenSource()
        input_stream = token_source.inputStream
        line, column = self.ctx.start.line, self.ctx.start.column
        start, stop = self.ctx.start.start, self.ctx.stop.stop
        return line, column, input_stream.getText(start, stop)

    def __str__(self):
        line, column, text = self.extract_error_details()
        return f"'line: {line}:{column} '{text}' - {self.message}"


class ValidationError(Exception):
    pass


class PromQLSyntaxError(Exception):
    def __init__(self, recognizer, offending_symbol, line, column, msg, e):
        super().__init__(f"line: {line}:{column} {msg}")
        self.recognizer = recognizer
        self.offending_symbol = offending_symbol
        self.line = line
        self.column = column
        self.e = e
