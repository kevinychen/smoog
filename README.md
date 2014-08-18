smoog
=====

Easily encrypt files in your git repository.

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
    ```

5. Add sensitive files, commit, and push. When pushing to remote, your
sensitive files will be automatically encrypted.

    ```shell
    $ git add sensitive.txt
    $ git commit
    $ git push
    ```

### Cloning a Git repository protected by Smoog

1. Clone the repository.

2. Run smoog.py from the root directory of the git repository. When prompted,
enter the secret passphrase. Now all the sensitive files are readable by you!

    Note: Do *not* change `SALT` in smoog.py.

3. Modify the sensitive files, commit, and push. Your changes will be
automatically encrypted.

### Adding additional sensitive files

If you change `SENSITIVE_FILES` in smoog.py, you must run smoog.py again. When
others pull your modified code, they will need to run `python smoog.py reset`
to decrypt the new files.

*IMPORTANT:* Every time you git add a sensitive file, make sure that you have
run smoog.py beforehand with that file pattern listed in `SENSITIVE_FILES`.

### Changing passphrases/resetting Smoog

At any time, run `python smoog.py reset` to reset the passphrase or re-sync
Smoog with your repository.

*IMPORTANT:* This command resets your git repository to HEAD, so make sure
that all your changes are committed before running this command.

## Credits

Thanks to https://github.com/shadowhand/git-encrypt, where most of this code
came from.

## License

The MIT License (MIT)

Copyright (c) 2014 Kevin Y. Chen kyc2915@mit.edu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
