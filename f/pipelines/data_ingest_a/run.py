# requirements:
# openbao-client@git+https://github.com/JWindy92/openbao_client.git
# data-ingest-a@git+https://github.com/JWindy92/data-ingest-a.git

import wmill
from openbao_client import OpenBaoClient
from data_ingest import pipeline


def main():
    token = wmill.get_variable("f/infrastructure/openbao_token")

    bao = OpenBaoClient(
        address="http://openbao:8200",
        token=token,
    )

    return pipeline.run(bao)
