import json
import sys
from typing import List, Tuple

import click

from tdameritrade_client.client import TDClient


def get_positions(client: TDClient) -> Tuple[str, List[List[str]]]:
    """
    Retrieve all positions for the authenticated account.

    Args:
        client: An authorized TDClient object.

    Returns:
        The current liquidation value of the account and a list of positions where each position is
        `[position_id, position_type, position_value]`.

    """

    acct_info = client.get_positions()
    try:
        positions = acct_info['securitiesAccount']['positions']
        liq_value = acct_info['securitiesAccount']['currentBalances']['liquidationValue']
        extracted_data = [
            [pos['instrument']['symbol'],
             pos['instrument']['assetType'],
             pos['marketValue']] for pos in positions]
    except KeyError:
        if 'error' in acct_info.keys():
            click.echo(f'ERROR: {acct_info["error"]} (requested account number {client._acct_number}).')
            sys.exit()
        else:
            click.echo(json.dumps(acct_info))
            raise KeyError('Received invalid response.')

    return liq_value, extracted_data
