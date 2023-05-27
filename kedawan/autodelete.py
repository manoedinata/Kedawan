"""
Python script to automatically delete expired short URLs.

This is not a part of Kedawan Flask app, but rather a cron script
that will be executed in each ~5 mins.
"""

from datetime import datetime
from pytz import timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config
from db import FastLinks

engine = create_engine(
    f"mariadb://{config['MYSQL_USER']}:{config['MYSQL_PASSWORD']}@{config['MYSQL_HOST']}:{config.get('MYSQL_PORT', 3306)}/{config['MYSQL_DATABASE']}",
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

jakartaTz = timezone("Asia/Jakarta") 

# Get expired URLs
# Where current date is larger than expire date
expiredURLs = session.query(FastLinks).filter(
    datetime.now(jakartaTz) >= FastLinks.expire
    # datetime.now(jakartaTz) <= FastLinks.expire   # Testing
).all()

if not expiredURLs:
    print("No expiring URLs! Exiting...")
    exit()

for url in expiredURLs:
    print(f"Marking ({url.slug}) for deletion...")
    session.delete(url)

print("Committing...")
session.commit()
