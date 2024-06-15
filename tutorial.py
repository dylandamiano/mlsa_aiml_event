# ***************************************************** #
# |-> Azure Dependencies
from azure.ai.documentintelligence import \
    DocumentIntelligenceClient
from azure.ai.documentintelligence.models import \
    AnalyzeDocumentRequest
from azure.storage.blob import \
    BlobServiceClient
from azure.core.credentials import \
    AzureKeyCredential

# ***************************************************** #
# |-> OpenAI Dependencies
from openai import OpenAI

# ***************************************************** #
# |-> Other Dependencies
import toml
import time

# ***************************************************** #

_ENV = toml.load(".\\keys.toml")

# Initialize the Document Intelligence Client
# Initialize the Blob Client
# |--> The Blob Client is going to allow us to upload content if needed, which can be retrieved later on by the Document Intelligence Client
# |--> The Document Intelligence Client is going to allow us to analyze the content that we uploaded to the Blob Storage
 
doc_client: DocumentIntelligenceClient = DocumentIntelligenceClient(
    endpoint=_ENV["DOC_INTEL_SERVICE"]["URL"],
    credential=AzureKeyCredential(_ENV["DOC_INTEL_SERVICE"]["KEY"])
)

blob_client = BlobServiceClient(
    account_url=_ENV["AI_BLOB_SERVICE"]["URL"], 
    credential=_ENV["AI_BLOB_SERVICE"]["KEY"]
)

oai_client: OpenAI = OpenAI(api_key=_ENV["OPENAI_PLATFORM"]["KEY"])

# ***************************************************** #
# |-> The following code is going to allow us to upload a file to the Blob Storage
# |-> This will also allow us to retrieve content from a file that we have uploaded, which we are going to try to use the content from to reconstruct it using ChatGPT-4o

container_client = blob_client.get_container_client(_ENV["AI_BLOB_SERVICE"]["CONTAINERS"][0])
f_name = f".\\sample_documents{time.time()}.pdf"

container_client.upload_blob(name=f_name, data=open(".\\sample_documents\\cloduskills.png", "rb"))
bytes_source=blob_client.get_blob_client(_ENV["AI_BLOB_SERVICE"]["CONTAINERS"][0], f_name).download_blob().content_as_bytes()
res = doc_client.begin_analyze_document(
        "prebuilt-read", 
        AnalyzeDocumentRequest(bytes_source=bytes_source)
    ).result()

reconstruct_query = [x["content"]+"\n" for x in res["paragraphs"]]
reconstruct_query = str('').join(reconstruct_query)

# ***************************************************** #
# -> Establish a conversation with ChatGPT-4o to reconstruct the content of the file
returned = oai_client.chat.completions.create(
        messages=[
            {"role": "system", "content": f"You help me reconstruct information given missing pieces."},
            {"role": "user", "content": f"Help me recover as much lost detail from the file provided and RETURN AS HTML: " + reconstruct_query}
        ],
        model="gpt-4o"
    )

with open(f"{time.time()}.html", 'w') as f:
       f.write(returned.choices[0].message.content)
# ***************************************************** #