import threetaps

client = threetaps.Threetaps('93be912480aa733d0d19bcb25a1563579cec89177c002b9566cb8921a7a992c2ef58f914d54423dbb4e0e191d0218facc3677f17620fa6e40ef048360469a257')

client.reference.sources()
client.reference.locations()
client.search.search(params={'location.city': 'CAN-YUL'})