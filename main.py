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
    def __init__(self, text_file, img_file, result_file='res.bmp'):
        self.__text_file = text_file
        self.__img_file = img_file
        self.__result_file = result_file
        self.__data = self.__encode_text()

    def __encode_text(self):
        with open(self.__text_file, mode='r', encoding='utf8') as f:
            res = ''
            text = f.read()
            for i in text:
                bin_symb = bin(ord(i))[2:]
                res += '0' * (8 - len(bin_symb)) + bin_symb
        return res

    def encode_to_img(self):
        with open(self.__img_file, mode='rb') as img, open(self.__result_file, mode='wb') as res:
            res.write(img.read(54))
            for i in self.__data:
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

    def decode_img(self, orig_file):
        with open(self.__img_file, mode='rb') as img, open(
                self.__result_file, mode='w', encoding='utf8') as res_file, open(
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
            res_file.write(res)


text = PVD('text.txt', 'test_img.bmp')
text.encode_to_img()
decode = PVD(img_file='res.bmp', result_file='output.txt', text_file='text.txt')
decode.decode_img('test_img.bmp')
