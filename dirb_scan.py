import os,sys,re,time,subprocess

subnet = raw_input("what is the subnet range to scan? i.e 192.168.0.0/24:    ")


wordlist = raw_input("What is your Super 1337 W0rdlist: ")
ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
http_regex = r'^(?:80)\/tcp$'
https_regex = r'^(?:443)\/tcp$'


returned = []
extensions = [".bak", " .bac", ".old", ".000", ".~", ".01", "._bak", ".001", ".inc", ".Xxx"] 

def sweep():
    try:
        nmapsweep = subprocess.Popen(('nmap %s') % (subnet),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        (nmap_stdout_result, nmap_stderr_result) = nmapsweep.communicate()
        nmap_stdout = nmap_stdout_result.split()
        for line in nmap_stdout:
            line = line.strip()
            ips = re.findall(ip_regex,line)
            if re.match(ip_regex,line):
                returned.append(ips)
    except:
            print "No Match!"
sweep()


def sublist3r():
    try:
        sublist3r = subprocess.Popen(('sublist3r.py -d %s') % (subnet),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (sublist3r_stdout_result, sublist3r_stderr_result) = sublist3r.communicate()
        print "STDOUT: %s \n" %sublist3r_stdout_result
        #print "STDERR: %s \n" %sublist3r_stderr_result
    except:
        print "Sublist3r Failed!"
sublist3r() 


def whatweb():
    try:
        whatweb = subprocess.Popen(('whatweb -a 3 -v %s') %(subnet),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        (whatweb_stdout_result, whatweb_stderr_result) = whatweb.communicate()
        print "STDOUT: %s \n" % (whatweb_stdout_result)
        print "STDERR: %s \n" % (whatweb_stderr_result)
    except:
        print "WhatWeb Failed! \n"
whatweb()


def dirb_scan():
    try:
        for ip in returned:
            ip = str(ip)
            print "Launching Nmap Version Scan On: %s" %ip[2:-2]
            nmap_version_proc = subprocess.Popen(('nmap -sV %s \n') % (ip[2:-2]),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
            (nmap_version_stdout_result, nmap_version_stderr_result) = nmap_version_proc.communicate()
            print "STDOUT: %s" %nmap_version_stdout_result
            nmap_version_stdout = nmap_version_stdout_result.split()
            webtargets = [webtarget.strip() for webtarget in nmap_version_stdout]
            for webtarget in webtargets:
                webtarget = webtarget.strip()
                http = re.findall(http_regex,webtarget)
                https = re.findall(https_regex,webtarget)
                if re.match(http_regex,webtarget):
                    for extension in extensions:
                    	print "Launching Dirb HTTP Scan On: %s" %ip[2:-2]
                        dirb_http_proc = subprocess.Popen(('dirb http://%s %s -X %s') % (ip[2:-2], wordlist, extension),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
                        (stdout_result_dirb_http, stderr_result_dirb_http) = dirb_http_proc.communicate()
                        print "STDOUT: %s \n" % (stdout_result_dirb_http)
                        print "STDERR: %s \n" % (stderr_result_dirb_http)
                elif re.match(https_regex,webtarget):
                    for extension in extensions:
                        print "Launching Dirb HTTPS Scan On: %s" %ip[2:-2]
                        dirb_https_proc = subprocess.Popen(('dirb https://%s %s -X %s') % (ip[2:-2], wordlist, extension),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
                        (stdout_result_dirb_https, stderr_result_dirb_https) = dirb_https_proc.communicate()
                        print "STDOUT: %s \n" % (stdout_result_dirb_https)
                        print "STDERR: %s \n" % (stderr_result_dirb_https)           
    except:
        print "Nmap version scan failed!"           
dirb_scan()  

