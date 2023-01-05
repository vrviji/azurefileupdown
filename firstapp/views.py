from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
import os
# Create your views here.
def index(request):
    
    if request.POST.get('upload') and request.method == "POST":
        
        fn = request.POST.get('filename')
        
        
        uploadblob(fn)
        return render(request,"index.html")
    elif request.POST.get('download') and request.method == "POST":
        downblob()
        print("download")
        return render(request,"index.html")
    else:
        return render(request,"index.html")
def downblob():    
    import os
    import uuid
    
    # Import the client object from the SDK library
   
    from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
    conn_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]

    # Create the client object for the resource identified by the connection
    # string, indicating also the blob container and the name of the specific
    # blob we want.
    blob_service_client = BlobServiceClient.from_connection_string(
        conn_string,
        container_name="blobcontainer2"
        
    )

  
    
    # Download the blob to a local file
    # Add 'DOWNLOAD' before the .txt extension so you can see both files in the data directory
    download_file_path = os.path.join(settings.BASE_DIR, 'DOWNLOAD.txt')
    container_client = blob_service_client.get_container_client(container="blobcontainer2") 
    print("\nDownloading blob to \n\t" + download_file_path)
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)

    with open(file=download_file_path, mode="wb") as download_file:
        download_file.write(container_client.download_blob(blob.name).readall())
    print("Downlaoded")

  
        
def uploadblob(fn):
    import os
    import uuid
    
    # Import the client object from the SDK library
    from azure.storage.blob import BlobClient

    # Retrieve the connection string from an environment variable. Note that a
    # connection string grants all permissions to the caller, making it less
    # secure than obtaining a BlobClient object using credentials.
    conn_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]

    # Create the client object for the resource identified by the connection
    # string, indicating also the blob container and the name of the specific
    # blob we want.
    blob_client = BlobClient.from_connection_string(
        conn_string,
        container_name="blobcontainer2",
        blob_name=f"sample-blob-{str(uuid.uuid4())[0:5]}.txt",
    )

    # Open a local file and upload its contents to Blob Storage
    with open(fn, "rb") as data:
        blob_client.upload_blob(data)
        print(f"Uploaded file to {blob_client.url}")
     