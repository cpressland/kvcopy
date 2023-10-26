# kvcopy

Copies Secret objects from one Azure Key Vault to another.

> Disclaimer: This requires Azure CLI (`az`) to be installed and logged in.

## Installation

via pipx:

```shell
$ pipx install kvcopy
```

## Usage

Copy a secret

```shell
$ kvcopy --src example-src-vault --dest example-dest-vault --name my_secret
```
