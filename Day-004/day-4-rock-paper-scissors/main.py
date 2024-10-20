rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

#Write your code below this line 👇
import random
user_choice = int(input("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors."))

if user_choice == 0:
  print(rock)
elif user_choice == 1:
  print(paper)
else:
  print(scissors)

computer_choice = random.randint(0,2)
print(f"Computer chose {computer_choice}")
if computer_choice == 0:
  print(rock)
elif computer_choice == 1:
  print(paper)
else:
  print(scissors)
if user_choice == 0 and computer_choice == 2:
   print("You win!")
elif computer_choice == 0 and user_choice == 2:
  print("You lose")
elif computer_choice == 0 and user_choice == 1:
  print("You win!")
elif user_choice == 0 and computer_choice == 1:
  print("You lose")
elif computer_choice == 1 and user_choice == 2:
  print("You win!")
elif user_choice == 1 and computer_choice == 2:
  print("You lose")
elif computer_choice == user_choice:
  print("It's a draw")
elif user_choice >= 3 or user_choice < 0:
  print("You typed an invalid number, you lose!")