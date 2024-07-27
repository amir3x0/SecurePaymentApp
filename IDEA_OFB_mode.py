class IDEA:
    def __init__(self, key):
        self.key = self.expand_key(key)
        self.decryption_key = self.invert_key(self.key)

    def expand_key(self, key):
        """
        Expands the given key to generate subkeys for each round.

        Args:
            key (int): The original key.

        Returns:
            list: A list of subkeys generated from the original key.

        """
        key_schedule = []
        for i in range(0, 8):
            subkey = (key >> (112 - i * 16)) & 0xFFFF
            key_schedule.append(subkey)
        for i in range(8, 52):
            if (i % 8) < 6:
                subkey = ((key_schedule[i - 8] << 9) | (key_schedule[i - 7] >> 7)) & 0xFFFF
            elif (i % 8) == 6:
                subkey = ((key_schedule[i - 7] << 9) | (key_schedule[i - 14] >> 7)) & 0xFFFF
            elif (i % 8) == 7:
                subkey = ((key_schedule[i - 15] << 9) | (key_schedule[i - 14] >> 7)) & 0xFFFF
            key_schedule.append(subkey)
        return key_schedule
    
    def invert_key(self, key):
        """
        Inverts the given key for decryption.

        Args:
            key (list): The key to be inverted.

        Returns:
            list: The inverted key for decryption.
        """
        decrypt_key = [0] * 52
        decrypt_key[48] = self.mul_inv(key[0])
        decrypt_key[49] = -key[1] & 0xFFFF
        decrypt_key[50] = -key[2] & 0xFFFF
        decrypt_key[51] = self.mul_inv(key[3])
        for i in range(7):
            decrypt_key[42 - i * 6] = key[6 * i + 4]
            decrypt_key[43 - i * 6] = key[6 * i + 5]
            decrypt_key[44 - i * 6] = self.mul_inv(key[6 * i])
            decrypt_key[45 - i * 6] = -key[6 * i + 2] & 0xFFFF
            decrypt_key[46 - i * 6] = -key[6 * i + 1] & 0xFFFF
            decrypt_key[47 - i * 6] = self.mul_inv(key[6 * i + 3])
        decrypt_key[4] = key[48]
        decrypt_key[5] = key[49]
        decrypt_key[0] = self.mul_inv(key[50])
        decrypt_key[1] = -key[51] & 0xFFFF
        decrypt_key[2] = -key[49] & 0xFFFF
        decrypt_key[3] = self.mul_inv(key[48])
        return decrypt_key
    

    def encrypt_block(self, block):
        """
        Encrypts a single block using the IDEA encryption algorithm.

        Args:
            block (int): The block to be encrypted.

        Returns:
            int: The encrypted block.

        """
        x1, x2, x3, x4 = (block >> 48) & 0xFFFF, (block >> 32) & 0xFFFF, (block >> 16) & 0xFFFF, block & 0xFFFF
        for round in range(8):
            k = self.key[round * 6:(round + 1) * 6]
            x1 = self.mul(x1, k[0])
            x2 = (x2 + k[1]) & 0xFFFF
            x3 = (x3 + k[2]) & 0xFFFF
            x4 = self.mul(x4, k[3])
            t1 = x1 ^ x3
            t2 = x2 ^ x4
            t1 = self.mul(t1, k[4])
            t2 = (t2 + t1) & 0xFFFF
            t2 = self.mul(t2, k[5])
            t1 = (t1 + t2) & 0xFFFF
            x1 = x1 ^ t2
            x4 = x4 ^ t1
            t1 = t1 ^ x2
            x2 = t2 ^ x3
            x3 = t1
        x1, x2, x3, x4 = self.mul(x1, self.key[48]), (x3 + self.key[49]) & 0xFFFF, (x2 + self.key[50]) & 0xFFFF, self.mul(x4, self.key[51])
        return (x1 << 48) | (x2 << 32) | (x3 << 16) | x4
    
    def decrypt_block(self, block):
        """
        Decrypts a single block using the IDEA OFB mode algorithm.

        Args:
            block (int): The block to be decrypted.

        Returns:
            int: The decrypted block.

        """
        x1, x2, x3, x4 = (block >> 48) & 0xFFFF, (block >> 32) & 0xFFFF, (block >> 16) & 0xFFFF, block & 0xFFFF
        for round in range(8):
            k = self.decryption_key[round * 6:(round + 1) * 6]
            x1 = self.mul(x1, k[0])
            x3 = (x3 + k[1]) & 0xFFFF
            x2 = (x2 + k[2]) & 0xFFFF
            x4 = self.mul(x4, k[3])
            t1 = x1 ^ x3
            t2 = x2 ^ x4
            t1 = self.mul(t1, k[4])
            t2 = (t2 + t1) & 0xFFFF
            t2 = self.mul(t2, k[5])
            t1 = (t1 + t2) & 0xFFFF
            x1 = x1 ^ t2
            x4 = x4 ^ t1
            t1 = t1 ^ x2
            x2 = t2 ^ x3
            x3 = t1
        x1, x2, x3, x4 = self.mul(x1, self.decryption_key[48]), (x3 + self.decryption_key[49]) & 0xFFFF, (x2 + self.decryption_key[50]) & 0xFFFF, self.mul(x4, self.decryption_key[51])
        return (x1 << 48) | (x2 << 32) | (x3 << 16) | x4

    def mul(self, a, b):
        if a == 0:
            a = 65536
        if b == 0:
            b = 65536
        product = (a * b) % 65537
        if product == 65536:
            product = 0
        return product

    def mul_inv(self, x):
        if x == 0:
            return 0
        return pow(x, 65537 - 2, 65537)  # Modular multiplicative inverse using Fermat's Little Theorem

# OFB mode implementation
def idea_ofb_mode(idea, iv, data, mode='encrypt'):
    """
    Process data using IDEA in Output Feedback (OFB) mode.

    Args:
        idea (IDEA): An instance of the IDEA class used for encryption/decryption.
        iv (bytes): The initialization vector (IV) used for the OFB mode.
        data (bytes): The data to be processed.
        mode (str, optional): The mode of operation ('encrypt' or 'decrypt'). Defaults to 'encrypt'.

    Returns:
        bytes: The processed data.

    """
    block_size = 64  # IDEA block size is 64 bits
    iv = int.from_bytes(iv, byteorder='big')
    result = bytearray()
    for i in range(0, len(data), block_size // 8):
        iv = idea.encrypt_block(iv)
        block = data[i:i + block_size // 8]
        if len(block) < block_size // 8:
            block = block.ljust(block_size // 8, b'\x00')
        keystream = iv.to_bytes(block_size // 8, byteorder='big')
        cipher_block = bytes([_a ^ _b for _a, _b in zip(block, keystream)])
        result.extend(cipher_block)
    return bytes(result)