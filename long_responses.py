import random

R_SORRY = "i'm sorry to hear that. is there anything I can do to help?"
def unknown():
    response = ['Could you please re-phrase that?',
                "Sorry I dont't understand that",
                "Sounds about right",
                "What does that mean?"][random.randrange(4)]
    return response