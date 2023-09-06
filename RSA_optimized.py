import time
import rabin_miller as rm


class RSA_NHOM6:
    def generate_key(self, e_default=65537, save_path='keys'):
        """
        input: p, q: both prime, p # q
        output: public key {e, n} and private key {d, n}
        """
        
        def gcd(a, b):
            if b == 0:
                return a
            return gcd(b, a%b)
        
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
        max_tries = 10
        while max_tries > 0:
            n_bit = 1024 # modulus size, default: 1024 bits

            # Select random large prime numbers p and q
            p, q = -1, -1
            while True:
                p = rm.getLowLevelPrime(n_bit)
                if rm.isMillerRabinPassed(p):
                    break
            
            while True:
                q = rm.getLowLevelPrime(n_bit)
                if rm.isMillerRabinPassed(q):
                    break

            n = p * q
            phi_n = (p - 1) * (q - 1)

            # Select e
            e = e_default
            if e > phi_n or e < 1:
                print('ERROR: The e value must be 1 < e < phi(n)')
                continue
            elif gcd(phi_n, e) != 1:
                print('ERROR: The greatest common division of phi_n and e does not equal 1')
                continue

            # Caculate d using Extended Euclidean Algorithm appoarch
            _, d, _ = extended_gcd(e, phi_n)

            if d > phi_n or d < 1:
                print('ERROR: The d value must be 1 < e < phi(n)')
                continue
            
            max_tries -= 1
        
        print(f'Keys were generated successfully after {time.time() - generate_time}s')
        # print('Public key:', (e, n))
        # print('Private key:', (d, n))

        with open(f'{save_path}/public_key.txt', mode='w') as f:
            f.write(f'{e},{n}')
        
        with open(f'{save_path}/private_key.txt', mode='w') as f:
            f.write(f'{d},{n}')
        
        print(f'Saved keys in {save_path}/')

        return (e, n), (d, n)

    def load_key(self, path='keys'):
        public_key, private_key = None, None
        with open(f'{path}/public_key.txt', mode='r') as f:
            public_key = map(int, f.read().split(','))
        
        with open(f'{path}/private_key.txt', mode='r') as f:
            private_key = map(int, f.read().split(','))
        
        return public_key, private_key

    # calculate a^b mod m using modular exponentiation
    def mod_pow(self, a, b, m): # Log(n)
        result = 1
        while b > 0:
            if b & 1:
                result = (result * a) % m
            
            a = (a * a) % m;
            b >>= 1
        return result

    # encrypt message
    def encrypt(self, M, public_key):
        e, n = public_key
        if M > n:
            print('Can not encrypt plaintext')
            return None
        C = self.mod_pow(M, e, n)
        return C
    
    # decrypt ciphertext
    def decrypt(self, C, private_key):
        d, n = private_key
        M = self.mod_pow(C, d, n)
        return M


if __name__ == '__main__':
    RSA = RSA_NHOM6()
    # public_key, private_key = RSA.generate_key()
    public_key, private_key = RSA.load_key()

    text = 123456
    C = RSA.encrypt(text, public_key)
    M = RSA.decrypt(C, private_key)

    print('Plaintext:', text)
    print('Ciphertext:', C)
    print('Decrypted ciphertext:', M)
