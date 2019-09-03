#!/usr/bin/python3.6
import os, sys, time, locale
from tqdm import tqdm

# root directory of the maildir account directory of thunderbird
maildir = '/mnt/c/Users/Andreas/AppData/Roaming/Thunderbird/Profiles/z3mwnjgu.default/ImapMail/imap.mail.yahoo.com'
# own email address(es)
address = 'esan2013@yahoo.com'

def stats():
	""" read all mail files and collect data """
	mailfiles = []
	mails_per_year = { 'in': {}, 'out': {} }
	# get all mail files
	for root,dirs,files in os.walk(maildir):
		for f in files:
			filename, file_extension = os.path.splitext(f)
			if file_extension == '.eml':
				mailfiles.append(os.path.join(root, f))

	# process all mail files to get data
	for f in tqdm(mailfiles, unit='mails', mininterval=0.05):
		mailtype = None
		maildate = None
		for line in open(f, 'r', encoding='latin1'):
			# decide wether an email was sent or received
			if line.startswith('From: '):
				mailtype = 'out' if address in line else 'in'
			# get mail date
			if line.startswith('Date: '):
				startindex = line.index(',')+2 if ',' in line else line.index(' ')+1
				datestring = line[startindex:].strip()
				datestring = datestring[:datestring.rindex(" ")] if len(datestring.split(" "))>5 else datestring
				maildate = time.strptime(datestring, '%d %b %Y %H:%M:%S %z')
			# if maildate was not found, try alternative approach
			if maildate is None and ' +0000' in line and len(line)>26:
				datestring = line[line.index(' +0000')-20:line.index(' +0000')+6]
				try:
					maildate = time.strptime(datestring, '%d %b %Y %H:%M:%S %z')
				except ValueError:
					maildate = None
			# save found data
			if line.startswith('Content-Length: ') and mailtype is not None and maildate is not None:
				if maildate.tm_year in mails_per_year[mailtype]:
					mails_per_year[mailtype][maildate.tm_year] += 1
				else:
					mails_per_year[mailtype][maildate.tm_year] = 1
				break

	return True

# output
print('Processing mails...')
if stats():
	print('Finished.')