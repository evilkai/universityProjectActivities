import os
from random import randint


for i in range(1):
    numb = randint(243, 299)
    d =str(numb) + " days ago"
    with open("a.txt", 'a') as file:
        file.write("a")
    os.system('git add .')
    os.system('git commit --date="' + d +'" -m "commit"')
    os.system('git push origin main')

    for i in range(randint(0,5)):
        n2 = randint(numb-4,numb+4)
        v = str(n2) + " days ago"
        with open("a.txt", 'a') as file:
            file.write("a")
        os.system('git add .')
        os.system('git commit --date="' + v +'" -m "commit"')
        os.system('git push origin main')