# quiz-generator-api

## Live Demo

The API is live at: https://pcnara.pythonanywhere.com

No setup needed — just open the link in your browser.

## How to Use

### Option 1 — Browser (easiest)
1. Open https://pcnara.pythonanywhere.com
2. Paste any English story or article into the text box
3. Choose how many questions you want (1–10)
4. Click **Generate Quiz**
5. A `quiz.js` file will download automatically
6. Answer the questions in the browser — correct answers highlight green, wrong ones red
7. To reload a saved quiz later, click **📂 Open File** and select any previously downloaded `quiz.js`

### Option 2 — API directly (via curl or Postman)
Send a POST request to the generate endpoint:

```bash
curl -X POST https://pcnara.pythonanywhere.com/api/generate-quiz \
  -H "Content-Type: application/json" \
  -d '{"story": "In 1969, Apollo 11 landed on the Moon.", "question_count": 3}'
```

### Option 3 — Run locally
1. Clone this repo
2. Install dependencies: `pip3 install -r requirements.txt`
3. Create `api-key.env` with your own Groq key:
   `GROQ_API_KEY=your_key_here`
4. Run: `python3 app.py`
5. Open: `http://127.0.0.1:3000`

## How Questions Are Generated
Questions are generated using Groq's LLM API with the 
`llama-3.3-70b-versatile` model. The story and question count 
are sent as a structured prompt, and the model returns JSON 
which is parsed, normalized, and returned to the client.
