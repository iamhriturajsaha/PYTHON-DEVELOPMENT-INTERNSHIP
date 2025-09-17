# TUPLE TASKS

# Create a tuple of 5 cities
cities = ("New York", "Paris", "Tokyo", "London", "Paris")

# Print the first and last city
print("First city:", cities[0])
print("Last city:", cities[-1])

# Try to change one city (will throw an error if uncommented)
# cities[1] = "Berlin"  # ❌ Tuples are immutable

# Count how many times a particular city appears
print("Count of 'Paris':", cities.count("Paris"))

# Find the index of a given city
print("Index of 'Tokyo':", cities.index("Tokyo"))

# Iterate and print cities in uppercase
print("Cities in uppercase:")
for city in cities:
    print(city.upper())
