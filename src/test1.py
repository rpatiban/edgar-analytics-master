import sys
import csv
import datetime

# Feature 1 - Dictionary to keep the count for active sessions
dict_ASCnt= dict()

# Feature 1 - Dictionary to keep start time stamp for active sessions
dict_ASStartTimes = dict()

# Feature 1 - Dictionary to keep last reuest time stamp for active sessions
dict_ASLastReqeust = dict()

inactivity_duration = 2
input_file = "../input/1sec.csv"
output_file = "../output/sessionization.txt"

# Function to populate all the dictionaries for an active session
def populateDicts(ip, ts) :
    if ip in dict_ASCnt :		
        dict_ASCnt[ip] += 1
    else :
        dict_ASCnt[ip] = 1

    dict_ASLastReqeust[ip] = ts
    if (ip not in dict_ASStartTimes) :
        dict_ASStartTimes[ip] = ts


# Function write output when a session ends for an ip address
def writeOutput(ip) :
    activeDur = int((dict_ASLastReqeust[ip] - dict_ASStartTimes[ip]).total_seconds()) + 1
    with open(output_file, 'w') as f:
        f.write('{},{},{},{},{}\n'.format(ip, dict_ASStartTimes[ip], dict_ASLastReqeust[ip], activeDur, dict_ASCnt[ip]))

    #print(ip + "," + str(dict_ASStartTimes[ip]) + "," + str(dict_ASLastReqeust[ip]) + "," + str(activeDur) + "," + str(dict_ASCnt[ip]))

# Function to remove inactive session
def removeSession(ip) :
    dict_ASStartTimes.pop(ip, None)
    dict_ASLastReqeust.pop(ip, None)
    dict_ASCnt.pop(ip, None)



with open('../input/1sec.csv', 'r') as csvfile:
    reader =  csv.DictReader(csvfile)
    for row in reader:
        rowIP = row['ip']
        
        # Get Timestamp from the current line
        str_LineTS = row['date'] + ":" + row['time']
        lineTS = datetime.datetime.strptime(str_LineTS, '%Y-%m-%d:%H:%M:%S')

        # Looping for closable sessions
        for k in dict_ASLastReqeust: 
            tsLastRequest = dict_ASLastReqeust[k]
            sessionEndTS = tsLastRequest + datetime.timedelta(seconds=inactivity_duration)

            # Check if session can be ended
            if (sessionEndTS < lineTS) :
                writeOutput(k)
                removeSession(k)
 
        # Continue with adding active session
        populateDicts(rowIP, lineTS)

    # EOF closing all active sessions
    print(len(dict_ASCnt), len(dict_ASStartTimes), len(dict_ASLastReqeust))
    for k in dict_ASLastReqeust : 
        writeOutput(k)
