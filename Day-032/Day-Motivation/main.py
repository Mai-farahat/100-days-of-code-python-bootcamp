import datetime as dt
import smtplib
import random

my_email = "maifarahat00@gmail.com"
password = "fvuxfnicbpahrwht"
to_email = "mai_farahat74@icloud.com"

now = dt.datetime.now()
week_day = now.weekday()
if week_day in range(0, 7):
    with open("quotes.txt", "r") as quotes_file:
        all_quotes = quotes_file.readlines()
        quote = random.choice(all_quotes)

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject:Day Motivation\n\n{quote}"
        )


