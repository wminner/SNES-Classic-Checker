#!/usr/bin/env python3

import re, sys
import getopt, pickle
import time, datetime

import urllib.request
import smtplib
from email.mime.text import MIMEText
import getpass

def main(argv):
	default_send_email = "<your_sender_gmail>@gmail.com"
	default_receive_email = "<your_receiver_gmail>@gmail.com"
	sleep_time = 60
	test_run = False
	max_alerts = -1  # -1 means unlimited alerts
	num_alerts = 0

	websites = ['Bestbuy', 'Walmart', 'BHPhoto']
	search_strings = {
		'Amazon' : b"Currently unavailable.",
		'Bestbuy' : b"data-add-to-cart-message=\"Coming Soon\"",
		'Walmart' : b"<span class=\"copy-mini display-block-xs font-bold u-textBlack\">Out of stock<link itemprop=\"availability\" href=\"https://schema.org/OutOfStock\"/></span>",
		'BHPhoto' : b"data-selenium=\"notStock\">New Item - Coming Soon"
	}
	urls = {
		'Amazon' : "https://www.amazon.com/gp/product/B0721GGGS9",
		'Bestbuy' : "http://www.bestbuy.com/site/nintendo-entertainment-system-snes-classic-edition/5919830.p?skuId=5919830",
		'Walmart' : "https://www.walmart.com/ip/PO-HDW-PLACEHOLDER-652-WM50-Universal/55791858",
		'BHPhoto' : "https://www.bhphotovideo.com/c/product/1347308-REG/nintendo_snes_super_nintendo_classic_edition.html"
	}

	def print_usage():
		print("Usage: snesc_checker.py [option(s)]")
		print("  [-n <max_num_of_alerts>] limits the max number of alerts")
		print("  [-s <sleep_time_in_sec>] changes the sleep time")
		print("  [-t] test email mode")

	def search_website(website, url):
		if website == 'Amazon':
			response = urllib.request.Request(url, None, headers={'User-Agent' : 'Mozilla/5.0'})
		else:
			response = urllib.request.Request(url)  # Bestbuy likes to freeze python if you fake the headers?
		try:
			html = urllib.request.urlopen(response).read()
		except:
			print("Exception occurred during {0} fetch!".format(website))
			return 0
		if search_strings[website] in html:
			print("{0} Unavailble {1}...".format(website, datetime.datetime.now()))
			# send_email(sender, sender_pass, receiver, "Not in stock", "test {0}".format(url))
			return 0
		else:
			print("\n{0} IN STOCK {1}!!!!!!!!!!!!!!!!!!!!!!!!!\n".format(website.upper(), datetime.datetime.now()))
			send_email(sender, sender_pass, receiver, "SNES CLASSIC IN STOCK AT {0}".format(website.upper()), url)
			return 1

	def progress_bar():
		print("|0%", end="")
		for k in range(int(sleep_time/2)-6):
			print(" ", end="")
		print("Sleep ", end="")
		for k in range(int(sleep_time/2)-6):
			print(" ", end="")
		print("100%|\n|", end="")
		
		sleep_cnt = 0
		while sleep_cnt < sleep_time:
			time.sleep(1)
			print(".", end="", flush=True)
			sleep_cnt += 1
		print('|')

	# Parse arguments
	if len(sys.argv) != 0:
		try:
			opts, args = getopt.getopt(argv, "htn:s:", ["num=, sleep="])
		except getopt.GetoptError:
			print_usage()
			sys.exit(2)

		for opt, arg in opts:
			if opt == '-h':
				print_usage()
				sys.exit()
			elif opt == '-t':
				test_run = True
			elif opt in ('-s', '--sleep='):
				sleep_time = int(arg)
			elif opt in ('-n', '--num='):
				max_alerts = int(arg)
				if max_alerts <= 0:
					print("Invalid max number of alerts! Exiting...")
					sys.exit(2)

	# Get email and password from which to send and receive alerts
	sender = get_gmail_address(default_send_email, "send")
	sender_pass = get_password(sender)
	receiver = get_gmail_address(default_receive_email, "receive")
	print("")

	if test_run:
		print("Sent test email.")
		send_email(sender, sender_pass, receiver, "SNES Classic Checker - Test Email", "It works!")
	
	# Main loop
	try:
		while True:
			for website in websites:
				num_alerts += search_website(website, urls[website])
				if max_alerts >= 0 and num_alerts >= max_alerts:
					print("Reached max number of alerts! Exiting...")
					sys.exit()
			# Wait for a while before checking again
			# time.sleep(sleep_time)
			progress_bar()
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
		last_addr = None
	
	if mode == "send":
		if last_addr:
			addr = input("Enter your {0} gmail address (or return to use {1}): ".format(mode.upper(), last_addr)) or last_addr
		else:
			addr = input("Enter your {0} gmail address: ".format(mode.upper()))
	else:
		if last_addr:
			addr = input("Enter your {0} gmail address (or return to use {1}): ".format(mode.upper(), last_addr)) or last_addr
		else:
			addr = input("Enter your {0} gmail address: ".format(mode.upper()))

	# Validate address
	pattern = re.compile("[^@]+@gmail.com")
	match = re.match(pattern, addr)
	if not match:
		print("Gmail address \"{0}\" is not valid!".format(addr))
		sys.exit(1)

	# Save the last used IP address to pickle file
	with open(last_email_addr, 'wb') as fp:
		pickle.dump(addr, fp)

	return addr


# Gets your gmail password (does not cache)
def get_password(email):
	password = getpass.getpass("Enter password for {0}: ".format(email))
	if not password:
		print("Email password should not be empty!")
		sys.exit(1)

	return password


# Strip off script name in arg list
if __name__ == "__main__":
	main(sys.argv[1:])
