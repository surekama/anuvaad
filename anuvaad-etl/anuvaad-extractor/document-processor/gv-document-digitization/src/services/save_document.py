import requests
from config import SAVE_URL, SAVE_NO_PAGE
import src.utilities.app_context as app_context
from flask.json import jsonify
import copy 
from anuvaad_auditor.loghandler import log_info
from anuvaad_auditor.loghandler import log_exception

# token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6ImphaW55LmpveUB0YXJlbnRvLmNvbSIsInBhc3N3b3JkIjoiYickMmIkMTIkcXFjYUM2WW5yU2RFM2hDT2h4aXpnT0ZILjBxeFR4UWJBTHloZDFjTjBFOWluSnRqaTguOWknIiwiZXhwIjoxNjE2NTcxMjM3fQ.vCOncRM7BNK0qsv0OWnioIDfy-lOusTcMERsusm_ics"
# headers = {'auth-token' :token }
def save_page_res(res,file_name):
    try:
        tmp_file = copy.deepcopy(res['rsp'])
        del tmp_file['input']
        tmp_file['files'] =  res['rsp']['outputs']
        del tmp_file['outputs']
        json_file_name = file_name['output'][0]['outputFile']
        for file in [tmp_file]:
            recordID = file['jobID']+'|'+json_file_name
            page_idx = 0
            total_pages = len(file['files'][0]['pages'])
            file['files'][0]['config']   = copy.deepcopy(file['files'][0]['config']['OCR'])
            while page_idx<total_pages:
                
                save_file = copy.deepcopy(file)
                pages = file['files'][0]['pages'][page_idx:page_idx+SAVE_NO_PAGE]
                save_file['files'][0]['pages'] = pages
                save_file['recordID'] = recordID
                page_idx = page_idx+SAVE_NO_PAGE
                rsp = requests.post(SAVE_URL,json=save_file)
                log_info("successfully saved data to database with record id: "+str(recordID+str(rsp)),save_file)
    except Exception as e:
        log_exception("Error occured during saving page response",  app_context.application_context, e)
        
            
        
            




    
    