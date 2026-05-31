with open("my_name.txt", "r") as f:
    full_name = f.read()

name_parts = full_name.split()

first_name = name_parts[1]
middle_name = name_parts[2]
last_name = name_parts[0]

print(f"my names are: \n\tfirst_name: {first_name}\n\tmiddle_name: {middle_name}\n\tlast_name: {last_name}")