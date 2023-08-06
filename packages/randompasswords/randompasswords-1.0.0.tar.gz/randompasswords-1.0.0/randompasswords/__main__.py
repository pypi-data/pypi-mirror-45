#__main__.py for randompasswords

from randompasswords.passwordgenerator import *
from faker import Faker


def main():

    fake = Faker()

    with open("pw.txt", "w+") as fh:    # open or create a textfile to store inputted keywords
        inputKeywords(fh)
        fh.write(fake.email() + "\n")
        fh.write(fake.address() + "\n")
        fh.write(str(fake.longitude()) + "\n")
        fh.write(str(fake.latitude()) + "\n")

    with open("pw.txt", "r+") as fh:    # takes keywords and puts them in data structures to prepare for generating pws
        storage = storeKeywords(fh)

    passwords = generatePasswords(storage)
    print("\nPrinting passwords now\n\n")

    with open("pw.txt", "a") as fh:
        storePasswords(fh, passwords)


if __name__ == "__main__":
    main()
