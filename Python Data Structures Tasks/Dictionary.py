# DICTIONARY TASKS

# Create a dictionary of 5 students
marks = {
    "Alice": 85,
    "Bob": 92,
    "Charlie": 78,
    "David": 90,
    "Eva": 88
}

# Access the marks of a particular student
print("Bob's marks:", marks["Bob"])

# Add a new student and update existing student's marks
marks["Frank"] = 95
marks["Alice"] = 89
print("Updated dictionary:", marks)

# Delete one student
del marks["Charlie"]
print("After deleting Charlie:", marks)

# Iterate and print keys, values, and both
print("Keys:")
for name in marks.keys():
    print(name)

print("Values:")
for score in marks.values():
    print(score)

print("Keys and Values:")
for name, score in marks.items():
    print(name, ":", score)

# Find the student with highest marks
highest_student = max(marks, key=marks.get)
print("Topper:", highest_student, "with marks", marks[highest_student])
