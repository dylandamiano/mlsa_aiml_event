from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.storage.blob import BlobServiceClient
import getpass

# Initialize the Document Intelligence Client
# Initialize the Blob Client
# |--> The Blob Client is going to allow us to upload content if needed, which can be retrieved later on by the Document Intelligence Client
# |--> The Document Intelligence Client is going to allow us to analyze the content that we uploaded to the Blob Storage
 
doc_client: DocumentIntelligenceClient = DocumentIntelligenceClient()
blob_client: BlobServiceClient = BlobServiceClient()