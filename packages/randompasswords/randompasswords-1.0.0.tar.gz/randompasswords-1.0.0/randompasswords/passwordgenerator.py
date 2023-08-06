"""
asks for keyword input and stores keywords in pw.txt
passes on the keywords to encoding algorithm
"""

from random import randint

# writes inputted words into text file until user presses ENTER
def inputKeywords(file):
    print("Input keywords (ENTER to stop)")
    file.write("\tK\n")

    while True:
        keyword = input("Enter keyword: ")
        file.write(keyword + "\n")

        if not keyword:
            break

    file.write("\tPW\n")


def storeKeywords(file):
    stop = '\tPW\n'
    store_keywords = []
    store_keywords_list = []

    # grab each line from pw.txt and convert each char to ascii int then append to storeKeywords
    for line in file:
        store_keywords.append(strToAscii(line))

        if line == stop:
            break

    # get rid of first line of file "K" and last 2 lines "\n" and "PW"
    del(store_keywords[0])
    del(store_keywords[len(store_keywords)-1])
    #del(store_keywords[len(store_keywords)-1])

    # concatenate every ascii list into one
    for n in store_keywords:
        store_keywords_list.extend(n)

    return store_keywords_list


def generatePasswords(arg_list):
# takes list of keywords and generates 10 random passwords in ascii number form for each password lengths 6 to 10
    output_list = []
    length_min = input("Enter password length minimum (Enter if none):")
    length_max = input("Enter password length maximum (Enter if none):")
    requirements = []

    while True:
        enter = input("Add special character requirements:")
        if enter == "":
            break
        requirements.extend(strToAscii(enter))


    if(length_min == ""):
        length_min = 6
    else:
        length_min = int(length_min)
    if(length_max == ""):
        length_max = 11
    else:
        length_max = int(length_max) + 1


    for password_length in range(length_min, length_max):
        password_amount = 0                 # zero out password amount for each length of passwords

        while password_amount < 10:
            storage = list(arg_list)        # make copy of list
            storage.extend(requirements)    # add the special character requirements into possible passwords
            pw = []                         # where individual passwords will be assembled

            while((len(pw) < password_length) and (len(storage) > 0)):
                random_int = randint(0, len(storage)-1)
                temp = storage.pop(random_int)
                pw.append(temp)

            password_amount += 1
            output_list.append(pw)
    print("\nOutput list\n")

    return output_list

def storePasswords(file, arg_list):
    passwords = []
    for pw in arg_list:
        word = ''.join(chr(x) for x in pw if x != 32)
        passwords.append(word)
        print("{0} has been appended!".format(word))
        file.write(word + "\n")



def strToAscii(word):
    result = []
    for c in word:
        ascii = ord(c)
        if((ascii >= 32) and (ascii < 127)):
            result.append(ascii)

    return result








