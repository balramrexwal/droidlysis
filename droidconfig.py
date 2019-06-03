import os
import ConfigParser

# ------------------------- DroidLysis Configuration file -----------------

APKTOOL_JAR = os.path.join( os.path.expanduser("~/softs"), "apktool_2.3.0.jar")
AXMLPRINTER_JAR = os.path.join( os.path.expanduser("~/softs"), "AXMLPrinter2.jar")
BAKSMALI_JAR = os.path.join(os.path.expanduser("~/softs"), "baksmali-2.2.2.jar")
DEX2JAR_CMD = os.path.join(os.path.expanduser("~/softs/dex2jar-0.0.9.16-SNAPSHOT"), "d2j-dex2jar.sh")
PROCYON_JAR = os.path.join( os.path.expanduser("~/softs"), "procyon-decompiler-0.5.30.jar")
KEYTOOL = os.path.join( "/usr/bin/keytool" )
INSTALL_DIR = os.path.expanduser("~/dev/droidlysis")
SQLALCHEMY = 'sqlite:///droidlysis.db' # https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls

# ------------------------- Property configuration files -------------------
SMALI_CONFIGFILE = os.path.join(os.path.join(INSTALL_DIR, './conf/smali.conf'))
WIDE_CONFIGFILE= os.path.join(os.path.join(INSTALL_DIR, './conf/wide.conf'))
ARM_CONFIGFILE =  os.path.join(os.path.join(INSTALL_DIR, './conf/arm.conf'))
KIT_CONFIGFILE =  os.path.join(os.path.join(INSTALL_DIR, './conf/kit.conf'))

# ------------------------- Reading *.conf configuration files -----------

class droidconfig:
    def __init__(self, filename, verbose=False):
        assert filename != None, "Filename is invalid"

        self.filename = filename
        self.verbose = verbose
        self.configparser = ConfigParser.RawConfigParser()

        if self.verbose:
            print "Reading configuration file: '%s'" % (filename)
        self.configparser.read(filename)

    def get_sections(self):
        return self.configparser.sections()

    def get_pattern(self, section):
        return self.configparser.get(section, 'pattern')

    def get_description(self, section):
        try:
            return self.configparser.get(section, 'description')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            pass
        return None

    def get_all_regexp(self):
        # reads the config file and returns a list of all patterns for all sections
        # the patterns are concatenated with a |
        # throws NoSectionError, NoOptionError
        allpatterns=''
        for section in self.configparser.sections():
            if allpatterns == '':
                allpatterns = self.configparser.get(section, 'pattern')
            else:
                allpatterns= self.configparser.get(section, 'pattern') + '|' + allpatterns
        return allpatterns

    def match_properties(self, match, properties):
        '''
        Call this when the recursive search has been done to analyze the results
        and understand which properties have been spotted.

        match: returned by droidutil.recursive_search. This is a dictionary
        of matching lines ordered by matching keyword (pattern)

        properties: dictionary of properties where the key is the property name
        and the value will be False/True if set or not
        
        throws NoSessionError, NoOptionError
        '''
        for section in self.configparser.sections():
            pattern_list = self.configparser.get(section, 'pattern').split('|')
            properties[section] = False
            for pattern in pattern_list:
                if match[pattern]:
                    if self.verbose:
                        print "Setting properties[%s] = True (matches %s)" % (section, pattern)
                    properties[section] = True
                    break
