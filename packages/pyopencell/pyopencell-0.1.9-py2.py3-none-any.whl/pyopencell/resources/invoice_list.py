from pyopencell.client import Client
from pyopencell.resources.base_resource_list import BaseResourceList
from pyopencell.resources.invoice import Invoice
from pyopencell.responses.paged_response import PagedResponse
from pyopencell.responses.action_status import ActionStatus


class InvoiceList(BaseResourceList):
    _name = "invoices"
    _url_path = "/list"
    items_resource_class = Invoice

    invoices = []

    @classmethod
    def get(cls):
        """
        Returns a Invoice list with invoice instances data.

        :return: PagedResponse:
        """
        response_data = Client().get(
            cls._url_path
        )

        status = response_data.get("status")
        if status and status != "SUCCESS":
            return ActionStatus(**response_data)

        return PagedResponse(cls, **response_data)
