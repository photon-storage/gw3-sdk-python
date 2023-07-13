import gw3

client = gw3.GW3Client(
    "YOUR-ACCESS-KEY",
    "YOUR-ACCESS-SECRET",
)

data = "EThe Times 03/Jan/2009 Chancellor on brink of second bailout for banks"

# Post the data to the IPFS network, receiving a CID as a result
cid = client.upload(data.encode())
print(f"Data posted to IPFS network, CID is: {cid}")

# Create a new IPNS record and bind it to a CID.
ipns = client.create_ipns(cid)
print(f"IPNS is: {ipns}")

# Update the IPNS record to a new CID.
new_cid = "QmNYERzV2LfD2kkfahtfv44ocHzEFK1sLBaE7zdcYT2GAZ"
client.update_ipns(ipns, new_cid)
print("update IPNS success!")