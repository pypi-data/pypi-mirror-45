import requests

from django.conf import settings

try:
    from mailqueue.models import MailerMessage
except:
    pass

from saleboxdjango.models import TransactionEvent


class SaleboxEventHandler:
    def __init__(self):
        # get list of events
        tes = TransactionEvent \
                .objects \
                .filter(processed_flag=False) \
                .order_by('-created')

        # loop through and process them
        for te in tes:
            if te.event == 'shipping_packed':
                self.event_shipping_packed(te)
            elif te.event == 'shipping_picked':
                self.event_shipping_picked(te)
            elif te.event == 'shipping_shipped':
                self.event_shipping_shipped(te)
            elif te.event == 'transaction_created':
                self.event_transaction_created(te)

    def event_shipping_packed(self, event):
        """
        Add your code here
        Don't forget to set the processed_flag when done
        """
        event.processed_flag=True
        event.save()

    def event_shipping_picked(self, event):
        """
        Add your code here
        Don't forget to set the processed_flag when done
        """
        event.processed_flag=True
        event.save()

    def event_shipping_shipped(self, event):
        """
        Add your code here
        Don't forget to set the processed_flag when done
        """
        event.processed_flag=True
        event.save()

    def event_transaction_created(self, event):
        """
        Add your code here
        Don't forget to set the processed_flag when done
        """
        event.processed_flag=True
        event.save()

    def _fetch_transaction(self, event):
        post = {
            'pos': settings.SALEBOX['API']['KEY'],
            'license': settings.SALEBOX['API']['LICENSE'],
            'platform_type': 'ECOMMERCE',
            'platform_version': '0.1.6',
            'pos_guid': event.transaction_guid
        }

        # do request
        url = '%s/api/pos/v2/transaction/fetch' % settings.SALEBOX['API']['URL']
        try:
            r = requests.post(url, data=post)
            return r.json()['transaction']
        except:
            return None

    # optional: for use with django-mail-queue
    def _mailqueue(self, to_address, subject, content, html=None, cc=None, bcc=None, from_address=None):
        try:
            MailerMessage
        except:
            return

        # from address
        if from_address is None:
            from_address = settings.DEFAULT_FROM_EMAIL

        # create message
        msg = MailerMessage()
        msg.from_address = from_address
        msg.subject = subject
        msg.to_address = to_address
        msg.content = content
        msg.app = 'Salebox'

        # optional extras
        if html is not None:
            msg.html_content = html
        if cc is not None:
            msg.cc_address = cc
        if bcc is not None:
            msg.bcc_address = bcc

        # save in queue
        msg.save()