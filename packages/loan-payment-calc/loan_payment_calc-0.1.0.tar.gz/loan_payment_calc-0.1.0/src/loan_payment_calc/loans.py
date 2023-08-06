'''
The loans module.

This module contains functionality for loan management and payment strategies
#doctest: +NORMALIZE_WHITESPACE
'''

from datetime import datetime

class Loan:
	''' Class to hold Loan values.
	
	Attributes
	----------
	amount : float, default 0.0
		Initial amount of the loan. This value is malleable and will increase 
		and decrease based on the payments applied.
	name : str
		Name of the loan
	min_payment : float
		Minimum payment required per month
	date_created : datetime
		Day that the loan was created

	>>> loans.Loan(5, 'MyLoan')
	Loan Object:
	Name:  MyLoan
	Amount:  5
	Minimum Payment:  None
	Date Created:  None
	'''
	num_payments = 0

	def __init__(
		self, amount=0.0, name=None, min_payment=None, date_created=None):
		self.name = name
		self.amount = amount
		self.min_payment = min_payment
		self.date_created = date_created


	def __str__(self):
		''' Method used to change how the loan is displayed with a print()

		Examples
	    --------
		When printing or representing the loan, a detailed report should appear

		>>> loan = Loan() 
		>>> loan
			Loan Object:
		Name:  None
		Amount:  0.0
		Minimum Payment:  None
		Date Created:  None
		'''
		return (
	        f'\tLoan Object:\nName:  {self.name}\n'
	        f'Amount:  {self.amount}\nMinimum Payment:  {self.min_payment}\n'
	        f'Date Created:  {self.date_created}'
	    )


	def __repr__(self):
	    return str(self)


	def SetAmount(self, amount):
		''' Method used to set the loan amount

		Parameters
		----------
		amount : float
			Amount of money remaining for the loan
		'''
		self.amount = amount


	def SetName(self, name):
		''' Method used to set the loans name

		Parameters
		----------
		name : str
			Name of the loan
		'''
		self.name = name


	def SetDateCreated(self, date_created):
		''' Method used to set the date the loan was created

		Parameters
		----------
		date_created : datetime
			Date the loan was created
		'''
		self.date_created = date_created


	def SetMinPayment(self, amount):
		''' Method used to set the minimum payment required for the loan

		Parameters
		----------
		amount : float
			Minimum payment required per month
		'''
		self.min_payment = amount


class LoanPayment(Loan):
	''' Class to hold payment for a specific loan

	Attributes
	----------
	num_payments : int
		Number of payments relative to the date the loan was created
	amount : float
		Amount of money the payment is
	date_paid : datetime
		Date the payment was made

	'''
	num_payments = 0
	def __init__(self, amount, date_paid):
		super().__init__()
		self.amount = amount
		self.date_paid = date_paid

	def SetPaymentAmount(self, amount):
		''' Method used to set the amount the payment was

		Parameters
		----------
		amount : float
			Amount of money the payment is
		'''
		self.amount = amount