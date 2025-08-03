# enChat
enChat is a terminal based and end-to-end encrypted chatting application.
For encryption, it uses asymmetric key encryption (RSA) for key exchange
and symmetric key encryption (AES with Cipher block chaining) for subsequent
messages between the client and server. Passwords are also securely stored by
using salted hashes (a random 32-byte salt and SHA256 for hashing).

## Side Notes
- The public and private key pair in the `keys/` directory are for demonstration. If this was a real appplication, these keys should NOT be in the git repository. NEVER commit key-pairs to git and github!

- For this project I came up with my own protocol of communication and avoided using libraries like `request` that have inbuilt security features so that I could learn deeply about creating a secure application from scratch. 

## Installation

**Step 1**: Pull the git repo into your local computer by running the following command in your terminal:
```sh
git clone git@github.com:0xRickey/enChat-Server.git
```

**Step 2**: Start a Python virtual environment
```sh
python3 -m venv .venv
```

**Step 3**: install dependencies
```sh
pip install -r requirements.txt
```

After this you should have everything ready to go to run the server.

## Running the server
To start the server and allow it to begin accepting client requests, first change into the `enChat-Server` directory and run then following:
```sh
python3 server.py
```