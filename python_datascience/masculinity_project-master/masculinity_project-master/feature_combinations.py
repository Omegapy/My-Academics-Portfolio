'''
To combine different features,
I modified the combinations() function from the itertools libray into the function f_combinations() 
to better suit the combinations of features.

Author: Alex Ricciardi
'''
def f_combinations(features_list, num):
    '''
        - Takes the arguments:
            - features_list, list data type, single features names list.
            - mum, integer type, the number of features per combination desired.

        - uses the nCr combination type to combine single features names into combinations of mum features names.
        - saves the combined feature names as list data type ocjects into a combinations list.

        - returns the combinations list.
    '''
    n = len(features_list)
    # Checks if the number of wanted combinations is larger than the number of element in the feature_list
    if num > n:
        return
    # Range value of the number of wanted combinations
    indices = list(range(num))
    # Returns the beginning of the feature list ranged to the number of wanted combinations
    yield list(features_list[i] for i in indices)
    # Infinte loop no break then return
    # for loops also have an else.
    # The else clause executes after the loop completes normally.
    # This means that the loop did not encounter a break statement.
    while True:
        # Reverse range of the number of wanted combinations
        for i in reversed(range(num)):
            # Checks if the value at index i of the reverse range value of the number of wanted combinations
            # is not equal to the number of features + i minus the number of wanted combinations
            if indices[i] != i + n - num:
                break
        # If not break
        else:
            return
        # If breack true
        indices[i] += 1
        # Increments by 1 the values of indices
        for j in range(i + 1, num):
            indices[j] = indices[j - 1] + 1
        # Returns the features_list values at the index values of the incremented indices
        yield list(features_list[i] for i in indices)