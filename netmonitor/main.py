#!/usr/bin/python3

import os
import cmail
import argparse
import datetime
import sys

services = [
	# List services here. Just makes command call to `ping`.
]


def poll(address):
	return os.system("ping {} 2 {} >{}".format(
		'-n' if os.name == 'nt' else '-c',
		address,
		'nul' if os.name == 'nt' else '/dev/null'
	)) == 0


def do(username, password, smtp, port, f, to):
	failed = list()

	for service in services:
		print('Polling {}...'.format(service))
		if not poll(service):
			print('\tFailed!')
			failed.append(service)
		else:
			print('\tSuccess.')

	print('\n\nTested {} services, {} failed'.format(len(services), len(failed)))

	if not failed:
		return

	server = cmail.connect(username, password, smtp, port)
	msg = 'The following {} service{} failed a poll:\n{}'.format(
		len(failed),
		'' if len(failed) == 1 else 's',
		'\n'.join(failed)
	)
	subject = '[URGENT] netmonitor: service{} UNREACHABLE'.format('' if len(failed) == 1 else 's')
	cmail.send(server, f, to, subject, msg)


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

	args = vars(parser.parse_args())

	if None in args.values():
		sys.stderr.write('no value set for: {}\n'.format(
			', '.join([k for k in args if args[k] is None])
		))
		parser.print_help()
		sys.exit(2)

	try:
		do(
			args['username'],
			args['password'],
			args['smtp'],
			args['port'],
			args['from'],
			args['to']
		)
	except Exception as e:
		import traceback
		traceback.print_exc()
		print('netmonitor error: {}'.format(e))
		sys.exit(1)