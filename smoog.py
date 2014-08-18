################################################################################
#                                                                              #
# CONFIGURATION                                                                #
#                                                                              #
################################################################################

# Salt sequence: 16-character hex string. Can be generated with
#   $ python -c "import random; print '%016x' % random.randrange(16 ** 16)"
SALT = '8c6a5d9ae074282e'

# Files to be encrypted: list of patterns recognized by gitattributes:
#  https://www.kernel.org/pub/software/scm/git/docs/gitattributes.html.
SENSITIVE_FILES = ['secret.txt']


################################################################################
#                                                                              #
# SMOOG                                                                        #
#                                                                              #
# Credits to                                                                   #
#   https://github.com/shadowhand/git-encrypt/blob/develop/git-encrypt-init.sh #
#   by Jay Taylor [@jtaylor]                                                   #
#                                                                              #
# DO NOT EDIT ANYTHING BELOW                                                   #
#                                                                              #
################################################################################

import os
import shutil
import random
import getpass
import re
import stat

SMOOG_DIR = '.git/smoog'
GIT_CONFIG = '.git/config'
GIT_ATTRIBUTES = '.git/info/attributes'

def isConfirm(s):
    return s == 'y' or s == 'yes'

def validPass(p):
    return re.match(r'\w+$', p)

# Clean all references to smoog in this git repository
def clean():
    if os.path.exists(SMOOG_DIR):
        print 'Remove {0} (y/n)?'.format(SMOOG_DIR),
        if not isConfirm(raw_input()):
            return False
        shutil.rmtree(SMOOG_DIR)
    if os.path.exists(GIT_ATTRIBUTES):
        print 'Remove {0} (y/n)?'.format(GIT_ATTRIBUTES),
        if not isConfirm(raw_input()):
            return False
        os.remove(GIT_ATTRIBUTES)
    return True

# Define filter scripts
SSL_SCRIPTS = {
        'clean_filter_openssl': """#!/usr/bin/env bash
SALT_FIXED={1}
PASS_FIXED={0}
openssl enc -base64 -aes-256-ecb -S $SALT_FIXED -k $PASS_FIXED
""",
        'smudge_filter_openssl': """#!/usr/bin/env bash
PASS_FIXED={0}
openssl enc -d -base64 -aes-256-ecb -k $PASS_FIXED 2> /dev/null || cat
""",
        'diff_filter_openssl': """#!/usr/bin/env bash
PASS_FIXED={0}
openssl enc -d -base64 -aes-256-ecb -k $PASS_FIXED -in "$1" 2> /dev/null || cat "$1"
""",
}

# Git config links to filter scripts
SCRIPT_CONFIG = """[filter "openssl"]
	smudge = .git/smoog/smudge_filter_openssl
	clean = .git/smoog/clean_filter_openssl
[diff "openssl"]
	textconv = .git/smoog/diff_filter_openssl
"""

# Initialize SMOOG
def init():
    # Prompt user for password.
    password = ''
    while True:
        password = getpass.getpass('Enter passphrase: ')
        if not validPass(password):
            print 'Invalid passphrase.'
            continue
        confirmPassword = getpass.getpass('Confirm passphrase: ')
        if confirmPassword != password:
            print 'Passphrases do not match.'
            continue
        break

    # Initialize SMOOG_DIR
    print 'info: initializing', SMOOG_DIR
    os.mkdir(SMOOG_DIR);
    for filterType in SSL_SCRIPTS:
        filterScriptPath = os.path.join(SMOOG_DIR, filterType)
        with open(filterScriptPath, 'w') as fh:
            fh.write(SSL_SCRIPTS[filterType].format(password, SALT))
        os.chmod(filterScriptPath,
                os.stat(filterScriptPath).st_mode | stat.S_IEXEC)

    # Add ssl scripts to git config
    opensslApplied = False
    with open(GIT_CONFIG, 'r') as fh:
        if 'openssl' in fh.read():
            opensslApplied = True
    if opensslApplied:
        print 'info: openssl filter/diff already configured for this clone'
    else:
        print 'info: applying openssl filter/diff to this clone...'
        with open(GIT_CONFIG, 'a') as fh:
            fh.write(SCRIPT_CONFIG.format(SMOOG_DIR))

    # Add sensitive files to GIT_ATTRIBUTES
    print 'info: initializing file', GIT_ATTRIBUTES
    with open(GIT_ATTRIBUTES, 'w') as fh:
        for sensitiveFile in SENSITIVE_FILES:
            fh.write('{0} filter=openssl diff=openssl\n'.format(sensitiveFile))


# Run SMOOG
if __name__ == '__main__':
    # Ensure that we are running in the root of a git repository.
    if not os.path.exists(GIT_CONFIG):
        print 'fatal: this script can only be run in the root of a git repository'
        exit(1)
    if not clean():
        print 'Initialization script cancelled.'
        exit(1)
    init()
    os.system('git reset --hard HEAD')

