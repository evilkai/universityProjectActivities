import os
from random import randint


for i in range(20):
    numb = randint(243, 260)
    d =str(numb) + " days ago"
    with open("a.txt", 'a') as file:
        file.write("a")
    os.system('git add .')
    os.system('git commit --date="' + d +'" -m "commit"')
    os.system('git push origin master')
    for i in range(randint(0,2)):
        with open("a.txt", 'a') as file:
            file.write("a")
        os.system('git add .')
        os.system('git commit --date="' + d +'" -m "commit"')
        os.system('git push origin main')