import hashlib

class SHAChecker:
    def __init__(self, bytes_data1, bytes_data2):
        self.data1 = bytes_data1
        self.data2 = bytes_data2
        self.hash1 = hashlib.sha256(bytes_data1).hexdigest()
        self.hash2 = hashlib.sha256(bytes_data2).hexdigest()

    def compare_bytes_sha256(self):
        if self.hash1 == self.hash2:
            return True
        else:
            return False

    def new_data(self, bytes_data1, bytes_data2):
        self.data1 = bytes_data1
        self.data2 = bytes_data2
        self.hash1 = hashlib.sha256(bytes_data1).hexdigest()
        self.hash2 = hashlib.sha256(bytes_data2).hexdigest()

    def get_hash1(self):
        return self.hash1
    def get_hash2(self):
        return self.hash2