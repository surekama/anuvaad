#!/bin/python
import codecs
import logging
import os
import traceback

import numpy as np
import datetime as dt
from scipy.spatial import distance
from utilities.alignmentutils import AlignmentUtils
from repository.alignmentrepository import AlignmentRepository
from validator.alignmentvalidator import AlignmentValidator
from kafkawrapper.alignmentproducer import Producer

log = logging.getLogger('file')

alignmentutils = AlignmentUtils()
repo = AlignmentRepository()
producer = Producer()
util = AlignmentUtils()
validator = AlignmentValidator()

anu_dp_wf_aligner_out_topic = "anuvaad-dp-tools-aligner-output-new"



class AlignWflowService:
    def __init__(self):
        pass


    # Wrapper to build response compatibile with the anuvaad etl wf manager
    def getwfresponse(self, result, object_in, error):
        if error is not None:
            wfresponse = {"taskID": object_in["taskID"], "jobID": object_in["jobID"], "workflowCode": object_in["workflowCode"],
                      "stepOrder": object_in["stepOrder"], "status": "FAILED", "state": "SENTENCES-ALIGNED", "error": error}
        else:
            wfresponse = {"taskID": object_in["taskID"], "jobID": object_in["jobID"], "input": result["input"],
                          "output": result["output"], "workflowCode": object_in["workflowCode"],
                          "stepOrder": object_in["stepOrder"], "status": "SUCCESS", "state": "SENTENCES-ALIGNED",
                          "taskStartTime": result["startTime"], "taskEndTime": result["endTime"]}

        return wfresponse


    def update_wflow_details(self, result, object_in, error):
        wf_res = self.getwfresponse(result, object_in, error)
        producer.push_to_queue(wf_res, anu_dp_wf_aligner_out_topic)