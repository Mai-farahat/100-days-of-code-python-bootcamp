student_dict = {
    "student": ["Angela", "james", "lily"],
    "score": [56, 76, 98]
}

import pandas

student_data_frame = pandas.DataFrame(student_dict)
# print(student_data_frame)
#
# #Loop through a dataframe
# for (key, value) in student_data_frame.items():
#     print(value)

#Loop through rows of a dataframe
for (index, row) in student_data_frame.iterrows():
    if row.student == "Angela":
        print(row.score)