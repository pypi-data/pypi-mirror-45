import pathlib


class DirtyReader:

    # BaseActions
    def _read_n_bytes(self, bs, num):
        blocks =[b'']*num
        for i in range(num):
            blocks[i] = self.__file.read(bs)
        if num == 1:
            blocks = blocks[0]
        return blocks

    def _n_bytes_to_int(self, bs, num, be=True, sign=False):
        if bs < 1 or bs > 8:
            raise ValueError('Illegal byte amount '+num+'. valid range is 1-8')
        end = 'big' if be else 'little'
        dbg = self.__read_n_bytes(bs, num)
        if num == 1:
            return int.from_bytes(dbg, byteorder=end, signed=sign)
        else:
            for i in range(num):
                dbg[i] = int.from_bytes(dbg[i], byteorder=end, signed=sign)
            return dbg

    # Constructor
    def __init__(self, p):
        p = pathlib.Path(p)
        if p.is_file():
            self.__file = open(str(p), 'rb')
            self.__file.seek(0)
            self.p = p.resolve()
        else:
            self.__file = None
            self.p = None

    def is_reader_valid(self): return self.__file is not None

    def read_qwords(self, amount):
        return self.__read_n_bytes(8, amount)

    def read_qword_ints(self, amount, be=True, sign=False):
        return self.__n_bytes_to_int(8, amount, be, sign)

    def read_septets(self, amount):
        return self.__read_n_bytes(7, amount)

    def read_septet_ints(self, amount, be=True, sign=False):
        return self.__n_bytes_to_int(7, amount, be, sign)

    def read_sextets(self, amount):
        return self.__read_n_bytes(6, amount)

    def read_sextet_ints(self, amount, be=True, sign=False):
        return self.__n_bytes_to_int(6, amount, be, sign)

    def read_quintets(self, amount):
        return self.__read_n_bytes(5, amount)

    def read_quintet_ints(self, amount, be=True, sign=False):
        return self.__n_bytes_to_int(5, amount, be, sign)

    def read_dwords(self, amount):
        return self.__read_n_bytes(4, amount)

    def read_dword_ints(self, amount, be=True, sign=False):
        return self.__n_bytes_to_int(4, amount, be, sign)

    def read_triplets(self, amount):
        return self.__read_n_bytes(3, amount)

    def read_triplet_ints(self, amount, be=True, sign=False):
        return self.__n_bytes_to_int(3, amount, be, sign)

    def read_words(self, amount):
        return self.__read_n_bytes(2, amount)

    def read_word_ints(self, amount, be=True, sign=False):
        return self.__n_bytes_to_int(2, amount, be, sign)

    def read_bytes(self, amount):
        return self.__read_n_bytes(1, amount)

    def read_byte_ints(self, amount, be=True, sign=False):
        return self.__n_bytes_to_int(1, amount, be, sign)

    def tell(self): return self.__file.tell()

    def seek(self, amount, mode): return self.__file.seek(amount, mode)

    def read_nt_string(self):
        sec = self.tell()
        b = self.dirty_bytes(1)
        string = ""
        while b != b"\x00":
            if b == b"":
                self.seek(sec, 0)
                raise OverflowError('Reached end of file. File reverted to previous state')
            string += b.decode()
            b = self.dirty_bytes(1)
        return string
    
    def pad_out(self):
        inset = self.__file.tell() % 4
        if inset != 0:
            self.dirty_bytes(4-inset)
        return 0 if inset == 0 else 4-inset

    def skip_qword(self):
        self.__file.seek(8, 1)

    def skip_septet(self):
        self.__file.seek(7, 1)

    def skip_sextet(self):
        self.__file.seek(6, 1)

    def skip_quintet(self):
        self.__file.seek(5, 1)

    def skip_dword(self):
        self.__file.seek(4, 1)

    def skip_triplet(self):
        self.__file.seek(3, 1)

    def skip_word(self):
        self.__file.seek(2, 1)
        
    def skip_byte(self):
        self.__file.seek(1, 1)

    def close(self):
        self.__file.close()
        self.__file = None
        self.p = None

    def dirty_bytes(self,amount):
        return self.__file.read(amount)

    def rebase(self, p):
        if p.is_file():
            self.close()
            self.__file = open(str(p), 'rb')
            self.p = p.resolve()
            return True
        else:
            return False
