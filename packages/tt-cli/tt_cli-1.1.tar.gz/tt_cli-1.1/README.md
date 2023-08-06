# TT
Simple no-dependencies commandline timetracker

```sh
$ tt add 7 eating and sleeping..  # add 7 hours

$ tt show  # Show log
DATE                                | SPENT hrs | TASK
-------------------------------------------------------
2019-05-06 18:11:00 (0 days ago)    |     7 hrs | eating and sleeping..
-------------------------------------------------------
Total 7 hours

$ tt days  # Show log aggregated by days
DATE                                | SPENT hrs |
-------------------------------------------------------
2019-05-06                          |     7 hrs |
-------------------------------------------------------
Total 7 hours
```

# Installation
```sh
$ pip3 install tt_cli
```

Environment variables
* TT_DTFORMAT, `%Y-%m-%d %H:%M:%S`
* TT_FPATH, `~/.tt.csv`
