# aQracker

aQracker is a simple Python script for cracking password-protected archives using 7-Zip.

## Features

- Supports both wordlist and brute-force methods for cracking passwords.
- Utilizes multiprocessing for improved performance.
- Integrates colorized terminal output for better user interaction.

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Download and install 7-Zip from [here](https://www.7-zip.org/download.html) if not already installed.

*Note: You must install the 7-Zip at default location (C:\Program Files\7-Zip\7z.exe) or you can change the path in the script. Also the script is tested on Windows 10 only. So my linux people and macos users, in theory it should work on your system too but I haven't tested it. If it doesnt try to change the path of 7z executable in the script.*

## Usage

1. Run the script `aQracker.py`.
2. Enter the path to the archive file you want to crack.
3. Choose either the wordlist or brute-force method. (For wordlist method, you need to provide a wordlist file i.e. `.txt`.)
4. Follow the prompts to input necessary details such as wordlist path, character set, and password length.

## Requirements

- Python 3.x
- Libraries: `keyboard`, `pyfiglet`, `colorama`

## Author

- **0xQan** - [GitHub](https://github.com/furqanhun)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This script is for educational, research, and testing purposes only. The author is not responsible for any misuse of the tool. Use at your own risk.