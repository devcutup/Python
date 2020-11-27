"""Requirement 1 Solution console app """
# Copyright By MeanJustin 11/19/2020

## requirement - only push the data where all the services are down 
## in region like below (all the services shouldgo down like below)

import config

file_name = "service_log.txt"

def check_to_write(service_Detail) :
    flag = True
    with open('service_log.txt', 'r') as file_handler :
        for line in file_handler :
            line = line.strip()
            if not line :
                continue
            if service_Detail['service_name'] not in line :
                continue 
            if line[-1] == "Y" and service_Detail['status'] == "RECOVERY":
                flag = False
                continue
            if line[-1] == "N" and service_Detail['status'] == "DOWN":
                flag = False
                continue
            flag = True
    return flag

def write_file(service_Detail, filename) :
    if check_to_write(service_Detail) == True :
        with open(filename, 'w') as file_handler :
            file_handler.write(service_Detail['service_name'] + " :: " + service_Detail['status'] + "\n")


# Run
if __name__ == '__main__':

    # Read the file from read.txt and put it on one string
    oks, errors = {}, {}
    with open('refocus_fi_fd.txt', 'r') as f_in:
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            line = line.split('|')
            if '- OK' in line[-1]:
                oks.setdefault(line[0], []).append(line[-1])
            else:
                errors.setdefault(line[0], []).append(line[-1])

    ## all is ok case
    # print only if all services are down for FI in any FD:
    for k, v in oks.items():
    # If few or more services are up, please skip
        if k in errors:
            continue
        service_Detail = {"service_name" : k, "status": "RECOVERY"}
        write_file(service_Detail, "recovery.txt")
        print('\nFI_FD: "{}" is Recovery\nThe Services Status:'.format(k))
        for i in v:
            print(i)
        

    ## all is down case
    # print only if all services are down for FI in any FD:
    for k, v in errors.items():
    # If few or more services are up, please skip
        if k in oks:
            continue
        service_Detail = {"service_name" : k, "status": "DOWN"}
        write_file(service_Detail, "services_down.txt")
        print('\nFI_FD: "{}" is down\nThe Services Status:'.format(k))
        for i in v:
            print(i)