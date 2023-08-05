# Created by Q-ays.
# whosqays@gmail.com
from elasticsearch_dsl import Q

doc_type0 = 'doc'


def repo_wrap(doc_type):
    class BaseRepo:

        def __init__(self, ModelType, doc_type=doc_type):
            self.Model = ModelType
            self.index = ModelType.Index.name
            self.type = doc_type

        def add(self, data):
            print(data)
            model = self.Model(**data)
            model.save()
            return model

        def delete(self, did=None):
            if did:
                res = self.Model.get(did)
                res.delete()
                return res

        def update(self, did, data):
            model = self.Model.get(did)
            for key in data:
                if hasattr(model, key):
                    setattr(model, key, data[key])
            model.save()
            return model

        def get(self, did=None, p=None, **kwargs):
            if did:
                if isinstance(did, list):
                    obj = self.Model.mget(did)
                else:
                    obj = self.Model.get(did)
            else:
                s = self.Model.search()
                for key in kwargs:
                    if isinstance(kwargs[key], dict):
                        s = s.query('nested', path=key, query=Q('match', **{str(key) + '.id': kwargs[key].get('id')}))
                    else:
                        s = s.query('match', **{key: kwargs[key]})

                if isinstance(p, list) or isinstance(p, tuple):
                    s = s[p[0]:p[1]]
                    res = s.execute()
                else:
                    res = s.scan()

                obj = []
                for o in res:
                    obj.append(o)

            return obj

        def paging(self, p=(0, 10), **kwargs):
            s = self.Model.search()
            for key in kwargs:
                if isinstance(kwargs[key], dict):
                    s = s.query('nested', path=key, query=Q('match', **{str(key) + '.id': kwargs[key].get('id')}))
                else:
                    s = s.query('match', **{key: kwargs[key]})

            if isinstance(p, list) or isinstance(p, tuple):
                s = s[p[0]:p[1]]
                res = s.execute()
                obj = []
                for o in res:
                    obj.append(o)

                data = dict()
                data['loc'] = p[0]
                data['size'] = p[1]
                data['total'] = res.hits.total
                data['data'] = obj

                return data

    return BaseRepo


Repo = repo_wrap(doc_type0)
