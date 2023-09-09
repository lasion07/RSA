import time
import rabin_miller as rm


class RSA_NHOM6:
    def __init__(self):
        self.public_key = None
        self.private_key = None

    def generate_key(self, e_default=65537, save_path='keys'):
        """
        input: p, q: both prime, p # q
        output: public key {e, n} and private key {d, n}
        """
        
        def gcd(a, b):
            if b == 0:
                return a
            return gcd(b, a%b)
        
        def lcm(a, b):
            return (a // gcd(a, b))*b
        
        def extended_gcd(a, b): # Log(n)
            # Base Case
            if a == 0:
                return b, 0, 1
        
            gcd, x1, y1 = extended_gcd(b % a, a)
        
            # Update x and y using results of recursive
            # call
            x = y1 - (b//a) * x1
            y = x1
        
            return gcd, x, y

        generate_time = time.time()
        n_bit = 1024 # modulus size, default: 1024 bits

        # Select random large prime numbers p and q
        p, q = -1, -1
        while True:
            p = rm.getLowLevelPrime(n_bit)
            if rm.isMillerRabinPassed(p):
                break
        
        while True:
            q = rm.getLowLevelPrime(n_bit)
            if p != q and rm.isMillerRabinPassed(q):
                break

        n = p * q
        phi_n = lcm(p-1, q-1)#(p - 1) * (q - 1)

        # Select e
        e = e_default
        if e > phi_n or e < 1:
            print('ERROR: The e value must be 1 < e < phi(n)')
            max_tries -= 1
            return None, None
        elif gcd(phi_n, e) != 1:
            print('ERROR: The greatest common division of phi_n and e does not equal 1')
            max_tries -= 1
            return None, None

        # Caculate d using Extended Euclidean Algorithm appoarch
        _, d, _ = extended_gcd(e, phi_n)

        if d < 0:
            d += phi_n

        if d > phi_n or d < 1:
            print('ERROR: The d value must be 1 < e < phi(n)')
            max_tries -= 1
            return None, None
        
        print(f'Keys were generated successfully after {time.time() - generate_time}s')
        # print('Public key:', (e, n))
        # print('Private key:', (d, n))
        self.public_key = (e, n)
        self.private_key = (d, n)

        with open(f'{save_path}/public_key_temp.txt', mode='w') as f:
            f.write(f'{e},{n}')
        
        with open(f'{save_path}/private_key_temp.txt', mode='w') as f:
            f.write(f'{d},{n}')
        
        print(f'Saved temp keys in {save_path}/')

    def load_key(self, pu_path, pr_path):
        with open(pu_path, mode='r') as pu:
            self.public_key = tuple(map(int, pu.read().split(',')))
        
        with open(pr_path, mode='r') as pr:
            self.private_key = tuple(map(int, pr.read().split(',')))
        
        if self.public_key == None or self.private_key == None:
            print('Can not load key')

    # encrypt message
    def encrypt(self, M):
        # calculate a^b mod m using modular exponentiation
        def mod_pow(a, b, m): # Log(n)
            result = 1
            while b > 0:
                if b & 1:
                    result = (result * a) % m
                
                a = (a * a) % m;
                b >>= 1
            return result

        e, n = self.public_key
        if M > n:
            print('Can not encrypt plaintext')
            return None
        C = mod_pow(M, e, n)
        return C
    
    # decrypt ciphertext
    def decrypt(self, C):
        # calculate a^b mod m using modular exponentiation
        def mod_pow(a, b, m): # Log(n)
            result = 1
            while b > 0:
                if b & 1:
                    result = (result * a) % m
                
                a = (a * a) % m;
                b >>= 1
            return result

        d, n = self.private_key
        M = mod_pow(C, d, n)
        return M

    # First converting each character to its ASCII value and
    # then encoding it then decoding the number to get the
    # ASCII and converting it to character
    def encode(self, message):
        encoded = []
        # Calling the encrypting function in encoding function
        for letter in message:
            encoded.append(self.encrypt(ord(letter)))
        
        encoded_message = ''.join(str(p) + ' ' for p in encoded)
        return encoded_message
    
    def decode(self, encoded_message):
        s = ''
        encoded = []
        temp = encoded_message.split()
        for i in temp:
            encoded.append(int(i))
        # Calling the decrypting function decoding function
        for num in encoded:
            s += chr(self.decrypt(num))
        
        # message = ''.join(str(p) + ' ' for p in s)
        return s


if __name__ == '__main__':
    RSA = RSA_NHOM6()
    # RSA.generate_key()
    RSA.load_key()
