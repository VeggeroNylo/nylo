"""
Contains the Parser class definition.
"""


class Parser:
    """Stores the code and keeps track of the character
    the parser are reading at.
    """

    def __init__(self, code, reading_at=0):
        """Initialize the class

        Args:
            code (str): the code string to parse
            reading_at (int): the character parser are reading
        """
        from nylo.tokens.struct import Struct
        self.code = list(f'({code}\n),\n\0')
        self.indent = 0
        self.parsed, self.parsing = [], [Struct()]
        self.reading_at = reading_at
        self.line, self.char = 1, 1

    @staticmethod
    def parsecode(code):
        parser = Parser(code)
        while parser.parsing:
            parser.avoid_whitespace()
            parser.parsing.pop().parse(parser)
            parser.avoid_whitespace()
        return parser.parsed.pop()

    def read(self):
        """Read the current character"""
        return self.code[self.reading_at]

    def move(self, todo=1):
        """Move {todo} characters on"""
        if self.read() == '\n':
            self.line += 1
            self.char = 1
        else:
            self.char += 1
        self.reading_at += 1
        if self.read() == '\0':
            raise SyntaxError('EOF while scanning.')
        if todo > 1:
            self.move(todo - 1)
        return self.code[self.reading_at - 1]

    def any_starts_with(self, starts):
        """Check if the reading_at character starts
        with any of the starts
        """
        for start in starts:
            if self.starts_with(start):
                return start
        return False

    def starts_with(self, string):
        """Check if the reading_at character starts
        with the given string
        """
        return ''.join(self.code).startswith(string, self.reading_at)

    def avoid_whitespace(self):
        """Makes two things: move on until first non-withespace
        character, but also insert a "(" if indented code is found,
        or a ")" if deindent is found. Also separates line on the
        with the same indent with ","
        """
        if self.starts_with('//'):
            while self.move() != '\n':
                pass
        while self.read() in ' \t':
            self.move()
        if self.read() == '\n':
            i = self.reading_at + 1
            while self.code[i] in '\t ':
                i += 1
            if self.code[i] == '\n':
                self.reading_at = i
                return self.avoid_whitespace()
            newindent = i - (self.reading_at + 1)
            if newindent <= self.indent:
                self.code.insert(i, ',')
            for y in range(abs(self.indent - newindent)):
                if newindent > self.indent:
                    self.code.insert(i, '(')
                elif newindent < self.indent:
                    self.code.insert(i, ')')
            self.move()
            self.indent = newindent

    def parse(self, *args):
        "Add tokens to be parsed."
        self.parsing.extend(args)

    def hasparsed(self, *args):
        "Add parsed tokens."
        self.parsed.extend(args)

    def getarg(self):
        "Get the last parsed token."
        return self.parsed.pop()
