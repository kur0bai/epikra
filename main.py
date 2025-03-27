from functions import Functions

if __name__ == '__main__':
    functions = Functions()
    text = input('Please insert the text: ')
    functions.generate(text, 'outpuit.png')