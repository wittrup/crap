# CRAP
Code scRAtch Pad

Dependencies
============

```python
Dependencies = None if that_I_know_of is True else False
```

Features
============
- FunCom, just some stuff containing something that in general is useful everywhere
- startup.py a beautiful little piece of code to be used for your python consoling, dunno if it even runs without errors in linux, it should... maybe it does, maybe is doesn't
- fileinfo.py class generating a lot of info, to be used like this:
```python
fileinfo = Fileinfo(['MD5', 'SHA1', 'SHA256', 'SHA512', 'SHA384'])
for chunk in open(filename, 'rb'):
    fileinfo.update(chunk)
fileinfo.clear()
print(fileinfo.hasobj['MD5'].hexdigest())
print(fileinfo.crc32)
```

Usage
============
```bash
Free of charge, for everyone!
```
