import socket

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    # Extended Euclidean Algorithm to calculate modular inverse
    d = 0
    x1, x2, y1, y2 = 0, 1, 1, 0
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = y2 - temp1 * y1

        x2 = x1
        x1 = x
        y2 = y1
        y1 = y

    if temp_phi == 1:
        d = y2 + phi

    return d

def encrypt(message, public_key):
    e, n = public_key
    encrypted_msg = [pow(ord(char), e, n) for char in message]
    return encrypted_msg

def decrypt(encrypted_msg, private_key):
    d, n = private_key
    decrypted_msg = ''.join([chr(pow(char, d, n)) for char in encrypted_msg])
    return decrypted_msg

def get_manual_keys():
    print("Enter public key (e, n):")
    e = int(input("e: "))
    n = int(input("n: "))
    public_key = (e, n)

    print("Enter private key (d, n):")
    d = int(input("d: "))
    private_key = (d, n)

    return public_key, private_key

def client_program():
    host = socket.gethostname()
    port = 5013

    client_socket = socket.socket()
    client_socket.connect((host, port))

    # Manually input RSA keys
    public_key, private_key = get_manual_keys()

    print("Public key (e, n):", public_key)
    print("Private key (d, n):", private_key)

    while True:
        message = input(" -> ")

        if message.lower().strip() == "bye":
            break

        encrypted_message = encrypt(message, public_key)
        # Convert the encrypted message to a string representation before sending
        str_encrypted_message = ' '.join(map(str, encrypted_message))
        client_socket.send(str_encrypted_message.encode())

        data = client_socket.recv(1024).decode()
        try:
            encrypted_data = [int(num) for num in data.split()]
            decrypted_data = decrypt(encrypted_data, private_key)
            print("Received from server (encrypted):", encrypted_data)
            print("Received from server (decrypted):", decrypted_data)
        except ValueError:
            print("Error decoding data from server.")
            continue

    client_socket.close()

if __name__ == "__main__":
    client_program()

