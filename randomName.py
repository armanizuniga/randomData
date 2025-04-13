import faker


# Function generates random names and returns array of names
def generate_names():
    # Initialize Faker
    # fake = faker.Faker('en_US')
    # Array to store names
    names = ['Sharon Frost', 'Patty Flores', 'Monkey D. Luffy', 'Nicole Strickland', 'Kevin Miles', 'Micheal Wright',
             'Stephen Willis', 'Naruto Uzumaki', 'John Hart', 'Eren Yeager', 'Jessica Burnett', 'Michael Hernandez',
             'Anthony Adams', 'Levi Ackerman', 'Amy Castaneda', 'Caleb Ramirez', 'Paula Duarte', 'Gon Freecss',
             'Robin Hutchinson', 'Alexandra Brown', 'Erica Wilson', 'Mikasa Ackerman', 'Lelouch Lamperouge',
             'Natalie Hall', 'Tanjiro Kamado', 'Brian Holloway', 'Christopher Reed', 'David Franklin', 'Anna Gardner',
             'Christine Richardson', 'Jordan Dickerson', 'Ronald Jones', 'Edward Elric', 'Light Yagami',
             'Christopher Ortiz', 'Elaine Schmitt', 'Joseph Bradley', 'Gojo Satoru', 'Richard Hughes', 'Shinji Ikari']

    # Generate 40 random names and store into an array
    # for _ in range(40):
    #   temp_name = fake.name()
    #   names.append(temp_name)

    # print(names)
    # Add period as output file prefix
    # with open(output_file, "w") as f:
    #   f.write(str(names))
    return names
