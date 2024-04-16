import sys

class Module1:

    # class scope variables
     firstterm = 0.0
     secondterm = 0.0
     _sum = 0.0
     _product = 0.0
     _difference = 0.0
     _quotient = 0.0

    # class constructor – more of this Module 5
     def __init__(self):
        pass

    # setter method for first term – more of this in Module 5
     def set_first_term(self,first_term):
         self._first_term = first_term
         return

    # getter method for the first_term – more of this in Module 5
     def get_first_term(self):
         return self._first_term

    # setter method for second term – more of this in Module 5
     def set_second_term(self,second_term):
         self._second_term = second_term
         return

    # getter method for the first_term – more of this in Module 5
     def get_second_term(self):
        return self._second_term

def main():
    example1 = Module1()
    try:
     first_number = float(input('Input first number:'))
     example1.set_first_term(first_number)
    except ValueError:
     print('Not a number!')
     sys.exit()
    try:
     second_number = float(input('Input second number:'))
     example1.set_second_term(second_number)
    except ValueError:
     print('Not a number!')
     sys.exit()

# print out the sum
    print(str(example1.get_first_term()) +  '+'  \
     + str(example1.get_second_term()) +  '='  \
     + str(example1.get_first_term() + example1.get_second_term()))

if __name__ == '__main__': main()