from flask import Flask, render_template, request, redirect, url_for, flash
import joblib
from groq import Groq
import sqlite3
from datetime import datetime

import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

def get_db_connection():
    conn = sqlite3.connect('user.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/main", methods=["GET", "POST"])
def main():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM user ORDER BY timestamp DESC').fetchall()
    conn.close()
    return render_template("main.html", users=users)

@app.route("/add_user", methods=["POST"])
def add_user():
    username = request.form.get('username')
    if not username:
        flash('Username is required!')
        return redirect(url_for('main'))
    
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO user (name, timestamp) VALUES (?, ?)', 
                    (username, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()
        log_action('ADD', username)
        flash('User added successfully!', 'success')
    except sqlite3.IntegrityError:
        flash('User already exists!', 'error')
    
    return redirect(url_for('main'))

@app.route("/delete_user", methods=["POST"])
def delete_user():
    username = request.form.get('username')
    if not username:
        flash('Username is required!')
        return redirect(url_for('main'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user WHERE name = ?', (username,))
    rows_deleted = cursor.rowcount
    conn.commit()
    
    if rows_deleted > 0:
        log_action('DELETE', username)
        flash('User deleted successfully!', 'success')
    else:
        flash('User not found!', 'error')
    conn.close()
    
    return redirect(url_for('main'))

@app.route("/llama",methods=["GET","POST"])
def llama():
    return(render_template("llama.html"))

@app.route("/llama_reply",methods=["GET","POST"])
def llama_reply():
    q = request.form.get("q")
    # load model
    client = Groq()
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": q
            }
        ]
    )
    return(render_template("llama_reply.html",r=completion.choices[0].message.content))

@app.route("/deepseek",methods=["GET","POST"])
def deepseek():
    return(render_template("deepseek.html"))

@app.route("/deepseek_reply",methods=["GET","POST"])
def deepseek_reply():
    q = request.form.get("q")
    # load model
    client = Groq()
    completion_ds = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {
                "role": "user",
                "content": q
            }
        ]
    )
    return(render_template("deepseek_reply.html",r=completion_ds.choices[0].message.content))

@app.route("/dbs",methods=["GET","POST"])
def dbs():
    return(render_template("dbs.html"))

@app.route("/prediction",methods=["GET","POST"])
def prediction():
    q = float(request.form.get("q"))
    # load model
    model = joblib.load("dbs.jl")
    # make prediction
    pred = model.predict([[q]])
    return(render_template("prediction.html",r=pred))

import requests

@app.route("/telegram",methods=["GET","POST"])
def telegram():
    domain_url = 'https://dsat-ft1-stackupdev.onrender.com'
    # The following line is used to delete the existing webhook URL for the Telegram bot
    delete_webhook_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"
    requests.post(delete_webhook_url, json={"url": domain_url, "drop_pending_updates": True})
    # Set the webhook URL for the Telegram bot
    set_webhook_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={domain_url}/webhook"
    webhook_response = requests.post(set_webhook_url, json={"url": domain_url, "drop_pending_updates": True})
    if webhook_response.status_code == 200:
        # set status message
        status = "The telegram bot is running."
    else:
        status = "Failed to start the telegram bot."
    return(render_template("telegram.html", r=status))

@app.route("/stop_telegram",methods=["GET","POST"])
def stop_telegram():
    domain_url = 'https://dsat-ft1-stackupdev.onrender.com'
    # The following line is used to delete the existing webhook URL for the Telegram bot
    delete_webhook_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"
    webhook_response = requests.post(delete_webhook_url, json={"url": domain_url, "drop_pending_updates": True})
    # Set the webhook URL for the Telegram bot
    if webhook_response.status_code == 200:
        # set status message
        status = "The telegram bot has stop."
    else:
        status = "Failed to stop the telegram bot."
    return(render_template("stop_telegram.html", r=status))

@app.route("/webhook",methods=["GET","POST"])
def webhook():
    # This endpoint will be called by Telegram when a new message is received
    update = request.get_json()
    if "message" in update and "text" in update["message"]:
        # Extract the chat ID and message text from the update
        chat_id = update["message"]["chat"]["id"]
        query = update["message"]["text"]

        # Pass the query to the Groq model
        client = Groq()
        completion_ds = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {
                    "role": "user",
                    "content": query
                }
            ]
        )
        response_message = completion_ds.choices[0].message.content

        # Send the response back to the Telegram chat
        send_message_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(send_message_url, json={
            "chat_id": chat_id,
            "text": response_message
        })
    return('ok', 200)

def log_action(action, username):
    """Log user actions to the database"""
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO logs (action, username, timestamp) 
        VALUES (?, ?, ?)
    ''', (action, username, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

@app.route("/logs")
def view_logs():
    """Display all logs"""
    conn = get_db_connection()
    logs = conn.execute('''
        SELECT * FROM logs 
        ORDER BY timestamp DESC
    ''').fetchall()
    conn.close()
    return render_template("logs.html", logs=logs)

if __name__ == "__main__":
    # Initialize database tables if they don't exist
    conn = sqlite3.connect('user.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user (
            name TEXT PRIMARY KEY,
            timestamp TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            username TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL
        )
    ''')
    conn.close()
    
    # Add flash message support
    app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key
    app.run(debug=True)

