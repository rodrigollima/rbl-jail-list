#!/usr/bin/env python
import sys
import urllib2
import argparse
import re
import dns.resolver
from urllib2 import urlopen
from colorama import Fore, Back, Style
from colorama import init
from netaddr import *
from datetime import datetime
import sqlite3
init()

bls = ["dnsbl.cobion.com", "b.barracudacentral.org", "bl.spamcannibal.org",
       "bl.spamcop.net", "cbl.abuseat.org", "cdl.anti-spam.org.cn",
       "combined.abuse.ch", "combined.rbl.msrbl.net", "db.wpbl.info",
       "dnsbl-1.uceprotect.net", "dnsbl-2.uceprotect.net",
       "dnsbl-3.uceprotect.net", "dnsbl.cyberlogic.net",
       "dnsbl.sorbs.net", "drone.abuse.ch", "drone.abuse.ch",
       "duinv.aupads.org", "dul.dnsbl.sorbs.net", "dul.ru",
       "dyna.spamrats.com", "dynip.rothen.com",
       "http.dnsbl.sorbs.net", "images.rbl.msrbl.net",
       "ips.backscatterer.org", "ix.dnsbl.manitu.net",
       "korea.services.net", "misc.dnsbl.sorbs.net",
       "noptr.spamrats.com", "orvedb.aupads.org", "pbl.spamhaus.org",
       "phishing.rbl.msrbl.net", "proxy.bl.gweep.ca", "rbl.interserver.net",
       "relays.bl.gweep.ca", "relays.nether.net",
       "residential.block.transip.nl", "smtp.dnsbl.sorbs.net",
       "socks.dnsbl.sorbs.net", "spam.abuse.ch",
       "spam.dnsbl.sorbs.net", "spam.rbl.msrbl.net", "spam.spamrats.com",
       "spamrbl.imp.ch", "tor.dnsbl.sectoor.de",
       "torserver.tor.dnsbl.sectoor.de", "ubl.lashback.com",
       "ubl.unsubscore.com", "virus.rbl.jp",
       "virus.rbl.msrbl.net", "web.dnsbl.sorbs.net", "wormrbl.imp.ch",
       "xbl.spamhaus.org", "zen.spamhaus.org", "zombie.dnsbl.sorbs.net",
       "rracudacentral.org", "cbl.abuseat.org", "http.dnsbl.sorbs.net",
       "misc.dnsbl.sorbs.net", "socks.dnsbl.sorbs.net", "web.dnsbl.sorbs.net",
       "dnsbl-1.uceprotect.net", "dnsbl-3.uceprotect.net", "sbl.spamhaus.org",
       "zen.spamhaus.org", "psbl.surriel.com", "dnsbl.njabl.org", "rbl.spamlab.com",
       "noptr.spamrats.com", "cbl.anti-spam.org.cn", "dnsbl.inps.de",
       "httpbl.abuse.ch", "korea.services.net", "virus.rbl.jp", "wormrbl.imp.ch",
       "rbl.suresupport.com", "ips.backscatterer.org", "opm.tornevall.org", "multi.surbl.org",
       "tor.dan.me.uk", "relays.mail-abuse.org", "rbl-plus.mail-abuse.org",
       "access.redhawk.org", "rbl.interserver.net", "bogons.cymru.com", "bl.spamcop.net",
       "dnsbl.sorbs.net", "dul.dnsbl.sorbs.net", "smtp.dnsbl.sorbs.net", "spam.dnsbl.sorbs.net",
       "zombie.dnsbl.sorbs.net", "dnsbl-2.uceprotect.net", "pbl.spamhaus.org", "xbl.spamhaus.org",
       "ubl.unsubscore.com", "combined.njabl.org", "dyna.spamrats.com", "spam.spamrats.com", "cdl.anti-spam.org.cn",
       "drone.abuse.ch", "dul.ru", "short.rbl.jp", "spamrbl.imp.ch", "virbl.bit.nl", "dsn.rfc-ignorant.org",
       "dsn.rfc-ignorant.org", "netblock.pedantic.org", "ix.dnsbl.manitu.net", "rbl.efnetrbl.org",
       "blackholes.mail-abuse.org", "dnsbl.dronebl.org", "db.wpbl.info", "query.senderbase.org",
       "bl.emailbasura.org", "combined.rbl.msrbl.net",
       "cblless.anti-spam.org.cn", "cblplus.anti-spam.org.cn", "blackholes.five-ten-sg.com",
       "sorbs.dnsbl.net.au", "rmst.dnsbl.net.au", "dnsbl.kempt.net", "blacklist.woody.ch",
       "rot.blackhole.cantv.net", "virus.rbl.msrbl.net", "phishing.rbl.msrbl.net",
       "images.rbl.msrbl.net", "spam.rbl.msrbl.net", "spamlist.or.kr", "dnsbl.abuse.ch",
       "bl.deadbeef.com", "ricn.dnsbl.net.au", "forbidden.icm.edu.pl", "probes.dnsbl.net.au",
       "ubl.lashback.com", "ksi.dnsbl.net.au", "uribl.swinog.ch", "bsb.spamlookup.net",
       "dob.sibl.support-intelligence.net", "url.rbl.jp", "dyndns.rbl.jp", "omrs.dnsbl.net.au",
       "osrs.dnsbl.net.au", "orvedb.aupads.org", "relays.nether.net", "relays.bl.gweep.ca",
       "relays.bl.kundenserver.de", "dialups.mail-abuse.org", "rdts.dnsbl.net.au",
       "duinv.aupads.org", "dynablock.sorbs.net", "residential.block.transip.nl",
       "dynip.rothen.com", "dul.blackhole.cantv.net", "mail.people.it", "blacklist.sci.kun.nl",
       "all.spamblock.unit.liu.se", "spamguard.leadmon.net", "csi.cloudmark.com"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Is This IP Bad?')
    parser.add_argument('-i', '--ip', help='IP range address to check ex.177.154.132.128/26')
   
    args = parser.parse_args()

    if args is not None and args.ip is not None and len(args.ip) > 0:
        ip_list = IPNetwork(args.ip)
    else:
        raise('=/')

    for ip in ip_list:

        for bl in bls:
            try:
                
                conn = sqlite3.connect('database/rbl.db')
                cursor = conn.cursor()
                
                my_resolver = dns.resolver.Resolver()
                query = '.'.join(reversed(str(ip).split("."))) + "." + bl
                my_resolver.timeout = 5
                my_resolver.lifetime = 5

                answers = my_resolver.query(query, "A")
                answer_txt = my_resolver.query(query, "TXT")
            
                cursor.execute("""
                    SELECT * FROM rbl WHERE ip=? AND rbl=? AND text=?
                    """, (str(ip),str(bl),str(answer_txt[0])))
               
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO rbl (ip, rbl, text, created_at)
                        VALUES (?,?,?,?)
                        """, (str(ip), str(bl), str(answer_txt[0]), datetime.now()))
                else:
                    cursor.execute("""
                        UPDATE rbl set updated_at = ?
                        WHERE ip = ?, rbl = ?, text = ? 
                        """, (datetime.now(), str(ip), str(bl), str(answer_txt[0])))      
                                      
                conn.commit()
                conn.close()

                print ((Fore.RED + str(ip) + ' is listed in ' + bl)
                       + ' (%s: %s)' % (answers[0], answer_txt[0]))

            except dns.resolver.NXDOMAIN:
                pass#print (Fore.GREEN + str(ip) + ' is not listed in ' + bl)
    
            except dns.resolver.Timeout:
                pass#print ('WARNING: Timeout querying ' + bl)

            except dns.resolver.NoNameservers:
                pass#print ('WARNING: No nameservers for ' + bl)

            except dns.resolver.NoAnswer:
                pass#print ('WARNING: No answer for ' + bl)        
