from enum import Enum

coffee_price = 3.5  # price of a coffee
coffee_cost = 0.8  # raw cost of a coffee


class GamblerType(Enum):
    __order__ = 'true average conservative moral'
    true = (0.25, 1, "True Gambler")
    average = (0.5, 2, "Average Gambler")
    conservative = (0.75, 3, "Conservative Gambler")
    moral = (1, 4, "Moral Person")

    def __init__(self, probability, input_option, description):
        self.probability = probability
        self.description = description
        self.input_option = input_option

    @classmethod
    def lookup_gambler_by_input(cls, input_option):
        for gambler in cls:
            if gambler.input_option == input_option:
                return gambler


def calculate_discount(alpha, rate_of_customer_increase, gambler_type):
    """ This function returns winning probability q_w and discount rates d_w and d_l when you win/lose.
    :return: Output:[q_w,d_w,d_l] = [winning probability, discount rate when you win, discount rate when you lose].
    :param gambler_type: an integer, a choice of discount options, 1 = TG, 2 = AG, 3 = CG and 4 = MP.
    :param rate_of_customer_increase: a positive real number, expected increase in the no of customers /day
    :param alpha: a positive real number, goal profit increase
    """
    return _calculate_discount_given_probability(alpha, gambler_type.probability, rate_of_customer_increase)


def _calculate_discount_given_probability(alpha, q_w, rate_of_customer_increase):
    grad_l = -(1 - q_w) / q_w
    intercept_l = (alpha / rate_of_customer_increase + coffee_cost / coffee_price * (
        1 - alpha / rate_of_customer_increase)) / q_w
    start = max(coffee_cost / coffee_price, q_w * intercept_l)
    end = min(1, (coffee_cost / coffee_price - intercept_l) / grad_l) if grad_l != 0 else 1
    d_l = (1 - q_w) * (end - start) + start
    d_w = grad_l * d_l + intercept_l
    return [q_w, d_w, d_l]


def calculate_reputation(alpha, range_alpha):
    return round(100*(1 - (alpha - range_alpha[0])/(range_alpha[1] - range_alpha[0])))