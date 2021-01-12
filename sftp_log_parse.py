import subprocess
from collections import OrderedDict

def create_ip_user_dict(outputlist):
    '''Create dictionary for user/IP combinations'''
    sftpdict = {}
    for i in outputlist:
        if len(i) > 0:
            user = i.split()[8]
            ip = i.split()[10]
            if not user in sftpdict:
                sftpdict[user] = [ip]
            else:
                if not ip in sftpdict[user]:
                    sftpdict[user].append(ip)
    return sftpdict

def print_hosts_allow(s):
    '''Iterate through Dictionary Keys and Print in /etc/hosts.allow Format'''
    for i in s.keys():
        print("#",i)
        for x in range(len(s[i])):
            print("sshd:", s[i][x])

def main():

    print("Enter the Log Folder Path:")
    folderpath = str(input('folderpath: '))
    print("Enter the Number of Days to Search: ")
    days = str(input('days: '))

    '''Call linux find command to locate logfiles and grep for accepted connections'''
    logfiles = subprocess.Popen(('find', folderpath, '-type', 'f', '-mtime', days, '-print0'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('xargs', '-0', 'zgrep', 'Accepted'), stdin=logfiles.stdout)

    '''Decode bytes object retured by subprocess output into string'''
    newoutput = output.decode("utf-8")

    '''Create List by splitting string at newlines'''
    outputlist = newoutput.split('\n')

    '''Get IP_User Dictionary'''
    sftpdict = create_ip_user_dict(outputlist)

    '''Sort dictionary'''
    s = OrderedDict(sorted(sftpdict.items(), key=lambda t: t[0]))

    '''Print hosts.allow output from dictionary'''
    print_hosts_allow(s)

if __name__ == '__main__':
    main()