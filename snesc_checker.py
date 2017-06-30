#!/usr/bin/env python3

import re, sys
import getopt, pickle
import time, datetime

import urllib.request
import smtplib
from email.mime.text import MIMEText
import pyautogui

def main(argv):
	default_send_email = "<your_sender_gmail>@gmail.com"
	default_receive_email = "<your_receiver_gmail>@gmail.com"
	sleep_time = 60

	websites = ['Amazon', 'Bestbuy', 'Walmart']
	search_strings = {
		'Amazon' : b"Currently unavailable.",
		'Bestbuy' : b"data-add-to-cart-message=\"Coming Soon\"",
		'Walmart' : b"<span class=\"copy-mini display-block-xs font-bold u-textBlack\">Out of stock<link itemprop=\"availability\" href=\"https://schema.org/OutOfStock\"/></span>"
	}
	links = {
		'Amazon' : "https://www.amazon.com/gp/product/B0721GGGS9",
		'Bestbuy' : "http://www.bestbuy.com/site/nintendo-entertainment-system-snes-classic-edition/5919830.p?skuId=5919830",
		'Walmart' : "https://www.walmart.com/ip/PO-HDW-PLACEHOLDER-652-WM50-Universal/55791858"
	}

	def print_usage():
		print("Usage: snesc_checker.py [-s <sleep_time_in_sec>]")

	def search_website(website, link):
		with urllib.request.urlopen(link) as response:
			html = response.read()
			if search_strings[website] in html:
				print("{0} Unavailble {1}...".format(website, datetime.datetime.now()))
				# send_email(sender, sender_pass, receiver, "Not in stock", "test {0}".format(link))
			else:
				print("\n{0} IN STOCK {1}!!!!!!!!!!!!!!!!!!!!!!!!!\n".format(website.upper(), datetime.datetime.now()))
				send_email(sender, sender_pass, receiver, "SNES CLASSIC IN STOCK AT {0}".format(website.upper()), link)

	# Parse arguments
	if len(sys.argv) != 0:
		try:
			opts, args = getopt.getopt(argv, "s:", ["sleep="])
		except getopt.GetoptError:
			printUsage()
			sys.exit(2)

		for opt, arg in opts:
			if opt == '-h':
				printUsage()
				sys.exit()
			elif opt in ('-s', '--sleep='):
				sleep_time = int(arg)

	# Get email and password from which to send and receive alerts
	sender = get_gmail_address(default_send_email, "send")
	sender_pass = get_password(sender)
	receiver = get_gmail_address(default_receive_email, "receive")
	
	# Main loop
	try:
		while True:
			for website in websites:
				search_website(website, links[website])
			print("")	
			# Wait for 30 seconds before checking again
			time.sleep(sleep_time)
	except KeyboardInterrupt:
		print("\nExiting...")


# Create email with subject and body, then sends via gmail address provided
def send_email(sender, sender_pass, receiver, subject, body):
	# Create email
	msg = MIMEText(body)
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = receiver

	# Send email out
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(sender, sender_pass)
	server.send_message(msg)
	server.quit()


# Gets and caches your gmail address
def get_gmail_address(default_addr, mode):
	last_email_addr = "{0}_email.pkl".format(mode)

	# Try to get pickle of last IP address
	try:
		with open(last_email_addr, 'rb') as fp:
			last_addr = pickle.load(fp)
	except IOError:
		last_addr = default_addr
	
	if mode == "send":
		addr = pyautogui.prompt(text="Enter your {0} gmail address".format(mode), title="{0} Gmail Address".format(mode.capitalize()), default=last_addr)
	else:
		addr = pyautogui.prompt(text="Enter your {0} gmail address (may be the same as send gmail address)".format(mode), title="{0} Gmail Address".format(mode.capitalize()), default=last_addr)		

	# Validate address
	pattern = re.compile("[^@]+@gmail.com")
	match = re.match(pattern, addr)
	if not match:
		pyautogui.alert(text="Gmail Address \"{0}\" is not valid!".format(addr), title="Invalid Gmail Address", button='Exit')
		sys.exit(1)

	# Save the last used IP address to pickle file
	with open(last_email_addr, 'wb') as fp:
		pickle.dump(addr, fp)

	return addr


# Gets your gmail password (does not cache)
def get_password(email):
	password = pyautogui.password(text="Enter password for {0}".format(email), title="Password", mask='*')
	if not password:
		pyautogui.alert(text="Password should not be empty!", title="Invalid Password", button='Exit')
		sys.exit(1)

	return password


# Strip off script name in arg list
if __name__ == "__main__":
	main(sys.argv[1:])