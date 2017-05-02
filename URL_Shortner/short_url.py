
class ShortUrl():

    def __init__(self):
        self._alphabet = '23456789bcdfghjkmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ-_'
        self._base = len(self._alphabet)

    def encode(self, number):
        string = ''
        while number > 0:
            string = self._alphabet[number % self._base] + string
            number //= self._base
        return string

    def decode(self, string):
        number = 0
        for char in string:
            number = number * self._base + self._alphabet.index(char)
        return number
