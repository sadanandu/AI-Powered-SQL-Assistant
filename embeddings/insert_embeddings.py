import os
import array
import oracledb
from generate_embeddings import generate_embeddings
WALLET_PATH = os.path.dirname(os.path.abspath(__file__))

# TNS name of your service from tnsnames.ora (usually ends with _high, _low, or _tp)
SERVICE_NAME = "m04vxfqnjt7h6fh0_high"

# Credentials from OCI when setting up DB user
DB_USER = "admin"
DB_PASSWORD = "Welcome_123#"

# Initialize thin mode with wallet
#oracledb.init_oracle_client(lib_dir=None)  # Set lib_dir only for thick mode; None enables thin mode
#oracledb.init_oracle_client(lib_dir=None)  # Set lib_dir only for thick mode; None enables thin mode

conn = oracledb.connect(
    user=DB_USER,
    password=DB_PASSWORD,
    dsn=f"{SERVICE_NAME}",
    config_dir=WALLET_PATH,
    wallet_location=WALLET_PATH,
    wallet_password=None  # Only needed if you set a wallet password
)

print("Connected to Oracle Autonomous Database.")

cursor = conn.cursor()

# Sample record
documents = [{"title" : "Customer languages",
"content": "Customers from Mumbai tend to speak in marathi or hindi. while customers from Delhi are mainly speaking in Hindi"
}, {"title": "Customer complaints", "content" : "There are more complains by people from Delhi"},
            {"title": "Customer Occupation", "content": "Customers from Mumbai are having mixed occupation like salary and business while Delhi customers tend to have business as primary source of income"}]

for each_record in documents:
    title = each_record["title"]
    content = each_record["content"]

    embeddings = generate_embeddings(content)
    if embeddings:
        emb_list = embeddings.embeddings[0]
    else:
        emb_list = []
    
    if emb_list:
        print("Inserting embeddings")
        # Convert to Python array for upload
        vec = array.array("f", emb_list)
        
        cursor.execute(
            "INSERT INTO documents (title, content, embedding) VALUES (:1, :2, :3)",
            [title, content, vec]
        )
        
        conn.commit()
cursor.close()
conn.close()
print("done")
