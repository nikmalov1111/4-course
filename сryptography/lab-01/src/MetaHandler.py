import json
import os

ALGORITHMS = ("stream", "aes-ctr", "aes-ecb")
ACTIONS = ("encrypt", "decrypt")
default_png_encrypted_path = "../images/encrypted/"
default_png_decrypted_path = "../images/decrypted/"



class MetaHandler:
    def __init__(self, meta_path):
        self.action = "null"
        self.algorithm = "null"
        self.source = "null"
        self.nonce = "null"
        self.salt = "null"
        self.decrypted_path = "null"
        self.encrypted_path = "null"
        self.seed = "null"
        self.secret_key = "null"
        self.meta_for_decrypt = "null"


        self.meta = {}
        self.open_meta(meta_path)

    def open_meta(self, meta_path):
        with open(meta_path, 'r', encoding='utf-8') as f:
            self.meta = json.load(f)
        if ("action" in self.meta) and (self.meta["action"] in ACTIONS):
            self.action = self.meta["action"]
        else:
            raise Exception(f"action в {meta_path} указано неверно или не существует")

        if self.action == "decrypt":
            if ("meta_for_decrypt" in self.meta) and (os.path.isfile(self.meta["meta_for_decrypt"])):
                self.meta_for_decrypt = self.meta["meta_for_decrypt"]
            else:
                raise Exception(f"meta_for_decrypt в {meta_path} указан неверно или не существует")



        if ("algorithm" in self.meta) and (self.meta["algorithm"] in ALGORITHMS):
            self.algorithm = self.meta["algorithm"]
        else:
            raise Exception(f"algorithm в {meta_path} указан неверно или не существует")




        if self.algorithm == "stream":
            if ("seed" in self.meta) and (self.meta["seed"].isdigit()):
                self.seed = int(self.meta["seed"])
            else:
                raise Exception(f"seed в {meta_path} не указан")
        else:
            if "secret_key" in self.meta:
                self.secret_key = self.meta["secret_key"]
            else:
                raise Exception(f"secret в {meta_path} не указан")



        if ("source" in self.meta) and (os.path.isfile(self.meta["source"])):
            self.source = self.meta["source"]
        else:
            raise Exception("source в {meta_path} указан неверно или не существует")



        if "nonce" in self.meta:
            self.nonce = self.meta["nonce"]

        if "salt" in self.meta:
            self.salt = self.meta["salt"]

        if ("encrypted_path" in self.meta) and (self.meta["encrypted_path"] != "null"):
            self.encrypted_path = self.meta["encrypted_path"]
        else:
            self.encrypted_path = default_png_encrypted_path + self.algorithm + "_png_encrypted.png"



        if ("decrypted_path" in self.meta) and (self.meta["decrypted_path"] != "null"):
            self.decrypted_path = self.meta["decrypted_path"]
        else:
            self.decrypted_path = default_png_decrypted_path + self.algorithm + "_png_decrypted.png"


