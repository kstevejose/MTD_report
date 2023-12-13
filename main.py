import os

var = input('Hello Ma, Should I run MTD report script?(y/n) ')

if var == 'y':

    print('Ok, Beeni Ma...I am running it')
    exec(open('mtd_report.py').read())
    print('I have completed running the program, Ma. You can check the file name which starts with "MTD report"')

elif var == 'n':

    print('Mo ti gbo e')
else:

    print('Invalid Option')
