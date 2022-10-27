rx_check
===============

Welcome to the `rx_check` documentation.

Prerequisites
=============

To run the tool, you need:

+ a **Python 3** interpreter
+ **msc_pyparser** - a SecRule parser (>=1.2.1)
+ **google-re2** - Google's re2 engine, python package

The best way to install the required packages just run

```
pip3 install -r requirements.txt
```

How does it work
================

The script expects an argument at least - this would be a single file or a file list, eg: `-r /path/to/crs-setup.conf -r /path/to/coreruleset/*.conf`.

The other option is the `-o`, which tells the script in which type of format you want to see the result. Allowed formats are `native` and `github`.

The script open the files, parses them and finds all of the `SecRule` lines. If a rule has `@rx` operator, then it tries to build the operand
with the Google's re2 engine. If it fails, then notices you.

Normally, you should run the script:

```
./rules-check.py --output=github -r /path/to/coreruleset/crs-setup.conf -r /path/to/coreruleset/*.conf 2>/dev/null
```

In this case, each line will have a prefix, which could be `::debug` or `::error`. See [this](https://docs.github.com/en/actions/learn-github-actions/workflow-commands-for-github-actions#setting-an-error-message) article.

Note: yes, you have to redirect the stderr to `/dev/null`, because `re2.compile()` does not provide any exception if the compilation has failed.
