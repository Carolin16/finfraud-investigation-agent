class InvoiceValidator:
    def validate(self,invoice:dict)->None:
        if "invoice_amount" not in invoice:
            raise ValueError("Missing field: invoice_amount")
        if "po_amount" not in invoice:
            raise ValueError("Missing field: po_amount")
        if "gr_amount" not in invoice:
            raise ValueError("Missing field: gr_amount")