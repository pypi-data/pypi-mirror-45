# python `aer` library

A library for reading ".aedat" files for logging outputs from
[DVS event-based cameras](https://inivation.com/dvs/).

# How to install

```
pip install aerpy
```

# How to use

```
import aer

# read all at once
events = aer.AEData("mylogfile.aedat")

# read only the first 1000 events in the file
events = aer.AEData("mylogfile.aedat", n=1000)

```

# License

MIT
