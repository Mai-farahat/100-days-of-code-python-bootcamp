import random
#import my_module
#print(my_module.pi)

random_integer = random.randint(1, 10)
#print(random_integer)

# 0.000000 - 0.9999999
random_float = random.random()
#print(random_float)

# 0.000000 - 4.9999999999
random_decimal = random_float * 5
#print(random_decimal)

states_of_america = ["Delaware", "Pennsylvania", "New Jersey"]
print(states_of_america[0])
#count from the end of the list
print(states_of_america[-1])
#change the item in the list
states_of_america[1] = "Pencilvania"
print(states_of_america)
#add an item to the end of the list
states_of_america.append("Angelaland")
print(states_of_america)
#add a list to the end of the list
states_of_america.extend(["Angelaland", "Jack Bauer Land"])
print(states_of_america)

print(len(states_of_america))
print(states_of_america[5])

#dirty_dozen = ["Strawberries", "Spinach", "Kale", "N
fruits = ["Strawberries", "Nectarines", "Apples", "Grapes", "Peaches", "Cherries", "Pears"]
vegetables = ["Spinach", "Kale", "Tomatoes", "Celery", "Potatoes"]

dirty_dozen = [fruits, vegetables]
print(dirty_dozen)
print(dirty_dozen[0])
print(dirty_dozen[1])
print(dirty_dozen[1][2])
print(dirty_dozen[1][3])