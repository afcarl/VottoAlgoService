#Discount Algorithm 1: 
#Each transaction, you get four options: True Gambler, Average Gambler, 
#Conservative Gambler and Moral Person. 

import numpy as np
import random

def DiscountDeals(alpha, R, Option,p,r):
    ''' This function provides a list of 4 dicount options.
    alpha :a positive real number, goal profit increase
    R     :a positive real number, expected increase in the no of customers /day
    Option:an integer, a choice of discount options, 1 = TG, 2 = AG, 3 = CG and 4 = MP. 
    Output:a 3 x 4 matrix whose each column (q_w,d_w,d_l). 
    '''
    if Option == 1: #True Gambler
        q_w = 0.25 #winning prob
        grad_l = -(1-q_w)/q_w
        intcept_l = (alpha/R + r/p*(1-alpha/R))/q_w
        Start = max(r/p, q_w*intcept_l)
        End = min(1,(r/p - intcept_l)/grad_l)
        d_l = (1-q_w)*(End - Start) + Start
        d_w = grad_l*d_l + intcept_l
        return [q_w, d_w, d_l]
    elif Option == 2: #Average Gambler
        q_w = 0.5 #winning prob
        grad_l = -(1-q_w)/q_w
        intcept_l = (alpha/R + r/p*(1-alpha/R))/q_w
        Start = max(r/p, q_w*intcept_l)
        End = min(1,(r/p - intcept_l)/grad_l)
        d_l = (1-q_w)*(End - Start) + Start
        d_w = grad_l*d_l + intcept_l
        return [q_w, d_w, d_l]
    elif Option == 3: #Conservative Gambler
        q_w = 0.75 #winning prob
        grad_l = -(1-q_w)/q_w
        intcept_l = (alpha/R + r/p*(1-alpha/R))/q_w
        Start = max(r/p, q_w*intcept_l)
        End = min(1,(r/p - intcept_l)/grad_l)
        d_l = (1-q_w)*(End - Start) + Start
        d_w = grad_l*d_l + intcept_l
        return [q_w, d_w, d_l]
    elif Option == 4: #Moral Person
        q_w = 1
        d_w = (alpha/R + r/p*(1-alpha/R))
        d_l = (alpha/R + r/p*(1-alpha/R))
        return [q_w, d_w, d_l]
        
       
        
          
def Algorithm_1(alpha=1.1,R=1.2,range_alpha=[1.0,1.2], no_inc = 10): 
    '''
    This is the main algorithm which starts an interactive simulation. 
    alpha:initial values 
    R    :initial values
    range_alpha : [a,b], range of alpha e.g. [1.1,1.5]. Here the upper bdd a > alpha to make sure negative discounts!!!
    no_inc      : no of default increments for each update of R
    '''
    print ""
    print "                     Welcome to the world of gambling!"
    print ""
    #Fixed parameters:
    p = 3.5 # price of a coffee
    r = 0.8 # raw cost of a coffee 
    print "The price for a coffee is %s $." % p
    
    #Fundamentals:
    width_inc = (range_alpha[1] - range_alpha[0])/no_inc #default width of an increment
    History = () #history of past transactions
    gambler_type = 4 #initial gambler type 
    gambler_labels = ['True Gambler', 'Average Gambler', 'Safe Player', 'Moral Person']
    save = 0
    no_win = 0
    no_lose = 0
    weight  = [1.0, 0.75, 0.5, 0] #when you win/lose, decrease/increase alpha by width_inc*weight[gambler_type-1].
    Continue = 1 
            
    while Continue == 1:
        print '---------------------'
        print "Choose from below:"
        print " "
        for Option in range(1,5):
            [q_w, d_w, d_l] = DiscountDeals(alpha, R, Option,p,r)    
            print "          %s : %s, Winning Probability = %s %%" %(Option,gambler_labels[Option-1],int(100*q_w))
            #print "  Win and get %s    OR    Lose and get %s" %(d_w,d_l)
            print "          Win and save %s $    OR    Lose and save %s $" %(round(p*(1-d_w),2),round(p*(1-d_l),2))
            print " "
                    
        gambler_type  = int(raw_input("Which type of gambler are you?: "))
        
        if gambler_type < 5:
            [q_w, d_w, d_l] = DiscountDeals(alpha, R, gambler_type, p,r) 
            
            dice = random.random() #Generate a random number [0,1)
            if dice < q_w:
                win = round(p*(1-d_w),2)
                print "Congratulations! You won %s $!" % win
                save   += p*(1-d_w)
                no_win +=1 
                History += ('W',[q_w, d_w, d_l]) #update history
                
                if (alpha - width_inc*weight[gambler_type-1]) > range_alpha[0]:
                    alpha -= width_inc*weight[gambler_type-1] # update alpha!
                else:
                    alpha = range_alpha[0]
            else:
                lose = round(p*(1-d_l),2)
                print "Sorry, you only won on %s $!" % lose
                save   += p*(1-d_l)
                no_lose +=1 
                History += ('L',[q_w, d_w, d_l]) #update history
                
                if (alpha + width_inc*weight[gambler_type-1]) < range_alpha[1]:
                    alpha += width_inc*weight[gambler_type-1] # update alpha!
                else:
                    alpha = range_alpha[1]
        else: 
            print "Please choose from options 1, 2, 3, 4."
        
        print "You've saved %s $ so far!" % round(save,2)
        #print "The current value of alpha is:",alpha   
        Continue  = int(raw_input("Would you like to continue (1 = yes, 0 = no): "))       
        
      
    print "---------------------"
    print "Thanks for playing the game :)"
    print "Summary:"
    print "You've saved:", save
    
    no_total = no_win + no_lose
    print "You've won %s times out of %s games" %(no_win, no_total)
    print "Check variable 'History' to see the history of your past transactions."
    return History
    
Algorithm_1(alpha=1.1,R=1.35,range_alpha=[1.0,1.35], no_inc = 10)