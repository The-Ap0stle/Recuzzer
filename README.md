# RECUZZER 

### Recuzzer is a recursive directory fuzzing tool designed for bug hunters and security researchers. 

## Features
  - Supports multi-threaded directory fuzzing.
  - Recursive fuzzing based on HTTP status codes.
  - Avoids duplicate URLs during output generation.
  - Fully customizable with adjustable recursion depth and thread count.

## Installation
  1. Install `pipx`:
  ```
  sudo apt install pipx
  ```
  2. Install `recuzzer`:
  ```
  git clone https://github.com/The-Ap0stle/Recuzzer.git && cd Recuzzer && pipx install .
  ```
  > Note: If you are using an old version of python, use pip instead of pipx

## Usage
  - Fuzzing a URL that gives 200 status for upto 3 sub-directories: 
  ```
  recuzzer -u [url] -w [wordlist_path] -r 200 -c 3 -o [output_path]
  ```
  - Fuzzing a list of URL's in a file for upto 3 sub-directories: 
  ```
  recuzzer -w [wordlist_path] -r [url_file_path] -c 3 -o [output_path]
  ```
## Disclaimer
This tool is for educational and ethical pentesting purposes only. Use responsibly and at your own risk. Any misuse will not be the responsibility of the developers nor the distributors.