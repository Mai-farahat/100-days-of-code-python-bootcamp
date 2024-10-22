#FileNotFound
# with open("a_file.txt") as file:
#     file.read()

#KeyError
# a_dictionary = {"key": "value"}
# value = a_dictionary["non_existent_key"]

#IndexError
# fruit_list = ["Apple", "Banana", "Pear"]
# fruit = fruit_list[3]

#TypeError
# text = "abc"
# print(text + 5)

# try:
#     file = open('a_file.txt')
#     a_dictionary = {"key": "value"}
#     print(a_dictionary["key"])
# except FileNotFoundError:
#     file = open('a_file.txt', "w")
#     file.write("Something")
# except KeyError as error_message:
#     print(f"The key {error_message} doesn't  exist.")
# else:
#     content = file.read()
#     print(content)
# finally:
#     # file.close()
#     # print("File was closed")
#     raise KeyError("This is an error that i made up")


# height = float(input("Height: "))
# weight = float(input("Weight: "))
#
# if height > 3:
#     raise ValueError("Human height should not be over 3 meters.")
#
# bmi = weight / height ** 2
# print(bmi)

