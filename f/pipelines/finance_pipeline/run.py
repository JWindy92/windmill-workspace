# requirements:
# wmill
# openbao-client@git+https://github.com/JWindy92/openbao_client.git
# finance-pipeline@git+https://github.com/JWindy92/budget_tool.git

import wmill
from openbao_client import OpenBaoClient
from finance_pipeline.simplefin import ingest_simplefin


def main():
    token = wmill.get_variable("f/infrastructure/openbao_token")

    bao = OpenBaoClient(
        address="http://openbao:8200",
        token=token,
    )

    secret = bao.get_secret("finance_pipeline")
    access_url = secret["simplefin_access_url"]

    return ingest_simplefin(
        access_url=access_url,
        output_path="/tmp/account_balances.json",
    )
