from flask import Flask, render_template, jsonify, request, redirect, url_for  # Added redirect and url_for imports
from nltk.sentiment import SentimentIntensityAnalyzer

app = Flask(__name__)

sia = SentimentIntensityAnalyzer()

# Simulated Products List with 25 products, each having an image URL
products = [
    {"id": 1, "name": "Pack of 3 T-Shirt", "description": "A timeless cotton polo shirt, perfect for casual outings.", "price": 25,
     "reviews": [], "image_url": "/static/images/product1.jpg"},
    {"id": 2, "name": "Slim Fit Jeans", "description": "Stylish slim-fit denim jeans for a modern look.", "price": 45,
     "reviews": [], "image_url": "/static/images/product2.jpg"},
    {"id": 3, "name": "Leather Jacket", "description": "Premium leather jacket for a bold style statement.", "price": 120,
     "reviews": [], "image_url": "/static/images/product3.jpg"},
    {"id": 4, "name": "Summer Dress", "description": "Light and breezy dress for sunny days.", "price": 35,
     "reviews": [], "image_url": "/static/images/product4.jpg"},
    {"id": 5, "name": "Running Shoes", "description": "Comfortable and durable running shoes for athletes.", "price": 60,
     "reviews": [], "image_url": "/static/images/product5.jpg"},
    {"id": 6, "name": "Woolen Scarf", "description": "Warm and cozy scarf for winter days.", "price": 15,
     "reviews": [], "image_url": "/static/images/product6.jpg"},
    {"id": 7, "name": "Baseball Cap", "description": "Stylish cap to keep you cool under the sun.", "price": 10,
     "reviews": [], "image_url": "/static/images/product7.jpg"},
    {"id": 8, "name": "Formal Suit", "description": "Elegant suit for formal occasions.", "price": 200,
     "reviews": [], "image_url": "/static/images/product8.jpg"},
    {"id": 9, "name": "Yoga Pants", "description": "Stretchy and comfortable yoga pants.", "price": 30,
     "reviews": [], "image_url": "/static/images/product9.jpg"},
    {"id": 10, "name": "Graphic T-Shirt", "description": "Cool T-shirt with a unique graphic design.", "price": 20,
     "reviews": [], "image_url": "/static/images/product10.jpg"},
    {"id": 11, "name": "Fleece Hoodie", "description": "Soft fleece hoodie for chilly weather.", "price": 50,
     "reviews": [], "image_url": "/static/images/product11.jpg"},
    {"id": 12, "name": "Sports Jacket", "description": "Lightweight jacket perfect for outdoor activities.", "price": 75,
     "reviews": [], "image_url": "/static/images/product12.jpg"},
    {"id": 13, "name": "Denim Shorts", "description": "Casual denim shorts for summer days.", "price": 25,
     "reviews": [], "image_url": "/static/images/product13.jpg"},
    {"id": 14, "name": "Raincoat", "description": "Waterproof raincoat to keep you dry in the rain.", "price": 40,
     "reviews": [], "image_url": "/static/images/product14.jpg"},
    {"id": 15, "name": "Knitted Sweater", "description": "Cozy knitted sweater for winter warmth.", "price": 60,
     "reviews": [], "image_url": "/static/images/product15.jpg"},
    {"id": 16, "name": "Flip Flops", "description": "Comfortable flip-flops for the beach.", "price": 10,
     "reviews": [], "image_url": "/static/images/product16.jpg"},
    {"id": 17, "name": "Tank Top", "description": "Cool and breathable tank top for hot days.", "price": 15,
     "reviews": [], "image_url": "/static/images/product17.jpg"},
    {"id": 18, "name": "Leather Belt", "description": "Durable leather belt for everyday use.", "price": 20,
     "reviews": [], "image_url": "/static/images/product18.jpg"},
    {"id": 19, "name": "Formal Shoes", "description": "Polished shoes for business and formal events.", "price": 80,
     "reviews": [], "image_url": "/static/images/product19.jpg"},
    {"id": 20, "name": "Casual Sneakers", "description": "Trendy sneakers for casual wear.", "price": 55,
     "reviews": [], "image_url": "/static/images/product20.jpg"},
    {"id": 21, "name": "Wool Coat", "description": "Sophisticated wool coat for a classic look.", "price": 150,
     "reviews": [], "image_url": "/static/images/product21.jpg"},
    {"id": 22, "name": "Athletic Socks", "description": "Comfortable socks for sports and exercise.", "price": 8,
     "reviews": [], "image_url": "/static/images/product22.jpg"},
    {"id": 23, "name": "Base Layer Top", "description": "Perfect base layer for outdoor adventures.", "price": 35,
     "reviews": [], "image_url": "/static/images/product23.jpg"},
    {"id": 24, "name": "Backpack", "description": "Durable and spacious backpack for travel.", "price": 70,
     "reviews": [], "image_url": "/static/images/product24.jpg"},
    {"id": 25, "name": "Beach Hat", "description": "Wide-brimmed hat to protect you from the sun.", "price": 25,
     "reviews": [], "image_url": "/static/images/product25.jpg"},
]


@app.route('/')
def index():
    # Pagination: Display 5 products per page
    page = request.args.get('page', 1, type=int)
    products_per_page = 10
    start = (page - 1) * products_per_page
    end = start + products_per_page
    paginated_products = products[start:end]

    total_pages = len(products) // products_per_page + (1 if len(products) % products_per_page else 0)
    
    return render_template('index.html', products=paginated_products, page=page, total_pages=total_pages)

@app.route('/product/<int:product_id>')
def product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404
    return render_template('product.html', product=product)

@app.route('/analyze_reviews', methods=['POST'])
def analyze_reviews():
    reviews = request.json.get('reviews', [])
    analyzed = []
    
    for review in reviews:
        sentiment_score = sia.polarity_scores(review)["compound"]
        
        if sentiment_score >= 0.05:
            sentiment = "positive"
        elif sentiment_score <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        analyzed.append({
            "review": review,
            "sentiment": sentiment,
            "score": sentiment_score
        })
        
    return jsonify(analyzed)

@app.route('/submit_review/<int:product_id>', methods=['POST'])
def submit_review(product_id):
    review = request.form.get('review')
    sentiment_score = sia.polarity_scores(review)["compound"]
    
    if sentiment_score >= 0.05:
        sentiment = "positive"
    elif sentiment_score <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    # Find product and add the review
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        product['reviews'].append({"review": review, "sentiment": sentiment})
    
    # Redirect to the product page after submitting a review
    return redirect(url_for('product', product_id=product_id))  # Use url_for to generate the URL dynamically

if __name__ == '__main__':
    app.run(debug=True)