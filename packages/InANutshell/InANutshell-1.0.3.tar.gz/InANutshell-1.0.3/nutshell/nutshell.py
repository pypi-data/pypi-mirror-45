import pyperclip as pc
from nutshell import text

print(text.intro)

def meme():
    """ Makes user input into nutshell text """

    counter = 1
    user_input = input("What would you like put in a nutshell? ")
    input_split = list(user_input.lower())
    split_string = []

    for i in input_split:
        if counter % 2 != 0:
            split_string.append(i)
        elif counter % 2 == 0:
            split_string.append(i.upper())
        counter += 1    

    output ="".join(split_string)

    print(f"Someone: \"{user_input}\"")
    print(f"Me: {output}")

    copy_query = input(text.copy_it).lower()

    while copy_query != "y" or copy_query != "n":
        if copy_query == "y":
            print(f"Copied \"{output}\".")
            pc.copy(output)
            copy_query = ""
            break
        elif copy_query == "n":
            copy_query = ""
            break
        else:
            print(text.error)
            copy_query = input(text.copy_it).lower()

def restart_meme():
    restart = input(text.restart_it).lower()
    while restart != "y" or restart != "n":
        if restart == "y":
            restart = ""
            meme()
        elif restart == "n":
            restart = ""
            print(text.outro)
            break
        else:
            print(text.error)
            restart = input(text.restart_it).lower()

def run():
    meme()
    restart_meme()

if __name__ == '__main__':
    run()
