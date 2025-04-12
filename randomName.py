import faker


# Function generates random names and returns array of names
def generate_names():
    # Initialize Faker
    fake = faker.Faker('en_US')

    # Array to store names
    names = []

    # Generate 40 random names and store into an array
    for _ in range(40):
        temp_name = fake.name()
        names.append(temp_name)

    return names
