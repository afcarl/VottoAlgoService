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

from discount.discount import GamblerType, calculate_discount, calculate_reputation, coffee_price, coffee_cost

def compute_range_of_alpha(d_max = 0.8):
    """
    :param  d_max: the max discount e.g. 0.7 means 30% off
    :return the corresponding range of alpha
    """
    alpha_max = (coffee_price - coffee_cost)/(coffee_price*d_max - coffee_cost)
    return [1, alpha_max]

def display_max_discount_options(d_max = 0.8):
    """
    :param d_max        : the max discount e.g. 0.8 means 20% off
    :return             : the max discount options
    """
    print ""
    print "                    The below are the maximal discount options"
    print ""
    print "The price for a coffee is %s $." % coffee_price

    # Fundamentals:
    range_alpha = compute_range_of_alpha(d_max)
    alpha = range_alpha[0]
    rate_of_customer_increase = range_alpha[1]

    # Display 4 gambling options:
    print "Choose from below:"
    print " "

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



def command_line_client(d_max = 0.8, no_inc = 4):
    """
    This is the main algorithm which starts an interactive simulation.
    :param d_max        : the max discount e.g. 0.8 means 20% off
    to make sure that you always save money even when you lose!
    :param no_inc      : no of default increments for each update of R
    """
    print ""
    print "                     Welcome to the world of gambling!"
    print ""
    print "The price for a coffee is %s $." % coffee_price

    # Fundamentals:
    range_alpha = compute_range_of_alpha(d_max)
    alpha = (range_alpha[1] + range_alpha[0])/2
    print alpha
    rate_of_customer_increase = range_alpha[1]
    width_inc = (range_alpha[1] - range_alpha[0]) / no_inc  # default width of an increment
    alpha_mid =  range_alpha[0] + (range_alpha[1] - range_alpha[0]) / 2        # middle alpha value
    history = []  # history of past transactions
    save = 0
    no_win = 0
    no_lose = 0
    should_continue = 1



    while should_continue == 1:

        # Display the reputation (1 - 100) : the closer to 100, the better discounts you get.
        potential = int(calculate_reputation(alpha, range_alpha))
        print ""
        print "Your Gambler potential is %s (on the scale 1 - 100)" % potential
        print ""
        # Display 4 gambling options:
        print '---------------------'
        print "Choose from below:"
        print " "
        # print "Current alpha = %s" % alpha
        # print "Mid alpha is %s" % alpha_mid

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
            save += win
            no_win += 1
            history += ['W', [q_w, d_w, d_l]]  # update history

            #print input_option
            #print type(input_option)

            if (input_option in [1, 2, 3]) and ((alpha - width_inc * (1.25 - gambler_type.probability)) > range_alpha[0]):
                alpha -= width_inc * (1.25 - gambler_type.probability)  # update alpha!
            elif (input_option == 4) and (alpha > alpha_mid):
                print 'If the MP option is selected when your reputation is below 50, we raise it by 1/4 of the default increment.'
                # print 'If the MP option is selected when alpha is above the mid-point, reduce by 1/4 of the default increment.'
                alpha -= width_inc * (1.25 - gambler_type.probability)
            elif (input_option == 4) and (alpha < alpha_mid):
                print 'If the MP option is selected when your reputation is above 50, we reduce it by 1/4 of the default increment.'
                # print 'If the MP option is selected when alpha is below the mid-point, raise by 1/4 of the default increment.'
                alpha += width_inc * (1.25 - gambler_type.probability)
            elif (input_option == 4) and (alpha == alpha_mid):
                print 'If the MP option is selected when your reputation is exactly 50, it stays where it is.'
                # print 'If the MP option is selected when alpha is at the mid-point, its value stays as it is.'
                alpha = alpha
            else:
                alpha = range_alpha[0]
        else:
            lose = round(coffee_price * (1 - d_l), 2)
            print "Sorry, you only won on %s $!" % lose
            save += lose
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
# command_line_client()
