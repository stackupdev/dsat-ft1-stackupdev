# DSAI Chatbot & Prediction Web Flask App 

A Flask-based web application that combines chatbot interfaces, machine learning prediction, user session management, and Telegram bot integration. Designed for interactive demos, educational use, or as a foundation for production ML/AI web services.

## Features

- **User Login & Session Management**: Simple login using a username, tracked in a SQLite database.
- **Chatbots**:
  - **LLAMA Chatbot**: Query the LLAMA-3.1-8b-instant model via Groq API.
  - **Deepseek Chatbot**: Query the Deepseek-R1-Distill-Llama-70b model via Groq API.
- **DBS Share Price Prediction**: Enter USD/SGD exchange rate and get a predicted DBS share price using a pre-trained ML model.
- **Image Processing**: Sepia filter demo via embedded Gradio app.
- **Telegram Bot Integration**: Start/stop a Telegram bot and interact with LLMs via Telegram chat.
- **User Logging**: All logins and actions are tracked in a local SQLite database, with options to view and delete logs.

## App Structure

| Route               | Template              | Description                                 |
|---------------------|----------------------|---------------------------------------------|
| `/`                 | `index.html`         | Homepage, user login                        |
| `/main`             | `main.html`          | Dashboard, navigation                       |
| `/llama`            | `llama.html`         | LLAMA chatbot input                         |
| `/llama_reply`      | `llama_reply.html`   | LLAMA chatbot response                      |
| `/deepseek`         | `deepseek.html`      | Deepseek chatbot input                      |
| `/deepseek_reply`   | `deepseek_reply.html`| Deepseek chatbot response                   |
| `/dbs`              | `dbs.html`           | DBS price prediction input                  |
| `/prediction`       | `prediction.html`    | DBS price prediction result                 |
| `/sepia`            | `sepia.html`         | Sepia filter (Gradio app)                   |
| `/telegram`         | `telegram.html`      | Telegram bot status                         |
| `/stop_telegram`    | `stop_telegram.html` | Telegram bot stop status                    |
| `/user_log`         | `user_log.html`      | User log display                            |
| `/delete_log`       | `delete_log.html`    | Log deletion confirmation                   |

## Requirements

- Python 3.8+
- Flask
- gunicorn
- joblib
- scikit-learn
- groq
- requests

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. **Set Environment Variables**
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token (required for Telegram integration).

2. **Run the App**
```bash
python app.py
```

3. **Access in Browser**
   - Go to `http://localhost:5000`

4. **Telegram Integration**
   - Start/stop the bot from the dashboard.
   - Interact with the bot via Telegram chat (webhook is set automatically).

## File Structure

```
├── app.py                # Main Flask app
├── requirements.txt      # Python dependencies
├── user.db               # SQLite database for user logs
├── dbs.jl                # Serialized ML model (joblib)
├── static/
│   └── styles.css        # Stylesheet
├── templates/
│   ├── index.html        # Homepage/login
│   ├── main.html         # Dashboard
│   ├── llama.html        # LLAMA chatbot input
│   ├── llama_reply.html  # LLAMA chatbot response
│   ├── deepseek.html     # Deepseek chatbot input
│   ├── deepseek_reply.html # Deepseek chatbot response
│   ├── dbs.html          # DBS prediction input
│   ├── prediction.html   # DBS prediction result
│   ├── sepia.html        # Sepia filter demo
│   ├── telegram.html     # Telegram bot status
│   ├── stop_telegram.html # Telegram bot stop status
│   ├── user_log.html     # User log display
│   └── delete_log.html   # Log deletion confirmation
```

## Notes
- For ML prediction, ensure `dbs.jl` exists and is a valid joblib model file.
- For Telegram features, set your bot token as an environment variable.
- The sepia filter feature uses an embedded Gradio app hosted externally.

## License
MIT License
