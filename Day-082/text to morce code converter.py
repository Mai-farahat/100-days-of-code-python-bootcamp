MORSE_CODE = {
    'A': '.-',   'B': '-...', 'C': '-.-.', 'D': '-..',  'E': '.',
    'F': '..-.', 'G': '--.',  'H': '....', 'I': '..',   'J': '.---',
    'K': '-.-',  'L': '.-..', 'M': '--',   'N': '-.',   'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.',  'S': '...',  'T': '-',
    'U': '..-',  'V': '...-', 'W': '.--',  'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
    '!': '-.-.--', '/': '-..-.', '(': '-.--.',  ')': '-.--.-',
    '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-',
    '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.',
    '$': '...-..-', '@': '.--.-.', ' ': '/'
}


def text_to_morse(text: str) -> str:
    result = []
    for char in text.upper():
        if char in MORSE_CODE:
            result.append(MORSE_CODE[char])
        else:
            result.append(f'[{char}]')  # unsupported characters shown as-is
    return ' '.join(result)


def morse_to_text(morse: str) -> str:
    REVERSE = {v: k for k, v in MORSE_CODE.items()}
    words = morse.strip().split(' / ')
    decoded_words = []
    for word in words:
        letters = word.split()
        decoded_word = ''
        for code in letters:
            decoded_word += REVERSE.get(code, f'[{code}]')
        decoded_words.append(decoded_word)
    return ' '.join(decoded_words)


def print_banner():
    print("""
  __  __                     ____          _      
 |  \\/  | ___  _ __ ___  ___/ ___|___   __| | ___ 
 | |\\/| |/ _ \\| '__/ __|/ _ \\___ \\/ _ \\ / _` |/ _ \\
 | |  | | (_) | |  \\__ \\  __/___) |  __/| (_| |  __/
 |_|  |_|\\___/|_|  |___/\\___|____/ \\___| \\__,_|\\___|
                    Morse Code Converter
    """)


def main():
    print_banner()
    print("Options:")
    print("  1. Text  → Morse Code")
    print("  2. Morse → Text")
    print("  3. Quit\n")

    while True:
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == '1':
            text = input("Enter text: ")
            morse = text_to_morse(text)
            print(f"\n📡 Morse Code:\n{morse}\n")

        elif choice == '2':
            print("(Separate letters with spaces, words with ' / ')")
            morse = input("Enter Morse code: ")
            text = morse_to_text(morse)
            print(f"\n📝 Decoded Text:\n{text}\n")

        elif choice == '3':
            print("73 de Morse! (That means goodbye in ham radio speak 👋)")
            break

        else:
            print("Invalid option. Please choose 1, 2, or 3.\n")


if __name__ == "__main__":
    main()