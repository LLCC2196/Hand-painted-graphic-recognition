import getopt
import sys

def getargv(argv):
    IMAGEPATH = ''
    LOGPATH = ''
    OUTCSVPATH = ''
    IMAGENAME = ''
    OUTCSVNAME = ''
    try:
        opts, args = getopt.getopt(argv,"hi:l:o:n:c:",["IMAGEPATH=","LOGPATH=","OUTCSVPATH=","IMAGENAME=","OUTCSVNAME="])
    except getopt.GetoptError:
        print('test.py -i <IMAGEPATH> -l <LOGPATH> -o <OUTCSVPATH> -n <IMAGENAME> -c <OUTCSVNAME>')
        print('e.g: #test.py -i ./image/ -l ./image/ -o ./image/ -n 32.212.54.126_qwer_Line_2017-05-19-09-18-33_6786.jpeg -c batchoutput.csv')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -imgp <IMAGEPATH> -logp <LOGPATH> -outp <OUTCSVPATH> -imgn <IMAGENAME> -outn <OUTCSVNAME>')
            sys.exit()
        elif opt in ("-i", "--IMAGEPATH"):
            IMAGEPATH = arg
        elif opt in ("-l", "--LOGPATH"):
            LOGPATH = arg
        elif opt in ("-o", "--OUTCSVPATH"):
            OUTCSVPATH = arg
        elif opt in ("-n", "--IMAGENAME"):
            IMAGENAME = arg
        elif opt in ("-c", "--OUTCSVNAME"):
            OUTCSVNAME = arg
    return IMAGEPATH,LOGPATH,OUTCSVPATH,IMAGENAME,OUTCSVNAME
#test.py -i ./image/ -l ./image/ -o ./image/ -n 32.212.54.126_qwer_Line_2017-05-19-09-18-33_6786.jpeg -c batchoutput.csv
IMAGEPATH,LOGPATH,OUTCSVPATH,IMAGENAME,OUTCSVNAME = getargv(sys.argv[1:])
print(IMAGEPATH,LOGPATH,OUTCSVPATH,IMAGENAME,OUTCSVNAME)
