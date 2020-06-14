import rsa


def run_example(keysize):
    print("Generating RSA Key pair")
    public_key, private_key = rsa.newkeys(keysize, poolsize=8)
    print("Public key:", public_key)
    print("Public Key (Modulus n) =", public_key.n)
    print("Public Key (Exponent e) =", public_key.e)
    print("Private key:", private_key)
    print("Private key (Secret d - must be kept as secret)=", private_key.d)
    pub_key_file = open('../output/public_key.DER', 'w')
    pub_key_file.write(public_key.save_pkcs1().decode('utf-8'))
    pub_key_file.close()
    private_key_file = open('../output/private_key.DER', 'w')
    private_key_file.write(private_key.save_pkcs1().decode('utf-8'))
    private_key_file.close()


if __name__ == '__main__':
    key_size = 2048
    run_example(key_size)
