import os
import array
import oracledb
from generate_embeddings import generate_embeddings
WALLET_PATH = "/Users/sadanandupase/PycharmProjects/23AI"

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
# documents = [
#     {"title" : "Customer languages","content": "Customers from Mumbai tend to speak in marathi or hindi. while customers from Delhi are mainly speaking in Hindi"}, 
#     {"title": "Customer complaints", "content" : "There are more complaints by people from Delhi"},
#     {"title": "Customer Occupation", "content": "Customers from Mumbai are having mixed occupation like salary and business while Delhi customers tend to have business as primary source of income"},
#     {"title": "Customer Gender", "content": "There are more female customers in mumbai while delhi has more male customers"} ]

documents = [
    {
        "title": "Payment Failure - Manoj",
        "content": "Customer reported failed transaction on the app using UPI. Tried twice; both times app timed out. Asked for status via support in Hindi. Seemed frustrated but calm."
    },
    {
        "title": "Service Language Preference - Manoj",
        "content": "Customer prefers communication in Marathi. Asked if support is available in Marathi for future interactions. Also wanted product labels in local language."
    },
    {
        "title": "Incorrect Item - Andres",
        "content": "Customer received wrong model of headphones. Instead of X2000, he got X1000. Called in Spanish, mentioned urgency and need for replacement before weekend trip."
    },
    {
        "title": "Refund Delay - Andres",
        "content": "Customer mentioned refund for incorrect product hasn’t arrived after 8 days. He sounded patient but disappointed."
    },
    {
        "title": "App Navigation Issues - Bala",
        "content": "Customer found app too cluttered. Buttons too small on older Android device. Preferred navigating in Tamil. Suggested cleaner interface."
    },
    {
        "title": "Feedback on Support - Bala",
        "content": "Happy with how fast support responded in Tamil. Requested a feedback form in local language. Appreciated agent’s patience."
    },
    {
        "title": "Delivery Feedback - Gabriela",
        "content": "Pleased with early delivery. Called to confirm whether product was shipped from Guadalajara warehouse. Suggested Spanish packaging."
    },
    {
        "title": "Language Barrier - Gabriela",
        "content": "Asked if documentation is available in Spanish. Found current guide only in English and hard to understand. Support promised to follow up."
    },
    {
        "title": "UX Complaint - Andy",
        "content": "Customer said dark mode causes contrast issues in new update. Also found keyboard navigation broken in desktop view. Suggested rollback."
    },
    {
        "title": "Subscription Issue - Andy",
        "content": "Renewal failed due to bank redirect error. Called support who fixed it. Appreciated the quick fix but wants a retry button next time."
    },
    {
        "title": "Refund Delay - Geetha",
        "content": "Refund request pending over 15 days. Agent said escalation in progress. Geetha was upset; wants faster processing. Mentioned legal route if delay persists."
    },
    {
        "title": "Voice Recognition Glitch - Geetha",
        "content": "Support call to voice assistant failed to pick up Malayalam phrases. Requested fix to multilingual support in IVR. Switched to English to continue."
    }
]

for each_record in documents:
    title = each_record["title"]
    content = each_record["content"]

    # embeddings = generate_embeddings(content)
    # if embeddings:
    #     emb_list = embeddings.embeddings[0]
    # else:
    #     emb_list = []
    # 
    # if emb_list:
    print("Inserting embeddings")
    # Convert to Python array for upload
    #vec = array.array("f", emb_list)
    sql = """
    INSERT INTO documents (title, content, embedding)
VALUES (:title, :content,
    VECTOR_EMBEDDING(ALL_MINILM_L12_V2 USING :content AS data))
    """
    cursor.execute(
        sql,
        {"title": title, "content": content}
    )
    conn.commit()
cursor.close()
conn.close()
print("done")
