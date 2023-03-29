import re
import long_responses as long
from  database.responses import get_response

while True:
    print('Bot: ' + get_response(input('You: ')))
