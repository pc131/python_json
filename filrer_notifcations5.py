from re import I
import os
import shutil

script_path = 'c:\\Users\\skocz\\Desktop\\CGI\\source\\' # root folder for script and JSON file

ORID = '2000097391C01' # ORID to look for
filename = 'TC-TRANSFER-PH3-ORID-2000097391C01-ORID.json' # file with JSON messages from HUB

f1_file = script_path + filename # source file to work on

filename_no_ext = filename.replace('.json', '') # get filename without extension
f1 = open(f1_file, 'r') # open source file
f1_content= f1.read() #r ead source file into

requests_start = f1_content.find('Request:') # find where Requests (with Reponses) start in the source file
requests_end = f1_content.find('Peek Message:') # find where Requests (with Reponses) end in the source file

requests = f1_content[requests_start:requests_end] # assign all Requests (with Reponses) to string variable requests
peeked_notifications = f1_content[requests_end:] # assign all Peeked Notifications to string variable peeked_notifications, Peeked Notifications start where Requests end and are until end of suorce file

ORID1_start = requests.find('"ORID": "') + 9 # look for ORID in first accepted Request
ORID1_end = ORID1_start + 13 # assign to ORID1 value of first accepted Request
ORID1 = requests[ORID1_start:ORID1_end] # assign to ORID1 value of first accepted Request

# set destination folder for output files - WORK ON IT!!!!!!!!!!!!!!
dest_folder = script_path  + '\\' + filename_no_ext + ORID + '-ORID' 
print(dest_folder)
if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)
# set destination folder for output files WORK ON IT!!!!!!!!!!!!!!

f2_file = script_path + filename_no_ext + ORID + '-ORID' +  '\\' +filename_no_ext + ORID +  '-ORID_01_RQX_ONLY.json' # file with only Requests
f3_file = script_path + filename_no_ext + ORID + '-ORID' +  '\\' +filename_no_ext + ORID +  '-ORID_02_NTX_ONLY.json' # file with only Notifications
f4_file = script_path + filename_no_ext + ORID + '-ORID' +  '\\' +filename_no_ext + ORID +  '-ORID_03_RQX_NTX.json' # file Requests and Notifications WITHOUT T291.M or just Notifications in case of IF T291.M NOTIFICATIONS FILE
f2 = open(f2_file, 'w')
f3 = open(f3_file, 'w')
f4 = open(f4_file, 'w')

requests_lines = requests.split('\n') # split requests string into requests_lines LIST

requests_trx = [] # python list to keep particular requests

# This code works on requests_lines variable and saves JSON Requests without JSON Responses to FILE2
keep_current_line = False
for line in requests_lines:
    if line.startswith("Request:"):
        keep_current_line = True # save Requests
    elif line.startswith("Response:"):
        keep_current_line = False #skip Reponses
    if keep_current_line:
        #print(line)   
        requests_trx.append(line) # append to requests_trx only JSON Requests
        f2.write(line + '\n') # # write every requests_trx LIST item and add new line to FILE

requests_in_list = [i for i, x in enumerate(requests_trx) if x == "Request:"] # NOT SURE WHAT THIS IS DOING!!!

############################## REQUESTS ########################

# NOT SURE WHAT THIS IS DOING!!!
requests2 = []
for i in range(len(requests_in_list)):

    if i != len(requests_in_list) - 1:
        #append to requests 2 all lines between Requests: lines
        requests2.append(requests_trx[requests_in_list[i]:requests_in_list[i+1]])
    else:
        #for last element look until end of first list     
        requests2.append(requests_trx[requests_in_list[i]:])
# NOT SURE WHAT THIS IS DOING!!!

# trx_list is list of lists, for example:
# [['T321.R', 'ca00a5f088154a9b93bf1a12361d5fd0', 'MOSLTEST-R'],
#  ['T201.W', 'e8e133ca2a364420baf207f0eee39d84', 'MOSLTEST-W'],
#  ['T203.W', 'efe9a9ed0471407895836f7d3955d00b', 'MOSLTEST-W']]
trx_list =[]
for i in range(len(requests2)):
    request_trx = str(requests2[i])

    trx_name_start = request_trx.find('"DataTransaction": "') +  20
    trx_name_end = trx_name_start +  6
    trx_name = request_trx[trx_name_start:trx_name_end]

    orig_ref_start = request_trx.find('"OriginatorsReference": "') +  25
    orig_ref_end = orig_ref_start + 32
    orig_ref = request_trx[orig_ref_start:orig_ref_end]
    
    src_org_id_start = request_trx.find('"TransactionSourceOrgID": "') +  27
    src_org_id_end = request_trx.find('",', src_org_id_start)
    src_org_id = request_trx[src_org_id_start:src_org_id_end]

    trx_list.append([trx_name, orig_ref, src_org_id]) 
