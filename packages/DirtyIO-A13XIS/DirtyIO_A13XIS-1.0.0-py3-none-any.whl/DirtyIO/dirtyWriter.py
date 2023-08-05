import pathlib


class DirtyWriter:
    # BaseActions
    def write_bytes(self, bts):
        self.__file.write(bts)

    def write_ints(self, blocks, be=True, sign=False):
        end = 'big' if be else 'little'
        self.write_bytes(blocks.to_bytes(4, byteorder=end, signed=sign))

    # Constructor
    def __init__(self, p):
        p = pathlib.Path(p)
        if p.parent.is_dir():
            self.__file = open(str(p), 'wb')
            self.p = p.resolve()
        else:
            self.__file = None
            self.p = None

    def is_writer_valid(self):
        return self.__file is not None

    # def tell(self):
    #    return self.__file.tell()

    # def seek(self, amount, mode):
    #    return self.__file.seek(amount, mode)

    def write_bytes_as_nt_string(self,bs):
        self.__write_bytes(bs+b'\x00')

    def close(self):
        self.__file.flush()
        self.__file.close()
        self.__file = None
        self.p = None

    def rebase(self, p):
        if p.is_file():
            self.close()
            self.__file = open(str(p), 'rb')
            self.p = p.resolve()
            return True
        else:
            return False