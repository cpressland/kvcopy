# kvcopy

Copies Secret objects from one Azure Key Vault to another.

> Disclaimer: This requires Azure CLI (`az`) to be installed and logged in for local use.

## Installation

via pipx:

```shell
$ pipx install kvcopy
```

via docker:
```shell
$ docker pull ghcr.io/cpressland/kvcopy:latest
```

## Usage

Copy a secret

```shell
$ kvcopy copy --src-vault-name $src_vault_name --dest-vault-name $dest_vault_name --key-name $key_name
```

Sync an entire vault

```shell
$ kvcopy sync --src-vault-name $src_vault_name --dest-vault_name $dest_vault_name
```