# trx_list is list of lists, for example:
# [['T321.R', 'ca00a5f088154a9b93bf1a12361d5fd0', 'MOSLTEST-R'],
#  ['T201.W', 'e8e133ca2a364420baf207f0eee39d84', 'MOSLTEST-W'],
#  ['T203.W', 'efe9a9ed0471407895836f7d3955d00b', 'MOSLTEST-W']]
    # print(trx_name)
    # print(orig_ref)
    # print(src_org_id)
############################## REQUESTS ########################

############################## NOTIFICATIONS ########################

notifications_lines = peeked_notifications.split('\n') # split peeked_notifications string into notifications_lines LIST

# save to FILE3 all Peeked Messages line by line
notifications_trx = []
for line in notifications_lines:
        notifications_trx.append(line) 
        f3.write(line + '\n') # write every notifications_trx LIST item and add new line to FILE
# save to FILE3 all Peeked Messages line by line

# NOT SURE WHAT THIS IS DOING!!!
notifications_in_list = [i for i, x in enumerate(notifications_trx) if x == "Peek Message:"] 
# NOT SURE WHAT THIS IS DOING!!!

# NOT SURE WHAT THIS IS DOING!!!
#list with elements that start with "Peek Message:"
notifications2 = []

for i in range(len(notifications_in_list)):

    if i != len(notifications_in_list) - 1:
        #append to requests 2 all lines between Requests: lines
        notifications2.append(notifications_trx[notifications_in_list[i]:notifications_in_list[i+1]])
    else:
        #for last element look until end of first list     
        notifications2.append(notifications_trx[notifications_in_list[i]:])
# NOT SURE WHAT THIS IS DOING!!!

# ntx_list is list of lists, for example:
# [['T321.M', 'ca00a5f088154a9b93bf1a12361d5fd0', 'MOSLTEST-W'],
#  ['T291.M', 'e8e133ca2a364420baf207f0eee39d84', 'MOSLTEST2-R'],
#  ['T201.M', 'e8e133ca2a364420baf207f0eee39d84', 'MOSLTEST-R'],
#  ['T203.M', 'efe9a9ed0471407895836f7d3955d00b', 'MOSLTEST-R']]
ntx_list = []
for i in range(len(notifications2)):
    notifications_trx = str(notifications2[i])

    if ORID in notifications_trx:

        trx_name_start = notifications_trx.find('"DataTransaction": "') +  20
        trx_name_end = trx_name_start +  6
        trx_name = notifications_trx[trx_name_start:trx_name_end]

        orig_ref_start = notifications_trx.find('"OriginatorsReference": "') +  25
        orig_ref_end = orig_ref_start + 32
        orig_ref = notifications_trx[orig_ref_start:orig_ref_end]

        dest_org_id_start = notifications_trx.find('"TransactionDestinationOrgID": "') +  32
        dest_org_id_end = notifications_trx.find('",', dest_org_id_start)
        dest_org_id = notifications_trx[dest_org_id_start:dest_org_id_end]

        ntx_list.append([trx_name, orig_ref, dest_org_id])
# ntx_list is list of lists, for example:
# [['T321.M', 'ca00a5f088154a9b93bf1a12361d5fd0', 'MOSLTEST-W'],
#  ['T291.M', 'e8e133ca2a364420baf207f0eee39d84', 'MOSLTEST2-R'],
#  ['T201.M', 'e8e133ca2a364420baf207f0eee39d84', 'MOSLTEST-R'],
#  ['T203.M', 'efe9a9ed0471407895836f7d3955d00b', 'MOSLTEST-R']]

