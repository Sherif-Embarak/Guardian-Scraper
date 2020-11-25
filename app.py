from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from pymongo import TEXT
from guardian.settings import MONGO_URI, MONGO_DATABASE
from guardian.items import GuardianItem

guardian_api = Flask(__name__)
# get last backslash position
last_bs_pos = MONGO_URI.rfind('/') + 1
# append database name to URI
MONGO_DB_URI = MONGO_URI[:last_bs_pos] + MONGO_DATABASE + MONGO_URI[last_bs_pos:]
guardian_api.config["MONGO_URI"] = MONGO_DB_URI
mongo = PyMongo(guardian_api)
# get model fields
FIELDS = list(GuardianItem.__dict__['fields'].keys())


def return_list(return_str):
    params = dict()
    # remove _id field
    params['_id'] = 0
    # select return fields
    if return_str is '':
        for field in FIELDS:
            params[field] = 1
    else:
        for field in return_str.split(','):
            if field in FIELDS:
                params[field] = 1
            else:
                return field
    return params


@guardian_api.route('/article', methods=['GET'])
def get_articles():
    # get request parameters 
    query = request.args.get('query', None)
    limit = int(request.args.get('limit', 10))
    return_str = request.args.get('return_list', '')
    # select db collection
    articles = mongo.db.articles_article
    # create return list
    params = return_list(return_str)
    if not isinstance(params, dict):
        return params + " is not found"
        # add index and text search
    if query is not None:
        params['score'] = {'$meta': 'textScore'}
        articles.create_index([("$**", TEXT)], default_language='english')
        res = articles.find({"$text": {"$search": query}}, params)
        res.sort([('score', {'$meta': 'textScore'})]).limit(limit)
    else:
        res = articles.find({}, params).limit(limit)
    # return json result
    return jsonify(list(res))


if __name__ == '__main__':
    guardian_api.run()
