import os
import tornado.web
from views import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS = {
    "template_path": os.path.join(BASE_DIR, "template_path"),
    "static_path": os.path.join(BASE_DIR, "static"),
}

HANDLERS = [    
    (r"/", HomePage),

    (r"/stainfo/whois/whoissign", MalRegistrarHandler),
    (r"/stainfo/whois/whoisdomains", MalTldHandler),
    (r"/stainfo/whois/whoisall", AllWhoisHandler),

    (r"/stainfo/people/peoplename", BlackNameHandler),
    (r"/stainfo/people/peopletel", BlackTelHandler),
    (r"/stainfo/people/peopleemail", BlackEmailHandler),

    (r"/stainfo/time/timeyear", ExAndCrHandler),
    (r"/stainfo/time/allexsit", ExsitSituationHandler),
    (r"/stainfo/time/updatefrequency", UpdateFrequencyHandler),

    (r"/stainfo/ip/ipnum", DomainSituationHandler),
    (r"/stainfo/ip/ipsur", IpFrequencyHandler),

    (r"/stainfo/space/spaceinfo", RegionDomainHandler),

    (r"/check", CheckInfoHandler),

    (r"/homepage", MaliciousNumHandler)



]


application = tornado.web.Application(
    handlers = HANDLERS,
**SETTINGS)
