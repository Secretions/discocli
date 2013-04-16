#!/usr/bin/env python

import sys
import inspect

### For tokenizing input
import shlex

### If readline is available, we get history! Yay!
try:
    import readline
except ImportError:
    try:
        import pyreadline as readline
    except ImportError:
        pass

class term(object):
    "DiscoCLI Terminal Object"

    def __init__(self, name='> ', context='default', debug=False, **kwargs):
        self.name = name
        self.context = context
        self.debug = debug
        self.commands = {}
        self.commands['default'] = {}

        ### Default actions

        # Actions for processing non-commands
        self.add_item('default_action', 'Default Action', term.default_default_action, context='system', hidden=True)
        self.add_item('invalid_action', 'Invalid Action', term.default_invalid_action, context='system', hidden=True)

        # Special actions
        self.add_item('help', 'Help', term.default_help_action, aliases = ['?','-h','--help'], context='system')
        self.add_item('exit', 'Exit {0}'.format(self.name), term.default_exit_action, aliases = ['quit'], context='system')

    '''
    run() - Process command or start interactive mode
    '''
    def run(self, line = None):
        # Process a single command
        if line:
            self.run_line(self.parse_input(line))
            return

        # Run in interactive mode
        while True:
            line = raw_input(self.prompt())
            self.run_line(self.parse_input(line))

    '''
    run_line - Executes a single commandline entry
    '''
    def run_line(self, tokens):
        self.dbprint("Tokens:",tokens)
        print ""

        if len(tokens) == 0:
            self.dbprint("No command, running default action...")
            self.commands['system']['default_action']['run'](self,tokens)
            return
        
        command = tokens[0]

        # Current context overrides system
        if command in self.commands[self.context]:
            self.dbprint("Command '{0}' exists in current context '{1}', running...".format(command, self.context))
            self.commands[self.context][command]['run'](self,tokens)
        elif command in self.commands['system']:
            self.dbprint("Command '{0}' exists as system command, running...".format(command))
            self.commands['system'][command]['run'](self,tokens)                    
        else:
            self.dbprint("Command '{0}' doesn't exist in current context '{1}', running invalid action...".format(command, self.context))
            self.commands['system']['invalid_action']['run'](self,tokens)

        print ""

    '''
    add_item - Adds a menu item to a context
    '''
    def add_item(self, name, description, function, hidden=False, aliases=None, context='default'):
        if context not in self.commands:
            self.commands[context] = {}
        self.commands[context][name] = {}
        self.commands[context][name]['run'] = function
        self.commands[context][name]['desc'] = description
        self.commands[context][name]['hidden'] = hidden
        if aliases:
            for alias in aliases:
                self.commands[context][alias] = {}
                self.commands[context][alias]['hidden'] = True
                self.commands[context][alias]['alias'] = name
                self.commands[context][alias]['run'] = self.commands[context][name]['run']


    ### Basic Default Actions

    '''
    default_help_action - Display help for current context
    '''
    def default_help_action(self, tokens):
        print "Help for:",self.context,"\n"
        for command in self.commands[self.context]:
            if not self.commands[self.context][command]['hidden']:
                print command,'-',self.commands[self.context][command]['desc']
        print "\nGlobal commands:\n"
        for command in self.commands['system']:
            if not self.commands['system'][command]['hidden']:
                print command,'-',self.commands['system'][command]['desc']

    '''
    default_default_action - Do nothing
    '''
    def default_default_action(self, tokens):
        print ""

    '''
    default_invalid_action - Whine
    '''
    def default_invalid_action(self, tokens):
        print "Unknown command:",tokens[0]

    '''
    default_exit_action - Exit
    '''
    def default_exit_action(self, tokens):
        print "Exiting..."
        exit(0);

    ### Utility functions Which may be useful to override
    '''
    parse_input() - default function for tokenizing input
    '''
    def parse_input(self, line):
        return shlex.split(line)

    '''
    prompt() - Returns prompt for current context
    '''
    def prompt(self):
        return '{0} [{1}]> '.format(self.name, self.context)

    ### Helper functions
    def dbprint(self, *args):
        if self.debug == True:
            output = '{0}:'.format(inspect.stack()[1][3])
            for arg in args:
                output = '{0} {1}'.format(output, arg)
            print >> sys.stderr, output
