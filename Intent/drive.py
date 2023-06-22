from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

folder = "0BwGyIFDgxKAwfjdnRXgxbDhVMUhJZnBYclRrYlRGNC1oTU9hSFlmNGg3SEVoUFZ5QUZQRVk"

file1 = drive.CreateFile({"parents": [{"id": folder}], "title":"hello.txt"})
file1.SetContentString("Hello World")
file1.Upload()