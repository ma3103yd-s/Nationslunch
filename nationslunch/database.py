import gspread
from gspread import Client
import json
from authlib.client import AssertionSession

FILENAME = 'c:/users/markus/desktop/projects/nationslunch/spider/nationslunchspider/output/images.jl'

class MyClient(Client):
    scopes = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive',
            ]

    def __init__(self, file):
        session = self.create_assertion_session(file, MyClient.scopes)
        Client.__init__(self,None,session)


    def create_assertion_session(self,conf_file, scopes, subject=None):
        with open(conf_file, 'r') as f:
            conf = json.load(f)

        token_url = conf['token_uri']
        issuer = conf['client_email']
        key = conf['private_key']
        key_id = conf.get('private_key_id')

        header = {'alg': 'RS256'}
        if key_id:
            header['kid'] = key_id

        claims = {'scope': ' '.join(scopes)}
        return AssertionSession(
            grant_type=AssertionSession.JWT_BEARER_GRANT_TYPE,
            token_url=token_url,
            issuer=issuer,
            audience=token_url,
            claims=claims,
            subject=subject,
            key=key,
            header=header,
            )


class Spreadsheet(object):


    def __init__(self, client, name,sheet_nbr):
        self.sheet = client.open(name)
        self.sheets = []
        self.sheets.append(self.sheet.get_worksheet(sheet_nbr))


    def update_sheet(self,sheet_nbr, values):
        index = 1
        for value in values:
            self.sheets[sheet_nbr].update_cell(index,1,value)
            index +=1


    def get_values(self,sheet_nbr):
        sheet = self.sheets[sheet_nbr]
        values = sheet.col_values(1).remove('URL')
        return values

    def add_sheet(self):
        self.sheets.append(self.sheet.get_worksheet(len(self.sheets)))
