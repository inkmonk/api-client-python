from openpyxl import load_workbook
import sys
import inkmonk
from toolspy import subdict


def load_recipients_from_xls(xlbook):
    wb = load_workbook(filename=xlbook)
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
    for size, contents in skus.items():
        if isinstance(contents, tuple):
            recipients1 = recipients[size][:len(recipients[size]) / 2]
            recipients2 = recipients[size][len(recipients[size]) / 2:]
            ships = inkmonk.Shipment.create_all(
                contents=contents[0], recipients=recipients1)
            ships += inkmonk.Shipment.create_all(
                contents=contents[1], recipients=recipients2)
        else:
            ships = inkmonk.Shipment.create_all(
                contents=contents, recipients=recipients[size])
        shipments += ships
    return shipments


if __name__ == '__main__':
    recipients = load_recipients_from_xls(sys.argv[1])
    key = sys.argv[2]
    secret = sys.argv[3]
    skus = {
        'S': [['U326-SNCKDWN-VSTIK-TS-RNE-PC-PLYCTT9AA-GRA-S-INCH', 1],
              ['U326-CDCHFLGOSTCKR-V14-ST-DCU-2.5X2.B76-OP-2.5X2.5-INCH', 1],
              ['U326-LNGLGOSTCKR-V14-ST-DCU-1.5X5DE77-OP-1.5X5-INCH', 1],
              ['U326-NMSKU-SNACKDOWNBADGE', 1]],

        'M': [['U326-SNCKDWN-VSTIK-TS-RNE-PC-PLYCTT9AA-GRA-M-INCH', 1],
              ['U326-CDCHFLGOSTCKR-V14-ST-DCU-2.5X2.B76-OP-2.5X2.5-INCH', 1],
              ['U326-LNGLGOSTCKR-V14-ST-DCU-1.5X5DE77-OP-1.5X5-INCH', 1],
              ['U326-NMSKU-SNACKDOWNBADGE', 1]],

        'L': [['U326-SNCKDWN-VSTIK-TS-RNE-PC-PLYCTT9AA-GRA-L-INCH', 1],
              ['U326-RFRECHFSTCKR-V14-ST-DCU-2.5X2.B76-OP-2.5X2.5-INCH', 1],
              ['U326-PRTECHFSTCKR-V14-ST-DCU-3X3D-C7FC-OP-3X3-INCH', 1],
              ['U326-NMSKU-SNACKDOWNBADGE', 1]],

        'XL': (
            [['U326-SNCKDWN-VSTIK-TS-RNE-PC-PLYCTT9AA-GRA-XL-INCH', 1],
             ['U326-SPRHROCHFSTCKR-V14-ST-DCU-2.5X2.B76-OP-2.5X2.5-INCH', 1],
             ['U326-CDCHFLGOSTCKR-V14-ST-DCU-2.5X2.B76-OP-2.5X2.5-INCH', 1],
             ['U326-NMSKU-SNACKDOWNBADGE', 1]],

            [['U326-SNCKDWN-VSTIK-TS-RNE-PC-PLYCTT9AA-GRA-XL-INCH', 1],
             ['U326-SPRHROCHFSTCKR-V14-ST-DCU-2.5X2.B76-OP-2.5X2.5-INCH', 1],
             ['U326-RFRECHFSTCKR-V14-ST-DCU-2.5X2.B76-OP-2.5X2.5-INCH', 1],
             ['U326-NMSKU-SNACKDOWNBADGE', 1]]
        ),

        'XXL': [['U326-SNCKDWN-VSTIK-TS-RNE-PC-PLYCTT9AA-GRA-XXL-INCH', 1],
                ['U326-SPRHROCHFSTCKR-V14-ST-DCU-2.5X2.B76-OP-2.5X2.5-INCH', 1],
                ['U326-PRTECHFSTCKR-V14-ST-DCU-3X3D-C7FC-OP-3X3-INCH', 1],
                ['U326-NMSKU-SNACKDOWNBADGE', 1]],

        'XXXL': [['U326-SNCKDWN-VSTIK-TS-RNE-PC-PLYCTT9AA-GRA-XXXL-INCH', 1],
                 ['U326-SPRHROCHFSTCKR-V14-ST-DCU-2.5X2.B76-OP-2.5X2.5-INCH', 1],
                 ['U326-PRTECHFSTCKR-V14-ST-DCU-3X3D-C7FC-OP-3X3-INCH', 1],
                 ['U326-NMSKU-SNACKDOWNBADGE', 1]]
    }
    shipments = create_shipments(
        skus=skus, recipients=recipients, key=key, secret=secret)
    print "Read %s rows from the sheet" % sum(
        len(v) for v in recipients.values())
    print "Split up to send"
    print "Found %s valid entries for shipments" % sum(
        len(v) for v in subdict(recipients, skus.keys()).values())
    print "Created following %s shipments:" % len(shipments)
    print shipments
