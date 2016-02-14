from discount import GamblerType, calculate_discount, coffee_price
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Gettin' rich"


@app.route('/discounts/<gambler_type>/<float:alpha>/')
def handle_discount_request(gambler_type, alpha):
    gambler = GamblerType[gambler_type]
    # Hard code the rate of customer increase for now.
    [win_probability, win_discount, lose_discount] = calculate_discount(alpha, 1.35, gambler)
    win_amount = (1 - win_discount) * coffee_price
    lose_amount = (1 - lose_discount) * coffee_price
    return jsonify(winProbability=win_probability,
                   winDiscount=win_discount,
                   loseDiscount=lose_discount,
                   winAmount=win_amount,
                   loseAmount=lose_amount)


@app.route('/<shop>/')
def shop_price():
    # Return the hard coded price for now.
    return coffee_price


if __name__ == "__main__":
    app.run(debug=True)
