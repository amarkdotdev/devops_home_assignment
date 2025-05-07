import os

def print_all_files_and_contents():
    for filename in os.listdir('.'):
        if os.path.isfile(filename):
            print(f"\n--- {filename} ---")
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    print(f.read())
            except Exception as e:
                try:
                    with open(filename, 'rb') as f:
                        content = f.read()
                        print(content.decode('utf-8', errors='replace'))
                except Exception as err:
                    print(f"[Cannot read file: {err}]")

if __name__ == "__main__":
    print_all_files_and_contents()
