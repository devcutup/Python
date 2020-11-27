
"""Requirement 4 Solution console app """
# Copyright By MeanJustin 11/19/2020

#import config for __name__
import config
import smtplib, ssl
import csv

# data contains whole details of oncalling
totalData = []

# parse each data
def parseEach (original, role) :
    print (role)
    print ("========================")
    parsed_data = eval(str(original))
    
    output = ""
    ## Just confirm the data is evaled correctly
    ## Define the data_dict variable which woubld be parsed from parsed_data
    data_dict = []
    
    ## Looping the entire parsed_data value and build the data_dict dictionary value
    for item in parsed_data :
        # Define the each person variable
        temp_list = {
            role : item
        }

        print (role + ":", item)
        output += role + ":" + item + "\n"

        # Looping the start,end pair and print that on the console for confirming results
        for duration in parsed_data[item] :
            output += "start time: " + duration['start'] + "\n"
            output += "end time: " +  duration['end'] + "\n"
            print ("start time: ", duration['start'])
            print ("end time: ", duration['end'])

            # store into the totalData
            temp_data = {}
            if role == 'Primary Oncall Engineer Belowoncall Primary' :
                temp_data['ShiftStart'] = duration['start']
                temp_data['EndTime'] = duration['end']
                temp_data['Primary'] = item
                totalData.append(temp_data)
            else :
                for index, calllog in enumerate(totalData) :
                    if calllog['ShiftStart'] == duration['start'] and calllog['EndTime'] == duration['end']:
                        totalData[index]['Secondary'] = item


        temp_list['duration'] = parsed_data[item]
        data_dict.append(temp_list)
    print("\n")
    print("\n")
    return output

    # Confirm the data is rightly parsed

def send_Email (data) :
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"


    receiver_email = "subbu181987@gmail.com"
    message = """\
    Subject: Hi there. It's made by Python Guy Oleksandr T. """ + "\n" + data + """\
        This message is sent from Python Guy Oleksandr T."""

    sender_email = input("Type your Email and press enter: ")
    password = input("Type your password and press enter: ")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    return True


## Shift Start | End time. | Primary | Secondary
## Writing onto csv file
def write_CSV () :
    # field names  
    fields = ['ShiftStart', 'EndTime', 'Primary', 'Secondary']
    # name of csv file  
    filename = "CallingLog.csv"
        
    # writing to csv file  
    with open(filename, 'w') as csvfile:  
        # creating a csv dict writer object  
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames = fields)  
        # writing headers (field names)  
        writer.writeheader()  
        # writing data rows  
        writer.writerows(totalData)

# Run
if __name__ == '__main__':

    # Read the file from read.txt and put it on one string
    string = ""
    with open('read.txt') as text_file:
        string = text_file.read()

    ## from string get dict value using eval function
    # print (string)
    # parsed_data = eval(string)
    
    length = len("Primary Oncall details below:")
    split_index = string.find("Secondary Oncall Details below:")
    primary_string = string[length + 2 : split_index - 2]
    #print (primary_string)
    output = parseEach(primary_string,"Primary Oncall Engineer Belowoncall Primary")


    length = len("Secondary Oncall Details below:")
    secondary_string = string[length + split_index + 1 : -1]

    output += parseEach(secondary_string,"Secondary Oncall Engineer Belowoncall Secondary")

    print (totalData)
    # send_Email(output)
    write_CSV()
