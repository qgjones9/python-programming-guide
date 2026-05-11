import sys
import argparse



def main():
    DESCRIPTION = "Pass an input string to the program"
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
    parser.add_argument("input_string", type=str, help="The input string to pass to the program")
    input_string = sys.argv[1]
    print(f"Hello, {input_string}!") # Hello, World!
