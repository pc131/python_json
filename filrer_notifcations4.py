from re import I
import os
import shutil

script_path = 'c:\\Users\\skocz\\Desktop\\CGI\\source\\' # root folder for script and JSON file

ORID = '2000097391C01' # ORID to look for
filename = 'TC-TRANSFER-PH3-ORID-2000097391C01-ORID.json' # file with JSON messages from HUB

filename_no_ext = filename.replace('.json', '')

f1_file = script_path + filename

filename_no_ext = filename.replace('.json', '')
f1 = open(f1_file, 'r')
f1_content= f1.read()

requests_start = f1_content.find('Request:')
requests_end = f1_content.find('Peek Message:')

requests = f1_content[requests_start:requests_end]
peeked_notifications = f1_content[requests_end:]

ORID1_start = requests.find('"ORID": "') + 9
ORID1_end = ORID1_start + 13
ORID1 = requests[ORID1_start:ORID1_end]

dest_folder = script_path  + '\\' + filename_no_ext + ORID1 + '-ORID'
print(dest_folder)
if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)

f2_file = script_path + filename_no_ext + ORID1 + '-ORID' +  '\\' +filename_no_ext + ORID1 + '-ORID_RQS.json'
f3_file = script_path + filename_no_ext + ORID1 + '-ORID' +  '\\' +filename_no_ext + ORID1 + '-ORID_NTX.json'
f4_file = script_path + filename_no_ext + ORID1 + '-ORID' +  '\\' +filename_no_ext + ORID1 + '-ORID_ALL.json'
f2 = open(f2_file, 'w')
f3 = open(f3_file, 'w')
f4 = open(f4_file, 'w')

requests_lines = requests.split('\n')

#List of all lines - requests and responses
requests_trx = []

keep_current_line = False
for line in requests_lines:
    if line.startswith("Request:"):
        keep_current_line = True
    elif line.startswith("Response:"):
        keep_current_line = False
    if keep_current_line:
        #print(line)   
        requests_trx.append(line)
        f2.write(line + '\n')

requests_in_list = [i for i, x in enumerate(requests_trx) if x == "Request:"]

#list with elements that start with "Request:"
requests2 = []

for i in range(len(requests_in_list)):

    if i != len(requests_in_list) - 1:
        #append to requests 2 all lines between Requests: lines
        requests2.append(requests_trx[requests_in_list[i]:requests_in_list[i+1]])
    else:
        #for last element look until end of first list     
        requests2.append(requests_trx[requests_in_list[i]:])

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

    # print(trx_name)
    # print(orig_ref)
    # print(src_org_id)


############################## NOTIFICATIONS ########################

notifications_lines = peeked_notifications.split('\n')

#List of all lines - requests and responses
notifications_trx = []
for line in notifications_lines:
        notifications_trx.append(line)
        f3.write(line + '\n')

notifications_in_list = [i for i, x in enumerate(notifications_trx) if x == "Peek Message:"]

#list with elements that start with "Peek Message:"
notifications2 = []

for i in range(len(notifications_in_list)):

    if i != len(notifications_in_list) - 1:
        #append to requests 2 all lines between Requests: lines
        notifications2.append(notifications_trx[notifications_in_list[i]:notifications_in_list[i+1]])
    else:
        #for last element look until end of first list     
        notifications2.append(notifications_trx[notifications_in_list[i]:])

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

trx_count = 0
ntx_count = 0
f4.write('Number of requests: ' + str(len(trx_list)) + '\n')
f4.write('Number of notifications: ' + str(len(ntx_list)) + '\n\n')
for i in range(len(trx_list)):
    trx_count += 1
    ##ntx_count = 0 #to have 14.01 14.03 14.03... - without it is 14.39 14.40. 14.14
    for j in range(len(ntx_list)):
        # compare OriginatorsReference from both lists of lists
        #if ewual print matching values
        
        if trx_list[i][1] == ntx_list[j][1]:
            ntx_count += 1
            f4_line = '[' + ((f"{trx_count:02d}")) + '.' + str((f"{ntx_count:02d}")) + ']\t[' + trx_list[i][0] + ']\t[' + trx_list[i][2] + ']\t[' + trx_list[i][1] + ']\t[' + ntx_list[j][0] + ']\t[' + ntx_list[j][2]+ ']'
            # don't add new line aster last row
            if (i==len(trx_list)-1 and j==len(ntx_list)-1):
                f4.write(f4_line)
                print(f4_line)
            else:
                f4.write(f4_line + '\n')
                print(f4_line)

    f4.write('\n')

#f4.write('\nNumber of requests: ' + str(trx_count) + '\nNumber of notifications: ' + str(ntx_count))
print('Number of requests: ' + str(trx_count))
print('Number of notifications: ' + str(ntx_count))
f1.close()

dest_folder = script_path  + '\\' + filename_no_ext + ORID1 + '-ORID'
print(dest_folder)
if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)
shutil.copy2(f1_file, dest_folder + '\\' + filename_no_ext + ORID1 + '-ORID.json')
f2.close()
f3.close()
f4.close()