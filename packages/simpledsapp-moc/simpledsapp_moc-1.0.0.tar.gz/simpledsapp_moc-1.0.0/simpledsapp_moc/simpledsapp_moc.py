#!/usr/bin/env python                                            
#                                                            _
# simpledsapp_moc ds app
#
# (c) 2016-2019 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import  sys
import  os
import  shutil
import  time
import  sys
import  time
import  json
# import the Chris app superclass
from    chrisapp.base   import ChrisApp

Gstr_title = """

     _                 _          _                                             
    (_)               | |        | |                                            
 ___ _ _ __ ___  _ __ | | ___  __| |___  __ _ _ __  _ __   _ __ ___   ___   ___ 
/ __| | '_ ` _ \| '_ \| |/ _ \/ _` / __|/ _` | '_ \| '_ \ | '_ ` _ \ / _ \ / __|
\__ \ | | | | | | |_) | |  __/ (_| \__ \ (_| | |_) | |_) || | | | | | (_) | (__ 
|___/_|_| |_| |_| .__/|_|\___|\__,_|___/\__,_| .__/| .__/ |_| |_| |_|\___/ \___|
                | |                          | |   | |______                    
                |_|                          |_|   |_|______|                   

"""

Gstr_synopsis = """

    NAME

       simpledsapp_moc.py 

    SYNOPSIS

        python simpledsapp_moc.py                                       \\
            [--prefix <filePrefixString>]                               \\
            [--sleepLength <sleepLength>]                               \\
            [--ignoreInputDir]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            [--man]                                                     \\
            [--meta]                                                    \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            mkdir in out && chmod 777 out
            python simpledsapp_moc.py in out

    DESCRIPTION

        `simpledsapp_moc.py` basically does an explicit copy of each file in 
        an input directory to the output directory, prefixing an optional
        string to each filename.

    ARGS

        [--prefix <prefixString>]
        If specified, a prefix string to append to each file copied.

        [--sleepLength <sleepLength>]
        If specified, sleep for <sleepLength> seconds before starting
        script processing. This is to simulate a possibly long running 
        process.

        [--ignoreInputDir] 
        If specified, ignore the input directory. Simply write a single json 
        file to the output dir that is a timestamp. Useful if the input 
        directory contains large nested file trees.

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--version]
        If specified, print version number. 
        
        [--man]
        If specified, print (this) man page.

        [--meta]
        If specified, print plugin meta data.

"""

class Simpledsapp_moc(ChrisApp):
    """
    A simple DS type ChRIS application specifically created for the Massachusetts Open Cloud remote computing environment..
    """
    AUTHORS                 = 'FNNDSC (dev@babyMRI.org)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'simpleDSapp_moc'
    CATEGORY                = 'testing'
    TYPE                    = 'ds'
    DESCRIPTION             = 'A simple DS type ChRIS application specifically created for the Massachusetts Open Cloud remote computing environment.'
    DOCUMENTATION           = 'http://wiki'
    VERSION                 = '1.0.0'
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictinary is saved when plugin is called with a ``--saveoutputmeta`` 
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}
 
    def manPage_show(self):
        """
        Print some quick help.
        """
        print(Gstr_synopsis)

    def metaData_show(self):
        """
        Print the plugin meta data
        """
        l_metaData  = dir(self)
        l_classVar  = [x for x in l_metaData if x.isupper() ]
        for str_var in l_classVar:
            str_val = getattr(self, str_var)
            print("%20s: %s" % (str_var, str_val))

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        """
        self.add_argument('--prefix', 
                           dest         = 'prefix', 
                           type         = str, 
                           optional     = True,
                           help         = 'prefix for file names',
                           default      = '')
        self.add_argument('--ignoreInputDir',
                           dest         = 'b_ignoreInputDir',
                           type         = bool,
                           optional     = True,
                           help         = 'if set, ignore the input dir completely',
                           action       = 'store_true',
                           default      = False)
        self.add_argument('--sleepLength',
                           dest         = 'sleepLength',
                           type         = str,
                           optional     = True,
                           help         = 'time to sleep before performing plugin action',
                           default      = '0')
        self.add_argument("-v", "--verbosity",
                            help        = "verbosity level for app",
                            type        = str,
                            dest        = 'verbosity',
                            optional    = True,
                            default     = "0")
        self.add_argument('--man',
                            help        = 'if specified, print man page',
                            type        = bool,
                            dest        = 'b_man',
                            action      = 'store_true',
                            optional    = True,
                            default     = False)
        self.add_argument('--meta',
                            help        = 'if specified, print plugin meta data',
                            type        = bool,
                            dest        = 'b_meta',
                            action      = 'store_true',
                            optional    = True,
                            default     = False)
        self.add_argument('--version',
                            help        = 'if specified, print version number',
                            type        = bool,
                            dest        = 'b_version',
                            action      = 'store_true',
                            optional    = True,
                            default     = False)

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        if options.b_man:
            self.manPage_show()
            sys.exit(0)

        if options.b_meta:
            self.metaData_show()
            sys.exit(0)

        if options.b_version:
            print('Plugin Version: %s' % Simpledsapp_moc.VERSION)
            sys.exit(0)

        print(Gstr_title)
        print('Version: %s' % Simpledsapp_moc.VERSION)
        print('Sleeping for %s' % options.sleepLength)
        time.sleep(int(options.sleepLength))
        if options.b_ignoreInputDir:
            # simply create a timestamp in the output dir
            d_timeStamp = {
                'year':     time.strftime('%Y'),
                'month':    time.strftime('%m'),
                'day':      time.strftime('%d'),
                'hour':     time.strftime('%H'),
                'minute':   time.strftime('%M'),
                'second':   time.strftime('%S'),
            }
            print('Saving timestamp object')
            print(json.dumps(d_timeStamp, indent = 4))
            with open('%s/timestamp.json' % options.outputdir, 'w') as f:
                json.dump(d_timeStamp, f, indent = 4)
        else:
            for (dirpath, dirnames, filenames) in os.walk(options.inputdir):
                relative_path  = dirpath.replace(options.inputdir, "").strip("/")
                output_path =  os.path.join(options.outputdir, relative_path)
                for dirname in dirnames:
                    print('Creating directory... %s' % os.path.join(output_path, dirname))
                    os.makedirs(os.path.join(output_path, dirname))
                for name in filenames:
                    new_name    = options.prefix + name
                    str_outpath = os.path.join(output_path, new_name)
                    print('Creating new file... %s' % str_outpath)
                    shutil.copy(os.path.join(dirpath, name), str_outpath)

# ENTRYPOINT
if __name__ == "__main__":
    app = Simpledsapp_moc()
    app.launch()
