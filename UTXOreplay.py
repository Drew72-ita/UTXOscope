import sys
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    if not (3 <= len(sys.argv) <= 4):
        print("Usage: python UTXOreplay.py <logfile.txt> <delay_ms> [start_block]")
        sys.exit(1)

    logfile = sys.argv[1]
    delay_ms = int(sys.argv[2])
    delay_sec = delay_ms / 1000.0

    start_block = None
    if len(sys.argv) >= 4:
        start_block = sys.argv[3]

    try:
        with open(logfile, "r") as f:
            frame = []
            for line in f:
                if start_block:
                    if line.startswith(f"--- block {start_block}"):
                        start_block = None 
                        frame = [line]  
                    continue  

                if line.startswith("--- block"):
                    if frame:
                        clear_screen()
                        print("".join(frame), end="")
                        time.sleep(delay_sec)
                        frame = []

                frame.append(line)
                
        input()

    except FileNotFoundError:
        print(f"File not found: {logfile}")
        sys.exit(1)

if __name__ == "__main__":
    main()