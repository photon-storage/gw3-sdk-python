import gw3

client = gw3.GW3Client(
    "YOUR-ACCESS-KEY",
    "YOUR-ACCESS-SECRET",
)

data = b"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"

# Post the data to the IPFS network, receiving a CID as a result
cid = client.upload(data)
print(f"Data posted to IPFS network, CID is: {cid}")

# Request the gateway to pin the CID data, ensuring its persistence
client.pin(cid)
print("CID data is pinned by the Gateway3")

# Retrieve the data from the IPFS network using the CID
got = client.get_ipfs(cid)
print(f"Data retrieved from IPFS network: {got.decode()}")