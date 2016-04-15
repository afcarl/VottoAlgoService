# Discount Algorithm 1:

# Key assumptions: the shop under consideration sells only one product and every customer always uses the app.

# Each transaction, you choose from four options (of equal expected gain): True Gambler (TG), Average Gambler (AG), Safe
# Player (SP) and Moral Person (MP) in the ascending order of winning probability (25%, 50%, 75% and 100%).

# Main principle:
# You risk big, you win/lose big.
# For example, if you are a TG, not only do you save significantly more/less money when you win/lose but also your odds
# at the next transaction improves/drops more dramatically. On the other hand, if you're so ethical that you insist on
# option MP, you always save some money but not an impressive/disappointing amount. And you odds remain the same. The
# odds are adjusted by varying the desired profit increase \alpha in a certain range.
# DS is testing

import random

from discount.discount import GamblerType, calculate_discount, coffee_price


def command_line_client(alpha=1.175, rate_of_customer_increase=1.35, range_alpha=[1.0, 1.35], no_inc=4):
    """
    This is the main algorithm which starts an interactive simulation.
    :param alpha:the desired rate of profit increase (>1)
    :param rate_of_customer_increase    :the expected rate of increase in no. of customers.
    :param range_alpha : [lower bound, upper bound], range of alpha e.g. Here the upper bdd is strictly smaller than R
    to make sure that you always save money even when you lose!
    :param no_inc      : no of default increments for each update of R
    """
    print ""
    print "                     Welcome to the world of gambling!"
    print ""
    print "The price for a coffee is %s $." % coffee_price

    # Fundamentals:
    width_inc = (range_alpha[1] - range_alpha[0]) / no_inc  # default width of an increment
    history = []  # history of past transactions
    save = 0
    no_win = 0
    no_lose = 0
    should_continue = 1

    while should_continue == 1:

        # Display 4 gambling options:
        print '---------------------'
        print "Choose from below:"
        print " "
        print "Current alpha = %s" % alpha

        # Print the output for immoral gamblers
        for gambler_type in GamblerType:
            if gambler_type != GamblerType.moral:
                [q_w, d_w, d_l] = calculate_discount(alpha, rate_of_customer_increase, gambler_type)
                print "          %s : %s, Winning Probability = %s %%" % (
                    gambler_type.input_option, gambler_type.description, int(100 * q_w))
                # print "  Win and get %s    OR    Lose and get %s" %(d_w,d_l)
                print "          Win and save %s $    OR    Lose and save %s $" % (
                    round(coffee_price * (1 - d_w), 2), round(coffee_price * (1 - d_l), 2))
                print " "

        # Print the output for our scrupulous friends out there (moral person)
        [q_w, d_w, d_l] = calculate_discount(alpha, rate_of_customer_increase, GamblerType.moral)
        print "          %s : %s, Guaranteed save %s $" % (GamblerType.moral.input_option,
                                                           GamblerType.moral.description,
                                                           round(coffee_price * (1 - d_w), 2))
        print " "

        # Ask for a preferred gambling option:
        input_option = raw_input("Which type of gambler are you?: ")

        # Show the result of the gamble and update the odds:
        while not (input_option in ['1', '2', '3', '4']):
            input_option = raw_input("Please choose from options 1, 2, 3 or 4.")
        input_option = int(input_option)

        gambler_type = GamblerType.lookup_gambler_by_input(input_option)
        [q_w, d_w, d_l] = calculate_discount(alpha, rate_of_customer_increase,
                                             gambler_type)

        dice = random.random()  # Generate a random number [0,1)
        if dice < q_w:
            win = round(coffee_price * (1 - d_w), 2)
            print "Congratulations! You won %s $!" % win
            save += coffee_price * (1 - d_w)
            no_win += 1
            history += ['W', [q_w, d_w, d_l]]  # update history

            if (alpha - width_inc * (1.25 - gambler_type.probability)) > range_alpha[0]:
                alpha -= width_inc * (1.25 - gambler_type.probability)  # update alpha!
            else:
                alpha = range_alpha[0]
        else:
            lose = round(coffee_price * (1 - d_l), 2)
            print "Sorry, you only won on %s $!" % lose
            save += coffee_price * (1 - d_l)
            no_lose += 1
            history += ['L', [q_w, d_w, d_l]]  # update history

            if (alpha + width_inc * (1.25 - gambler_type.probability)) < range_alpha[1]:
                alpha += width_inc * (1.25 - gambler_type.probability)  # update alpha!
            else:
                alpha = range_alpha[1]
        print "You've saved %s $ so far!" % round(save, 2)

        # Ask whether to cotinue:
        should_continue = raw_input("Would you like to continue (1 = yes, 0 = no): ")
        while not (should_continue == '0' or should_continue == '1'):
            should_continue = raw_input("Please press number 1 or 0 (1 = yes, 0 = no): ")
        should_continue = int(should_continue)

    print "---------------------"
    print "Thanks for playing the game :)"
    print "Summary:"
    print "You've saved:", save

    no_total = no_win + no_lose
    print "You've won %s times out of %s games" % (no_win, no_total)
    print "Check variable 'History' to see the history of your past transactions."
    return history


# Run an interactive session:    
command_line_client()
