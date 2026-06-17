from flask import Flask, render_template, request, redirect, url_for, flash
from data import users_db

app = Flask(__name__)
app.secret_key = "nexura_secret_key_gold_standard"

# Password Generator Helper for Web 2 (a=1, b=2, ..., z=26)
def calculate_dynamic_password(username, domain):
    def string_to_numbers(s):
        return ",".join(str(ord(char.lower()) - 96) for char in s if char.isalpha())
    
    user_part = string_to_numbers(username)
    domain_part = string_to_numbers(domain)
    return f"{user_part},{domain_part}"

# --- WEB 1: Money Transfer ---
@app.route('/')
def index():
    return render_template('index.html', users=users_db)

@app.route('/send_money', methods=['POST'])
def send_money():
    sender_name = request.form.get('sender_name')
    password = request.form.get('password')
    receiver_name = request.form.get('receiver_name')
    amount = request.form.get('amount')

    # Validations
    if sender_name not in users_db or users_db[sender_name]['password'] != password:
        flash("Invalid Sender Name or Password!", "danger")
        return redirect(url_for('index'))
    
    if receiver_name not in users_db:
        flash("Receiver Account does not exist!", "danger")
        return redirect(url_for('index'))

    try:
        amount = int(amount)
    except ValueError:
        flash("Please enter a valid amount!", "danger")
        return redirect(url_for('index'))

    if amount <= 0:
        flash("Amount must be greater than 0!", "danger")
        return redirect(url_for('index'))

    if users_db[sender_name]['balance'] < amount:
        flash(f"Insufficient Funds! Your Balance is Rs. {users_db[sender_name]['balance']:,}", "danger")
        return redirect(url_for('index'))

    # Transaction Execution
    users_db[sender_name]['balance'] -= amount
    users_db[receiver_name]['balance'] += amount
    flash(f"Successfully transferred Rs. {amount:,} to {receiver_name}!", "success")
    return redirect(url_for('index'))


# --- WEB 2: Domain Seller ---
@app.route('/sell-domain', methods=['GET', 'POST'])
def sell_domain():
    if request.method == 'POST':
        username = request.form.get('username')
        domain = request.form.get('domain')
        entered_password = request.form.get('password')
        target_account = request.form.get('target_account')

        # Check calculated password logic
        correct_password = calculate_dynamic_password(username, domain)
        
        if entered_password != correct_password:
            flash(f"Invalid Password! Expected password format for '{username}' & '{domain}' is: {correct_password}", "danger")
            return redirect(url_for('sell_domain'))

        if target_account not in users_db:
            flash("Target account for funds transfer does not exist!", "danger")
            return redirect(url_for('sell_domain'))

        # Process Domain Sale (Add 10,000 Rs, Add Star, Handle Levels)
        users_db[target_account]['balance'] += 10000
        users_db[target_account]['stars'] += 1
        
        # Level Up Mechanism (Every 5 stars increases level up to 10)
        current_stars = users_db[target_account]['stars']
        new_level = 1 + (current_stars // 5)
        if new_level > 10:
            new_level = 10
        users_db[target_account]['level'] = new_level

        flash(f"Domain '{domain}' Sold! Rs. 10,000 added to {target_account}. Star Added!", "success")
        return redirect(url_for('sell_domain'))

    return render_template('domain.html', users=users_db)

if __name__ == '__main__':
    app.run(debug=True)