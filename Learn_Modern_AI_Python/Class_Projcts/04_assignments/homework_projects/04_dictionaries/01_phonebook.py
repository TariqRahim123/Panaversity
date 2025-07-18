# ## Problem Statement

# In this program we show an example of using dictionaries to keep track of information in a phonebook.

# ## Starter Code

# ```bash
# def main():
#     print("Delete this line and write your code here! :)")


# # This provided line is required at the end of
# # Python file to call the main() function.
# if __name__ == '__main__':
#     main()
# ```

# ## Solution

# ```bash
# def read_phone_numbers():
#     """
#     Ask the user for names/numbers to story in a phonebook (dictionary).
#     Returns the phonebook.
#     """
#     phonebook = {}                   # Create empty phonebook

#     while True:
#         name = input("Name: ")
#         if name == "":
#             break
#         number = input("Number: ")
#         phonebook[name] = number

#     return phonebook


# def print_phonebook(phonebook):
#     """
#     Prints out all the names/numbers in the phonebook.
#     """
#     for name in phonebook:
#         print(str(name) + " -> " + str(phonebook[name]))


# def lookup_numbers(phonebook):
#     """
#     Allow the user to lookup phone numbers in the phonebook
#     by looking up the number associated with a name.
#     """
#     while True:
#         name = input("Enter name to lookup: ")
#         if name == "":
#             break
#         if name not in phonebook:
#             print(name + " is not in the phonebook")
#         else:
#             print(phonebook[name])


# def main():
#     phonebook = read_phone_numbers()
#     print_phonebook(phonebook)
#     lookup_numbers(phonebook)


# # Python boilerplate.
# if __name__ == '__main__':
#     main()
# ```



def read_phone_numbers():
    """
    Ask the user for names/numbers to store in a phonebook (dictionary).
    Returns the phonebook.
    """
    phonebook = {}  # Create empty phonebook

    while True:
        name = input("Name: ")
        if name == "":
            break
        number = input("Number: ")
        phonebook[name] = number

    return phonebook


def print_phonebook(phonebook):
    """
    Prints out all the names/numbers in the phonebook.
    """
    print("\nPhonebook Entries:")
    for name in phonebook:
        print(f"{name} -> {phonebook[name]}")


def lookup_numbers(phonebook):
    """
    Allow the user to look up phone numbers in the phonebook
    by entering a name.
    """
    print("\nLookup Numbers:")
    while True:
        name = input("Enter name to lookup: ")
        if name == "":
            break
        if name in phonebook:
            print(f"{name}'s number is {phonebook[name]}")
        else:
            print(f"{name} is not in the phonebook.")


def main():
    phonebook = read_phone_numbers()
    print_phonebook(phonebook)
    lookup_numbers(phonebook)


# This line ensures the main function runs when the file is executed
if __name__ == '__main__':
    main()
