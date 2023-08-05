
SIDErunner
====
A framework for running Selenium IDE tests from within Python without having to export those
tests.   It reads the tests in their native XML format and makes corresponding webdriver calls
based on the contents of the XML files.

It can run both tests and test suites.

Installation
----

    pip install siderunner

To use in headless mode you'll need selenium, pyvirtualdisplay and a browser such as FireFox.

    $ apt-get install xvfb xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic
    $ apt-get install pyvirtualdisplay
    $ apt-get install selenium
    $ apt-get install firefox


Example
----
This example runs a simple test suite created with Selenium IDE and saved as .xml files.


    #!/usr/bin/python

    import os
    import siderunner

    here = os.path.join(os.path.dirname(__file__), 'tests')

    class SystemTests(siderunner.SeleniumTests):

        headless = True
        url = 'http://localhost'
        path = os.path.join(here, 'scripts')
        size = (1024, 2048)

        def test_suite_one(self):
            self.run_suite('suite-one')

        def test_suite_two(self):
            self.run_suite('suite-two')

