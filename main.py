import sys


def decode_text(data):
    res = ''
    for i in range(len(data) // 8):
        char = data[i * 8: (i + 1) * 8]
        if char == '00000000':
            break
        char = int(char, 2)
        char = chr(char)
        res += char
    return res


class PVD:
    def __encode_text(self, data):
        res = ''
        for i in data:
            bin_symb = bin(ord(i))[2:]
            res += '0' * (8 - len(bin_symb)) + bin_symb
        return res

    def encode_to_img(self, data, img_file, result_file='res.bmp'):
        data = self.__encode_text(data)
        with open(img_file, mode='rb') as img, open(result_file, mode='wb') as res:
            res.write(img.read(54))
            for i in data:
                c1, c2 = img.read(1), img.read(1)
                if i == '1':
                    c1 = int.from_bytes(c1, sys.byteorder)
                    c2 = int.from_bytes(c2, sys.byteorder)
                    if 255 > c2 >= 0:
                        c2 += 1
                    elif c2 < 255:
                        c2 -= 1
                    res.write(c1.to_bytes(1, sys.byteorder))
                    res.write(c2.to_bytes(1, sys.byteorder))
                if i == '0':
                    res.write(c1)
                    res.write(c2)
            res.write(img.read())
            print(f'Encoding done, check {result_file}')

    def decode_img(self, orig_file, img_file):
        with open(img_file, mode='rb') as img, open(
                orig_file, mode='rb') as orig:
            img.seek(54)
            orig.seek(54)
            data = img.read()
            res = ''
            for byte in range(0, len(data), 2):
                c1, c2 = data[byte], data[byte + 1]
                o1, o2 = int.from_bytes(orig.read(1), sys.byteorder), int.from_bytes(orig.read(1), sys.byteorder)
                if abs(c1 - c2) == abs(o1 - o2):
                    res += '0'
                if abs(abs(c1 - c2) - abs(o1 - o2)) == 1:
                    res += '1'
            res = decode_text(res)
            print(res)


PVD().encode_to_img(input('Input text:\n'), img_file=input('Input filename:\n'))
PVD().decode_img(input('Input orig filename:\n'), input('Input filename with message:\n'))
