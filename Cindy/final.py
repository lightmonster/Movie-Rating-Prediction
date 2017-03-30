import sys

def get_expected_rating(user, movie):
	return 1

file_test = open("test.txt","r")
line_test = []
for line in file_test:
	line_test.append(line)

for i in range(1, len(line_test)):
	parse_line = line_test[i].split(",")
	rating = get_expected_rating(parse_line[1],parse_line[2])
	j = str(parse_line[0]) + " "
	j += str(rating)
	print(j)