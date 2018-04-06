import sys
import csv
import datetime


# Dictionary to keep the count for active sessions
dict_ASCnt= dict()

# Dictionary to keep start time stamp for active sessions
dict_ASStartTimes = dict()

# Dictionary to keep last reuest time stamp for active sessions
dict_ASLastReqeust = dict()

# ============ Subroutines ==============================

# Subroutine to populate all the dictionaries for an active session
def populateDicts(ip, ts) :
    if ip in dict_ASCnt :		
        dict_ASCnt[ip] += 1
    else :
        dict_ASCnt[ip] = 1

    dict_ASLastReqeust[ip] = ts
    if (ip not in dict_ASStartTimes) :
        dict_ASStartTimes[ip] = ts


# Subroutine write output when a session ends for an ip address
def writeOutput(ip) :
    output_file = sys.argv[3]
    #output_file = r"../output/sessionization_test1.txt"
    activeDur = int((dict_ASLastReqeust[ip] - dict_ASStartTimes[ip]).total_seconds()) + 1

    with open(output_file, 'a') as f:
        f.write('{},{},{},{},{}\n'.format(ip, dict_ASStartTimes[ip], dict_ASLastReqeust[ip], activeDur, dict_ASCnt[ip]))


# Subroutine to remove inactive session
def removeSession(ip) :
    dict_ASStartTimes.pop(ip, None)
    dict_ASCnt.pop(ip, None)


# ============= Main flow Starts Here ==========================
# Main flow
def main_func() :

    #Getting starting time
    current_time = datetime.datetime.now()
    print(current_time)

    if (len(sys.argv) != 4) :
        print('ERROR: not enough parameters')
        exit()
    else :
        # Assigning parameters to appropriate variables
        # in case of parameters sequence change - please change it here
        input_file = sys.argv[1]
        inact_file = sys.argv[2]

        try :
            #inact_file = r"../input/inactivity_period.txt"
            #input_file = r"../input/log_test1.csv"

            # Reading inactive duration from the file
            with open(inact_file, 'r') as inactF:
                inact_period = int(inactF.read())

            with open(input_file, 'r') as csvfile:
                reader =  csv.DictReader(csvfile)
                for row in reader:
                    rowIP = row['ip']
        
                    # Get Timestamp from the current line
                    str_LineTS = row['date'] + ":" + row['time']
                    lineTS = datetime.datetime.strptime(str_LineTS, '%Y-%m-%d:%H:%M:%S')

                    # Looping for closable sessions

                    tplKeys = ();  # tuple for caching the keys of inactive sessions
                    for ipkey in dict_ASLastReqeust: 
                        tsLastRequest = dict_ASLastReqeust[ipkey]
                        sessionTolorateTS = tsLastRequest + datetime.timedelta(seconds=inact_period)

                        # Check if session can be ended
                        if (sessionTolorateTS < lineTS) :
                            tplKeys = (*tplKeys, ipkey)
                            writeOutput(ipkey)
                            removeSession(ipkey)

                    # Remove the keys of inactive sessions 
                    list(map(dict_ASLastReqeust.__delitem__, filter(dict_ASLastReqeust.__contains__,tplKeys)))
 
                    # Continue with adding active session
                    populateDicts(rowIP, lineTS)

            # EOF closing all active sessions
            #print(len(dict_ASCnt), len(dict_ASStartTimes), len(dict_ASLastReqeust))
            for ipkey in dict_ASLastReqeust : 
                writeOutput(ipkey)

        # Exception handling
        except:
            e=sys.exc_info()
            print('ERROR: something went wrong ')
            print(e)


    #Getting Ending time
    current_time = datetime.datetime.now()
    print(current_time)

# ============= Main flow Ends Here ==========================

if __name__ == '__main__':
    main_func()
