import base64
import io
import os
import subprocess
from pathlib import Path

from algosdk import account, kmd, mnemonic
from algosdk.constants import microalgos_to_algos_ratio, min_txn_fee
from algosdk.error import WrongChecksumError, WrongMnemonicLengthError
from algosdk.future.transaction import AssetConfigTxn, PaymentTxn
from algosdk.v2client import algod, indexer
from algosdk.wallet import Wallet

INITIAL_FUNDS = 1000000000  # in microAlgos


## SANDBOX
def _call_sandbox_command(*args):
    """Call and return sandbox command composed from provided arguments."""
    return subprocess.Popen(
        [_sandbox_executable(), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _sandbox_executable():
    """Return full path to Algorand's sandbox executable.

    The location of sandbox directory is retrieved either from the SANDBOX_DIR
    environment variable or if it's not set then the location of sandbox directory
    is implied to be the sibling of this Django project in the directory tree.
    """
    sandbox_dir = os.environ.get("SANDBOX_DIR") or str(
        Path(__file__).resolve().parent.parent.parent / "sandbox"
    )
    return sandbox_dir + "/sandbox"


def cli_passphrase_for_account(address):
    """Return passphrase for provided address."""
    process = _call_sandbox_command("goal", "account", "export", "-a", address)
    passphrase = ""
    output = [line for line in io.TextIOWrapper(process.stdout)]
    for line in output:
        parts = line.split('"')
        if len(parts) > 1:
            passphrase = parts[1]
    if passphrase == "":
        raise ValueError(
            "Can't retrieve passphrase from the address: %s\nOutput: %s"
            % (address, output)
        )
    return passphrase


## CLIENTS
def _algod_client():
    """Instantiate and return Algod client object."""
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    return algod.AlgodClient(algod_token, algod_address)


def _indexer_client():
    """Instantiate and return Indexer client object."""
    indexer_address = "http://localhost:8980"
    indexer_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    return indexer.IndexerClient(indexer_token, indexer_address)


def _kmd_client():
    """Instantiate and return kmd client object."""
    kmd_address = "http://localhost:4002"
    kmd_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    return kmd.KMDClient(kmd_token, kmd_address)


def add_standalone_account():
    """Create standalone account and return two-tuple of its private key and address."""
    private_key, address = account.generate_account()
    return private_key, address

def passphrase_from_private_key(private_key):
    """Return passphrase from provided private key."""
    return mnemonic.from_private_key(private_key)