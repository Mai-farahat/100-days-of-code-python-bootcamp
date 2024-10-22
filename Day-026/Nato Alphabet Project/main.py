import pandas


#TODO 1. Create a dictionary in this format:
data = pandas.read_csv("nato_phonetic_alphabet.csv")
df = pandas.DataFrame(data)
phonetic_dict = {row.letter: row.code for (index, row) in df.iterrows()}
# print(phonetic_dict)

#TODO 2. Create a list of the phonetic code words from a word that the user inputs.
def generate_phonatic():
    word = input("Enter the Word:").upper()
    try:
        output_list = [phonetic_dict[n] for n in word]
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
        generate_phonatic()
    else:
        print(output_list)

generate_phonatic()