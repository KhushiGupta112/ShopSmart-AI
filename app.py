from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Demo catalog for hackathon prototype. Replace with an authorized product API/dataset for a real deployment.
PRODUCTS = [
    {"id": 1, "name": "Wireless Headphones", "category": "Electronics", "price": 2499, "rating": 4.4,
     "description": "Over-ear headphones with long battery life and comfortable cushions.", "tags": ["audio", "music", "travel", "wireless"], "icon": "🎧"},
    {"id": 2, "name": "Bluetooth Speaker", "category": "Electronics", "price": 1799, "rating": 4.2,
     "description": "Portable speaker for music at home or outdoors.", "tags": ["audio", "music", "portable", "wireless"], "icon": "🔊"},
    {"id": 3, "name": "Smart Watch", "category": "Wearables", "price": 3299, "rating": 4.1,
     "description": "Everyday smartwatch with activity tracking and notifications.", "tags": ["fitness", "health", "watch", "wearable"], "icon": "⌚"},
    {"id": 4, "name": "Laptop Backpack", "category": "Accessories", "price": 999, "rating": 4.3,
     "description": "Lightweight backpack with a padded laptop compartment.", "tags": ["college", "laptop", "bag", "travel"], "icon": "🎒"},
    {"id": 5, "name": "Mechanical Keyboard", "category": "Electronics", "price": 2899, "rating": 4.5,
     "description": "Tactile keyboard for coding, gaming, and everyday typing.", "tags": ["coding", "computer", "keyboard", "gaming"], "icon": "⌨️"},
    {"id": 6, "name": "USB-C Hub", "category": "Accessories", "price": 1299, "rating": 4.0,
     "description": "Compact hub for connecting common peripherals to a laptop.", "tags": ["laptop", "computer", "usb", "accessories"], "icon": "🔌"},
    {"id": 7, "name": "Insulated Water Bottle", "category": "Lifestyle", "price": 599, "rating": 4.2,
     "description": "Reusable bottle for carrying water to class, work, or travel.", "tags": ["college", "travel", "water", "bottle"], "icon": "🥤"},
    {"id": 8, "name": "Desk Lamp", "category": "Home", "price": 799, "rating": 4.1,
     "description": "Adjustable desk lamp for study sessions and home offices.", "tags": ["study", "desk", "home", "college"], "icon": "💡"},
    {"id": 9, "name": "Running Shoes", "category": "Fashion", "price": 2199, "rating": 4.3,
     "description": "Lightweight shoes designed for walking and daily runs.", "tags": ["fitness", "running", "shoes", "sports"], "icon": "👟"},
    {"id": 10, "name": "Webcam", "category": "Electronics", "price": 1599, "rating": 4.0,
     "description": "USB webcam for online classes, meetings, and streaming.", "tags": ["online class", "video", "computer", "study"], "icon": "📷"},
]

def recommend_products(query="", category="All", max_price=None):
    words = [w.lower() for w in query.strip().split() if len(w) > 1]
    results = []
    for p in PRODUCTS:
        if category != "All" and p["category"] != category:
            continue
        if max_price is not None and p["price"] > max_price:
            continue
        haystack = " ".join([p["name"], p["category"], p["description"], *p["tags"]]).lower()
        score = sum(2 if word in p["name"].lower() else 1 for word in words if word in haystack)
        if not words or score > 0:
            item = dict(p)
            item["match_score"] = score
            results.append(item)
    results.sort(key=lambda x: (x["match_score"], x["rating"]), reverse=True)
    return results

@app.route("/")
def index():
    categories = ["All"] + sorted({p["category"] for p in PRODUCTS})
    return render_template("index.html", products=PRODUCTS, categories=categories)

@app.route("/api/products")
def api_products():
    query = request.args.get("q", "")
    category = request.args.get("category", "All")
    raw_budget = request.args.get("budget", "").strip()
    try:
        budget = int(raw_budget) if raw_budget else None
    except ValueError:
        budget = None
    return jsonify(recommend_products(query, category, budget))

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({"reply": "Tell me what you need, your budget, or what you want to compare."})
    lower = message.lower()

    # Simple explainable demo assistant (no external AI/API key required).
    budget = None
    import re
    budget_match = re.search(r"(?:under|below|within|budget(?: of)?|₹|rs\.?)\s*([0-9,]{2,})", lower)
    if budget_match:
        try:
            budget = int(budget_match.group(1).replace(",", ""))
        except ValueError:
            pass

    if "compare" in lower or " vs " in lower or " versus " in lower:
        mentioned = [p for p in PRODUCTS if p["name"].lower() in lower]
        if len(mentioned) >= 2:
            a, b = mentioned[0], mentioned[1]
            cheaper = a if a["price"] < b["price"] else b
            higher_rated = a if a["rating"] > b["rating"] else b
            return jsonify({"reply": f"{a['name']} costs ₹{a['price']} and is rated {a['rating']}/5. {b['name']} costs ₹{b['price']} and is rated {b['rating']}/5. Lower price: {cheaper['name']}. Higher rating: {higher_rated['name']}."})
        return jsonify({"reply": "To compare, type two exact product names, for example: “Compare Wireless Headphones and Bluetooth Speaker”."})

    query = message
    if budget:
        query = re.sub(r"(?:under|below|within|budget(?: of)?|₹|rs\.?)\s*[0-9,]{2,}", "", query, flags=re.I)
    results = recommend_products(query, max_price=budget)
    if not results:
        results = recommend_products("", max_price=budget)
    if results:
        top = results[:3]
        names = "; ".join(f"{p['name']} (₹{p['price']}, rating {p['rating']}/5)" for p in top)
        return jsonify({"reply": f"Based on the demo catalog, these may fit: {names}. This is a keyword-based prototype, not a live Amazon search. Tell me a use case or a budget to refine the suggestions."})
    return jsonify({"reply": "I couldn't find a demo item matching that. Try terms like coding, study, audio, travel, fitness, or give a budget such as under 2000."})

if __name__ == "__main__":
    app.run(debug=True)
