#If the bill was $150.00, split between 5 people, with 12% tip.

#Each person should pay (150.00 / 5) * 1.12 = 33.6
#Format the result to 2 decimal places = 33.60

#Tip: There are 2 ways to round a number. You might have to do some Googling to solve this.💪

#Write your code below this line 👇

print("Welcome to the tip calculator.")
total_bill = input("What was the total bill? $")
percent = input("What percentage tip would you like to give? 10, 12, or 15?")
no_people = input("How many people to spilt the bill?")
pay_each_person = (float(total_bill) / int(no_people)) * (1 + int(percent) / 100)

#final = round(pay_each_person , 2)
final = "{:.2f}".format(pay_each_person)
print(f"Each person should pay: ${final} ")