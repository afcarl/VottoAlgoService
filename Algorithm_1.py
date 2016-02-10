#Discount Algorithm 1: 

#Key assumptions: the shop under consideration sells only one product and every customer always uses the app. 

#Each transaction, you choose from four options (of equal expected gain): True Gambler (TG), Average Gambler (AG), Safe Player (SP) and Moral Person (MP) in the ascending order of winning probability (25%, 50%, 75% and 100%). 

#Main principle: 
#You risk big, you win/lose big.
#For example, if you are a TG, not only do you save significantly more/less money when you win/lose but also your odds at the next transaction improves/drops more dramatically. On the other hand, if you're so ethical that you insist on option MP, you always save some money but not an impressive/dissapointing amount. And you odds remain the same. The odds are adjusted by varying the desired profit increase \alpha in a certain range. 

import numpy as np
import random

def DiscountDeals(alpha, R, Option,p,r):
    ''' This function returns winning probability q_w and discount rates d_w and d_l when you win/lose. 
    alpha :a positive real number, goal profit increase
    R     :a positive real number, expected increase in the no of customers /day
    Option:an integer, a choice of discount options, 1 = TG, 2 = AG, 3 = CG and 4 = MP. 
    Output:[q_w,d_w,d_l] = [winning probability, discount rate when you win, discount rate when you lose]. 
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
    alpha:the desired rate of profit increase (>1)
    R    :the expected rate of increase in no. of customers. 
    range_alpha : [lower bound, upper bound], range of alpha e.g. Here the upper bdd is strictly smaller than R to make sure that you always save money even when you lose!
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
    History = [] #history of past transactions
    gambler_type = 4 #initial gambler type 
    gambler_labels = ['True Gambler', 'Average Gambler', 'Safe Player', 'Moral Person']
    save = 0
    no_win = 0
    no_lose = 0
    weight  = [1.0, 0.75, 0.5, 0] #when you win/lose, decrease/increase alpha by width_inc*weight[gambler_type-1].
    Continue = 1 
            
    while Continue == 1:
        
        #Display 4 gambling options: 
        print '---------------------'
        print "Choose from below:"
        print " "
        for Option in range(1,4):
            [q_w, d_w, d_l] = DiscountDeals(alpha, R, Option,p,r)    
            print "          %s : %s, Winning Probability = %s %%" %(Option,gambler_labels[Option-1],int(100*q_w))
            #print "  Win and get %s    OR    Lose and get %s" %(d_w,d_l)
            print "          Win and save %s $    OR    Lose and save %s $" %(round(p*(1-d_w),2),round(p*(1-d_l),2))
            print " "
        
        [q_w, d_w, d_l] = DiscountDeals(alpha, R, 4,p,r)    
        print "          %s : %s, Guaranteed save %s $" %(4,gambler_labels[3], round(p*(1-d_w),2))
        print " "
        
        #Ask for a prefeered gambling option:
        gambler_type  = raw_input("Which type of gambler are you?: ")
        
        #Show the result of the gamble and update the odds:
        while not(gambler_type in ['1','2','3','4']):
            gambler_type  = raw_input("Please choose from options 1, 2, 3 or 4.")
        gambler_type = int(gambler_type)    
            
        [q_w, d_w, d_l] = DiscountDeals(alpha, R, gambler_type, p,r) 
        
        dice = random.random() #Generate a random number [0,1)
        if dice < q_w:
            win = round(p*(1-d_w),2)
            print "Congratulations! You won %s $!" % win
            save   += p*(1-d_w)
            no_win +=1 
            History += ['W',[q_w, d_w, d_l]] #update history
            
            if (alpha - width_inc*weight[gambler_type-1]) > range_alpha[0]:
                alpha -= width_inc*weight[gambler_type-1] # update alpha!
            else:
                alpha = range_alpha[0]
        else:
            lose = round(p*(1-d_l),2)
            print "Sorry, you only won on %s $!" % lose
            save   += p*(1-d_l)
            no_lose +=1 
            History += ['L',[q_w, d_w, d_l]] #update history
            
            if (alpha + width_inc*weight[gambler_type-1]) < range_alpha[1]:
                alpha += width_inc*weight[gambler_type-1] # update alpha!
            else:
                alpha = range_alpha[1]
        print "You've saved %s $ so far!" % round(save,2)   
        
        #Ask whether to cotinue:
        Continue  = raw_input("Would you like to continue (1 = yes, 0 = no): ")     
        while not(Continue == '0' or Continue == '1'):
            Continue  = raw_input("Please press number 1 or 0 (1 = yes, 0 = no): ")
        Continue = int(Continue)
      
    print "---------------------"
    print "Thanks for playing the game :)"
    print "Summary:"
    print "You've saved:", save
    
    no_total = no_win + no_lose
    print "You've won %s times out of %s games" %(no_win, no_total)
    print "Check variable 'History' to see the history of your past transactions."
    return History
    
# Run an interactive session:    
History = Algorithm_1(alpha=1.1,R=1.35,range_alpha=[1.0,1.35], no_inc = 10)