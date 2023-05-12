

def input_converter(user_input):
    if user_input in ["Yes", "yes", 'Y', "y"]:
        user_input = True
    if user_input in ["No", "no", "N", "n"]:
        user_input = False
    return input
