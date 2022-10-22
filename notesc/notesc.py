m4_changecom(,)m4_dnl
#!m4__PYTHON3_PATH
m4_changecom(`#')m4_dnl

import argparse
import os
import subprocess
import tempfile
import traceback
import sys

def do(args):
    data = {'output_p': args['output']}

    if not args['input']:
        if os.isatty(sys.stdin.fileno()):
            raise Exception('no bytes in stdin')
        else:
            data['input'] = ''.join(sys.stdin.readlines())
    else:
        input_path = os.path.expanduser(args['input'])
        if not os.path.exists(input_path):
            raise Exception('input file {} does not exist'.format(input_path))

        with open(input_path, 'r') as f:
            data['input'] = ''.join(f.readlines())


    data['prepend'] = []
    if args['prepend']:
        for p in args['prepend']:
            p = os.path.expanduser(p)

            if not os.path.exists(p):
                raise Exception('prepend file {} does not exist'.format(p))

            with open(p, 'r') as f:
                data['prepend'].append(''.join(f.readlines()))

    if args['template']:
        p = os.path.expanduser(args['template'])
        if not os.path.exists(p):
            raise Exception('template file {} does not exist'.format(p))

        data['template_p'] = p
    else:
        data['template_p'] = None

    run(data)


def run(data):
    temp_file_o = tempfile.NamedTemporaryFile(mode='w')

    with open(temp_file_o.name, 'w') as f:
        if data['prepend']:
            f.write('\n'.join(data['prepend']))

        f.write(data['input'])
        f.flush()

    cmd = [
        'pandoc', 
        '-s', '--toc', '--pdf-engine=xelatex', '--to=pdf', '--from=markdown',
        '--filter=pandoc-crossref'
    ]

    if data['template_p']:
        cmd.append('--template={}'.format(data['template_p']))

    in_fd = open(temp_file_o.name)
    out_fd = open(data['output_p'], 'wb') if data['output_p'] and data['output_p'] != '-' else None

    subprocess.Popen(cmd, stdin=in_fd, stdout=out_fd).wait()

    in_fd.close()
    out_fd.close()

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", "-i", help="Input path. Use '-' or leave blank for stdin", nargs='?')
        parser.add_argument("--output", "-o", help="Output path. Use '-' or leave blank for stdout", nargs='?')
        parser.add_argument("--prepend", "-p", help="Path to file to prepend", nargs='*')
        parser.add_argument("--template", "-t", help="LaTeX Pandoc template", nargs='?')
        parser.add_argument('--debug', help='Debug', action='store_true')

        args = vars(parser.parse_args())

        do(args)
    except Exception as e:
        print('notesc error: {}'.format(e))

        if args['debug']:
            print(traceback.format_exc())