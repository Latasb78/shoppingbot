from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

with open('products.json') as f:
    products = json.load(f)

selected_product = None
selected_quantity = 1

@app.route('/')
def home():
    return render_template('index.html', products=products)

@app.route('/chat', methods=['POST'])
def chat():

    global selected_product
    global selected_quantity

    user_message = request.json['message'].lower()

    # HELLO MESSAGE

    if "hi" in user_message or "hello" in user_message:

        product_names = ""

        for product in products:
            product_names += f"• {product['name']}<br>"

        return jsonify({
            "reply":
            f"""
Welcome to Shopping Assistant 👋<br><br>

What product do you want?<br><br>

Available products:<br><br>

{product_names}
            """
        })

    # PRODUCT SELECTION

    for product in products:

        product_name = product['name'].lower()

        if product_name in user_message:

            selected_product = product

            return jsonify({

                "reply":
                f"""
Nice choice 👍<br><br>

You selected {product['name']}.<br><br>

You can ask:<br>
• price<br>
• quantity<br>
• order
                """,

                "image": product['image']
            })

    # PRICE

    if "price" in user_message or "rupees" in user_message or "cost" in user_message:

        if selected_product:

            return jsonify({

                "reply":
                f"""
{selected_product['name']} price is ₹{selected_product['price']}<br><br>

How many quantities do you want?
                """
            })

    # QUANTITY

    if "quantity" in user_message or user_message.isdigit():

        if selected_product:

            qty = ''.join(filter(str.isdigit, user_message))

            if qty == "":
                qty = "1"

            selected_quantity = int(qty)

            return jsonify({

                "reply":
                f"""
Quantity selected: {selected_quantity}<br><br>

Type:<br>
• order now<br><br>

to place your order 👍
                """
            })

    # ORDER

    if "order" in user_message or "buy" in user_message:

        if selected_product:

            total_price = (
                selected_product['price']
                * selected_quantity
            )

            return jsonify({

                "reply":
                f"""
🧾 BILL<br><br>

Product:<br>
{selected_product['name']}<br><br>

Price:<br>
₹{selected_product['price']}<br><br>

Quantity:<br>
{selected_quantity}<br><br>

Total:<br>
₹{total_price}<br><br>

✅ Order placed successfully ❤️<br><br>

Thank you for shopping 🛍️
                """
            })

    # DEFAULT MESSAGE

    return jsonify({

        "reply":
        """
Sorry 😔<br><br>

Please ask correctly.<br><br>

Example:<br>
• hi<br>
• i want iphone<br>
• price<br>
• quantity 2<br>
• order now
        """
    })

if __name__ == '__main__':
    app.run(debug=True)