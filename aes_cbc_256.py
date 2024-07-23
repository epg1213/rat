from os import remove, listdir
from os.path import isfile, isdir
from random import choice

s_box={'encrypt': {'00': '63', '01': '7c', '02': '77', '03': '7b', '04': 'f2', '05': '6b', '06': '6f', '07': 'c5', '08': '30', '09': '01', '0a': '67', '0b': '2b', '0c': 'fe', '0d': 'd7', '0e': 'ab', '0f': '76', '10': 'ca', '11': '82', '12': 'c9', '13': '7d', '14': 'fa', '15': '59', '16': '47', '17': 'f0', '18': 'ad', '19': 'd4', '1a': 'a2', '1b': 'af', '1c': '9c', '1d': 'a4', '1e': '72', '1f': 'c0', '20': 'b7', '21': 'fd', '22': '93', '23': '26', '24': '36', '25': '3f', '26': 'f7', '27': 'cc', '28': '34', '29': 'a5', '2a': 'e5', '2b': 'f1', '2c': '71', '2d': 'd8', '2e': '31', '2f': '15', '30': '04', '31': 'c7', '32': '23', '33': 'c3', '34': '18', '35': '96', '36': '05', '37': '9a', '38': '07', '39': '12', '3a': '80', '3b': 'e2', '3c': 'eb', '3d': '27', '3e': 'b2', '3f': '75', '40': '09', '41': '83', '42': '2c', '43': '1a', '44': '1b', '45': '6e', '46': '5a', '47': 'a0', '48': '52', '49': '3b', '4a': 'd6', '4b': 'b3', '4c': '29', '4d': 'e3', '4e': '2f', '4f': '84', '50': '53', '51': 'd1', '52': '00', '53': 'ed', '54': '20', '55': 'fc', '56': 'b1', '57': '5b', '58': '6a', '59': 'cb', '5a': 'be', '5b': '39', '5c': '4a', '5d': '4c', '5e': '58', '5f': 'cf', '60': 'd0', '61': 'ef', '62': 'aa', '63': 'fb', '64': '43', '65': '4d', '66': '33', '67': '85', '68': '45', '69': 'f9', '6a': '02', '6b': '7f', '6c': '50', '6d': '3c', '6e': '9f', '6f': 'a8', '70': '51', '71': 'a3', '72': '40', '73': '8f', '74': '92', '75': '9d', '76': '38', '77': 'f5', '78': 'bc', '79': 'b6', '7a': 'da', '7b': '21', '7c': '10', '7d': 'ff', '7e': 'f3', '7f': 'd2', '80': 'cd', '81': '0c', '82': '13', '83': 'ec', '84': '5f', '85': '97', '86': '44', '87': '17', '88': 'c4', '89': 'a7', '8a': '7e', '8b': '3d', '8c': '64', '8d': '5d', '8e': '19', '8f': '73', '90': '60', '91': '81', '92': '4f', '93': 'dc', '94': '22', '95': '2a', '96': '90', '97': '88', '98': '46', '99': 'ee', '9a': 'b8', '9b': '14', '9c': 'de', '9d': '5e', '9e': '0b', '9f': 'db', 'a0': 'e0', 'a1': '32', 'a2': '3a', 'a3': '0a', 'a4': '49', 'a5': '06', 'a6': '24', 'a7': '5c', 'a8': 'c2', 'a9': 'd3', 'aa': 'ac', 'ab': '62', 'ac': '91', 'ad': '95', 'ae': 'e4', 'af': '79', 'b0': 'e7', 'b1': 'c8', 'b2': '37', 'b3': '6d', 'b4': '8d', 'b5': 'd5', 'b6': '4e', 'b7': 'a9', 'b8': '6c', 'b9': '56', 'ba': 'f4', 'bb': 'ea', 'bc': '65', 'bd': '7a', 'be': 'ae', 'bf': '08', 'c0': 'ba', 'c1': '78', 'c2': '25', 'c3': '2e', 'c4': '1c', 'c5': 'a6', 'c6': 'b4', 'c7': 'c6', 'c8': 'e8', 'c9': 'dd', 'ca': '74', 'cb': '1f', 'cc': '4b', 'cd': 'bd', 'ce': '8b', 'cf': '8a', 'd0': '70', 'd1': '3e', 'd2': 'b5', 'd3': '66', 'd4': '48', 'd5': '03', 'd6': 'f6', 'd7': '0e', 'd8': '61', 'd9': '35', 'da': '57', 'db': 'b9', 'dc': '86', 'dd': 'c1', 'de': '1d', 'df': '9e', 'e0': 'e1', 'e1': 'f8', 'e2': '98', 'e3': '11', 'e4': '69', 'e5': 'd9', 'e6': '8e', 'e7': '94', 'e8': '9b', 'e9': '1e', 'ea': '87', 'eb': 'e9', 'ec': 'ce', 'ed': '55', 'ee': '28', 'ef': 'df', 'f0': '8c', 'f1': 'a1', 'f2': '89', 'f3': '0d', 'f4': 'bf', 'f5': 'e6', 'f6': '42', 'f7': '68', 'f8': '41', 'f9': '99', 'fa': '2d', 'fb': '0f', 'fc': 'b0', 'fd': '54', 'fe': 'bb', 'ff': '16'}, 'decrypt': {'63': '00', '7c': '01', '77': '02', '7b': '03', 'f2': '04', '6b': '05', '6f': '06', 'c5': '07', '30': '08', '01': '09', '67': '0a', '2b': '0b', 'fe': '0c', 'd7': '0d', 'ab': '0e', '76': '0f', 'ca': '10', '82': '11', 'c9': '12', '7d': '13', 'fa': '14', '59': '15', '47': '16', 'f0': '17', 'ad': '18', 'd4': '19', 'a2': '1a', 'af': '1b', '9c': '1c', 'a4': '1d', '72': '1e', 'c0': '1f', 'b7': '20', 'fd': '21', '93': '22', '26': '23', '36': '24', '3f': '25', 'f7': '26', 'cc': '27', '34': '28', 'a5': '29', 'e5': '2a', 'f1': '2b', '71': '2c', 'd8': '2d', '31': '2e', '15': '2f', '04': '30', 'c7': '31', '23': '32', 'c3': '33', '18': '34', '96': '35', '05': '36', '9a': '37', '07': '38', '12': '39', '80': '3a', 'e2': '3b', 'eb': '3c', '27': '3d', 'b2': '3e', '75': '3f', '09': '40', '83': '41', '2c': '42', '1a': '43', '1b': '44', '6e': '45', '5a': '46', 'a0': '47', '52': '48', '3b': '49', 'd6': '4a', 'b3': '4b', '29': '4c', 'e3': '4d', '2f': '4e', '84': '4f', '53': '50', 'd1': '51', '00': '52', 'ed': '53', '20': '54', 'fc': '55', 'b1': '56', '5b': '57', '6a': '58', 'cb': '59', 'be': '5a', '39': '5b', '4a': '5c', '4c': '5d', '58': '5e', 'cf': '5f', 'd0': '60', 'ef': '61', 'aa': '62', 'fb': '63', '43': '64', '4d': '65', '33': '66', '85': '67', '45': '68', 'f9': '69', '02': '6a', '7f': '6b', '50': '6c', '3c': '6d', '9f': '6e', 'a8': '6f', '51': '70', 'a3': '71', '40': '72', '8f': '73', '92': '74', '9d': '75', '38': '76', 'f5': '77', 'bc': '78', 'b6': '79', 'da': '7a', '21': '7b', '10': '7c', 'ff': '7d', 'f3': '7e', 'd2': '7f', 'cd': '80', '0c': '81', '13': '82', 'ec': '83', '5f': '84', '97': '85', '44': '86', '17': '87', 'c4': '88', 'a7': '89', '7e': '8a', '3d': '8b', '64': '8c', '5d': '8d', '19': '8e', '73': '8f', '60': '90', '81': '91', '4f': '92', 'dc': '93', '22': '94', '2a': '95', '90': '96', '88': '97', '46': '98', 'ee': '99', 'b8': '9a', '14': '9b', 'de': '9c', '5e': '9d', '0b': '9e', 'db': '9f', 'e0': 'a0', '32': 'a1', '3a': 'a2', '0a': 'a3', '49': 'a4', '06': 'a5', '24': 'a6', '5c': 'a7', 'c2': 'a8', 'd3': 'a9', 'ac': 'aa', '62': 'ab', '91': 'ac', '95': 'ad', 'e4': 'ae', '79': 'af', 'e7': 'b0', 'c8': 'b1', '37': 'b2', '6d': 'b3', '8d': 'b4', 'd5': 'b5', '4e': 'b6', 'a9': 'b7', '6c': 'b8', '56': 'b9', 'f4': 'ba', 'ea': 'bb', '65': 'bc', '7a': 'bd', 'ae': 'be', '08': 'bf', 'ba': 'c0', '78': 'c1', '25': 'c2', '2e': 'c3', '1c': 'c4', 'a6': 'c5', 'b4': 'c6', 'c6': 'c7', 'e8': 'c8', 'dd': 'c9', '74': 'ca', '1f': 'cb', '4b': 'cc', 'bd': 'cd', '8b': 'ce', '8a': 'cf', '70': 'd0', '3e': 'd1', 'b5': 'd2', '66': 'd3', '48': 'd4', '03': 'd5', 'f6': 'd6', '0e': 'd7', '61': 'd8', '35': 'd9', '57': 'da', 'b9': 'db', '86': 'dc', 'c1': 'dd', '1d': 'de', '9e': 'df', 'e1': 'e0', 'f8': 'e1', '98': 'e2', '11': 'e3', '69': 'e4', 'd9': 'e5', '8e': 'e6', '94': 'e7', '9b': 'e8', '1e': 'e9', '87': 'ea', 'e9': 'eb', 'ce': 'ec', '55': 'ed', '28': 'ee', 'df': 'ef', '8c': 'f0', 'a1': 'f1', '89': 'f2', '0d': 'f3', 'bf': 'f4', 'e6': 'f5', '42': 'f6', '68': 'f7', '41': 'f8', '99': 'f9', '2d': 'fa', '0f': 'fb', 'b0': 'fc', '54': 'fd', 'bb': 'fe', '16': 'ff'}}

