from tempfile import NamedTemporaryFile as NTF

__all__ = ['TemporaryFileWrapper']

class UsageCounter(object):
    def __init__(self,value=0):
        self.value = value
    def __bool__(self):
        return bool(self.value)
    def __iadd__(self,v):
        self.value += v
        return self
    def __isub__(self,v):
        self.value -= v
        return self

class TemporaryFileWrapper(object):
    _shared_db = dict()
    def __init__(self,*a,**kw):
        self._closed=0
        if len(a):
            file=a[0]
            a=a[1:]
        else:
            file=kw.pop('file',None)
        if file is None:
            if 'mode' not in kw and 'encoding' not in kw:
                kw['mode']='w+'
                kw['encoding']='utf-8'
            self.file = NTF(*a,**kw)
        else:
            self.file = file
        self._shared_db.setdefault(self.file.name,UsageCounter()).__iadd__(1)
    def __getattr__(self,key):
        return getattr(self.file,key)
    def close(self):
        if self._closed:
            return
        counter=self._shared_db[self.file.name]
        counter-=1
        if not counter:
            self.file.close()
        self._closed=True

