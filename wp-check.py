#!/usr/bin/python

import os
import sys
import time
import proxy
import optparse
from output import *
import requests as req
from time import strftime
from wplyzer import WPlyzer
from threading import Thread, Event
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

http_headers = { 'User-agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/47.0 (Chrome)' }

def banner():
    ban = '''-------------------------------------------------------------------------
             _       __               ______                     
            | |     / /___  _________/ / __ \________  __________
            | | /| / / __ \/ ___/ __  / /_/ / ___/ _ \/ ___/ ___/
            | |/ |/ / /_/ / /  / /_/ / ____/ /  /  __(__  |__  ) 
            |__/|__/\____/_/   \__,_/_/   /_/   \___/____/____/  
                                                                 
    ____  __            _               ________              __            
   / __ \/ /_  ______ _(_)___  _____   / ____/ /_  ___  _____/ /_____  _____
  / /_/ / / / / / __ `/ / __ \/ ___/  / /   / __ \/ _ \/ ___/ //_/ _ \/ ___/
 / ____/ / /_/ / /_/ / / / / (__  )  / /___/ / / /  __/ /__/ ,< /  __/ /    
/_/   /_/\__,_/\__, /_/_/ /_/____/   \____/_/ /_/\___/\___/_/|_|\___/_/     
              /____/        
                                        :- by Nasir Khan (r0ot h3x49)
-------------------------------------------------------------------------\n'''
    sys.stdout.write(sb + fg + str(ban))
class WordPress:

    def __init__(self):
        self._plugin_name = None
        self._plugin_url = None
        self._plugin_split_url = None
    
    def Plugin_Check(self, url, out, queue, total, run_event, outfile=None):
        while run_event.is_set():    
            tgt = url.get()
            progress = queue.get()
            try:
                r = req.get(tgt, headers = http_headers)
            except req.exceptions.MissingSchema:
                time.sleep(5)
            except req.exceptions.Timeout:
                time.sleep(5)
            except req.exceptions.RequestException:
                time.sleep(5)
            except req.exceptions.TooManyRedirects:
                time.sleep(5)
            else:
                result = r.status_code
                code, self._plugin_url = r.status_code, r.url
                if code == 200:
                    self._plugin_split_url = self._plugin_url.split('/')
                    self._plugin_name = self._plugin_split_url[-2]
                    if outfile:
                        sys.stdout.write('{}{}[+] {}{:<25} : {}{}{}{}{}        \n'.format(sb, fy, fg ,self._plugin_name, sd,fm, self._plugin_url, sb, fg))
                        self._file = (self._plugin_split_url[2]).replace('.','-') + '.txt'
                        fd = open(str(self._file),"a")
                        fd.write('[+] {:<20} : {}\n'.format(self._plugin_name, self._plugin_url))
                        fd.close()
                    else:
                        sys.stdout.write('{}{}[+] {}{:<25} : {}{}{}{}{}        \n'.format(sb, fy, fg ,self._plugin_name, sd,fm, self._plugin_url, sb, fg))
                else:
                    pass
                out.put(result)
                url.task_done()
                
    def Progress(self, curr, total):
        per = format(100.00 * (int(curr) / float(total)), '.2f')
        filledLength    = int(round(40 * int(curr) / float(total)))
        bar = '=' * filledLength + ' ' * (40 - filledLength)
        sys.stdout.write(sb + fr + '['+ sd + fm + str(bar) + sb + fr +'] '+ sb + fg + '( ' + str(int(curr)) +'/'+str(int(total))+' ) '+ str(per) +'%                                           \r')
            
                
                
    

