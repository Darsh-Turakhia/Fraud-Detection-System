from cardvalidator import luhn
from cardvalidator import formatter

def validate_card_number(number):
	return luhn.is_valid(number)

def get_issuer(number):
	if luhn.is_valid(number) == True:
		return formatter.get_format(number)
	else:
		return None

