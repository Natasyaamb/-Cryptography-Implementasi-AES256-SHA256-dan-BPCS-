# Program utama yang menampilkan menu pilihan operasi kepada pengguna

import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import numpy as np
import cv2

from bpcs_steg_decode import decode
from bpcs_steg_encode import encode
from bpcs_steg_capacity import capacity
from bpcs_steg_test import test_all


# Fungsi untuk mengenkripsi pesan menggunakan AES256 dengan PKCS7 padding
def encrypt_message(message, key):
    # Padding pesan dengan PKCS7
    block_size = AES.block_size
    padding_length = block_size - len(message) % block_size
    padded_message = message + bytes([padding_length]) * padding_length

    # Melakukan enkripsi AES256
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(padded_message)
    return cipher.iv, ciphertext


# Fungsi untuk mendekripsi pesan yang dienkripsi menggunakan AES256 dengan PKCS7 padding
def decrypt_message(ciphertext, key, iv):
    # Melakukan dekripsi AES256
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = cipher.decrypt(ciphertext)

    # Menghapus padding PKCS7
    padding_length = decrypted_message[-1]
    decrypted_message = decrypted_message[:-padding_length]

    return decrypted_message


# Fungsi untuk menghitung hash SHA256 dari sebuah pesan
def calculate_hash(message):
    return hashlib.sha256(message).digest()

# Fungsi untuk penamaan file otomatis
def get_next_ciphertext_filename():
    program_location = os.path.dirname(__file__)
    directory = os.path.join(program_location, r"Hasil\ciphertext")

    # Mengecek apakah direktori ada atau tidak
    if not os.path.exists(directory):
        # Jika tidak ada, membuat direktori tersebut
        os.makedirs(directory, exist_ok=True)

    # Mendapatkan daftar file dalam direktori
    files = os.listdir(directory)

    # Filter hanya file yang dimulai dengan "ciphertext"
    ciphertext_files = [file for file in files if file.startswith("ciphertext")]

    # Jumlah file ciphertext yang sudah ada
    num_existing_files = len(ciphertext_files)

    # Membuat nama file untuk ciphertext berikutnya
    next_filename = f"ciphertext{num_existing_files + 1}.txt"

    return next_filename

def get_next_hash_filename():
    program_location = os.path.dirname(__file__)
    directory = os.path.join(program_location, r"Hasil\ciphertext")

    # Mengecek apakah direktori ada atau tidak
    if not os.path.exists(directory):
        # Jika tidak ada, membuat direktori tersebut
        os.makedirs(directory, exist_ok=True)

    # Mendapatkan daftar file dalam direktori
    files = os.listdir(directory)

    # Filter hanya file yang dimulai dengan "ciphertext"
    ciphertext_files = [file for file in files if file.startswith("hash")]

    # Jumlah file ciphertext yang sudah ada
    num_existing_files = len(ciphertext_files)

    # Membuat nama file untuk ciphertext berikutnya
    next_filename = f"hash{num_existing_files + 1}.txt"

    return next_filename

#Fungsi mengecek kesamaan nilai hash
def check_hash(hash1, hash2):
    if hash1 == hash2:
        return "Nilai hash sesuai!"
    else:
        return "Nilai hash tidak sesuai!"

# Fungsi untuk menyimpan hasil enkripsi ke dalam file txt
def save_cipher_to_file(ciphertext, filename):
    try:
        program_location = os.path.dirname(__file__)
        
        # Menyimpan ciphertext ke file
        file_path = os.path.join(program_location, r"Hasil\ciphertext", filename)

        # Membuat folder "Hasil/ciphertext" jika belum ada
        os.makedirs(os.path.join(program_location, "/Hasil/ciphertext"), exist_ok=True)

        with open(file_path, 'w') as file:
            file.write(ciphertext)
        
        print("Hasil ciphering berhasil disimpan di:", file_path)
    except Exception as e:
        print("Terjadi kesalahan saat menyimpan hasil ciphering:", str(e))

# Membaca file ciphertext
def read_text_file(filename):
    try:
        program_location = os.path.dirname(__file__)

        file_path = os.path.join(program_location, r"Hasil\ciphertext", filename)

        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        print("Terjadi kesalahan saat membaca file:", str(e))
        return None

# Fungsi menghitung nilai PSNR
def calculate_psnr(original_image_path, embedded_image_path):
    original = cv2.cvtColor(cv2.imread(original_image_path), cv2.COLOR_RGB2BGR)
    embedded = cv2.cvtColor(cv2.imread(embedded_image_path), cv2.COLOR_RGB2BGR)
    psnr_value = cv2.PSNR(original, embedded)
    return psnr_value

