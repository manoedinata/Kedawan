from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

import requests

from dotenv import dotenv_values

from datetime import datetime
from pytz import timezone

from kedawan.db import db
from kedawan.db import FastLinks
from kedawan.db import Visitor

config = dotenv_values(".env") 

jakartaTz = timezone("Asia/Jakarta")

main_webui = Blueprint("main_webui", __name__, template_folder="templates")

@main_webui.route("/")
def home():
    return render_template("webui/home.html")

@main_webui.route("/<slug>")
def linksredirect(slug):
    fastlinks = FastLinks.query.filter_by(slug=slug).first()
    if not fastlinks:
        return "Not found!"

    # Increment visitor
    fastlinks.visitor += 1
    db.session.add(fastlinks)

    # Insert user IP country
    currentDate = datetime.now(jakartaTz)

    # IP
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr

    print(ip)

    try:
        ipInfoReq = requests.get("https://ipinfo.io/" + ip, params={
            "token": config["IPINFO_TOKEN"]
        }).json()
        country = ipInfoReq["country"]
    except:
        country = "00"

    visitor = Visitor(
        fast_links_id=fastlinks.id,
        country_code=country,
        visit_date=currentDate
    )
    db.session.add(visitor)

    # Commit the changes
    db.session.commit()

    return redirect(fastlinks.url)
