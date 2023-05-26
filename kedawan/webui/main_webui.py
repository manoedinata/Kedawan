from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

import requests

from datetime import datetime
from pytz import timezone

from kedawan.config import config

from sqlalchemy import func
from kedawan.db import db
from kedawan.db import FastLinks
from kedawan.db import Visitor
from kedawan.db import IPAddressLog
from kedawan.webui.utils import setIPFromDB

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
    # TODO: Check the total of specific column instead
    # Length of column(fast_links_id=id)
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

    ip_db = setIPFromDB(ip)
    # TODO: Check if ip_db succeed

    visitor = Visitor(
        fast_links_id=fastlinks.id,
        visit_date=currentDate,
        ip_address_id=ip_db["id"]
    )
    db.session.add(visitor)

    # Commit the changes
    db.session.commit()

    return redirect(fastlinks.url)
