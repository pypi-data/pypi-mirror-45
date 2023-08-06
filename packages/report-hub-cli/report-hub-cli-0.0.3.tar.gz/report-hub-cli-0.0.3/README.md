# ReportHub cli

[![N|Solid](http://test.igra.it/static/images/logo.png)](https://github.com/grib9544/report-hub-cli)

ReportHub cli is a support for configuration ReportHub server.

  - Send allure report folder to ReportHub server

### Tech

ReportHub cli uses a number of open source projects to work properly:

* [Click 7.0](https://github.com/pallets/click) - Python package for creating beautiful command line interfaces
* [requests 2.21.0](https://github.com/kennethreitz/requests) - Requests is the only Non-GMO HTTP library for Python, safe for human consumption.

And of course ReportHub itself is open source with a [public repository](https://github.com/grib9544/report-hub-cli) on GitHub.

### Installation

ReportHub cli requires [Python](https://www.python.org/) 3.4+ to run.

To install ReportHub cli, simply use pip:

```sh
$ pip install report-hub-cli
```


### Simple usage

```sh
$ report allure -h http://somehost -p some-project -m some-module
```

### Todos

 - Send short report to telegram bot

### License

MIT

**Free Software, Hell Yeah!**