# RECUZZER 

### Recuzzer is a Python-based recursive directory fuzzing tool designed for pentesters and security researchers. 

## Features
  - Supports multi-threaded directory fuzzing.
  - Recursive fuzzing based on HTTP status codes.
  - Avoids duplicate URLs during output generation.
  - Fully customizable with adjustable recursion depth and thread count.

## Installation
  1. Install `pipx` using:
  ```
  sudo apt install pipx
  ```
  2. Install `recuzzer` using:
  ```
  git clone https://github.com/The-Ap0stle/Recuzzer.git && cd Recuzzer && pipx install .
  ```
  > Note: If you are using an old version of python, use pip instead of pipx or install pipx

## Usage
  - If you want to fuzz the domains that give 200 status upto 3 sub-directories 
  ```
  recuzzer -u [url] -w [wordlist_path] -r 200 -c 3 -o [output_path]
  ```
## Disclaimer
This tool is for educational and ethical pentesting purposes only. Use responsibly and at your own risk. Any misuse will not be the responsibility of the creators.