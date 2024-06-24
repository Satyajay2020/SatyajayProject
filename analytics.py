from flask import Blueprint, render_template, url_for, request, redirect, flash, make_response
from flask_login import login_required, current_user
from models import *  # import database details
from sqlalchemy import or_
import matplotlib.pyplot as plt
import io
import base64
import sqlite3

# creating blueprint for analytics page
analytics = Blueprint("analytics", __name__)


@login_required
@analytics.route("/analysis")
def analysis():
    conn = sqlite3.connect('ticket.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, avg_rating FROM Show")
    data = cursor.fetchall()
    x = [row[0] for row in data]
    y = [row[1] for row in data]
    print(x)
    print(y)

    plt.plot(x, y)
    plt.xlabel('Show Name')
    plt.ylabel('Avg Rating')
    plt.title('Ratings graph')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='jpeg')
    buffer.seek(0)

    image_jpeg = buffer.getvalue()
    graph = base64.b64encode(image_jpeg).decode('utf-8')

    return render_template("analysis.html", user=current_user, admin=current_user, graph=graph)
