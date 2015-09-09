from openpyxl import load_workbook
import sys
import inkmonk
from toolspy import subdict


def load_recipients_from_xls(xlbook):
    wb = load_workbook(filename=sys.argv[1])
    ws = wb.worksheets[0]

    result = {}

    for row in ws.rows[1:]:
        recipient = {
            'name': row[1].value,
            'contact_number': row[2].value,
            'address1': row[5].value,
            'city': row[6].value,
            'pincode': row[7].value,
            'country': row[8].value
        }
        size = row[4].value
        if size in result:
            result[size].append(recipient)
        else:
            result[size] = [recipient]
    return result


def create_shipments(skus=[], recipients={}, key=None, secret=None):
    inkmonk.configure(key=key, secret=secret)
    shipments = []
    for size, sku in skus.items():
        ships = inkmonk.Shipment.create_all(
            contents=[[sku, 1]], recipients=recipients[size])
        shipments += ships
    return shipments


if __name__ == '__main__':
    recipients = load_recipients_from_xls(sys.argv[1])
    key = sys.argv[2]
    secret = sys.argv[3]
    skus = {
        'S': 'U7-AVNGRS-VSTIK-TS-RNE-CO-TRLPRC4FE-GRA-S-STD',
        'M': 'U7-AVNGRS-VSTIK-TS-RNE-CO-TRLPRC4FE-GRA-M-STD',
        'L': 'U7-AVNGRS-VSTIK-TS-RNE-CO-TRLPRC4FE-GRA-L-STD',
        'XL': 'U7-AVNGRS-VSTIK-TS-RNE-CO-TRLPRC4FE-GRA-XL-STD',
        'XXL': 'U7-AVNGRS-VSTIK-TS-RNE-CO-TRLPRC4FE-GRA-XXL-STD'
    }
    shipments = create_shipments(
        skus=skus, recipients=recipients, key=key, secret=secret)
    print "Read %s rows from the sheet" % sum(
        len(v) for v in recipients.values())
    print "Found %s valid entries for shipments" % sum(
        len(v) for v in subdict(recipients, skus.keys()).values())
    print "Created following %s shipments:" % len(shipments)
    print shipments
