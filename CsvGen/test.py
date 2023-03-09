from faker import Faker
import random
fake = Faker()

# print(fake.name())
# print(fake.address())
# print(fake.date())
# print(fake.email())
# print(fake.job())
# print(fake.company())
# print(fake.phone_number())
# print(fake.automotive())

i = 'date'

if i == 'name':
    print(fake.name())
elif i == 'date':
    print(fake.address())
elif i == 'email':
    print(fake.email())
else:
    print("wrong type")

r = random.randint(1, 3)

print(r)

