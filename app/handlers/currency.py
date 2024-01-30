"""
CurrencyHandler
"""
from typing import Dict, List
from uuid import UUID

from app.libs.consts.enums import CurrencyType
from app.libs.decorators.sentry_tracer import distributed_trace
from app.providers import CurrencyProvider
from app.schemas.currency import Currency
from app.serializers.v1.currency import CurrencyInfo, CurrencyNode, CurrencyTree, Currencies


class CurrencyHandler:
    """CurrencyHandler"""

    def __init__(self, currency_provider: CurrencyProvider):
        self.currency_provider = currency_provider

    @distributed_trace()
    async def get_currencies(self) -> Currencies:
        """
        Get currencies
        :return:
        """
        currencies = await self.currency_provider.get_currencies()
        return Currencies(
            currencies=[CurrencyInfo(
                id=currency.id,
                symbol=currency.symbol,
                description=currency.description,
                sequence=currency.sequence,
                parent_id=currency.parent_id
            ) for currency in currencies]
        )

    @distributed_trace()
    async def get_currency_tree(self) -> CurrencyTree:
        """
        Get the currency tree
        :return:
        """
        currencies = await self.currency_provider.get_currency_tree_data()
        currency_tree = self._build_tree_nodes(currencies)
        return CurrencyTree(nodes=currency_tree)

    @distributed_trace()
    async def create_currency(self, currency_info: CurrencyInfo):
        """
        Update currency
        :return:
        """
        currency = Currency(
            **currency_info.model_dump(),
            type=CurrencyType.PAYMENT if currency_info.parent_id else CurrencyType.GENERAL,
            path=f"{str(currency_info.parent_id)}/{str(currency_info.id)}" if currency_info.parent_id else str(currency_info.id)
        )
        return await self.currency_provider.create_currency(currency=currency)

    @distributed_trace()
    async def update_currency(
        self,
        currency_id: UUID,
        currency_info: CurrencyInfo
    ):
        """
        Update currency
        :return:
        """
        currency = Currency(
            **currency_info.model_dump(),
            type=CurrencyType.PAYMENT if currency_info.parent_id else CurrencyType.GENERAL,
            path=f"{str(currency_info.parent_id)}/{str(currency_info.id)}" if currency_info.parent_id else str(currency_info.id)
        )
        return await self.currency_provider.update_currency(currency_id=currency_id, currency=currency)

    def _build_tree_nodes(
        self,
        tree_data: Dict[str, Currency],
        parent_id: str = None,
        parent_node: CurrencyNode = None
    ) -> List[CurrencyNode]:
        """

        :param tree_data:
        :param parent_id:
        :param parent_node:
        :return:
        """
        nodes = []
        for raw_node in filter(lambda item: item.parent_id == parent_id, tree_data.values()):  # type: Currency
            node = CurrencyNode(
                id=raw_node.id,
                symbol=raw_node.symbol,
                description=raw_node.description,
                sequence=raw_node.sequence,
                parent_id=raw_node.parent_id
            )
            nodes.append(node)
            self._build_tree_nodes(tree_data, node.id, node)
        if nodes and parent_node:
            parent_node.children = nodes
        return nodes
