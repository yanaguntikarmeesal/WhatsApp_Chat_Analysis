


# 💬 WhatsApp Chat Analyzer

A Python and Streamlit project for analyzing exported WhatsApp chat data.


**Developed by:** **Yanaguntikar Meesal**


**📧 Email:** **[yanaguntikarm@gmail.com](mailto:yanaguntikarm@gmail.com)**


**🌐 Live Project:** https://whatsappchatanalysis-dhysuccmgtkyo84vsykyve.streamlit.app

https://whatsappchatanalysis-dhysuccmgtkyo84vsykyve.streamlit.app/
 

## 📁 Project Structure

```text
WhatsApp-Chat-Analyzer/
│
├── app.py
├── preprocessor.py
├── helper.py
├── stop_hinglish.txt
├── requirements.txt
└── README.md
````

---

# 🚀 Installation

## Step 1: Open Project

Open the project folder in VS Code.

Open the VS Code terminal.

---

## Step 2: Install Required Libraries

Run:

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

Run:

```bash
streamlit run app.py
```

If the above command does not work, use:

```bash
python -m streamlit run app.py
```

The Streamlit webpage will open in your browser.

---

# 📱 How to Get WhatsApp Chat File

Open WhatsApp.

Select the chat you want to analyze.

Choose:

```text
Chat Information
        ↓
Export Chat
        ↓
Without Media
```

Save the exported `.txt` file.

Upload that `.txt` file using the Streamlit sidebar.

---

# 📊 Features

The application provides:

### 1. Top Statistics

* Total Messages
* Total Words
* Media Shared
* Links Shared

### 2. Monthly Timeline

Shows the number of messages sent during each month.

### 3. Daily Timeline

Shows daily messaging activity.

### 4. Activity Map

Shows:

* Most Busy Day
* Most Busy Month

### 5. Weekly Activity Heatmap

Shows messaging activity by:

* Day
* Hour

### 6. Most Busy Users

Shows the users who sent the most messages.

### 7. Word Cloud

Displays frequently used words.

### 8. Most Common Words

Displays the top 25 frequently used words.

### 9. Emoji Analysis

Shows:

* Emoji frequency
* Top emojis
* Emoji pie chart

---

# 🛠️ Technologies Used

Python

Streamlit

Pandas

Matplotlib

Seaborn

WordCloud

Emoji

URLExtract

Regular Expressions

---

# 🎯 Project Workflow

```text
WhatsApp Exported Chat
          ↓
       app.py
          ↓
   preprocessor.py
          ↓
     Data Cleaning
          ↓
      helper.py
          ↓
   Data Analysis
          ↓
    Streamlit Dashboard
```

---

# 📌 Important

Keep all files in the same folder:

```text
app.py
preprocessor.py
helper.py
stop_hinglish.txt
requirements.txt
README.md
```

Do not rename `preprocessor.py` or `helper.py`, because `app.py` imports them.

---

# 👨‍💻 Run Command

```bash
python -m streamlit run app.py
```

Enjoy analyzing your WhatsApp chats! 💬📊

 
