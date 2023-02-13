# Introduction
This is a demo repository in that:
- device output on a local computer is simulated by a script that generates random 32x32 px black-and-white images.
- a Python (PySpark) script that uses functionality of Spark Structured Streaming detects newly generated images and transfers these to an Azure Blob Storage.
- an Azure Function is implemented that monitors above Azure Blob Storage and upon arrival of new images calculates the total sum of pixel values in each image (think of this as a dummy surrogate for performing some form of prediction on these images) and then writes this value to an Azure SQL database 


# Set up environment
- Set up a Python environment with the packages specified in the file "requirements.txt". I am running this example using Python 3.9.16. In order for PySpark to work properly, you might need to download the file "hadoop.dll" (available here: https://github.com/cdarlint/winutils/blob/master/hadoop-3.2.2/bin/hadoop.dll) and place it into your C:\Windows\System32 folder. In order for PyODBC to work, you might also need to install the needed ODBC driver (see https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16).


# Set up of Azure resources
- Blob storage:
    - First, we create a Azure Storage Account as shown in the screenshots below. Essentially, we just make the storage account non-public and leave everything else to Azure's default options:
<img src="./documentation/azure_storage_1.png" width=65% style="display: block; margin: 0 auto" /> </br>
<img src="./documentation/azure_storage_2.png" width=65% style="display: block; margin: 0 auto" />
    - After creation of our storage account, we create a container called "img".
<img src="./documentation/azure_storage_3.png" width=65% style="display: block; margin: 0 auto" />
    - In our credentials folder, to the credentials.py file we add the variables: <code> storage_account_name = "mydemonstrationstorage" </code> and <code> storage_container_name = "img" </code>.
    - Furthermore, we will store our the access key of our storage account to a variable <code> storage_access_key </code>. See the image below to learn where you can find your access key. Note that it is bad practice to store secrets in code. Because this is just a quick demonstration, we will do so anyways.
<img src="./documentation/azure_storage_4.png" width=65% style="display: block; margin: 0 auto" />

- SQL database
    - Create a SQL database as shown in the screenshots below. Make sure to change the expensive default database (under "Compute + storage" -> "Configure database") to a cheaper one. I use the basic option of the DTU-based pricing model here. Use SQL authentication as shown in the screenshot, set and remember your admin password. You will need it in the next step.
<img src="./documentation/azure_db_1.png" width=65% style="display: block; margin: 0 auto" /> </br>
<img src="./documentation/azure_db_2.png" width=65% style="display: block; margin: 0 auto" />
    - Find the ODBC connection string of your database (see below). Set it as variable <code> db_connection_str </code> in your ./credentials/credentials.py file. Make sure to substitute the placeholder in the "Pwd={your_password_here}" part with the password you set in the step before.
<img src="./documentation/azure_db_3.png" width=65% style="display: block; margin: 0 auto" />
    - In the networking tab of your database resource, allow access from selected networks. Add your client IPv4 address to the firewall exceptions and check the "Allow Azure services and resources to access this server" option and save:
<img src="./documentation/azure_db_4.png" width=65% style="display: block; margin: 0 auto" />
    - Initialize the database by running the "initialize_db.py" script.

- Azure Functions:

# Action
- Run your "stream_local_files_to_azure_blob_storage.py" script. You might also consider to schedule execution of this script automatically on start up using the Windows Task Scheduler. 
- Then, start your "generate_device_output.py" script.
- That's more or less it. Everything else you should know work as envisioned in the introduction. Query your database to see the final result.
