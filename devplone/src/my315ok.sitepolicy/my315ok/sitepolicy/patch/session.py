import binascii
def extractCredentials(self, request):
        creds={}

        if not self.cookie_name in request:
            return creds

        
        try:
            creds["cookie"]=binascii.a2b_base64(request.get(self.cookie_name))
        except binascii.Error:
            # If we have a cookie which is not properly base64 encoded it
            # can not be ours.
            return creds

        creds["source"]="plone.session" # XXX should this be the id?
        self.cookie_lifetime = 7
#        try:
#            import pdb
#            pdb.set_trace()
#            per = int(request.get( "__ac_persistent", 0 ))
#            
#        except:
#            pass
#        if  per:
#            self.cookie_lifetime = 7
#        else:
#            self.cookie_lifetime = 0           

        return creds