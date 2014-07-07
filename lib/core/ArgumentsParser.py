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
        mandatory.add_option("-s", "--site", help="Use \"site\" operator", action="store", type="string", dest="site", default=None)
        #mandatory.add_option("")

        #Optional settings
        settings = OptionGroup(parser, 'Optional Settings')
        settings.add_option("-p", "--only-parameters", help="Show only URLs with Parameters", \
            action="store_true", dest="parameters", default=False)
        settings.add_option("-e", "--extensions", help="Extensions list separated by comma (Example: php, asp)", \
            action="store", dest="extensions", default=None)
        settings.add_option("-c", "--custom-query", help="Custom query to add", \
            action="store", dest="custom", default=None)
        settings.add_option("-g", "--google", help="Search in Google", \
            action="store_true", dest="google", default=False)
        settings.add_option("-b", "--bing", help="Search in Bing", \
            action="store_true", dest="bing", default=False)
        settings.add_option("-a", "--all", help="Search with All Search Engines", \
            action="store_true", dest="allSearchs", default=False)
        settings.add_option("-r", "--recursive", help="Search recursively",
            action="store_true", dest="recursive", default=False)
        settings.add_option("-n", "--numeric-values", help="Only get with numeric values",
            action="store_true", dest="numeric", default=False)
        settings.add_option("--dynamic", "--dynamic-content", help="Search dynamic content", \
            action="store_true", dest="dynamic", default=False)
        settings.add_option("--static", "--static-content", help="Search static content", \
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


        if (options.query is None and options.site is None):
            print("-q|--query or -s|--site is missing!")
            exit(0)
        if (options.query is not None and options.site is not None):
            print("-q|--query and -s|--site are not compatible")
            exit(0)
        if (options.recursive and options.query is not None):
            print("-q|--query and -r|--recursive are not compatible (use with -s|--site)")
            exit(0)
        self.query = options.query
        self.site = options.site
        if options.extensions != None: 
            self.extensions = set([extension.strip() for extension in options.extensions.split(",")])
        else:
            self.extensions = None
        self.google = (options.google == True or options.allSearchs == True)
        self.bing = (options.bing == True or options.allSearchs == True)
        if (self.google is False and self.bing is False):
            print("Yoy must specify at least one search engine")
            exit(0)
             
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
        
        self.recursive = options.recursive
        self.custom = options.custom
        self.numeric = options.numeric
        self.parameters = (options.parameters == True)
       


