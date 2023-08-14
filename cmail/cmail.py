#!/usr/bin/python3

import smtplib, ssl, os, sys, datetime, traceback
import argparse
import re as regex


def connect(username, password, smtp, port):
	context = ssl.create_default_context()
	server = smtplib.SMTP(smtp, port)

	server.ehlo()
	server.starttls(context=context)
	server.ehlo()
	server.login(username, password)

	return server


def send(server, f, to, re, body):
	message = "From: {}\nTo: {}\nSubject: {}\n\n{}".format(
		f,
		to,
		re,
		body,
	)

	server.sendmail(f, regex.split(', |,', to), message)


if __name__ == '__main__':
	def get_env(key):
		return os.environ[key] if key in os.environ else None

	parser = argparse.ArgumentParser(description='Send electronic mail')
	parser.add_argument('-u', '--username', help='Server login username. Default env var \'CMAIL_USERNAME\'.', default=get_env('CMAIL_USERNAME'))
	parser.add_argument('-p', '--password', help='Server login password. Default env var \'CMAIL_PASSWORD\'.', default=get_env('CMAIL_PASSWORD'))
	parser.add_argument('-s', '--smtp', help='Server smtp address. Default env \'CMAIL_SMTP\'.', default=get_env('CMAIL_SMTP'))
	parser.add_argument('-sp', '--port', help='Server port. Default env \'CMAIL_SMTP_PORT\'.', type=int, default=get_env('CMAIL_SMTP_PORT'))
	parser.add_argument('-f','--from', help='From address', required=True)
	parser.add_argument('-t','--to', help='Recipient address', required=True)
	parser.add_argument('-re', '--subject', help='Email subject. Default date.', default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))

	args = vars(parser.parse_args())

	if None in args.values():
		sys.stderr.write('no value set for: {}'.format(
			', '.join([k for k in args if args[k] is None])
		))
		parser.print_help()
		sys.exit(2)

	try:
		if os.isatty(sys.stdin.fileno()):
			raise Exception('no bytes in stdin')

		server = connect(
			args['username'],
			args['password'],
			args['smtp'],
			args['port']
		)
		send(
			server, 
			args['from'], 
			args['to'], 
			args['subject'], 
			'\n'.join(sys.stdin.readlines())
		)
	except Exception as e:
		traceback.print_exc()
		print('cmail_error: {}'.format(e))
		sys.exit(1)