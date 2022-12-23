#!/usr/bin/env python3

"""
© 2022 ROMAIN DUDEK
This modules provides the ability to colorprint in terminal
via cprint() function. cprint() function uses the § symbol
to identify the coloured zones.

Full syntax is described in the README of this project

It uses ANSI codes : http://en.wikipedia.org/wiki/ANSI_escape_code
"""

class CodesGen:

    def __init__(self):
        # Generates the classes according to the codes
        for prop in dir(self):
            if not prop.startswith("_"):
                value = getattr(self, prop)
                setattr(self, prop, self.__codes_convert(value))
    
    def __codes_convert(self, code):
        return f"\033[{str(code)}m"

class ANSI(CodesGen):
    # Standard codes Front
    BLACK_FRONT     = 30
    RED_FRONT       = 31
    GREEN_FRONT     = 32
    YELLOW_FRONT    = 33
    BLUE_FRONT      = 34
    MAGENTA_FRONT   = 35
    CYAN_FRONT      = 36
    WHITE_FRONT     = 37
    # Standard codes Back
    BLACK_BACK      = 40
    RED_BACK        = 41
    GREEN_BACK      = 42
    YELLOW_BACK     = 43
    BLUE_BACK       = 44
    MAGENTA_BACK    = 45
    CYAN_BACK       = 46
    WHITE_BACK      = 47
    # Not standard Front but works most of the times
    BLACK_LIGHT_FRONT   = 90
    RED_LIGHT_FRONT     = 91
    GREEN_LIGHT_FRONT   = 92
    YELLOW_LIGHT_FRONT  = 93
    BLUE_LIGHT_FRONT    = 94
    MAGENTA_LIGHT_FRONT = 95
    CYAN_LIGHT_FRONT    = 96
    WHITE_LIGHT_FRONT   = 97
    # Not standard Back but works most of the times
    BLACK_LIGHT_BACK    = 100
    RED_LIGHT_BACK      = 101
    GREEN_LIGHT_BACK    = 102
    YELLOW_LIGHT_BACK   = 103
    BLUE_LIGHT_BACK     = 104
    MAGENTA_LIGHT_BACK  = 105
    CYAN_LIGHT_BACK     = 106
    WHITE_LIGHT_BACK    = 107
    # Reset
    RESET      = 0

StyleCode   = ANSI()


class CPrint:

    DEFAULT_ALERT_CODES = {
        'SUCCESS'    : 'GREEN',
        'INFO'      : 'CYAN',
        'WARNING'   : 'YELLOW',
        'DANGER'    : 'MAGENTA_LIGHT',
        'ERROR'     : 'RED',
        #Short tags
        '#S'        : 'GREEN',
        '#I'        : 'CYAN',
        '#W'        : 'YELLOW',
        '#D'        : 'MAGENTA_LIGHT',
        '#E'        : 'RED',
    }

    SUFFIX_DICT = {
        '-'         : '_FRONT',
        '_'         : '_BACK'
    }

    def __init__(self, contentString: str):
        self.initialContentString = contentString
        self.outputString = self.initialContentString
        self.outputString = self.__codes_gen()
    
    def __get_alert_code_and_string(self, rawString: str):
        for code in list(self.DEFAULT_ALERT_CODES.keys()):
            if rawString.startswith(f'_{code}') or rawString.startswith(f'-{code}'):
                return rawString[:len(code)+1], rawString[len(code)+1:]
        return False
        
    def __codes_gen(self):
        # split initialContentString
        splittedStrings: list = self.__split_string()
        if len(splittedStrings) == 1:
            return self.initialContentString
        elif len(splittedStrings) >= 2:
            for i, rawString in enumerate(splittedStrings, 0):
                if (i+1) % 2 == 0:
                    splittedString = self.__get_alert_code_and_string(rawString)
                    if splittedString:
                        splittedStrings[i] = self.__split_start_Code(splittedString)
                        if len(splittedStrings) > (i+1):
                            splittedStrings[i+1] = f"{StyleCode.RESET}{splittedStrings[i+1]}"
                    else:
                        splittedStrings[i] = f"§{splittedStrings[i]}"
            return f"{''.join(splittedStrings)}{StyleCode.RESET}"
    
    def __split_start_Code(self, splittedString):
        rawCode, textString = splittedString
        suffixCode = self.SUFFIX_DICT[f"{rawCode[:1]}"]
        code = f"{self.DEFAULT_ALERT_CODES[rawCode[1:]]}{suffixCode}"
        return (f"{getattr(StyleCode, code)}{textString}")

    def __split_string(self):
        return self.initialContentString.split("§")
        
def cprint(contentString, **kwargs):
    newprint = CPrint(contentString)
    print(newprint.outputString, **kwargs)
