import zlib
import base64
import json
from LokiPy import Requests
from RSPs.TransactionClass import Transaction
from RSPs.AssetClass import Asset
from typing import Union, Sequence


class Ops:
    def __init__(self, loki_py_instance: Requests.LokiPy):
        self.lp = loki_py_instance

    def broadcast_tx(self, tx: Transaction, callback=None, interval=3, repeats=3) -> None:
        if tx.type == "create_asset":
            self.lp.createAssets(
                tx.asset.issuer,
                tx.recipient,
                tx.asset.amount,
                tx.asset.asset_code,
                tx.fee,
                tx.asset.info,
                callback,
                interval,
                repeats
            )
        elif tx.type == "transfer_asset":
            self.lp.transferAssets(
                tx.asset.issuer,
                tx.recipient,
                tx.asset.amount,
                tx.asset.asset_code,
                tx.fee,
                tx.asset.info,
                callback,
                interval,
                repeats
            )

    def asset_balances(self) -> Sequence[Asset]:
        resp = self.lp.getBalances()
        assets = []
        for box in resp["result"]["boxes"]:
            if box["type"] == "Asset":
                assets.append(Asset(
                    box["assetCode"],
                    box["value"],
                    box["issuer"],
                    box["data"],
                    box["proposition"]
                ))
        return assets

    @staticmethod
    def broadcast_tx_from_unique_provider(
            tx: Transaction,
            provider: Requests.LokiPy,
            callback=None,
            interval=3,
            repeats=3) -> None:
        if tx.type == "create_asset":
            provider.createAssets(
                tx.asset.issuer,
                tx.recipient,
                tx.asset.amount,
                tx.asset.asset_code,
                tx.fee,
                tx.asset.info,
                callback,
                interval,
                repeats
            )
        elif tx.type == "transfer_asset":
            provider.transferAssets(
                tx.asset.issuer,
                tx.recipient,
                tx.asset.amount,
                tx.asset.asset_code,
                tx.fee,
                tx.asset.info,
                callback,
                interval,
                repeats
            )

    @staticmethod
    def compressed_serialize(rsp: Union[Asset, Transaction]) -> str:
        return base64.b64encode(
            zlib.compress(
                rsp.json().encode("utf-8")
            )
        ).decode("utf-8")

    @staticmethod
    def compressed_deserialize(s_rsp: str) -> Union[Asset, Transaction]:
        j = json.loads(
                zlib.decompress(
                    base64.b64decode(s_rsp)
                ).decode("utf-8")
            )
        if "type" in j:  # TODO : add a class-name member to all json serialized classes
            return Transaction.json_init(j)
        else:
            return Asset.json_init(j)

