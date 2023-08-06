"""
hudai.resources.person_quote
"""
from ..helpers.resource import Resource


class PersonQuoteResource(Resource):
    def __init__(self, client):
        Resource.__init__(self, client, base_path='/people/quotes')
        self.resource_name = 'PersonQuote'

    def list(self, person_id=None, article_id=None, term=None, min_importance=None, page=None):
        query_params = self._set_limit_offset({
            'article_id': article_id,
            'person_id': person_id,
            'term': term,
            'min_importance': min_importance,
            'page': page
        })

        return self.http_get('/', query_params=query_params)

    def create(self, person_id, article_id, term, text, importance_score=None):
        return self.http_post('/',
                              data={
                                  'article_id': article_id,
                                  'person_id': person_id,
                                  'term': term,
                                  'text': text,
                                  'importance_score': importance_score
                              })

    def fetch(self, quote_id):
        return self.http_get('/{id}', params={'id': quote_id})

    def delete(self, quote_id):
        return self.http_delete('/{id}', params={'id': quote_id})
