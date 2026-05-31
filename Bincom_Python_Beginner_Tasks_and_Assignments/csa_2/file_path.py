import os

print("without normalizing: ", os.path.abspath(__file__))
print("with normalizing: ", os.path.dirname(os.path.abspath(__file__)))