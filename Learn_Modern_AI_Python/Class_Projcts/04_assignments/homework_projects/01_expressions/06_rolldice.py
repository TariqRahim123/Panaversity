# ## Problem Statement

# Simulate rolling two dice, and prints results of each roll as well as the total.

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
# """
# Simulate rolling two dice, and prints results of each
# roll as well as the total.
# """
# # Import the random library which lets us simulate random things like dice!
# import random

# # Number of sides on each die to roll
# NUM_SIDES: int = 6

# def main():
#     # Setting a seed is useful for debugging (uncomment the line below to do so!)
#     # random.seed(1)
    
#     # Roll die
#     die1: int = random.randint(1, NUM_SIDES)
#     die2: int = random.randint(1, NUM_SIDES)
    
#     # Get their total
#     total: int = die1 + die2
    
#     # Print out the results
#     print("Dice have", NUM_SIDES, "sides each.")
#     print("First die:", die1)
#     print("Second die:", die2)
#     print("Total of two dice:", total)


# # This provided line is required at the end of a Python file
# # to call the main() function.
# if __name__ == '__main__':
#     main()

# ```


"""
Simulate rolling two dice, and print the results of each
roll as well as the total.
"""

import random

# Number of sides on each die
NUM_SIDES = 6

def main():
    # Optional: set a seed for reproducibility
    # random.seed(1)

    # Roll two dice
    die1 = random.randint(1, NUM_SIDES)
    die2 = random.randint(1, NUM_SIDES)

    # Calculate total
    total = die1 + die2

    # Print the results
    print("Dice have", NUM_SIDES, "sides each.")
    print("First die:", die1)
    print("Second die:", die2)
    print("Total of two dice:", total)


if __name__ == '__main__':
    main()
