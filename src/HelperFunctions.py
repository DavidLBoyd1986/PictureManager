

def input_converter(input):
    if input in ["Yes", "yes", 'Y', "y"]:
        input = True
    if input in ["No", "no", "N", "n"]:
        input = False
    return input