################### IF T291.M NOTIFICATIONS FILE, DO NOT MATCH WIHTH REQUESTS, AS THERE ARE DUMMY T207 WITH DUMMY ORID ####   
if any('T291.M' in sublist for sublist in ntx_list):
    #print('found T291 !!!!!!!!!!!!!!!!!!!!!!!!!')
    f4.write('Number of notifications: ' + str(len(ntx_list)) + '\n\n')
    #SORT LIST OF NOTIFICATIONS BY TRANSACTION NAME
    #ntx_list= sorted(ntx_list, key=lambda x: x[0])
    # CUSTOM SORT LIST OF NOTIFICATIONS BY TRANSACTION NAME
    SORT_ORDER = {"T291.M": 0, "T321.M": 1, "T201.M": 2, "T203.M": 3, "T204.M": 4, "T205.M": 2, "T206.M": 3, "T207.M": 4, "T208.M": 5, "T210.M": 6, "T211.M": 7, "T212.M": 8, "T213.M": 9, "T214.M": 10, "T215.M": 11, "T216.M": 12, "T217.M": 13, "218.M": 14}
    ntx_list.sort(key=lambda val: SORT_ORDER[val[0]])
    #SORT LIST OF NOTIFICATIONS BY TRANSACTION NAME
    ntx_count = 0
    for j in range(len(ntx_list)):
        ntx_count += 1
        # FOR T291.W PRINT/WRITE ORDER_NUMBER NOTIFICATION_NAME AND DESTINATION_ORG_ID     
        f4_line = '[' + str((f"{ntx_count:02d}")) + ']\t[' + ntx_list[j][0] + ']\t[' + ntx_list[j][2]+ ']'
        
        if (j==0):
            f4.write(f4_line + '\n')
            print(f4_line)       
        elif(j>0 and j<(len(ntx_list))):
            if ntx_list[j][0] == ntx_list[j-1][0]:
                f4.write(f4_line + '\n')
                print(f4_line)   
            else:
                f4.write('\n' + f4_line + '\n')
                print('\n' + f4_line)                        
        else:
            f4.write(f4_line)
            print(f4_line)

################### IF T291.M NOTIFICATIONS FILE DO NOT MATCH WIHTH REQUESTS, AS THERE ARE DUMMY T207 WITH DUMMY ORID #### 

else:
    
################### THIS IS FOR REGULAR TRANSACTIONS AND NOTIFICATIONS - WITHOUT T291.M ###
    trx_count = 0
    ntx_count = 0
    f4.write('Number of requests: ' + str(len(trx_list)) + '\n')
    f4.write('Number of notifications: ' + str(len(ntx_list)) + '\n\n')

    for i in range(len(trx_list)):
        trx_count += 1
        ##ntx_count = 0 #to have 14.01 14.03 14.03... - without it is 14.39 14.40. 14.14
        for j in range(len(ntx_list)):
            # compare OriginatorsReference from both lists of lists
            #if equal print matching values
            
            if trx_list[i][1] == ntx_list[j][1]:
                ntx_count += 1
                #FOR NON T291.W PRINT/WRITE TRX_NUMBER.NTX_NUMBER TRX_SOURCE_ORG_ID TRX_DESTINATION ORID NTX_ORG_ID NTX_DESTINATION    
                f4_line = '[' + ((f"{trx_count:02d}")) + '.' + str((f"{ntx_count:02d}")) + ']\t[' + trx_list[i][0] + ']\t[' + trx_list[i][2] + ']\t[' + trx_list[i][1] + ']\t[' + ntx_list[j][0] + ']\t[' + ntx_list[j][2]+ ']'
                # don't add new line after last row
                if (i==len(trx_list)-1 and j==len(ntx_list)-1):
                    f4.write(f4_line)
                    print(f4_line)
                else:
                    f4.write(f4_line + '\n')
                    print(f4_line)

        f4.write('\n')
    #if regular file (no T291.M) print number of Requests, as in T291.M Requests are dummy T207    
    print('Number of requests: ' + str(trx_count))
    
################### THIS IS FOR REGULAR TRANSACTIONS AND NOTIFICATIONS - WITHOUT T291.M###

# always print number of Notifications
print('Number of notifications: ' + str(ntx_count))
f1.close()

print(dest_folder)
if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)
# shutil.copy2(f1_file, dest_folder + '\\' + filename_no_ext + '-ORID.json') # copy source file to destination folder
shutil.copy2(f1_file, dest_folder + '\\' + filename_no_ext + '_ORIGINAL.json')
f2.close()
f3.close()
f4.close()