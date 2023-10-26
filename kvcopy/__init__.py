"""Main module for kvcopy project."""

import click
from azure.core.exceptions import ResourceNotFoundError, ServiceRequestError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


@click.command()
@click.option("--src", "-s", help="Source KeyVault Name")
@click.option("--dest", "-d", help="Destination KeyVault Name")
@click.option("--name", "-n", help="Name of the secret to copy")
def cli(src: str, dest: str, name: str) -> None:
    """Copy a secret from one KeyVault to another."""
    click.echo(f"Copying '{name}' from '{src}' to '{dest}'")
    credential = DefaultAzureCredential()
    try:
        src_keyvault_client = SecretClient(
            f"https://{src}.vault.azure.net", credential,
        )
        secret = src_keyvault_client.get_secret(name)
        dest_keuvault_client = SecretClient(
            f"https://{dest}.vault.azure.net", credential,
        )
        dest_keuvault_client.set_secret(name, secret.value)
    except ResourceNotFoundError:
        click.echo(f"Secret '{name}' not found in '{src}'", err=True)
    except ServiceRequestError:
        click.echo(f"Unable to connect to KeyVault '{src}'", err=True)


if __name__ == "__main__":
    cli()
