class ShortUrl:

    def __init__(self):
        self._alphabet = 'jkmnpqrstvwxyzBCDFGH23456789bcdfghJKLMNPQRSTVWXYZ-_'
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
            if char not in self._alphabet:
                # to avoid errors in creation of custom url
                return 999999999999
            number = number * self._base + self._alphabet.index(char)
        return number


if __name__ == '__main__':
    print(ShortUrl().decode("asdasd"))
    print(ShortUrl().encode(8989898))
