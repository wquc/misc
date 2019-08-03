import os
import sys
import time
from random import randint
from selenium import webdriver

### Modify the path of driver and e-mail address
driver_path = 'path_to_driver/chromedriver'
user_email  = 'username@mailname.com' 

### Do not modify the following unless server changed website
MMTSB_URL     = 'https://mmtsb.org/webservices/gomodel.html'

for i in range(9):
    pdbname = '%dubq'%(i+1)    # frame name without .pdb extensions
    waitime = randint(60, 120) # waiting time in seconds before submissions
    sys.stdout.write('> Processing %s ...\n'%pdbname)
    driver = webdriver.Chrome(driver_path)
    driver.get(MMTSB_URL)
    driver.find_element_by_name("pdbfile").send_keys(os.getcwd()+"/pdbsrc/%s.pdb"%pdbname)
    driver.find_element_by_name("tag").send_keys(pdbname)         #^^^^^^ all pdb files in this folder
    driver.find_element_by_name("email").send_keys(user_email)
    driver.find_element_by_css_selector("input[type='submit']").click()
    driver.close()
    ### time countdown
    for wt in reversed(range(waitime)):
        sys.stdout.write('\r> Next submission in %d seconds'%wt)
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write('\n')
