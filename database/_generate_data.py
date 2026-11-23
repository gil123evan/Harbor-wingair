import random
import mysql.connector
from faker import Faker

fake = Faker()

# Connect to XAMPP MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="harborwingair"
)
cursor = db.cursor()

print("Seeding database...")

# 1. Populate status_code
statuses = [
    ('CONFIRMED', 'Payment received and confirmed'),
    ('PENDING', 'Payment authorization pending'),
    ('FAILED', 'Payment transaction failed'),
    ('REFUNDED', 'Payment returned to passenger')
]
cursor.executemany("INSERT IGNORE INTO status_code (status_code, description) VALUES (%s, %s)", statuses)

# 2. Populate airport
airports = [
    ('PPS', 'Puerto Princesa International Airport', 'Puerto Princesa', 'Philippines'),
    ('MNL', 'Ninoy Aquino International Airport', 'Manila', 'Philippines'),
    ('CEB', 'Mactan-Cebu International Airport', 'Cebu', 'Philippines'),
    ('DVO', 'Francisco Bangoy International Airport', 'Davao', 'Philippines'),
    ('IAH', 'George Bush Intercontinental Airport', 'Houston', 'USA')
]
cursor.executemany("INSERT IGNORE INTO airport (airport_code, airport_name, city, country) VALUES (%s, %s, %s, %s)", airports)

# 3. Populate booking_agent (50 records)
agent_ids = []
for _ in range(50):
    cursor.execute(
        "INSERT INTO booking_agent (agent_name, email, phone) VALUES (%s, %s, %s)",
        (fake.company(), fake.unique.company_email(), fake.phone_number()[:20])
    )
    agent_ids.append(cursor.lastrowid)

# 4. Populate passenger (50 records)
passenger_ids = []
for _ in range(50):
    cursor.execute(
        "INSERT INTO passenger (first_name, last_name, email, phone) VALUES (%s, %s, %s, %s)",
        (fake.first_name(), fake.last_name(), fake.unique.email(), fake.phone_number()[:20])
    )
    passenger_ids.append(cursor.lastrowid)

# 5. Populate flight_schedule
flight_numbers = ['HW101', 'HW102', 'HW201', 'HW202', 'HW301']
schedules = [
    ('HW101', 'PPS', 'MNL', '08:00:00', '09:15:00'),
    ('HW102', 'MNL', 'PPS', '10:30:00', '11:45:00'),
    ('HW201', 'MNL', 'CEB', '13:00:00', '14:15:00'),
    ('HW202', 'CEB', 'MNL', '15:30:00', '16:45:00'),
    ('HW301', 'MNL', 'DVO', '18:00:00', '19:45:00')
]
cursor.executemany("INSERT IGNORE INTO flight_schedule (flight_number, departure_airport, arrival_airport, departure_time, arrival_time) VALUES (%s, %s, %s, %s, %s)", schedules)

# 6. Populate reservation (50 records)
reservation_ids = []
for _ in range(50):
    p_id = random.choice(passenger_ids)
    a_id = random.choice(agent_ids)
    b_date = fake.date_time_this_year()
    cursor.execute(
        "INSERT INTO reservation (passenger_id, booking_agent_id, booking_date) VALUES (%s, %s, %s)",
        (p_id, a_id, b_date)
    )
    reservation_ids.append(cursor.lastrowid)

# 7. Populate flight_leg & leg_cost (50 records)
for res_id in reservation_ids:
    f_num = random.choice(flight_numbers)
    cursor.execute(
        "INSERT INTO flight_leg (reservation_id, flight_number, leg_sequence) VALUES (%s, %s, %s)",
        (res_id, f_num, 1)
    )
    leg_id = cursor.lastrowid
    
    # Leg cost
    cost = round(random.uniform(50.00, 300.00), 2)
    cursor.execute(
        "INSERT INTO leg_cost (leg_id, cost_amount, currency) VALUES (%s, %s, %s)",
        (leg_id, cost, 'USD')
    )

# 8. Populate payment (50 records)
status_codes = ['CONFIRMED', 'PENDING', 'FAILED', 'REFUNDED']
for res_id in reservation_ids:
    amount = round(random.uniform(50.00, 300.00), 2)
    p_date = fake.date_time_this_year()
    st_code = random.choice(status_codes)
    cursor.execute(
        "INSERT INTO payment (reservation_id, payment_amount, payment_date, payment_status_code) VALUES (%s, %s, %s, %s)",
        (res_id, amount, p_date, st_code)
    )

db.commit()
print("Successfully seeded all 9 tables with test data!")
cursor.close()
db.close()