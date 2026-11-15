import json
import os

ALGORITHMS = ("p-lsb", "e-lsb", "er-lsb")

class MetaHandler:
    def __init__(self, meta_path):
        self.algorithm = "null"
        self.source = "null"
        self.message = "null"
        self.password = "null"
        self.embedded_message_file = "null"
        self.percent1 = "null"
        self.percent2 = "null"
        self.meta = {}

        self.open_meta(meta_path)

    def open_meta(self, meta_path):
        with open(meta_path, 'r', encoding='utf-8') as f:
            self.meta = json.load(f)
        if "algorithm" in self.meta:
            self.algorithm = self.meta["algorithm"]
        else:
            raise Exception("Algorithm not found in meta.json")

        if self.algorithm not in ALGORITHMS:
            raise Exception("incorrect algorithm in meta.json")

        if "source" in self.meta:
            self.source = self.meta["source"]
        else:
            raise Exception("Source not found in meta.json")

        if "message" in self.meta:
            self.message = self.meta["message"]
        else:
            raise Exception("Message not found in meta.json")


        if "password" in self.meta:
            self.password = self.meta["password"]
        elif self.algorithm != "p-lsb":
            raise Exception("Password not found in meta.json")


        if "embedded_message_file" in self.meta:
            self.embedded_message_file = self.meta["embedded_message_file"]
        else:
            file_path = "../images/embededMessageFiles/"+self.algorithm+"_stego_file_"
            i = 0
            while os.path.isfile(file_path + str(i) + ".png"):
                i += 1
            self.embedded_message_file = file_path + str(i) + ".png"

        if "percent1" in self.meta:
            self.percent1 = self.meta["percent1"]
        else:
            self.percent1 = "0.01"
        if "percent2" in self.meta:
            self.percent2 = self.meta["percent2"]
        else:
            self.percent2 = "0.05"
