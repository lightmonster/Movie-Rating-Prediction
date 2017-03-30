import sys

class User:
    def __init__(self,ID,gender,age,occupation):
        self.ID = ID
        if gender != "N/A":
            if gender == 'M':
                self.gender = 0
            else:
                self.gender = 1
        else:
            self.gender = None
        if age != "N/A":
            self.age = age
        else:
            self.age = None
        if occupation != "N/A":
            self.occupation = occupation
        else:
            self.occupation = None

user_dictionary = dict()
lines = []
count_user = -1

file_ = open("user.txt", "r")

for line in file_:
    lines.append(line)
    count_user += 1

for i in range(1,count_user + 1):
    result = lines[i].split(",")
    temp_user = User(result[0],[1],[2],[3])
    user_dictionary[result[0]] = temp_user

print (count_user)
