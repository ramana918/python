#!/usr/bin/python
import MySQLdb as my


class Customer():
    """A customer of ABC Bank with a checking account. Customers have the
    following properties:

    Attributes:
        name: A string representing the customer's name.
        balance: A float tracking the current balance of the customer's account.
    """

    def __init__(self, cust_id):
        """Return a Customer object whose name is *name*.""" 
        self.cust_id = cust_id
	try:
        	self.db = my.connect(host="127.0.0.1", user="root", passwd="root@123", db="cust_details")
	except:
		print "DB connection error"
        self.cursor = self.db.cursor()

        if cust_id != 0:
            sql = "select balance from accnt_details where CustID=%d" % cust_id
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            self.balance = int(data[0])

    def cust_registration(self):

        sql = "select MAX(CustID) from accnt_details"
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            next_cust_id = int(data[0]) + 1
        except Exception as e:
            print "Error with db operation1"
            exit(1)
        name = raw_input("Name: ")
        address = raw_input("Address:")
        init_balance = input("Amount you need to deposit: ")
        sql = "insert into accnt_details VALUES('%d', '%s', '%s', '%d')" % (next_cust_id, name , address, init_balance)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            self.db.close()
            print "Customer %s added successfullly.. %d is your customer ID" % (name, next_cust_id)
        except Exception as e:
            print  e
            exit(1)

    def withdraw(self, amount):
        """Return the balance remaining after withdrawing *amount*
        dollars."""
        if amount > self.balance:
            print 'Insufficient balance'
	    exit(1)
        self.balance -= amount
        #Same as self.balance = self.balance - amount

        sql = "update accnt_details SET balance = %d where CustID = %d" %(self.balance, self.cust_id)

        try:
            self.cursor.execute(sql)
            self.db.commit()
            self.db.close()
        except Exception as e:
            print  e
            exit(1)
        return self.balance

    def deposit(self, amount):
        """Return the balance remaining after depositing *amount*
        dollars."""
        self.balance += amount
        #Same as self.balance = self.balance + amount

        sql = "update accnt_details SET balance = %d where CustID = %d" %(self.balance, self.cust_id)

        try:
            self.cursor.execute(sql)
            self.db.commit()
            self.db.close()
        except Exception as e:
            print  e
            exit(1)

        return self.balance

    def balancecheck(self):
        
        """Return the balance remaining dollars."""
        return self.balance


def main():

    mode = input("Enter 1) Existing customers 2) New customers: ")

    if mode == 1:

        cust_id = input("Enter your customer ID: ")
        account = Customer(cust_id)
        action = input("Enter your choice: \n 1. Withdrawal \n 2. deposit \n 3. Balance check \n" )

        if action == 1:
                amount = input("Enter amount you need to withdraw:")
                result = account.withdraw(amount)
                print "You have %d remaining in your account" % result

        elif action == 2:
                amount = input("Enter amount you need to deposit:")
                result = account.deposit(amount)
                print "Amount %d deposited and your account balance is %d" % (amount, result)
         
        elif action == 3:
                result = account.balancecheck()
                print "You have $ %d in your account!!!" % result
        else:
                print "Invalid option"
                exit(1)

    elif mode == 2:

        cust_id = 0
        account = Customer(cust_id)
        account.cust_registration()

if __name__ == "__main__":

        main()
