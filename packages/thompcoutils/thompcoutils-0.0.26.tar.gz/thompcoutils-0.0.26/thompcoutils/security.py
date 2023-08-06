import base64
import argparse


class Security:
    def __init__(self, aes_key):
        self.aes_key = aes_key

    def encode(self, clear):
        if self.aes_key is None:
            return clear
        enc = []
        for i in range(len(clear)):
            key_c = self.aes_key[i % len(self.aes_key)]
            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc))

    def decode(self, enc):
        if self.aes_key is None:
            return enc
        dec = []
        enc = base64.urlsafe_b64decode(enc)
        for i in range(len(enc)):
            key_c = self.aes_key[i % len(self.aes_key)]
            dec_c = chr((256 + enc[i] - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)


def main():
    parser = argparse.ArgumentParser(description="Encrypts/Decrypts a string",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--key",
                        required=True,
                        help="AES key to use for encryption")
    parser.add_argument("--value",
                        required=True,
                        help="value to encrypt or decrypt")
    parser.add_argument("--dir",
                        default="encrypt",
                        choices=["encrypt", "decrypt"],
                        help="Direction of encryption")
    args = parser.parse_args()
    sec = Security(args.key)
    if args.dir == "encrypt":
        print(sec.encode(args.value))
    else:
        print(sec.decode(args.value))


if __name__ == '__main__':
    main()