def hexbyte(byte: int):
    h=hex(byte)[2:]
    if len(h)<2:
        h=f"0{h}"
    return h

def gmul(a, b):
    match b:
        case 1:
            return a
        case 2:
            return ((a << 1) ^ (0x1b & ((a >> 7) * 0xff))) & 0xff
        case 3:
            return gmul(a, 2) ^ a
        case 9:
            return gmul(gmul(gmul(a, 2), 2), 2) ^ a
        case 11:
            return gmul(gmul(gmul(a, 2), 2), 2) ^ gmul(a, 2) ^ a
        case 13:
            return gmul(gmul(gmul(a, 2), 2), 2) ^ gmul(gmul(a, 2), 2) ^ a
        case 14:
            return gmul(gmul(gmul(a, 2), 2), 2) ^ gmul(gmul(a, 2), 2) ^ gmul(a, 2)
        case _:
            return 0

class AES_CBC_256:
    def __init__(self, key: bytes):
        if not len(key)==32:
            raise Exception('Key must be 32 bytes.')
        self.s_box=s_box
        self.key=key
        self.rounded_key=self.RoundKey()

    def generate_key():
        key=''.join([choice("0123456789abcdef") for _ in range(64)])
        return bytes.fromhex(key)

    def save_key(key: bytes, filename="AES_CBC_256.key"):
        if not len(key)==32:
            raise Exception('Key must be 32 bytes.')
        with open(filename, "wb") as file:
            file.write(key)
    
    def load_key(filename="AES_CBC_256.key"):
        if not isfile(filename):
            raise Exception(f"No {filename} file found.")
        with open(filename, "rb") as file:
            text=file.read()
        if len(text)!=32:
            raise Exception('Key must be 32 bytes.')
        return text


    def generate_iv():
        key=''.join([choice("0123456789abcdef") for _ in range(32)])
        return bytes.fromhex(key)
    
    def plaintext_to_array(data: bytes):
        batch_size=16
        arr=[]
        counter=0
        to_add=""
        for byte in data:
            to_add+=hexbyte(byte)
            counter+=1
            if counter%batch_size==0:
                arr.append(bytes.fromhex(to_add))
                to_add=""
        to_add+="80"
        counter=len(to_add)
        while counter<batch_size*2:
            to_add+="00"
            counter+=2
        arr.append(bytes.fromhex(to_add))
        return arr

    def plaintext_from_array(arr: list):
        data=b''.join(arr)
        while data[-1:]==b'\x00':
            data=data[:-1]
        return data[:-1]
    
    def cipher_to_array(data: bytes):
        batch_size=16
        arr=[]
        counter=0
        to_add=""
        for byte in data:
            to_add+=hexbyte(byte)
            counter+=1
            if counter%batch_size==0:
                arr.append(bytes.fromhex(to_add))
                to_add=""
        if len(to_add)!=0:
            arr.append(bytes.fromhex(to_add))
        return arr

    def ByteSub(self, block: bytes, inverted=False):
        encdec='encrypt'
        if inverted:
            encdec='decrypt'
        out=""
        for byte in block:
            out+=self.s_box[encdec][hexbyte(byte)]
        return bytes.fromhex(out)
    
    def ShiftRow(self, block: bytes, inverted=False):
        if inverted:
            index_list=[0, 1, 2, 3, 7, 4, 5, 6, 10, 11, 8, 9, 13, 14, 15, 12]
        else:
            index_list=[0, 1, 2, 3, 5, 6, 7, 4, 10, 11, 8, 9, 15, 12, 13, 14]
        out=""
        for i in index_list:
            out+=hexbyte(block[i])
        return bytes.fromhex(out)
        
    def MixColumns(self, block: bytes, inverted=False):
        A=[i for i in block]
        C={}
        if inverted:
            for i in range(4):
                C[i]=gmul(A[i], 14) ^ gmul(A[i+4], 11) ^ gmul(A[i+8], 13) ^ gmul(A[i+12], 9)
                C[i+4]=gmul(A[i], 9) ^ gmul(A[i+4], 14) ^ gmul(A[i+8], 11) ^ gmul(A[i+12], 13)
                C[i+8]=gmul(A[i], 13) ^ gmul(A[i+4], 9) ^ gmul(A[i+8], 14) ^ gmul(A[i+12], 11)
                C[i+12]=gmul(A[i], 11) ^ gmul(A[i+4], 13) ^ gmul(A[i+8], 9) ^ gmul(A[i+12], 14)
        else:
            for i in range(4):
                C[i]=gmul(A[i], 2) ^ gmul(A[i+4], 3) ^ gmul(A[i+8], 1) ^ gmul(A[i+12], 1)
                C[i+4]=gmul(A[i], 1) ^ gmul(A[i+4], 2) ^ gmul(A[i+8], 3) ^ gmul(A[i+12], 1)
                C[i+8]=gmul(A[i], 1) ^ gmul(A[i+4], 1) ^ gmul(A[i+8], 2) ^ gmul(A[i+12], 3)
                C[i+12]=gmul(A[i], 3) ^ gmul(A[i+4], 1) ^ gmul(A[i+8], 1) ^ gmul(A[i+12], 2)
        out=''
        for i in range(16):
            out+=hexbyte(C[i])
        return bytes.fromhex(out)
    
    def AddKey(self, block, key_rounded):
        return bytes(a ^ b for a, b in zip(block, key_rounded))
    
    def RotWord(self, block):
        return bytes(list(block[1:])+[block[0]])

    def RoundKey(self):
        words=[]
        word=[]
        for i in range(len(self.key)):
            word.append(self.key[i])
            if i%4==3:
                words.append(bytes(word))
                word=[]
        rcon=[bytes.fromhex('01000000'), bytes.fromhex('02000000'), bytes.fromhex('04000000'), bytes.fromhex('08000000'), bytes.fromhex('10000000'), bytes.fromhex('20000000'), bytes.fromhex('40000000')]
        new_words=words
        for i in range(52):
            word=new_words[i+7]
            if i%4==0:
                word=self.ByteSub(word)
                if i%8==0:
                    word=bytes(a ^ b for a, b in zip(self.RotWord(word), rcon[i//8]))
            word=bytes(a ^ b for a, b in zip(word, new_words[i]))
            new_words.append(word)
        words=[]
        to_add=b''
        i=0
        for word in new_words:
            to_add+=word
            if i%4==3:
                words.append(to_add)
                to_add=b''
            i+=1
        return words
    
    def enc_block(self, block: bytes):
        i=0
        block=self.AddKey(block, self.rounded_key[i])
        while i<13:
            block=self.ByteSub(block)
            block=self.ShiftRow(block)
            block=self.MixColumns(block)
            i+=1
            block=self.AddKey(block, self.rounded_key[i])
        block=self.ByteSub(block)
        block=self.ShiftRow(block)
        i+=1
        block=self.AddKey(block, self.rounded_key[i])
        return block

    def encrypt(self, plaintext: bytes):
        arr=AES_CBC_256.plaintext_to_array(plaintext)
        iv=AES_CBC_256.generate_iv()
        ciphertext=iv
        for block in arr:
            xored=bytes(a ^ b for a, b in zip(block, iv))
            cipherblock=self.enc_block(xored)
            iv=cipherblock
            ciphertext+=cipherblock
        return ciphertext
    
    def encrypt_file(self, filename):
        if not isfile(filename):
            raise Exception(f"File not found: {filename}")
        with open(filename, 'rb') as file:
            text=self.encrypt(file.read())
        with open(f"{filename}.hanged", 'wb') as file:
            file.write(text)
        remove(filename)

    def encrypt_dir(self, dirname):
        if not isdir(dirname):
            raise Exception(f"Directory not found: {dirname}")
        for item in listdir(dirname):
            if isdir(f"{dirname}/{item}"):
                self.encrypt_dir(f"{dirname}/{item}")
            elif isfile(f"{dirname}/{item}"):
                self.encrypt_file(f"{dirname}/{item}")
    
    def dec_block(self, block: bytes):
        i=14
        block=self.AddKey(block, self.rounded_key[i])
        block=self.ShiftRow(block, True)
        block=self.ByteSub(block, True)
        while i>1:
            i-=1
            block=self.AddKey(block, self.rounded_key[i])
            block=self.MixColumns(block, True)
            block=self.ShiftRow(block, True)
            block=self.ByteSub(block, True)
        i-=1
        block=self.AddKey(block, self.rounded_key[i])
        return block

    def decrypt(self, ciphertext: bytes):
        try:
            ciphertext=AES_CBC_256.cipher_to_array(ciphertext)
            max_len=len(ciphertext)
            arr=[]
            for i in range(max_len-1):
                block=self.dec_block(ciphertext[max_len-i-1])
                last=ciphertext[max_len-i-2]
                xored=bytes(a ^ b for a, b in zip(block, last))
                arr.insert(0, xored)
            return AES_CBC_256.plaintext_from_array(arr)
        except:
            return b''
    
    def decrypt_file(self, filename):
        if filename.endswith('.hanged'):
            filename=filename[:-7]
        if not isfile(f"{filename}.hanged"):
            return
        with open(f"{filename}.hanged", 'rb') as file:
            text=self.decrypt(file.read())
        with open(filename, 'wb') as file:
            file.write(text)
        remove(f"{filename}.hanged")

    def decrypt_dir(self, dirname):
        if not isdir(dirname):
            raise Exception(f"Directory not found: {dirname}")
        for item in listdir(dirname):
            if isdir(f"{dirname}/{item}"):
                self.decrypt_dir(f"{dirname}/{item}")
            elif isfile(f"{dirname}/{item}"):
                self.decrypt_file(f"{dirname}/{item}")
