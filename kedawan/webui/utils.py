import requests

from dotenv import dotenv_values

from sqlalchemy import func
from kedawan.db import db
from kedawan.db import IPAddressLog

config = dotenv_values(".env") 

def reqIPInfoAPI(ipAddress: str) -> dict:
    ipInfoReq = requests.get("https://ipinfo.io/" + ipAddress, params={
        "token": config["IPINFO_TOKEN"]
    }).json()
    return ipInfoReq

def setIPFromDB(ipAddress: str) -> dict:
    ip_db = IPAddressLog.query.filter_by(
        ip_address = func.inet6_aton(ipAddress)
    ).first()

    if not ip_db:
        try:
            reqAPI = reqIPInfoAPI(ipAddress)
            country_code = reqAPI.get("country", "00")
        except:
            country_code = "00"

        try:
            ip_db = IPAddressLog(
                ip_address=func.inet6_aton(ipAddress),
                country_code=country_code
            )
            db.session.add(ip_db)
            db.session.commit()
        except:
            return {} # Return empty dict

    return ip_db.serialize
