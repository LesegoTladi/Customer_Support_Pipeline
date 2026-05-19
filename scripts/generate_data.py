import pandas as pd
import logging
import random

#faker - used to generate fake data 
from faker import Faker

#Configure logging
logging.basicConfig(
    level=logging.INFO,
    format= ('%(asctime)s | %(levelname)s | %(message)s')
)

#Intialise Faker
fake=Faker()

#Ensure same data generated every run
random.seed(42)
Faker.seed(42)