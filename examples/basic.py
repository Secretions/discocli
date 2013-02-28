#!/usr/bin/env python

import sys
sys.path.append('../')

import discocli

def new_prompt(self):
    return '{0} [{1}] -=> '.format(self.name, self.context)

def print_tokens(cli, tokens):
    print tokens

def yarnmode(cli, tokens):
    cli.context = 'yarn'

def normal(cli, tokens):
    cli.context = 'default'

cli = discocli.term('Test', debug=False)
functype = type(cli.prompt)
cli.prompt = functype(new_prompt, cli, discocli)

cli.add_item('print_tokens', 'Print Tokens', print_tokens, context='default')
cli.add_item('yarnmode', 'Enter "Yarn" Mode', yarnmode, context='default')
# Overrides normal exit, though not quit, etc.
cli.add_item('exit', 'Exit "Yarn" Mode', normal, context='yarn')

# run just a single line
cli.run('print_tokens')

# interactive mode
cli.run()
