### **[SeleniumBase is on Github](https://github.com/seleniumbase/SeleniumBase)**

**(``pytest-seleniumbase`` is a proxy for ``seleniumbase``)**

[<img src="https://cdn2.hubspot.net/hubfs/100006/images/super_logo_3.png" title="SeleniumBase" height="48">](https://github.com/seleniumbase/SeleniumBase/blob/master/README.md)

[<img src="https://img.shields.io/github/release/seleniumbase/SeleniumBase.svg" />](https://github.com/seleniumbase/SeleniumBase/releases) [<img src="https://dev.azure.com/seleniumbase/seleniumbase/_apis/build/status/seleniumbase.SeleniumBase?branchName=master" />](https://dev.azure.com/seleniumbase/seleniumbase/_build/latest?definitionId=1&branchName=master) [<img src="https://travis-ci.org/seleniumbase/SeleniumBase.svg?branch=master" alt="Build Status" />](https://travis-ci.org/seleniumbase/SeleniumBase) [<img src="https://badges.gitter.im/seleniumbase/SeleniumBase.svg" alt="Join the Gitter Chat" />](https://gitter.im/seleniumbase/SeleniumBase) [<img src="https://img.shields.io/badge/license-MIT-22BBCC.svg" alt="MIT License" />](https://github.com/seleniumbase/SeleniumBase/blob/master/LICENSE) [<img src="https://img.shields.io/github/stars/seleniumbase/seleniumbase.svg" alt="GitHub Stars" />](https://github.com/seleniumbase/SeleniumBase/stargazers)<br />

Reliable Browser Automation & Testing with [Selenium-WebDriver](https://www.seleniumhq.org/) and [Pytest](https://docs.pytest.org/en/latest/).

<img src="https://cdn2.hubspot.net/hubfs/100006/sb_demo_mode.gif" title="SeleniumBase" height="236"><br />
(<i>Above: [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py) from [examples/](https://github.com/seleniumbase/SeleniumBase/tree/master/examples) running in demo mode, which adds JavaScript for highlighting page actions.</i>)<br />
```
pytest my_first_test.py --demo_mode
```

## <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Quick Start:

(<i>Requires **[Python/Pip](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/install_python_pip_git.md)** [<img src="https://img.shields.io/badge/python-2.7,_3.x-22AADD.svg" alt="Python versions" />](https://www.python.org/downloads/). Optionally, you may want to use a [Python virtual environment](https://github.com/seleniumbase/SeleniumBase/blob/master/help_docs/virtualenv_instructions.md) to isolate Python dependencies between projects.</i>)

### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Git clone and install SeleniumBase:
```
git clone https://github.com/seleniumbase/SeleniumBase.git
cd SeleniumBase
pip install -e .
```

You can also install SeleniumBase from [PyPI](https://pypi.python.org/pypi/seleniumbase): [<img src="https://img.shields.io/badge/pypi-seleniumbase-22AAEE.svg" alt="pypi" />](https://pypi.python.org/pypi/seleniumbase)
```
pip install seleniumbase
```
* (Add ``--upgrade`` to get the latest packages and ``--force-reinstall`` with ``--no-cache-dir`` to force a reinstall without using the existing cache.)

You can also install a specific GitHub branch of SeleniumBase:
```
pip install -e git+https://github.com/seleniumbase/SeleniumBase.git@master#egg=seleniumbase
```

### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Download a web driver:

SeleniumBase can download a web driver to the [seleniumbase/drivers](https://github.com/seleniumbase/SeleniumBase/tree/master/seleniumbase/drivers) folder with the ``install`` command:
```
seleniumbase install chromedriver
```
* (You need a different web driver for each web browser you want to run automation on: ``chromedriver`` for Chrome, ``edgedriver`` for Edge, ``geckodriver`` for Firefox, ``operadriver`` for Opera, and ``iedriver`` for Internet Explorer.)

### <img src="https://cdn2.hubspot.net/hubfs/100006/images/super_square_logo_3a.png" title="SeleniumBase" height="32"> Run a test on Chrome:
```
cd examples
pytest my_first_test.py --browser=chrome
```
* (Chrome is the default browser if not specified with ``--browser``)

**Check out [my_first_test.py](https://github.com/seleniumbase/SeleniumBase/blob/master/examples/my_first_test.py) to see what a simple test looks like:**
* (<i>By default, [CSS Selectors](https://www.w3schools.com/cssref/css_selectors.asp) are used for finding page elements.</i>)