# ## Problem Statement

# Write a Python program that takes two integer inputs from the user and calculates their sum. The program should perform the following tasks:

# 1. Prompt the user to enter the first number.

# 2. Read the input and convert it to an integer.

# 3. Prompt the user to enter the second number.

# 4. Read the input and convert it to an integer.

# 5. Calculate the sum of the two numbers.

# 6. Print the total sum with an appropriate message.

# The provided solution demonstrates a working implementation of this problem, where the main() function guides the user through the process of entering two numbers and displays their sum.


def main():
    print("This program adds two numbers.")
    
    # Prompt and read first number
    num1 = int(input("Enter first number: "))
    
    # Prompt and read second number
    num2 = int(input("Enter second number: "))
    
    # Calculate sum
    total = num1 + num2

    # Display result
    print("The total is", total)


# Call main when the script is executed
if __name__ == '__main__':
    main()




