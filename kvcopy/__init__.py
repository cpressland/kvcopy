"""Main module for kvcopy project."""

import typer
from azure.core.exceptions import ResourceNotFoundError, ServiceRequestError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from loguru import logger
from typing_extensions import Annotated

cli = typer.Typer()


@cli.command()
def copy(
    src_vault_name: Annotated[str, typer.Option(help="The name of the KeyVault to copy from")],
    dest_vault_name: Annotated[str, typer.Option(help="The name of the KeyVault to copy to")],
    key_name: Annotated[str, typer.Option(help="The name of the secret to copy")],
) -> None:
    """Copy a secret from one KeyVault to another."""
    logger.info(f"Copying '{key_name}' from '{src_vault_name}' to '{dest_vault_name}'")
    credential = DefaultAzureCredential()
    try:
        src_keyvault_client = SecretClient(f"https://{src_vault_name}.vault.azure.net", credential)
        secret = src_keyvault_client.get_secret(key_name)
        dest_keuvault_client = SecretClient(f"https://{dest_vault_name}.vault.azure.net", credential)
        dest_keuvault_client.set_secret(key_name, secret.value)
    except ResourceNotFoundError:
        logger.info(f"Secret '{key_name}' not found in '{src_vault_name}'", err=True)
    except ServiceRequestError:
        logger.error(f"Unable to connect to KeyVault '{src_vault_name}'", err=True)


@cli.command()
def sync(
    src_vault_name: Annotated[str, typer.Option(help="The name of the KeyVault to copy from")],
    dest_vault_name: Annotated[str, typer.Option(help="The name of the KeyVault to copy to")],
) -> None:
    """Sync an entire KeyVault to another KeyVault."""
    logger.info(f"Syncing '{src_vault_name}' to '{dest_vault_name}'")
    credential = DefaultAzureCredential()
    try:
        src_keyvault_client = SecretClient(f"https://{src_vault_name}.vault.azure.net", credential)
        dest_keyvault_client = SecretClient(f"https://{dest_vault_name}.vault.azure.net", credential)
        for secret in src_keyvault_client.list_properties_of_secrets():
            secret_name = secret.name
            secret_value = src_keyvault_client.get_secret(secret_name).value
            secret_content_type = src_keyvault_client.get_secret(secret_name).properties.content_type
            try:
                existing_secret = dest_keyvault_client.get_secret(secret_name).value
            except ResourceNotFoundError:
                existing_secret = None
            if existing_secret is None or existing_secret != secret_value:
                logger.info(f"Copying '{secret_name}' from '{src_vault_name}' to '{dest_vault_name}'")
                dest_keyvault_client.set_secret(secret_name, secret_value, content_type=secret_content_type)
            else:
                logger.info(f"Skipping '{secret_name}' as it is already up to date in '{dest_vault_name}'")
    except ResourceNotFoundError:
        logger.error(f"KeyVault '{src_vault_name}' not found", err=True)
    except ServiceRequestError:
        logger.error(f"Unable to connect to KeyVault '{src_vault_name}'", err=True)


if __name__ == "__main__":
    cli()
