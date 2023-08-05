from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from urllib.parse import quote
from urllib.parse import urlencode
from datetime import datetime, timedelta
import requests


class GradCafeScraper(object):

    def query_dict(self):
        return {'q': self.college+' '+self.course, 'pp': self.page_limit}
    
    def url_endpoint(self):
        return 'https://www.thegradcafe.com/survey/index.php'

    def calculate_decision(self, decision_str):
        if 'Accepted' in decision_str:
            return True
        elif 'Rejected' in decision_str:
            return False
        else:
            return None
    
    def __init__(self, college,course, phd=False):
        self.college = college
        self.course = course
        self.phd = phd
        self.page_limit = 250
        
    def scrape_data(self):
        resp = requests.get(self.url_endpoint(), params=self.query_dict())
        soup = BeautifulSoup(resp.text, 'html.parser')
        self.table = soup.findAll(True, {'class':['row0', 'row1']})
    
    def prune_data_logic(self, untill_date):
        row_data = {}
        last_date = None
        for row in self.table:
            university_name = row.find_all(True, {'class':['instcol']})[0].getText()
            program_name = row.find_all(True, {'class':['tcol2']})[0].getText()
            decision = self.calculate_decision(row.find_all(True, {'class':['tcol3']})[0].getText())
            date = row.find_all(True, {'class':['tcol5']})[0].getText()
            date = datetime.strptime(date, '%d %b %Y')
            if self.college not in university_name:
                continue
            if self.phd == False:
                if "PhD" in program_name:
                    continue
            if self.phd == True:
                if "PhD" not in program_name:
                    continue
            if self.course not in program_name:
                continue
            if decision == None:
                continue
            if date<untill_date:
                break
            if self.phd == True:
                program_name = 'PhD in {0}'.format(self.course)
            else:
                program_name = 'Masters in {0}'.format(self.course)
            university_name = self.college
            if (university_name, program_name) in row_data:
                if decision == True:
                    row_data[(university_name, program_name)]['accept']+=1
                else:
                    row_data[(university_name, program_name)]['reject']+=1
            else:
                row_data[(university_name, program_name)] = {
                    'accept': 0,
                    'reject': 0
                }
                if decision == True:
                    row_data[(university_name, program_name)]['accept'] = 1
                else:
                    row_data[(university_name, program_name)]['reject'] = 1
            last_date=date
        return {
            'data': row_data,
            'last_date': last_date
        }
    
    def prune_data(self, date):
        self.scrape_data()
        return self.prune_data_logic(date)