def main():
    banner()
    Wp = WordPress()
    queue = Queue(1)
    run_event = Event()
    run_event.set()
    us = "%prog [OPTIONS] URL"
    version = "%prog version 1.0"
    parser = optparse.OptionParser(usage=us,version=version,conflict_handler="resolve")

    general = optparse.OptionGroup(parser, 'General')
    general.add_option(
        '-h', '--help',
        action='help',
        help='Print this help text and exit')
    general.add_option(
        '-v', '--version',
        action='version',
    help='Print program version and exit')
    

    target = optparse.OptionGroup(parser, "Target")
    target.add_option(
        "-u", "--url",
        type="string",
        dest='url',\
        help="Provide target url (e.g:- http://www.abc.com)")

    enum = optparse.OptionGroup(parser, "Enumeration")
    enum.add_option(
        "-d", "--default", 
        action='store_true',
        dest='default',\
        help="Analyzes plugins from source code")
    enum.add_option(
        "-b", "--bruteforce", 
        action='store_true',
        dest='brute',\
        help="Analyzes plugins using bruteforce")

    out = optparse.OptionGroup(parser, "Output")
    out.add_option(
        "-s", "--save", 
        action='store_true',
        dest='outfile',\
        help="Stores plugins in file with target url name.")

    
    other = optparse.OptionGroup(parser, "Custom")
    other.add_option(
        "-w", "--wordlist", 
        action='store_true', 
        default = 'plugins.txt',
        dest='list',\
        help="Provide plugin wordlist else it will use default.")
    other.add_option(
        "-t", "--threads", 
        action='store_true', 
        default = 2,
        dest='threads',\
        help="Provide threads default threads = 2")

    tor = optparse.OptionGroup(parser, "Proxy")
    tor.add_option(
        "--tor", 
        action='store_true',
        dest='tor',\
        help="Uses tor proxy network to send traffic through")
    tor.add_option(
        "--new-identity", 
        action='store_true',
        dest='new_identity',\
        help="Automated request for new identity on ip blocked")
    
    parser.add_option_group(general)
    parser.add_option_group(target)
    parser.add_option_group(out)
    parser.add_option_group(other)
    parser.add_option_group(tor)
    parser.add_option_group(enum)

    (options, args) = parser.parse_args()

    
    if not options.url:
        parser.print_help()

    elif options.url and not options.default and options.brute and options.threads is not True and options.list is not True:
        tor = options.tor
        newip = options.new_identity
        Proxy = proxy.Proxy()
        outf = options.outfile
        if tor is True and newip is None:
            Proxy.SetDefaultProxy
            r = req.get('http://my-ip.herokuapp.com/')
            resp = r.text
            sp = resp.replace('\n','')
            default_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            print '\n' + sb + fg + '[+]' + sb + fy + ' TOR: configuring tor proxy...'
            Proxy.ConfigureProxy
            try:
                r = req.get('http://my-ip.herokuapp.com/')
            except:
                print sb + fg + '[-]' + sb + fr + ' TOR: proxy connection error, make sure tor services are running...'
                Proxy.SetDefaultProxy
            resp = r.text
            sp = resp.replace('\n','')
            proxy_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            if default_ip != proxy_ip:
                print sb + fg + '[+]' + sb + fy + ' TOR: proxy configured successfully.'
                print sb + fg + '[+]' + sb + fy + ' TOR: network traffic will go through : (%s)' % (proxy_ip)
                print sb + fy + '\n-------------------------------------------------------------------------'
            else:
                print sb + fg + '[-]' + sb + fr + ' TOR: proxy configuration is failed'
                print sb + fy + '\n-------------------------------------------------------------------------'

        elif tor is True and newip is True:
            Proxy.SetDefaultProxy
            r = req.get('http://my-ip.herokuapp.com/')
            resp = r.text
            sp = resp.replace('\n','')
            default_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            print '\n' + sb + fg + '[+]' + sb + fy + ' TOR: configuring tor proxy...'
            time.sleep(1)
            print  sb + fg + '[+]' + sb + fy + ' TOR: requesting new identity...'
            time.sleep(1)
            _resp = Proxy.NewIdentity
            time.sleep(1)
            if '250 OK' in _resp:
                print sb + fg + '[+]' + sb + fy + ' TOR: request was successfull.'
                Proxy.ConfigureProxy
            else:
                print sb + fg + '[-]' + sb + fr + ' TOR: request was unsuccessfull.'
            r = req.get('http://my-ip.herokuapp.com/')
            resp = r.text
            sp = resp.replace('\n','')
            proxy_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            if default_ip != proxy_ip:
                print sb + fg + '[+]' + sb + fy + ' TOR: proxy configured successfully.'
                print sb + fg + '[+]' + sb + fy + ' TOR: network traffic will go through : (%s)' % (proxy_ip)
                print sb + fy + '\n-------------------------------------------------------------------------'
            else:
                print sb + fg + '[-]' + sb + fr + ' TOR: proxy configuration is failed'
                print sb + fy + '\n-------------------------------------------------------------------------'

            

        tgt = options.url
        threads = options.threads
        wordlist = options.list
        if 'http://' in tgt:
            tgt = tgt
        elif 'https://' in tgt:
            tgt = tgt
        else:
            tgt = 'http://%s' % (tgt)
        print '\n' + sb + fg + '[+]' + sb + fy + ' URL: ' + str(tgt)
        print sb + fg + '[+]' + sb + fy + ' Started: '+str(strftime('%a %b %d %I:%M:%S %Y'))
        print sb + fg + '[+]' + sb + fy + " Wordlist: using default wordlist '" +str(wordlist)+ "'"
        print sb + fy + '\n-------------------------------------------------------------------------'
        try:
            f_in = open(wordlist)
        except (OSError, WindowsError, IOError, Exception):
            if os.name == 'posix':
                sys.stdout.write("\n{}{}[-]{}{} Failed to open default wordlist {}{}'{}'\n{}{}[-]{}{} Wordlist '{}' does not exists in a default path '{}/{}'\n".format(sb, fy, sb, fr, sb, fw, wordlist, sb, fy, sd, fg, wordlist, os.getcwd(), wordlist))
            else:
                sys.stdout.write("\n{}{}[-]{}{} Failed to open default wordlist {}{}'{}'\n{}{}[-]{}{} Wordlist '{}' does not exists in a default path '{}\{}'\n".format(sb, fy, sb, fr, sb, fw, wordlist, sb, fy, sd, fg, wordlist, os.getcwd(), wordlist))
            sys.exit(0)
        plugins = set(list(line for line in (l.strip() for l in f_in) if line))
        url = Queue()
        out = Queue()
        total = len(plugins)
        td = int(threads)
        for i in range(1, td+1):
            try:
                if outf:
                    t = Thread(target=Wp.Plugin_Check, args=(url, out, queue, total, run_event, outf))
                    t.daemon = True
                    t.start()
                else:
                    t = Thread(target=Wp.Plugin_Check, args=(url, out, queue, total, run_event, outf))
                    t.daemon = True
                    t.start() 
            except KeyboardInterrupt:
                Proxy.SetDefaultProxy
                sys.stdout.write('\n{}{}[-]{}{} User Interrupted attempting to terminate threads..\n'.format(sb, fy, sd, fr))
                time.sleep(2)
                run_event.clear()
                #url.join()
                sys.stdout.write('{}{}[+]{}{} Threads successfully terminated....                                            \r\n'.format(sb, fy, sd, fg))
                sys.exit(0)
            except:
                pass

        for plugin in plugins:
            try:
                u = '%s/wp-content/plugins/%s' % (tgt, plugin)
                url.put(u)
            except KeyboardInterrupt:
                Proxy.SetDefaultProxy
                sys.stdout.write('\n{}{}[-]{}{} User Interrupted attempting to terminate threads..\n'.format(sb, fy, sd, fr))
                time.sleep(2)
                run_event.clear()
                #url.join()
                sys.stdout.write('{}{}[+]{}{} Threads successfully terminated....                                            \r\n'.format(sb, fy, sd, fg))
                sys.exit(0)
            except:
                pass

        for curr in range(total+1):
            try:
                Wp.Progress(curr, total)
                if curr == total:
                    if outf:
                        print sb + fy + '-------------------------------------------------------------------------'
                        print sb + fg + '[+]' + sb + fy +  ' Scan completed for target : (' + sd + fw + str(tgt) + sb + fy + ')'
                        print sb + fg + '[+]' + sb + fy +  ' Output is saved to : (' + sd + fw + str((tgt.split('/')[2]).replace('.','-')+'.txt') + sb + fy + ')'
                    else:
                        print sb + fy + '-------------------------------------------------------------------------'
                        print sb + fg + '[+]' + sb + fy +  ' Scan completed for target : (' + sd + fw + str(tgt) + sb + fy + ')'
                else:
                    queue.put(curr)
            except KeyboardInterrupt:
                Proxy.SetDefaultProxy
                sys.stdout.write('\n{}{}[-]{}{} User Interrupted attempting to terminate threads..\n'.format(sb, fy, sd, fr))
                time.sleep(2)
                run_event.clear()
                #url.join()
                sys.stdout.write('{}{}[+]{}{} Threads successfully terminated....                                            \r\n'.format(sb, fy, sd, fg))
                sys.exit(0)
            except:
                pass

        

    elif options.url and not options.default and options.brute and options.list is True and options.threads is not True:
        tor = options.tor
        newip = options.new_identity
        Proxy = proxy.Proxy()
        outf = options.outfile
        if tor is True and newip is None:
            Proxy.SetDefaultProxy
            r = req.get('http://my-ip.herokuapp.com/')
            resp = r.text
            sp = resp.replace('\n','')
            default_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            print '\n' + sb + fg + '[+]' + sb + fy + ' TOR: configuring tor proxy...'
            Proxy.ConfigureProxy
            try:
                r = req.get('http://my-ip.herokuapp.com/')
            except:
                print sb + fg + '[-]' + sb + fr + ' TOR: proxy connection error, make sure tor services are running...'
                Proxy.SetDefaultProxy
            resp = r.text
            sp = resp.replace('\n','')
            proxy_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            if default_ip != proxy_ip:
                print sb + fg + '[+]' + sb + fy + ' TOR: proxy configured successfully.'
                print sb + fg + '[+]' + sb + fy + ' TOR: network traffic will go through : (%s)' % (proxy_ip)
                print sb + fy + '\n-------------------------------------------------------------------------'
            else:
                print sb + fg + '[-]' + sb + fr + ' TOR: proxy configuration is failed'
                print sb + fy + '\n-------------------------------------------------------------------------'

        elif tor is True and newip is True:
            Proxy.SetDefaultProxy
            r = req.get('http://my-ip.herokuapp.com/')
            resp = r.text
            sp = resp.replace('\n','')
            default_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            print '\n' + sb + fg + '[+]' + sb + fy + ' TOR: configuring tor proxy...'
            time.sleep(1)
            print  sb + fg + '[+]' + sb + fy + ' TOR: requesting new identity...'
            time.sleep(1)
            _resp = Proxy.NewIdentity
            time.sleep(1)
            if '250 OK' in _resp:
                print sb + fg + '[+]' + sb + fy + ' TOR: request was successfull.'
                Proxy.ConfigureProxy
            else:
                print sb + fg + '[-]' + sb + fr + ' TOR: request was unsuccessfull.'
            r = req.get('http://my-ip.herokuapp.com/')
            resp = r.text
            sp = resp.replace('\n','')
            proxy_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            if default_ip != proxy_ip:
                print sb + fg + '[+]' + sb + fy + ' TOR: proxy configured successfully.'
                print sb + fg + '[+]' + sb + fy + ' TOR: network traffic will go through : (%s)' % (proxy_ip)
                print sb + fy + '\n-------------------------------------------------------------------------'
            else:
                print sb + fg + '[-]' + sb + fr + ' TOR: proxy configuration is failed'
                print sb + fy + '\n-------------------------------------------------------------------------'
                
        
        tgt = options.url
        wordlist = args[0]
        threads = options.threads
        if 'http://' in tgt:
            tgt = tgt
        elif 'https://' in tgt:
            tgt = tgt
        else:
            tgt = 'http://%s' % (tgt)

            
        if os.name == 'posix':
            wlname = wordlist.split('/')[-1] if '/' in wordlist else wordlist
        else:
            wlname = wordlist.split('\\')[-1] if '\\' in wordlist else wordlist
        print '\n' + sb + fg + '[+]' + sb + fy + ' URL: ' + str(tgt)
        print sb + fg + '[+]' + sb + fy + ' Started: '+str(strftime('%a %b %d %I:%M:%S %Y'))
        print sb + fg + '[+]' + sb + fy + " Wordlist: using provided wordlist '" +str(wlname)+ "'"
        print sb + fy + '\n-------------------------------------------------------------------------'
        try:
            f_in = open(wordlist)
        except (OSError, WindowsError, IOError, Exception, IndexError):
            Proxy.SetDefaultProxy
            if os.name == 'posix':
                sys.stdout.write("\n{}{}[-]{}{} Failed to open default wordlist {}{}'{}'\n{}{}[-]{}{} Wordlist '{}' does not exists in a given path '{}'\n".format(sb, fy, sb, fr, sb, fw, wlname, sb, fy, sd, fg, wlname, wordlist))
            else:
                sys.stdout.write("\n{}{}[-]{}{} Failed to open default wordlist {}{}'{}'\n{}{}[-]{}{} Wordlist '{}' does not exists in a given path '{}'\n".format(sb, fy, sb, fr, sb, fw, wlname, sb, fy, sd, fg, wlname, wordlist))
            sys.exit(0)

            
        plugins = set(list(line for line in (l.strip() for l in f_in) if line))
        url = Queue()
        out = Queue()
        total = len(plugins)
        td = int(threads)
        for i in range(1, td+1):
            try:
                if outf:
                    t = Thread(target=Wp.Plugin_Check, args=(url, out, queue, total, run_event, outf))
                    t.daemon = True
                    t.start()
                else:
                    t = Thread(target=Wp.Plugin_Check, args=(url, out, queue, total, run_event))
                    t.daemon = True
                    t.start()
            except KeyboardInterrupt:
                Proxy.SetDefaultProxy
                sys.stdout.write('\n{}{}[-]{}{} User Interrupted attempting to terminate threads..\n'.format(sb, fy, sd, fr))
                time.sleep(2)
                run_event.clear()
                #url.join()
                sys.stdout.write('{}{}[+]{}{} Threads successfully terminated....                                            \r\n'.format(sb, fy, sd, fg))
                sys.exit(0)
            except:
                pass

        for plugin in plugins:
            try:
                u = '%s/wp-content/plugins/%s' % (tgt, plugin)
                url.put(u)
            except KeyboardInterrupt:
                Proxy.SetDefaultProxy
                sys.stdout.write('\n{}{}[-]{}{} User Interrupted attempting to terminate threads..\n'.format(sb, fy, sd, fr))
                time.sleep(2)
                run_event.clear()
                #url.join()
                sys.stdout.write('{}{}[+]{}{} Threads successfully terminated....                                            \r\n'.format(sb, fy, sd, fg))
                sys.exit(0)
            except:
                pass

        for curr in range(total+1):
            try:
                Wp.Progress(curr, total)
                if curr == total:
                    if outf:
                        print sb + fy + '-------------------------------------------------------------------------'
                        print sb + fg + '[+]' + sb + fy +  ' Scan completed for target : (' + sd + fw + str(tgt) + sb + fy + ')'
                        print sb + fg + '[+]' + sb + fy +  ' Output is saved to : (' + sd + fw + str((tgt.split('/')[2]).replace('.','-')+'.txt') + sb + fy + ')'
                    else:
                        print sb + fy + '-------------------------------------------------------------------------'
                        print sb + fg + '[+]' + sb + fy +  ' Scan completed for target : (' + sd + fw + str(tgt) + sb + fy + ')'
                else:
                    queue.put(curr)
            except KeyboardInterrupt:
                Proxy.SetDefaultProxy
                sys.stdout.write('\n{}{}[-]{}{} User Interrupted attempting to terminate threads..\n'.format(sb, fy, sd, fr))
                time.sleep(2)
                run_event.clear()
                #url.join()
                sys.stdout.write('{}{}[+]{}{} Threads successfully terminated....                                            \r\n'.format(sb, fy, sd, fg))
                sys.exit(0)
            except:
                pass

        

    elif options.url and not options.default and options.brute and options.list is not True and options.threads is True:
        tor = options.tor
        newip = options.new_identity
        Proxy = proxy.Proxy()
        outf = options.outfile
        if tor is True and newip is None:
            Proxy.SetDefaultProxy
            r = req.get('http://my-ip.herokuapp.com/')
            resp = r.text
            sp = resp.replace('\n','')
            default_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            print '\n' + sb + fg + '[+]' + sb + fy + ' TOR: configuring tor proxy...'
            Proxy.ConfigureProxy
            try:
                r = req.get('http://my-ip.herokuapp.com/')
            except:
                print sb + fg + '[-]' + sb + fr + ' TOR: proxy connection error, make sure tor services are running...'
                Proxy.SetDefaultProxy
            resp = r.text
            sp = resp.replace('\n','')
            proxy_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            if default_ip != proxy_ip:
                print sb + fg + '[+]' + sb + fy + ' TOR: proxy configured successfully.'
                print sb + fg + '[+]' + sb + fy + ' TOR: network traffic will go through : (%s)' % (proxy_ip)
                print sb + fy + '\n-------------------------------------------------------------------------'
            else:
                print sb + fg + '[-]' + sb + fr + ' TOR: proxy configuration is failed'
                print sb + fy + '\n-------------------------------------------------------------------------'

        elif tor is True and newip is True:
            Proxy.SetDefaultProxy
            r = req.get('http://my-ip.herokuapp.com/')
            resp = r.text
            sp = resp.replace('\n','')
            default_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            print '\n' + sb + fg + '[+]' + sb + fy + ' TOR: configuring tor proxy...'
            time.sleep(1)
            print  sb + fg + '[+]' + sb + fy + ' TOR: requesting new identity...'
            time.sleep(1)
            _resp = Proxy.NewIdentity
            time.sleep(1)
            if '250 OK' in _resp:
                print sb + fg + '[+]' + sb + fy + ' TOR: request was successfull.'
                Proxy.ConfigureProxy
            else:
                print sb + fg + '[-]' + sb + fr + ' TOR: request was unsuccessfull.'
            r = req.get('http://my-ip.herokuapp.com/')
            resp = r.text
            sp = resp.replace('\n','')
            proxy_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            if default_ip != proxy_ip:
                print sb + fg + '[+]' + sb + fy + ' TOR: proxy configured successfully.'
                print sb + fg + '[+]' + sb + fy + ' TOR: network traffic will go through : (%s)' % (proxy_ip)
                print sb + fy + '\n-------------------------------------------------------------------------'
            else:
                print sb + fg + '[-]' + sb + fr + ' TOR: proxy configuration is failed'
                print sb + fy + '\n-------------------------------------------------------------------------'
        
        tgt = options.url
        threads = args[0]
        wordlist = options.list
        if 'http://' in tgt:
            tgt = tgt
        elif 'https://' in tgt:
            tgt = tgt
        else:
            tgt = 'http://%s' % (tgt)


        print '\n' + sb + fg + '[+]' + sb + fy + ' URL: ' + str(tgt)
        print sb + fg + '[+]' + sb + fy + ' Started: '+str(strftime('%a %b %d %I:%M:%S %Y'))
        print sb + fg + '[+]' + sb + fy + " Wordlist: using default wordlist '" +str(wordlist)+ "'"
        print sb + fy + '\n-------------------------------------------------------------------------'
        try:
            f_in = open(wordlist)
        except (OSError, WindowsError, IOError, Exception):
            if os.name == 'posix':
                sys.stdout.write("\n{}{}[-]{}{} Failed to open default wordlist {}{}'{}'\n{}{}[-]{}{} Wordlist '{}' does not exists in a default path '{}/{}'\n".format(sb, fy, sb, fr, sb, fw, wordlist, sb, fy, sd, fg, wordlist, os.getcwd(), wordlist))
            else:
                sys.stdout.write("\n{}{}[-]{}{} Failed to open default wordlist {}{}'{}'\n{}{}[-]{}{} Wordlist '{}' does not exists in a default path '{}\{}'\n".format(sb, fy, sb, fr, sb, fw, wordlist, sb, fy, sd, fg, wordlist, os.getcwd(), wordlist))
            sys.exit(0)
        
        plugins = set(list(line for line in (l.strip() for l in f_in) if line))
        url = Queue()
        out = Queue()
        total = len(plugins)
        td = int(threads)

        for i in range(1, td+1):
            try:
                if outf:
                    t = Thread(target=Wp.Plugin_Check, args=(url, out, queue, total, run_event, outf))
                    t.daemon = True
                    t.start()
                else:
                    t = Thread(target=Wp.Plugin_Check, args=(url, out, queue, total, run_event, outf))
                    t.daemon = True
                    t.start() 
            except KeyboardInterrupt:
                Proxy.SetDefaultProxy
                sys.stdout.write('\n{}{}[-]{}{} User Interrupted attempting to terminate threads..\n'.format(sb, fy, sd, fr))
                time.sleep(2)
                run_event.clear()
                #url.join()
                sys.stdout.write('{}{}[+]{}{} Threads successfully terminated....                                            \r\n'.format(sb, fy, sd, fg))
                sys.exit(0)
            except:
                pass

        for plugin in plugins:
            try:
                u = '%s/wp-content/plugins/%s' % (tgt, plugin)
                url.put(u)
            except KeyboardInterrupt:
                Proxy.SetDefaultProxy
                sys.stdout.write('\n{}{}[-]{}{} User Interrupted attempting to terminate threads..\n'.format(sb, fy, sd, fr))
                time.sleep(2)
                run_event.clear()
                #url.join()
                sys.stdout.write('{}{}[+]{}{} Threads successfully terminated....                                            \r\n'.format(sb, fy, sd, fg))
                sys.exit(0)
            except:
                pass


        for curr in range(total+1):
            try:
                Wp.Progress(curr, total)
                if curr == total:
                    if outf:
                        print sb + fy + '-------------------------------------------------------------------------'
                        print sb + fg + '[+]' + sb + fy +  ' Scan completed for target : (' + sd + fw + str(tgt) + sb + fy + ')'
                        print sb + fg + '[+]' + sb + fy +  ' Output is saved to : (' + sd + fw + str((tgt.split('/')[2]).replace('.','-')+'.txt') + sb + fy + ')'
                    else:
                        print sb + fy + '-------------------------------------------------------------------------'
                        print sb + fg + '[+]' + sb + fy +  ' Scan completed for target : (' + sd + fw + str(tgt) + sb + fy + ')'
                else:
                    queue.put(curr)
            except KeyboardInterrupt:
                Proxy.SetDefaultProxy
                sys.stdout.write('\n{}{}[-]{}{} User Interrupted attempting to terminate threads..\n'.format(sb, fy, sd, fr))
                time.sleep(2)
                run_event.clear()
                #url.join()
                sys.stdout.write('{}{}[+]{}{} Threads successfully terminated....                                            \r\n'.format(sb, fy, sd, fg))
                sys.exit(0)
            except:
                pass

        

    elif options.url and not options.default and options.brute and options.list is True and options.threads is True:
        tor = options.tor
        newip = options.new_identity
        Proxy = proxy.Proxy()
        outf = options.outfile
        if tor is True and newip is None:
            Proxy.SetDefaultProxy
            r = req.get('http://my-ip.herokuapp.com/')
            resp = r.text
            sp = resp.replace('\n','')
            default_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            print '\n' + sb + fg + '[+]' + sb + fy + ' TOR: configuring tor proxy...'
            Proxy.ConfigureProxy
            try:
                r = req.get('http://my-ip.herokuapp.com/')
            except:
                print sb + fg + '[-]' + sb + fr + ' TOR: proxy connection error, make sure tor services are running...'
                Proxy.SetDefaultProxy
            resp = r.text
            sp = resp.replace('\n','')
            proxy_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            if default_ip != proxy_ip:
                print sb + fg + '[+]' + sb + fy + ' TOR: proxy configured successfully.'
                print sb + fg + '[+]' + sb + fy + ' TOR: network traffic will go through : (%s)' % (proxy_ip)
                print sb + fy + '\n-------------------------------------------------------------------------'
            else:
                print sb + fg + '[-]' + sb + fr + ' TOR: proxy configuration is failed'
                print sb + fy + '\n-------------------------------------------------------------------------'

        elif tor is True and newip is True:
            Proxy.SetDefaultProxy
            r = req.get('http://my-ip.herokuapp.com/')
            resp = r.text
            sp = resp.replace('\n','')
            default_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            print '\n' + sb + fg + '[+]' + sb + fy + ' TOR: configuring tor proxy...'
            time.sleep(1)
            print  sb + fg + '[+]' + sb + fy + ' TOR: requesting new identity...'
            time.sleep(1)
            _resp = Proxy.NewIdentity
            time.sleep(1)
            if '250 OK' in _resp:
                print sb + fg + '[+]' + sb + fy + ' TOR: request was successfull.'
                Proxy.ConfigureProxy
            else:
                print sb + fg + '[-]' + sb + fr + ' TOR: request was unsuccessfull.'
            r = req.get('http://my-ip.herokuapp.com/')
            resp = r.text
            sp = resp.replace('\n','')
            proxy_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            if default_ip != proxy_ip:
                print sb + fg + '[+]' + sb + fy + ' TOR: proxy configured successfully.'
                print sb + fg + '[+]' + sb + fy + ' TOR: network traffic will go through : (%s)' % (proxy_ip)
                print sb + fy + '\n-------------------------------------------------------------------------'
            else:
                print sb + fg + '[-]' + sb + fr + ' TOR: proxy configuration is failed'
                print sb + fy + '\n-------------------------------------------------------------------------'

        
        
        if len(args[0]) > 2:
            wordlist = args[0]
            threads = args[1]
        else:
            wordlist = args[1]
            threads = args[0]

        tgt = options.url
        if 'http://' in tgt:
            tgt = tgt
        elif 'https://' in tgt:
            tgt = tgt
        else:
            tgt = 'http://%s' % (tgt)

        if os.name == 'posix':
            wlname = wordlist.split('/')[-1] if '/' in wordlist else wordlist
        else:
            wlname = wordlist.split('\\')[-1] if '\\' in wordlist else wordlist
            
        print '\n' + sb + fg + '[+]' + sb + fy + ' URL: ' + str(tgt)
        print sb + fg + '[+]' + sb + fy + ' Started: '+str(strftime('%a %b %d %I:%M:%S %Y'))
        print sb + fg + '[+]' + sb + fy + " Wordlist: using provided wordlist '" +str(wlname)+ "'"
        print sb + fy + '\n-------------------------------------------------------------------------'
        try:
            f_in = open(wordlist)
        except (OSError, WindowsError, IOError, Exception, IndexError):
            if os.name == 'posix':
                sys.stdout.write("\n{}{}[-]{}{} Failed to open default wordlist {}{}'{}'\n{}{}[-]{}{} Wordlist '{}' does not exists in a given path '{}'\n".format(sb, fy, sb, fr, sb, fw, wlname, sb, fy, sd, fg, wlname, wordlist))
            else:
                sys.stdout.write("\n{}{}[-]{}{} Failed to open default wordlist {}{}'{}'\n{}{}[-]{}{} Wordlist '{}' does not exists in a given path '{}'\n".format(sb, fy, sb, fr, sb, fw, wlname, sb, fy, sd, fg, wlname, wordlist))
            sys.exit(0)
            
        plugins = set(list(line for line in (l.strip() for l in f_in) if line))
        url = Queue()
        out = Queue()
        total = len(plugins)
        td = int(threads)
        
        for i in range(1, td+1):
            try:
                if outf:
                    t = Thread(target=Wp.Plugin_Check, args=(url, out, queue, total, run_event, outf))
                    t.daemon = True
                    t.start()
                else:
                    t = Thread(target=Wp.Plugin_Check, args=(url, out, queue, total, run_event, outf))
                    t.daemon = True
                    t.start() 
            except KeyboardInterrupt:
                Proxy.SetDefaultProxy
                sys.stdout.write('\n{}{}[-]{}{} User Interrupted attempting to terminate threads..\n'.format(sb, fy, sd, fr))
                time.sleep(2)
                run_event.clear()
                #url.join()
                sys.stdout.write('{}{}[+]{}{} Threads successfully terminated....                                            \r\n'.format(sb, fy, sd, fg))
                sys.exit(0)
            except:
                pass

        for plugin in plugins:
            try:
                u = '%s/wp-content/plugins/%s' % (tgt, plugin)
                url.put(u)
            except KeyboardInterrupt:
                Proxy.SetDefaultProxy
                sys.stdout.write('\n{}{}[-]{}{} User Interrupted attempting to terminate threads..\n'.format(sb, fy, sd, fr))
                time.sleep(2)
                run_event.clear()
                #url.join()
                sys.stdout.write('{}{}[+]{}{} Threads successfully terminated....                                            \r\n'.format(sb, fy, sd, fg))
                sys.exit(0)
            except:
                pass


        for curr in range(total+1):
            try:
                Wp.Progress(curr, total)
                if curr == total:
                    if outf:
                        print sb + fy + '-------------------------------------------------------------------------'
                        print sb + fg + '[+]' + sb + fy +  ' Scan completed for target : (' + sd + fw + str(tgt) + sb + fy + ')'
                        print sb + fg + '[+]' + sb + fy +  ' Output is saved to : (' + sd + fw + str((tgt.split('/')[2]).replace('.','-')+'.txt') + sb + fy + ')'
                    else:
                        print sb + fy + '-------------------------------------------------------------------------'
                        print sb + fg + '[+]' + sb + fy +  ' Scan completed for target : (' + sd + fw + str(tgt) + sb + fy + ')'
                else:
                    queue.put(curr)
            except KeyboardInterrupt:
                Proxy.SetDefaultProxy
                sys.stdout.write('\n{}{}[-]{}{} User Interrupted attempting to terminate threads..\n'.format(sb, fy, sd, fr))
                time.sleep(2)
                run_event.clear()
                #url.join()
                sys.stdout.write('{}{}[+]{}{} Threads successfully terminated....                                            \r\n'.format(sb, fy, sd, fg))
                sys.exit(0)
            except:
                pass


    elif options.url and not options.brute and options.default and options.list is not True and options.threads is not True:
        tor = options.tor
        newip = options.new_identity
        Proxy = proxy.Proxy()
        outf = options.outfile
        if tor is True and newip is None:
            Proxy.SetDefaultProxy
            r = req.get('http://my-ip.herokuapp.com/')
            resp = r.text
            sp = resp.replace('\n','')
            default_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            print '\n' + sb + fg + '[+]' + sb + fy + ' TOR: configuring tor proxy...'
            Proxy.ConfigureProxy
            try:
                r = req.get('http://my-ip.herokuapp.com/')
            except:
                print sb + fg + '[-]' + sb + fr + ' TOR: proxy connection error, make sure tor services are running...'
                Proxy.SetDefaultProxy
            resp = r.text
            sp = resp.replace('\n','')
            proxy_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            if default_ip != proxy_ip:
                print sb + fg + '[+]' + sb + fy + ' TOR: proxy configured successfully.'
                print sb + fg + '[+]' + sb + fy + ' TOR: network traffic will go through : (%s)' % (proxy_ip)
                print sb + fy + '\n-------------------------------------------------------------------------'
            else:
                print sb + fg + '[-]' + sb + fr + ' TOR: proxy configuration is failed'
                print sb + fy + '\n-------------------------------------------------------------------------'

        elif tor is True and newip is True:
            Proxy.SetDefaultProxy
            r = req.get('http://my-ip.herokuapp.com/')
            resp = r.text
            sp = resp.replace('\n','')
            default_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            print '\n' + sb + fg + '[+]' + sb + fy + ' TOR: configuring tor proxy...'
            time.sleep(1)
            print  sb + fg + '[+]' + sb + fy + ' TOR: requesting new identity...'
            time.sleep(1)
            _resp = Proxy.NewIdentity
            time.sleep(1)
            if '250 OK' in _resp:
                print sb + fg + '[+]' + sb + fy + ' TOR: request was successfull.'
                Proxy.ConfigureProxy
            else:
                print sb + fg + '[-]' + sb + fr + ' TOR: request was unsuccessfull.'
            r = req.get('http://my-ip.herokuapp.com/')
            resp = r.text
            sp = resp.replace('\n','')
            proxy_ip = (((sp.split(':')[-1]).replace('}','')).replace('"','')).replace(' ','')
            if default_ip != proxy_ip:
                print sb + fg + '[+]' + sb + fy + ' TOR: proxy configured successfully.'
                print sb + fg + '[+]' + sb + fy + ' TOR: network traffic will go through : (%s)' % (proxy_ip)
                print sb + fy + '\n-------------------------------------------------------------------------'
            else:
                print sb + fg + '[-]' + sb + fr + ' TOR: proxy configuration is failed'
                print sb + fy + '\n-------------------------------------------------------------------------'
        
        url = options.url
        if 'http://' in url:
            url = url
        elif 'https://' in url:
            url = url
        else:
            url = 'http://%s' % (url)
        print '\n' + sb + fg + '[+]' + sb + fy + ' URL: ' + str(url)
        print sb + fg + '[+]' + sb + fy + ' Started: '+str(strftime('%a %b %d %I:%M:%S %Y'))
        print sb + fy + '\n-------------------------------------------------------------------------'
        Wp = WPlyzer(url)
        resp = Wp.Request()
        plugins = Wp._parse_plugins(resp)
        if len(plugins) < 1:
            print sb + fy + '[-]' + sd + fr + ' try bruteforcing for plugins...'
        else:
            for name,ver in plugins.iteritems():
                path = '%s/wp-content/plugins/%s/' % (url, name)
                if outf:
                    print '{}[+] {}{}{:<40} : {}{:<8}{} --> {}{}{}{}{}'.format(fy, sb, fg ,name, fy, ver, fg, sd,fm, path, sb, fg)
                    fname = (url.split('/')[2]).replace('.','-') + '.txt'
                    fd = open(fname, "a")
                    fd.write('{:<40} : {:<8} --> {}\n'.format(name, ver, path))
                    fd.close()
                else:
                    print '{}[+] {}{}{:<40} : {}{:<8}{} --> {}{}{}{}{}'.format(fy, sb, fg ,name, fy, ver, fg, sd,fm, path, sb, fg)
            if outf:
                print sb + fy + '-------------------------------------------------------------------------'
                print sb + fg + '[+]' + sb + fy +  ' Scan completed for target : (' + sd + fw + str(url) + sb + fy + ')'
                print sb + fg + '[+]' + sb + fy +  ' Output is saved to : (' + sd + fw + str((url.split('/')[2]).replace('.','-') + '.txt') + sb + fy + ')'
            else:
                print sb + fy + '-------------------------------------------------------------------------'
                print sb + fg + '[+]' + sb + fy +  ' Scan completed for target : (' + sd + fw + str(url) + sb + fy + ')'
    


if __name__ == '__main__':
    main()
