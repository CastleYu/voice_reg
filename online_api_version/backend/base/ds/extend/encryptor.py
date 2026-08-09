from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os


# 基类 Encryptor
class Encryptor:
    def encrypt(self, data):
        raise NotImplementedError("Subclasses should implement this method")

    def decrypt(self, data):
        raise NotImplementedError("Subclasses should implement this method")


# AES加密器类
class AESEncryptor(Encryptor):
    def __init__(self, key: bytes):
        if len(key) not in [16, 24, 32]:  # AES密钥必须为16, 24或32字节
            raise ValueError("Key length must be 16, 24, or 32 bytes.")
        self.key = key
        self.iv = os.urandom(16)  # 随机生成一个初始化向量（IV）

    def encrypt(self, data: str) -> str:
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        data_bytes = data.encode('utf-8')
        padded_data = pad(data_bytes, AES.block_size)  # 填充数据
        encrypted = cipher.encrypt(padded_data)
        return base64.b64encode(self.iv + encrypted).decode('utf-8')  # 返回带IV的Base64编码密文

    def decrypt(self, encrypted_data: str) -> str:
        encrypted_data = base64.b64decode(encrypted_data)
        iv = encrypted_data[:16]  # 提取初始化向量
        encrypted_message = encrypted_data[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(encrypted_message), AES.block_size)
        return decrypted.decode('utf-8')


# Base64编码器类
class Base64Encryptor(Encryptor):
    def encrypt(self, data: str) -> str:
        return base64.b64encode(data.encode('utf-8')).decode('utf-8')

    def decrypt(self, encrypted_data: str) -> str:
        return base64.b64decode(encrypted_data).decode('utf-8')


# 示例：如何使用这些加密器

if __name__ == "__main__":
    # 使用AES加密器
    aes_key = os.urandom(32)  # 生成一个32字节的AES密钥
    aes_encryptor = AESEncryptor(aes_key)
    encrypted_aes = aes_encryptor.encrypt("Hello, AES encryption!")
    print(f"AES Encrypted: {encrypted_aes}")
    decrypted_aes = aes_encryptor.decrypt(encrypted_aes)
    print(f"AES Decrypted: {decrypted_aes}")

    # 使用Base64加密器
    base64_encryptor = Base64Encryptor()
    encrypted_base64 = base64_encryptor.encrypt("Hello, Base64 encoding!")
    print(f"Base64 Encrypted: {encrypted_base64}")
    decrypted_base64 = base64_encryptor.decrypt(encrypted_base64)
    print(f"Base64 Decrypted: {decrypted_base64}")
