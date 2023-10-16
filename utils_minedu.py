import pandas as pd
import pdb
import pandas as pd
from shareplum import Site
from shareplum import Office365
from shareplum.site import Version
from io import BytesIO

def loadShareFile(pathfolder, filename, username, password, url, path):
    authcookie = Office365(url, username=username, password=password).GetCookies()
    site = Site(path, version=Version.v365, authcookie=authcookie)
    folder = site.Folder(pathfolder)  
    return folder.get_file(filename)

def _get_file_XLSX(pathfolder, file, sheet_name,  url, path, username, password, header=[0]):
    df = pd.read_excel(BytesIO(loadShareFile(pathfolder=pathfolder, filename=file, url=url, path=path, username=username, password=password)), sheet_name=sheet_name, dtype='str', header=header)
    return df