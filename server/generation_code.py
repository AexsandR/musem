from random import choice
import string



class Generation_code:
    def __init__(self):
        self.generated_codes = set()
    def get_code(self, lenght: int) -> int:
        while True:
            code = self.__generation_code(lenght)
            if not code in self.generated_codes and code[:3] != "000":
                self.generated_codes.add(code)
                return code

    def __generation_code(self, lenght: int) -> str:
        if lenght == 0:
            return ""

        return choice(string.digits) + self.__generation_code(lenght - 1)