# Fungsi utama
def main():
    while True:
        print("Pilih operasi yang ingin dilakukan:")
        print("1. Enkripsi pesan")
        print("2. Dekripsi pesan")
        print("3. Sisipkan pesan ke gambar")
        print("4. Ekstraksi pesan dari gambar")
        print("5. Hitung Nilai PSNR Steganografi")
        print("6. Keluar")
        
        choice = input("Masukkan pilihan (1/2/3/4/5/6): ")
        
        if choice == '1':
            # Membaca pesan dari pengguna
            message = input("Masukkan pesan yang ingin dienkripsi: ")

            # Membaca kunci AES dari pengguna
            key = input("Masukkan kunci AES (32 bytes): ").encode('utf-8')
            if len(key) != 32:
                print("Panjang kunci harus 32 bytes.")
                continue

            # Enkripsi pesan menggunakan AES256
            iv, ciphertext = encrypt_message(message.encode('utf-8'), key)

            # Menampilkan hasil enkripsi pesan dan nilai hashnya
            print("\nEnkripsi berhasil dilakukan!")
            print("Message: ", message)
            print("Ciphertext: ", iv.hex() + ciphertext.hex())  # Menampilkan ciphertext dalam format heksadesimal
            print("Hash: ", calculate_hash(iv + ciphertext).hex(), "\n")

            # Menyimpan hasil enkripsi ke file txt
            filename = get_next_ciphertext_filename()
            save_cipher_to_file(iv.hex() + ciphertext.hex(), filename)
            hashfilename = get_next_hash_filename()
            save_cipher_to_file(calculate_hash(iv + ciphertext).hex(), hashfilename)


        elif choice == '2':
            # Membaca ciphertext dari pengguna
            filename_ciphertext = input("Masukkan nama file yang akan di dekripsi: ")
            ciphertext_input = read_text_file(filename_ciphertext)

            filename_hash = input("Masukkan nama file hash yang sesuai: ")
            hash_input = read_text_file(filename_hash)

            # Mendapatkan nilai hash dari ciphertext
            hash_value = calculate_hash(bytes.fromhex(ciphertext_input)).hex()

            # Mengonversi ciphertext dari heksadesimal menjadi bytes
            try:
                ciphertext_bytes = bytes.fromhex(ciphertext_input)
            except ValueError:
                print("Format ciphertext tidak valid. Pastikan ciphertext dalam format heksadesimal.")
                continue

            # Memisahkan IV dan ciphertext
            iv = ciphertext_bytes[:16]
            ciphertext = ciphertext_bytes[16:]

            # Membaca kunci AES dari pengguna
            key = input("Masukkan kunci AES (32 bytes): ").encode('utf-8')
            if len(key) != 32:
                print("Panjang kunci harus 32 bytes.")
                continue

            # Dekripsi pesan menggunakan AES256
            plaintext = decrypt_message(ciphertext, key, iv)

            # Menampilkan hasil dekripsi pesan, nilai hash, dan ciphertext
            print("\nDekripsi berhasil dilakukan!")
            print("Ciphertext: ", ciphertext_input)
            print("Plaintext: ", plaintext.decode('utf-8'))
            print(check_hash(hash_value, hash_input))
            print("New Hash : ", hash_value)
            print("Old Hash : ", hash_input)
        
        elif choice == '3':
            # Menambahkan nilai ambang untuk operasi BPCS
            alpha = input("Masukkan nilai ambang batas minimum (contoh: 0.3): ")
            alpha = float(alpha)

            # Memilih gambar cover-image
            vslfile = input("Masukkan path file cover-image (contoh: ../examples/image.jpg): ")

            # Memilih file pesan yang akan disisipkan ke dalam gambar
            message = input("Masukkan nama file ciphertext (contoh: ciphertext1.txt): ")
            msgfile = os.path.join(os.path.dirname(__file__), "Hasil/ciphertext", message)

            # Memberikan nama untuk file hasil penyisipan
            encfile_name = input("Masukkan nama file hasil steganografi (contoh: hasil.png): ")
            encfile = os.path.join(os.path.dirname(__file__), "Hasil/steganografi", encfile_name)

            capacity(vslfile, alpha) # Mengecek ukuran pesan yang dapat disisipkan
            encode(vslfile, msgfile, encfile, alpha) # Penyisipan pesan dengan BPCS
            

        elif choice == '4':
            # Menambahkan nilai ambang untuk operasi BPCS
            alpha = input("Masukkan nilai ambang batas minimum: ")
            alpha = float(alpha)

            # Memilih file stego-image
            encfile_name = input("Masukkan nama file hasil steganografi (contoh: hasil.jpg): ")
            encfile = os.path.join(os.path.dirname(__file__), "Hasil/steganografi", encfile_name)

            # Memasukkan nama untuk file hasil ekstraksi
            msgfile_name = input("Masukkan nama file hasil ekstraksi (contoh: hasil.txt): ")
            msgfile_decoded = os.path.join(os.path.dirname(__file__), "Hasil/ciphertext", msgfile_name)

            decode(encfile, msgfile_decoded, alpha) # Melakukan ekstraksi pesan tersembunyi dari file stego-image

        elif choice == '5':
            # Menginputkan path cover-image dan nama file steganografi
            cover_path = input("Masukkan path file cover-image: ")
            stegofile = input("Masukkan nama file hasil steganografi: ")
            stego_path = os.path.join(os.path.dirname(__file__), "Hasil/steganografi", stegofile)

            # Mendapatkan nilai PSNR dan menampilkannya
            psnr_value = calculate_psnr(cover_path, stego_path)
            print(f"PSNR antara file original and file hasil steganografi adalah : {psnr_value} dB")

        elif choice == '6':
            print("Terima kasih telah menggunakan program ini.")
            break
        
        else:
            print("Pilihan tidak valid. Silakan pilih 1, 2, 3, 4, 5, atau 6.")

if __name__ == "__main__":
    main()
