from optparse import OptionParser, OptionGroup

class ArgumentsParser:
    dynamicContent = [
        'php','php4','php5','asp','aspx','ashx','axd','jsp','do',
        'html','pl','cgi','xml'
        ]
    staticContent = ['htm', 'html', 'xhtml', 'conf','log','swf','sql','rdp','xml','txt']

    def __init__(self):
        usage = "Usage: %prog [-q|--query] query [-e|--extensions] extensions [options]"
        parser = OptionParser(usage)

        #Mandatory arguments
        mandatory = OptionGroup(parser, 'Mandatory')
        mandatory.add_option("-q", "--query", help="Search query", action="store", type="string", dest="query", default=None)
        #mandatory.add_option("")

        #Optional settings
        settings = OptionGroup(parser, 'Optional Settings')
        settings.add_option("-p", "--only-parameters", help="Show only URLs with Parameters", \
            action="store_true", dest="parameters", default=False)
        settings.add_option("-e", "--extensions", help="Extensions list separated by comma (Example: php, asp)", \
            action="store", dest="extensions", default=None)
        settings.add_option("-g", "--google", help="Search in Google", \
            action="store_true", dest="google", default=False)
        settings.add_option("-b", "--bing", help="Search in Bing", \
            action="store_true", dest="bing", default=False)
        settings.add_option("-a", "--all", help="Search with All Search Engines", \
            action="store_true", dest="allSearchs", default=False)
        settings.add_option("-d", "--dynamic-content", help="Search dynamic content", \
            action="store_true", dest="dynamic", default=False)
        settings.add_option("-s", "--static-content", help="Search static content", \
            action="store_true", dest="static", default=False)
        # -------------TODO------------------
        #settings.add_option("--domains", "--domains", help="Print founded domains and subdomains", \
        #    action="store_true", dest="domains", default=False)
        #settings.add_option("--seo-urls", "--seo-urls", help="EXPERIMENTAL: try to list SEO urls", \
        #    action="store_true", dest="seoUrls", default=False)
        # -------------END TODO--------------

        #Parse
        parser.add_option_group(mandatory)
        parser.add_option_group(settings)
        (options, arguments) = parser.parse_args()
        if (options.query == None):
            print("Query is missing!")
            exit(0)
        self.query = options.query
        if options.extensions != None: 
            self.extensions = set([extension.strip() for extension in options.extensions.split(",")])
        else:
            self.extensions = None
        self.google = (options.google == True or options.allSearchs == True)
        self.bing = (options.bing == True or options.allSearchs == True)
             
        if (options.dynamic == True):
            if (self.extension == None): 
                self.extensions = self.dynamicContent
            else:
                self.extensions = self.extensions + self.dynamicContent

        if (options.dynamic == True):
            if (self.extension == None): 
                self.extensions = self.dynamicContent
            else:
                self.extensions = self.extensions + self.dynamicContent
                

        if (options.static == True):
            if (self.extension == None): 
                self.extensions = self.static
            else:
                self.extensions = self.extensions + self.static
        
        self.parameters = (options.parameters == True)
       


