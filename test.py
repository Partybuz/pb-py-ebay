import datetime
import json
from ebaysdk.exception import ConnectionError
from ebaysdk.trading import Connection as Trading

print("started")

try:
    api = Trading(domain='api.ebay.com', config_file='ebay.yaml')
    response = api.execute('GetSellerList',{'IncludeVariations':"true",'EndTimeFrom':datetime.datetime.today(),'EndTimeTo':datetime.datetime.now()+datetime.timedelta(days=120)})

    file = open("latest_response.json", "w")
    print(json.dumps(response.dict(), indent=4), file=file)

    ItemsOut = {}

    for Item in response.reply.ItemArray.Item:
        ItemResponse = api.execute('GetItem',{'ItemID':Item.ItemID})
        ItemsOut[Item.ItemID] = ItemResponse.dict()

    outfile = open("output.json", "w")
    print(json.dumps(ItemsOut, indent=4), file=outfile)

    assert(response.reply.Ack == 'Success')
    assert(type(response.reply.Timestamp) == datetime.datetime)
    # assert(type(response.searchResult.item) == list)

    # item = response.reply.searchResult.item[0]
    # assert(type(item.listingInfo.endTime) == datetime.datetime)
    assert(type(response.dict()) == dict)
    print(response.dict())
    print(response.reply)


except ConnectionError as e:
    print(e)
    print(e.response.dict())