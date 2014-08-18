smoog
=====

Easily encrypt some list of files in your git repository.

## Usage

### Adding Smoog to a Git repository for the first time

1. Copy smoog.py into the root directory of your git repository.

2. At the top of smoog.py, replace `SENSITIVE_FILES` with a list of files
that you want to encrypt before adding to your repository.

    ```python
    SENSITIVE_FILES = ['sensitive.txt', 'secret_docs/*', '*.pem']
    ```

3. (Optional) For additional security, at the top of smoog.py, replace `SALT`
with a random 16 character hex string.

    ```shell
    $ python -c "import random; print '%016x' % random.randrange(16 ** 16)"
    5f04d06803aaf785
    ```

    ```python
    SALT = '5f04d06803aaf785'
    ```

4. Run smoog.py from the root directory of your git repository. When prompted,
enter a passphrase consisting of one or more alphanumeric characters.

    ```shell
    $ python smoog.py
    Enter passphrase: secret
    Confirm passphrase: secret

5. Add sensitive files, commit, and push. When pushing to remote, your
sensitive files will be automatically encrypted.

### Cloning a Git repository protected by Smoog

1. Clone the repository.

2. Run smoog.py from the root directory of the git repository. When prompted,
enter the secret passphrase. Now all the sensitive files are readable by you!

    Note: Do *not* change `SALT` in smoog.py.

3. Modify the sensitive files, commit, and push. Your changes will be
automatically encrypted.

### Adding additional sensitive files

If you wish to modify the list of sensitive files, follow these steps.

1. Change `SENSITIVE_FILES` in smoog.py as desired.

2. Re-run smoog.py. You will first be prompted to delete some Smoog settings
files. Then you will be prompted for a passphrase. You may use your old
passphrase or change to a new passphrase (but if you change the passphrase,
you will need to commit a new version of all sensitive files).

3. Add new sensitive files, commit, and push.

## Credits

Thanks to https://github.com/shadowhand/git-encrypt, where most of this code
came from.

