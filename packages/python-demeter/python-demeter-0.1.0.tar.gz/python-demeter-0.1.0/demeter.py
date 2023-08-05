import io

from oauth2client import file, client, tools
from apiclient import discovery, http

SCOPES = 'https://www.googleapis.com/auth/drive'

class Demeter(object):

    def __init__(self, credentials, client_secret):
        self.credentials = self._authorize(credentials, client_secret)
        self.service = self._build_service()
        self.files = self.service.files()

    def _authorize(self, credentials, client_secret):
        store = file.Storage(credentials)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(client_secret, SCOPES)
            credentials = tools.run_flow(flow, store)
        return credentials

    def _build_service(self):
        service = discovery.build('drive', 'v3', credentials=self.credentials)
        return service

    def get_filelist(self, page_size=100):
        fields = "nextPageToken, files(id, name)"
        results = self.files.list(pageSize=page_size, fields=fields).execute()
        items = results.get('files', [])
        if not items:
            return None
        return items

    def download_file(self, file_id, file_type, export_path):
        request = self.files.export_media(fileId=file_id, mimeType=file_type)
        fh = io.FileIO(export_path, 'wb')
        downloader = http.MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        return export_path
