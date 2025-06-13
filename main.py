import re

def main():
    code = "(λx. x)"
    tokens = tokenize(code)
    for t in tokens:
        print(t)

if __name__ == "__main__":
    main()

