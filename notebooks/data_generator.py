"""Generate synthetic beneficiary data."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from faker import Faker
import pandas as pd
import random
from config import BENEFICIARIES_RAW

fake = Faker()

data = []

for i in range(1000):
    data.append({
        "beneficiary_id": i,
        "name": fake.name(),
        "phone": fake.phone_number(),
        "address": fake.address(),
        "bank_account": random.randint(10000000,99999999),
        "scheme": random.choice(["Food Subsidy","Farmer Aid","Scholarship"]),
        "amount": random.choice([2000,5000,10000]),
        "district": fake.city(),
        "date": fake.date()
    })

# Ensure directory exists
BENEFICIARIES_RAW.parent.mkdir(parents=True, exist_ok=True)

df = pd.DataFrame(data)
df.to_csv(BENEFICIARIES_RAW, index=False)

print(f"Dataset generated! Saved to {BENEFICIARIES_RAW}")
