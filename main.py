import os
import requests
import argparse
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

RED = "\033[91m"
ORANGE = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

def is_url_alive(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def write_unique(output_file, url):
    if not os.path.exists(output_file):
        with open(output_file, "w") as f:
            f.write(f"{url}\n")
    else:
        with open(output_file, "r") as f:
            if url in f.read():
                return
        with open(output_file, "a") as f:
            f.write(f"{url}\n")

def fuzz_directory(url, directory, output_dir):
    try:
        full_url = urljoin(url, directory.strip())
        response = requests.get(full_url, timeout=5)
        status_code = response.status_code
        output_file = os.path.join(output_dir, f"{status_code}.txt")
        
        write_unique(output_file, full_url)
            
    except requests.RequestException:
        pass

def process_url_for_recursion(url, directory, recursive_status, new_file, other_files):
    try:
        full_url = f"{url}/{directory.strip()}"
        response = requests.get(full_url, timeout=5)
        status_code = response.status_code
            
        if status_code == recursive_status:
            write_unique(new_file, full_url)
        elif status_code in other_files:
            write_unique(other_files[status_code], full_url)
                
    except requests.RequestException:
        pass

def recursive_fuzzing(file_path, output_dir, wordlist_path, recursive_status, max_depth=5, threads=10, depth=1):
    if depth > max_depth:
        print(f"{ORANGE}Max recursion depth reached !{RESET}")
        return

    with open(file_path, "r") as f:
        urls = [url.strip() for url in f.readlines()]

    new_file = os.path.join(output_dir, f"{recursive_status}_{depth}.txt")
    other_files = {
        200: os.path.join(output_dir, f"{recursive_status}_200.txt"),
        302: os.path.join(output_dir, f"{recursive_status}_302.txt"),
        401: os.path.join(output_dir, f"{recursive_status}_401.txt"),
        403: os.path.join(output_dir, f"{recursive_status}_403.txt"),
        500: os.path.join(output_dir, f"{recursive_status}_500.txt"),
    }

    if os.path.exists(wordlist_path):
        with open(wordlist_path, "r") as wordlist, ThreadPoolExecutor(max_workers=threads) as executor:
            for url in urls:
                for directory in wordlist:
                    executor.submit(process_url_for_recursion, url, directory, recursive_status, new_file, other_files)
    else:
        print(f"{RED}Wordlist file {wordlist_path} does not exist{RESET}")
    
    if os.path.exists(new_file) and os.path.getsize(new_file) > 0:
        print(f"Recursing into {new_file}...")
        recursive_fuzzing(new_file, output_dir, wordlist_path, recursive_status, depth + 1, max_depth, threads)
    else:
        print(f"\n{ORANGE}No more URLs for recursion{RESET}")
        
def call_rec_func(output_dir, wordlist_path, recursive_status, max_depth, threads):
     recursive_status=0
     while recursive_status == 0:
        choice = input("Do you want to recursively fuzz? (y/n): ").strip().lower()
        if choice == 'y':
    
            try:
                recursive_status = int(input("\nEnter the status code or filename for recursive fuzzing: ").strip())
                initial_file_path = os.path.join(output_dir, f"{recursive_status}.txt")
                
                if os.path.exists(initial_file_path):
                    print(f"\n{ORANGE}Starting recursive fuzzing for : {recursive_status}.{RESET}")
                    recursive_fuzzing(initial_file_path, output_dir, wordlist_path, recursive_status, max_depth, threads)
                    recursive_status = 0
                    
                else:
                    print(f"{RED}No URLs found with status code {recursive_status} in output directory. Try again.{RESET}")
                    recursive_status = 0  

            except ValueError:
                print(f"{RED}Invalid input! Please enter a valid status code.{RESET}")
        
        elif choice == 'n':
            print("\nExiting.")
            break
        else:
            print(f"{RED}Invalid choice! Please enter 'y' or 'n'.{RESET}")


def main():
    parser = argparse.ArgumentParser(description="Recuzzer : Recursive Sub-Directory Fuzzing Tool")
    parser.add_argument("-u", "--url", help="The URL to fuzz (e.g., 'www.webapp.com').")
    parser.add_argument("-w", "--wordlist", required=True, help="The path to the directory wordlist file.")
    parser.add_argument("-r", "--recursive", default=0 , help="Status code or filename (without '.txt') to recursively fuzz.")
    parser.add_argument("-o", "--output", required=True, help="The path to the output directory")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads for concurrent requests.")
    parser.add_argument("-c", "--max-recursion", type=int, default=5, help="Maximum recursion depth.")
    
    args = parser.parse_args()
    input_url = args.url
    wordlist_path = args.wordlist
    recursive_status = args.recursive
    output_dir = args.output
    threads = args.threads
    max_depth = args.max_recursion

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    if not input_url: 
        initial_file_path = recursive_status
        if os.path.exists(initial_file_path):
            print(f"\n{ORANGE}Starting recursive fuzzing for : {recursive_status}{RESET}\nThis may take some time...")
            recursive_fuzzing(initial_file_path, output_dir, wordlist_path, recursive_status, max_depth, threads)
        call_rec_func(output_dir, wordlist_path, recursive_status, max_depth, threads)
        return

    if not input_url.startswith(("http://", "https://")):
        input_url = "http://" + input_url
    
    if not is_url_alive(input_url):
        print(f"{RED}The URL {input_url} is not valid or alive.\nExiting{RESET}")
        return
    
    print(f"{GREEN}The URL {input_url} is valid and alive{RESET}\nFuzzing...")

    if os.path.exists(wordlist_path):
        with open(wordlist_path, "r") as wordlist, ThreadPoolExecutor(max_workers=threads) as executor:
            for directory in wordlist:
                executor.submit(fuzz_directory, input_url, directory.strip(), output_dir)
    else:
        print(f"{RED}Directory wordlist file {wordlist_path} does not exist{RESET}")
        return
        
    
    if recursive_status:
        initial_file_path = os.path.join(output_dir, f"{recursive_status}.txt")
        if os.path.exists(initial_file_path):
            print(f"\n{ORANGE}Starting recursive fuzzing for status code: {recursive_status}{RESET}\nThis may take some time...")
            recursive_fuzzing(initial_file_path, output_dir, wordlist_path, recursive_status, max_depth, threads)
        call_rec_func(output_dir, wordlist_path, recursive_status, max_depth, threads)
    else:
        call_rec_func(output_dir, wordlist_path, recursive_status, max_depth, threads) 
  
if __name__ == "__main__":
    main()
