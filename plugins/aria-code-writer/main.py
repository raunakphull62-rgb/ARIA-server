# plugins/aria-code-writer/main.py
import os
import sys
from ai.router import get_completion

def write_code():
    prompt = input("Describe the code you want: ")
    filename = input("Save to file: ")
    # Use AI to generate code
    response = get_completion([{"role": "user", "content": f"Write Python code for: {prompt}. Only output the code, no explanation."}])
    with open(filename, 'w') as f:
        f.write(response)
    print(f"Code written to {filename}")

def refactor():
    filename = input("File to refactor: ")
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return
    with open(filename, 'r') as f:
        content = f.read()
    instructions = input("Refactoring instructions: ")
    response = get_completion([{"role": "user", "content": f"Refactor this code: {content}\nInstructions: {instructions}\nOutput only the refactored code."}])
    with open(filename, 'w') as f:
        f.write(response)
    print(f"{filename} refactored.")

def fix_file():
    filename = input("File to fix: ")
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return
    with open(filename, 'r') as f:
        content = f.read()
    errors = input("Describe the errors: ")
    response = get_completion([{"role": "user", "content": f"Fix errors in this code: {content}\nErrors: {errors}\nOutput only the fixed code."}])
    with open(filename, 'w') as f:
        f.write(response)
    print(f"{filename} fixed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <write-code|refactor|fix-file>")
    else:
        cmd = sys.argv[1]
        if cmd == "write-code":
            write_code()
        elif cmd == "refactor":
            refactor()
        elif cmd == "fix-file":
            fix_file()
        else:
            print(f"Unknown command: {cmd}")
