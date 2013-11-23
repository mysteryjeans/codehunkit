"""
CodeHunkit app classes
@author: faraz@fanaticlab.com
@copyright: Copyright (c) 2013 FanaticLab
"""

class CodeHunkitError(Exception):    
    def __init__(self, message):                
        self.message = message