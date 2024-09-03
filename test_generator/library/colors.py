class Colors:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_C = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def blue(message):
        return f'{Colors.OK_BLUE}{message}{Colors.END_C}'

    @staticmethod
    def error(message):
        return f'{Colors.FAIL}{message}{Colors.END_C}'

    @staticmethod
    def warning(message):
        return f'{Colors.WARNING}{message}{Colors.END_C}'

    @staticmethod
    def header(message):
        return f'{Colors.HEADER}{message}{Colors.END_C}'

    @staticmethod
    def success(message):
        return f'{Colors.OK_GREEN}{message}{Colors.END_C}'

    @staticmethod
    def bold(message):
        return f'{Colors.BOLD}{message}{Colors.END_C}'
