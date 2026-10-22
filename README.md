# ShopSmart AI — Independent Hackathon Prototype

A small shopping-assistant web app built with Flask, HTML, CSS, and JavaScript. It includes a demo product catalog, search and category/budget filters, and a keyword-based recommendation chatbot.

## Important notes
- This is an independent prototype, not an official Amazon product and not affiliated with Amazon.
- Product names, prices, and ratings are illustrative demo data. The app does not use live Amazon listings, inventory, reviews, or pricing.
- The assistant is rule/keyword-based, not a live LLM. You can connect an approved model/API later if the event rules allow it.
- Check the exact hackathon rules, theme, permitted APIs, team-size rules, and submission requirements before submitting.

## Requirements
- Python 3.10+
- pip

## Run on Windows
1. Extract the ZIP file.
2. Open the extracted `amazon_ai_shopping_assistant` folder.
3. In that folder, open Terminal / Command Prompt.
4. Run:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

5. Open the local URL shown in the terminal, usually `http://127.0.0.1:5000`.

## Run on macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Then open `http://127.0.0.1:5000`.

## Demo prompts
- “Gadgets for coding”
- “Study essentials under 1000”
- “Audio for travel”
- “Compare Wireless Headphones and Bluetooth Speaker”

## Project structure
```text
amazon_ai_shopping_assistant/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css
```

## Potential next steps
1. Add a user problem statement and evaluation criteria based on the actual hackathon theme.
2. Add an authorized catalog API or a clearly documented sample dataset.
3. Add a real AI model with safe API-key handling via environment variables.
4. Add accessibility, unit tests, and a short demo video.
5. Prepare a truthful architecture diagram and pitch deck based on what is actually implemented.
