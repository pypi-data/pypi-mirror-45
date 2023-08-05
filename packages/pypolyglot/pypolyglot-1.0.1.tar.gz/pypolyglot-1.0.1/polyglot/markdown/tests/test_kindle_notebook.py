import os
import nose
import shutil
import yaml
from polyglot.utKit import utKit
import unittest
from fundamentals import tools

su = tools(
    arguments={"settingsFile": None},
    docString=__doc__,
    logLevel="DEBUG",
    options_first=False,
    projectName="polyglot"
)
arguments, settings, log, dbConn = su.setup()

# # load settings
# stream = file(
#     "/Users/Dave/.config/headjack/headjack.yaml", 'r')
# settings = yaml.load(stream)
# stream.close()

# SETUP AND TEARDOWN FIXTURE FUNCTIONS FOR THE ENTIRE MODULE
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()

# load settings
stream = file(
    pathToInputDir + "/example_settings.yaml", 'r')
settings = yaml.load(stream)
stream.close()

import shutil
try:
    shutil.rmtree(pathToOutputDir)
except:
    pass

# Recursively create missing directories
if not os.path.exists(pathToOutputDir):
    os.makedirs(pathToOutputDir)

shutil.copyfile(pathToInputDir + "How_Light_Works_xx1578xx_-_Notebook.html",
                pathToOutputDir + "How_Light_Works_xx1578xx_-_Notebook.html")
shutil.copyfile(pathToInputDir + "Non-Kindle.html",
                pathToOutputDir + "Non-Kindle.html")

# xt-setup-unit-testing-files-and-folders


class test_kindle_notebook(unittest.TestCase):

    def test_kindle_notebook_function(self):

        from polyglot.markdown import kindle_notebook
        this = kindle_notebook(
            log=log,
            kindleExportPath=pathToOutputDir + "How_Light_Works_xx1578xx_-_Notebook.html",
            outputPath=pathToOutputDir + "How_Light_Works.md"
        )
        this.convert()

        from polyglot.markdown import kindle_notebook
        this = kindle_notebook(
            log=log,
            kindleExportPath=pathToOutputDir + "Non-Kindle.html",
            outputPath=pathToOutputDir + "How_Light_Works.md"
        )
        print this.convert()

    def test_kindle_notebook_function_exception(self):

        from polyglot.markdown import kindle_notebook
        try:
            this = kindle_notebook(
                log=log,
                settings=settings,
                fakeKey="break the code"
            )
            this.get()
            assert False
        except Exception, e:
            assert True
            print str(e)

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
