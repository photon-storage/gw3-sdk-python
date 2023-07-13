import gw3

client = gw3.GW3Client(
    "YOUR-ACCESS-KEY",
    "YOUR-ACCESS-SECRET",
)

# Create a new DAG by appending /example.txt
data = "EThe Times 03/Jan/2009 Chancellor on brink of second bailout for banks"

cid = client.dag_add(gw3.EMPTY_DAG_ROOT, "/example.txt", data.encode())
print(f"Created a new DAG, CID is: {cid}")

cid = client.dag_rm(cid, "/example.txt")
print(f"Removed the /example.txt, CID is: {cid}")
