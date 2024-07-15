import subprocess
import os
import string
import keyboard
from itertools import product
from multiprocessing import Pool, cpu_count
import pyfiglet
import colorama

colorama.init()

def generate_passwords(characters, length=8):
    """
    Generate passwords with a given length using a specified character set.
    """
    return (''.join(password) for password in product(characters, repeat=length))

def crack_archive(password_info):
    archive_path, output_folder, characters, length = password_info
    for password in generate_passwords(characters, length):
        print(f"Testing password: {colorama.Fore.GREEN}{password}{colorama.Style.RESET_ALL}")
        cmd = [r'C:\Program Files\7-Zip\7z.exe', 'x', f'-p{password}', archive_path, f'-o{output_folder}', '-y']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if result.returncode == 0:
            with open(os.path.join(output_folder, 'cracked_password.txt'), 'w') as f:
                f.write(password)
            return password
        if keyboard.is_pressed('shift+esc+q'):
            print(f"{colorama.Fore.YELLOW}Stopping...{colorama.Style.RESET_ALL}")
            return None
    return None

def crack_archive_exact(args):
    archive_path, output_folder, characters, exact_length = args
    return crack_archive((archive_path, output_folder, characters, exact_length))

def crack_archive_range(args):
    archive_path, output_folder, characters, min_length, max_length = args
    for length in range(min_length, max_length + 1):
        result = crack_archive((archive_path, output_folder, characters, length))
        if result:
            return result
    return None
def load_wordlist(path):
    """
    Load words from a wordlist file.
    """
    with open(path, 'r') as f:
        return [line.strip() for line in f.readlines()]

def crack_archive_wordlist(password_info):
    archive_path, output_folder, wordlist_path = password_info
    wordlist = load_wordlist(wordlist_path)
    for password in wordlist:
        print(f"Testing password: {colorama.Fore.GREEN}{password}{colorama.Style.RESET_ALL}")
        cmd = [r'C:\\Program Files\\7-Zip\\7z.exe', 'x', f'-p{password}', archive_path, f'-o{output_folder}', '-y']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if result.returncode == 0:
            with open(os.path.join(output_folder, 'cracked_password.txt'), 'w') as f:
                f.write(password)
            return password
    return None

def init_globals(archive_path, output_folder):
    global archive, output
    archive = archive_path
    output = output_folder

if __name__ == "__main__":
    print("\n" *4)
    print("Welcome to aQracker - A simple archive password cracker using 7-Zip.")
    print("-----------------------------------------")
    # use pyfiglet to print aQracker
    ascii_banner = pyfiglet.figlet_format("aQracker")
    print(f"{colorama.Fore.CYAN}{ascii_banner}{colorama.Style.RESET_ALL}")
    print("-----------------------------------------")
    print("v24.7.1 - Heatwave - 0xQan")
    print("\n" *4)
    archive_path = input("Enter Archive: ")
    if not os.path.exists(archive_path) or not os.path.isfile(archive_path):
        print(f"{colorama.Fore.RED}Archive not found!{colorama.Style.RESET_ALL}")
        exit()
    archive_name = os.path.splitext(os.path.basename(archive_path))[0]
    output_folder = f"{archive_name}_cracked"

    print("\n" *4)
    print("Select method to crack the archive:")
    print("1. Wordlist")
    print("2. Brute Force")
    print("--------------------------------------------------")
    method_choice = input("Enter number corresponding to your choice: ")

    if method_choice == '1':
        wordlist_path = input("Enter Wordlist: ")
        if not os.path.exists(wordlist_path) or not os.path.isfile(wordlist_path) or None:
            print(f"{colorama.Fore.RED}Wordlist not found!{colorama.Style.RESET_ALL}")
            exit()
        pool = Pool(cpu_count(), initializer=init_globals, initargs=(archive_path, output_folder))
        result = pool.apply(crack_archive_wordlist, args=((archive_path, output_folder, wordlist_path),))

    elif method_choice == '2':
        print("\n" *4)
        print("Select characters to include:")
        print("1. Numbers 0-9")
        print("2. Alphabets (small) a-z")
        print("3. Alphabets (capital) A-Z")
        print("4. Special Characters")
        print("5. Space/Whitespace/Null Character")
        print("6. All of the above")
        print("--------------------------------------------------")

        characters_choice = input("Enter numbers corresponding to your choices (e.g., '1,2,4' for Numbers, Small Alphabets, and Special Characters): ")
        characters = ''
        if '1' in characters_choice:
            characters += string.digits
        if '2' in characters_choice:
            characters += string.ascii_lowercase
        if '3' in characters_choice:
            characters += string.ascii_uppercase
        if '4' in characters_choice:
            characters += string.punctuation
        if '5' in characters_choice:
            characters += ' '
        if '6' in characters_choice:
            characters = string.ascii_letters + string.digits + string.punctuation + ' '

        exact_length_input = input("Enter exact password length (press Enter if none): ")
        if exact_length_input:
            exact_length = int(exact_length_input)
        else:
            exact_length = None

        if exact_length is not None:
            pool = Pool(cpu_count(), initializer=init_globals, initargs=(archive_path, output_folder))
            result = pool.apply(crack_archive_exact, args=((archive_path, output_folder, characters, exact_length),))
        else:
            min_length_input = input("Enter minimum password length (press Enter for default(0)): ")
            if min_length_input:
                min_length = int(min_length_input)
            else:
                min_length = 0

            max_length_input = input("Enter maximum password length (press Enter for default(8)): ")
            if max_length_input:
                max_length = int(max_length_input)
            else:
                max_length = 8

            pool = Pool(cpu_count(), initializer=init_globals, initargs=(archive_path, output_folder))
            result = pool.apply(crack_archive_range, args=((archive_path, output_folder, characters, min_length, max_length),))

    pool.close()
    pool.join()

    if result:
        print("-----------------------------------------")
        print(f"Success! Password found: {colorama.Fore.GREEN}{result}{colorama.Style.RESET_ALL}")
        print("-----------------------------------------")
    else:
        print("-----------------------------------------")
        print(f"{colorama.Fore.RED}Password not found.{colorama.Style.RESET_ALL}")