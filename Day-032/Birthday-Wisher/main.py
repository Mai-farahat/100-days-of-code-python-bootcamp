##################### Hard Starting Project ######################
import pandas as pd
import smtplib
import datetime as dt
import random

my_email = "maifarahat00@gmail.com"
password = "fvuxfnicbpahrwht"

now = dt.datetime.now()
month = now.month
day = now.day
today_tuple = (month, day)
data = pd.read_csv("birthdays.csv")
birthday_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}


if today_tuple in birthday_dict:
    birthday_person = birthday_dict[today_tuple]
    rand_letter = random.randint(1, 3)
    file_path = f"letter_templates/letter_{rand_letter}.txt"
    with open(file_path) as letter_file:
        content = letter_file.read()
        content = content.replace("NAME", birthday_person["name"])
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=birthday_person["email"],
            msg=f"Subject:Happy Birthday\n\n{content}"
        )



