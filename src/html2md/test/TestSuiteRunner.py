import unittest

import html2md.test.TestHTML2md as TestHTML2md
import html2md.test.TestHTML2mdConverter as TestHTML2mdConverter
import html2md.test.TestHTMLExtractor as TestHTMLExtractor
import html2md.test.TestHTMLParser2md as TestHTMLParser2md
import html2md.test.TestURLUtils as TestURLUtils

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(TestHTML2md))
suite.addTests(loader.loadTestsFromModule(TestHTML2mdConverter))
suite.addTests(loader.loadTestsFromModule(TestHTMLExtractor))
suite.addTests(loader.loadTestsFromModule(TestHTMLParser2md))
suite.addTests(loader.loadTestsFromModule(TestURLUtils))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
