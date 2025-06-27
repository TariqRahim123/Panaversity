# ## Problem Statement

# Implement the following function which takes in 3 integers as parameters:

# def in_range(n, low, high)
#   """
#   Returns True if n is between low and high, inclusive. 
#   high is guaranteed to be greater than low.
#   """

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
# def in_range(n, low, high):
#   """
#   Returns True if n is between low and high, inclusive. 
#   high is guaranteed to be greater than low.
#   """
#     if n >= low and n <= high:
# 	return True

#     # we could have also included an else statement, but since we are returning, it's fine without!
#     return False
# ```



def in_range(n, low, high):
    """
    Returns True if n is between low and high, inclusive.
    high is guaranteed to be greater than low.
    """
    return low <= n <= high  # Simple and clean one-liner


# No need to change this block
def main():
    # Example tests
    print(in_range(5, 1, 10))   # True
    print(in_range(1, 1, 10))   # True
    print(in_range(10, 1, 10))  # True
    print(in_range(0, 1, 10))   # False
    print(in_range(11, 1, 10))  # False


if __name__ == '__main__':
    main()
