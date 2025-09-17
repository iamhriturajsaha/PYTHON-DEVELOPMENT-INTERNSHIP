# 1️⃣ LIST TASKS

# Create a list of 10 student names
students = ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Hannah", "Ian", "Julia"]

# Print the 3rd and 7th name
print("3rd student:", students[2])   # Index 2 = 3rd element
print("7th student:", students[6])   # Index 6 = 7th element

# Add a new name and remove one old name
students.append("Kevin")   # Adding new name
students.remove("Charlie") # Removing "Charlie"
print("Updated student list:", students)

# Find the length of the list
print("Length of list:", len(students))

# Write a program to find the sum of all even numbers in a list
numbers = [1, 2, 3, 4, 5, 6, 10, 15, 20]
even_sum = sum([num for num in numbers if num % 2 == 0])
print("Sum of even numbers:", even_sum)

# Slice the list to get only the first 5 names
print("First 5 students:", students[:5])

# Iterate through the list using a for loop and print each element
print("All students:")
for name in students:
    print(name)
