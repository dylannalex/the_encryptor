import base_conversor as bc


class Encryptor:
    def __init__(self, password=None, pin=None):
        '''
        ### PARAMS ###

        password:       [str]
        pin:            [int]

        ### WARNINGS ###

        If hexa is true while encrypting, hexa must be true for decrypting!
        '''
        self.password = password
        self.pin = str(pin)

    @property
    def pin_values(self):
        return [ord(i) for i in self.pin]

    @property
    def password_values(self):
        return [ord(i) for i in self.password]

    def encrypt(self, txt):
        key = self._key(len(txt))
        encrypted = []
        for i in range(len(txt)):
            letter_value = ord(txt[i])
            pass_value = ord(self.password[i % len(self.password)])

            if key[i] % 2 == 0 or pass_value % 2 == 0:
                sign = -1
            else:
                sign = 1
            encrypted.append(
                (sign * (letter_value + key[i] + pass_value) - sum(self.password_values)))

        return tuple([bc.decimal_to_hexa(i, 1) for i in encrypted])

    def decrypt(self, enc_list):
        '''
        enc_list:    [list/tuple]
        '''
        key = self._key(len(enc_list))
        encrypted = [bc.hexa_to_decimal(i, 1) for i in enc_list]
        decrypted = []
        for i in range(len(encrypted)):

            pass_value = ord(self.password[i % len(self.password)])

            if key[i] % 2 == 0 or pass_value % 2 == 0:
                sign = -1
            else:
                sign = 1

            letter_value = sign * (encrypted[i] + sum(self.password_values))\
                - (key[i] + pass_value)
            decrypted.append(chr(letter_value))

        return ''.join(decrypted)

    def _key(self, len_txt):
        key = []
        for i in range(1, len_txt + 1):
            x = self.password_values[i % len(self.password_values)]
            y = self.pin_values[i % len(self.pin_values)]
            if x % 2 == 0:
                key.append((x + i) * y)

            elif y % 2 == 0:
                key.append((y + i) * x)

            else:
                key.append((x + y) * i)
        return key
