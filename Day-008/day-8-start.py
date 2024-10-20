# Review:
# Create a function called greet().
# Write 3 print statements inside the function.
# Call the greet() function and run your code.
def greet():
  print("Hello")
  print("Mai")
  print("How are you?")

#greet()

#Function that allows for input
def greet_with_name(name):
  print(f"Hello {name}")
  print(f"How do you do {name}?")
  print(f"Hi {name}")

#greet_with_name("Mai")

#Functions with more than 1 input
def greet_with(name, location):
  print(f"Hello {name}")
  print(f"What is it like in {location}?")

greet_with("Mai", "London")
#Functions with keyword arguments
greet_with(location = "london", name = "Mai")