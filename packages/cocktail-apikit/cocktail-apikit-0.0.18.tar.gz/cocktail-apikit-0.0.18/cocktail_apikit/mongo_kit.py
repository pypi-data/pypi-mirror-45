"""
Common mongo db client toolkit used by api project
"""
from datetime import datetime, timezone
from typing import Dict, List, Union, Any
from urllib.parse import urlencode

from bottle import BaseRequest
from bottle import request
from marshmallow import Schema
from math import ceil
from pymongo import MongoClient, ReturnDocument, DESCENDING, ASCENDING
from pymongo.cursor import Cursor, CursorType
from pymongo.errors import BulkWriteError, DuplicateKeyError
from pymongo.results import UpdateResult

from .bottle_kit import ValidationError
from .constants import (LIMIT_KEY, MONGO_LOOKUPS_MAPPINGS, PAGE_KEY, SKIP_KEY,
                        RECORD_ACTIVE_FLAG_FIELD, REQUEST_DESC_SORT_MARK,
                        REQUEST_LOOKUP_MARK, SORT_KEY, PROJECTION_KEY,
                        MONGO_ID_FIELD_NAME)
from .settings_kit import DefaultSettings
from .utils_kit import convert_py_uuid_to_mongodb_uuid


def _uuid_string_to_mongo_uuid(uuid_string):
    """
    Convert the UUID field value to be compatible with mongo
    """
    # if isinstance(uuid_string, str):
    #     return binary.UUIDLegacy(UUID(uuid_string))
    # if isinstance(uuid_string, UUID):
    #     return binary.UUIDLegacy(uuid_string)
    # else:
    #     raise ValidationError(
    #         'value "{}" should be a str or UUID type'.format(uuid_string))

    return convert_py_uuid_to_mongodb_uuid(uuid_string)


class MongoQuery(object):
    """
    Class to represent to mongo query collections, which including:
        1. conditions: dict (used for query)
        2. projections: dict (used for project field)
        3. skip: int (used for slice)
        4. limit: int (used for slice)
        5. page: int (will be used by pagination)
        6. sort: list
        6. base_query_string: str (used by pagination)
    """

    def __init__(self,
                 condition: dict = None,
                 projection: dict = None,
                 skip: int = 0,
                 limit: int = DefaultSettings.API_DEFAULT_LIMIT,
                 page: int = 1,
                 sort: list = None,
                 base_query_string: str = ''):
        self.condition = condition or {}
        self.projection = projection
        self.skip = skip
        self.limit = limit
        self.page = page
        self.sort = sort
        self.base_query_string = base_query_string

    def __setitem__(self, key, value):
        """
        Extra attribute will insert into conditions attribute
        """
        print(f"\nSetting key:{key}\n")
        if key in [PROJECTION_KEY, SKIP_KEY, LIMIT_KEY, PAGE_KEY, SORT_KEY]:
            setattr(self, key, value)
        else:
            self.condition[key] = value

    def __delitem__(self, key: str):
        """
        Delete key from condition container
        """
        del self.condition[key]

    @property
    def search_keys(self):
        """
        Return a copy of keys collection in condition
        """
        return list(self.condition.keys())

    def pop(self, key: str, default: Any = None):
        """
        Pop key from condition container
        """
        return self.condition.pop(key, default)

    def to_dict(self):
        self.condition.update(
            {
                PROJECTION_KEY: self.projection,
                SKIP_KEY: self.skip,
                LIMIT_KEY: self.limit,
                PAGE_KEY: self.page,
                SORT_KEY: self.sort
            }
        )
        return self.condition


class MongoQueryBuilderMixin:
    """
    Base class to build Mongo style query object 
    """

    @staticmethod
    def _get_page(page):
        """
        fetch the page parameter from request query
        """
        try:
            page = int(page)
            return page if page > 0 else -page
        except ValueError:
            return 1

    @staticmethod
    def _get_limit(limit):
        """
        fetch the limit parameter from request query
        """
        try:
            limit = int(limit)
            return limit
        except ValueError:
            return DefaultSettings.API_DEFAULT_LIMIT

    @staticmethod
    def _get_projection(projection_fields: list = None):
        """
        Fetch user declared projection field to mongo style 
        """

        if DefaultSettings.DEBUG:
            print('fetch projection fields:', projection_fields, '\n\n')
        if not projection_fields:
            return None

        return {key: True for key in projection_fields}

    @staticmethod
    def _build_mongo_sort(sort_fields: List[str] = None):
        """
        convert request sort field condition to mongo sort form
        """

        return [
            (field[1:], DESCENDING) if field.startswith(REQUEST_DESC_SORT_MARK) else (field, ASCENDING) for field in
            sort_fields
        ]

    def build_filter(self):
        for raw_key, value in self._query_data.items():

            # make id value be compatible with mongo
            if raw_key.startswith('id'):
                raw_key = '_{}'.format(raw_key)
                value = convert_py_uuid_to_mongodb_uuid(value)

            # simple field request without any extra operation
            if REQUEST_LOOKUP_MARK not in raw_key:
                self.conditions[raw_key] = value
                continue

            key, _, operator = raw_key.rpartition(REQUEST_LOOKUP_MARK)
            if operator not in MONGO_LOOKUPS_MAPPINGS:
                raise ValidationError(
                    "Query operator: '{}' does not exists!".format(operator))

            # Query by range, the list value is separated by ','
            if operator in ['in', 'nin'] and isinstance(value, str):
                value = value.split(',')

            self.conditions[key] = {
                MONGO_LOOKUPS_MAPPINGS.get(operator): value
            }

    def validate_filter_and_sort(self):
        """
        Validate if the client's request's query and sort fields are all valid
        """

        if not self.schema:
            return True

        valid_query_fields = self.schema.valid_mongo_query_fields()
        if DefaultSettings.DEBUG:
            print(valid_query_fields)

        for field in self.conditions:
            if field not in valid_query_fields:
                raise ValidationError(
                    "Query field: '{}' is not a valid query field!".format(field))

        for field in self.sort:
            if field[0] not in valid_query_fields:
                raise ValidationError(
                    "Sort field: '{}' is not a valid sort field!".format(field[0]))

        self.resolve_marshmallow_dump_to_fields_mapping(valid_query_fields)

    def resolve_marshmallow_dump_to_fields_mapping(self, valid_query_fields):
        """
        In case we declare dump_to attribute in marshmarllow schema field, 
        When user do query with dump_to name, we need to resolve mapping to orginal field name.
        Example:

            holder_type = feilds.String(dump_to='type')

            URL?type=xxx need to work to convert to URL?holder_type=xxx in the mongo query level
        """
        for field in valid_query_fields:
            if '->' in field:
                dump_to, original = field.split('->')
                original_field = '.'.join( [e for e in dump_to.split('.')[0:-1] if e]+[original])
                if self.conditions.get(dump_to):
                    self.conditions[original_field] = self.conditions.pop( dump_to)

    def to_mongo_query(self) -> MongoQuery:
        return MongoQuery(
            condition=self.conditions,
            projection=self.projections,
            skip=self.skip,
            page=self.page,
            limit=self.limit,
            sort=self.sort,
            base_query_string=self.base_query_string
        )


class RawMongoQueryBuilder(MongoQueryBuilderMixin):
    """
    Builder receive raw mongo query and projection data and do not do any convertion
    """

    def __init__(self, condition: dict = None, projection: dict = None, sort: list = None,
                 limit: int = DefaultSettings.API_DEFAULT_LIMIT, skip: int = 0, page: int = 1,
                 base_query_string: str = None):
        self.conditions = condition
        self.projections = projection
        self.sort = sort
        self.limit = limit
        self.skip = skip
        self.page = page
        self.base_query_string = base_query_string


class DictMongoQueryBuilder(MongoQueryBuilderMixin):
    """
    Builder to build a MongoQuery from a dict object 
    """

    def __init__(self, query_data: dict = None, schema: Schema = None):
        self._query_data = query_data or {}
        self.conditions = {}
        self.schema = schema
        self.sort = self._build_mongo_sort(self._query_data.pop(SORT_KEY, []))
        self.page = self._get_page(self._query_data.pop(PAGE_KEY, 1))
        self.limit = self._get_limit(self._query_data.pop(
            LIMIT_KEY, DefaultSettings.API_DEFAULT_LIMIT))
        self.skip = (self.page - 1) * self.limit
        self.projections = self._get_projection(
            self._query_data.pop(PROJECTION_KEY, None))
        self.build_filter()
        self.validate_filter_and_sort()
        request_query = request.query or {}
        request_query.pop(PAGE_KEY, None)
        self.base_query_string = '{}?{}'.format(
            request.fullpath, urlencode(request_query))


class BottleMongoQueryBuilder(DictMongoQueryBuilder):
    """
    Builder to build a MongoQuery from bottle framework's request object
    """

    def __init__(self, request: BaseRequest = None, schema: Schema = None):
        _raw_request_data = request.params
        sort_fields = _raw_request_data.getall(SORT_KEY)
        projection_fields = _raw_request_data.getall(PROJECTION_KEY)

        _raw_request_data.pop(SORT_KEY, None)
        _raw_request_data.pop(PROJECTION_KEY, None)

        query_data = dict(_raw_request_data)
        query_data.update(
            {
                SORT_KEY: sort_fields,
                PROJECTION_KEY: projection_fields
            }
        )

        print('query data:', query_data, '\n\n')

        super().__init__(query_data, schema=schema)


class MongoDBManager(object):
    """
    Base Mongo manager to manage all communication with MongoDB
    """
    DB_CONFIG = None

    def __init__(self, config: dict = None):
        self.config = config or self.DB_CONFIG
        assert self.config, 'Mongo DB configuration object is required!'
        self.client = MongoClient(self.config['MONGODB_URI'])
        self._check_duplicate_db_name(self.config['DB_NAME'])
        self.db = self.client.get_database(self.config['DB_NAME'])
        self.collection = self.db.get_collection(
            self.config['COLLECTION_NAME'])

    def _check_duplicate_db_name(self, config_db_name):
        """
        validation the configuration DB_NAME key, to avoid the mongo case-insensitive database name error
        """
        db_names = {
            name.lower(): name for name in self.client.list_database_names()}
        if config_db_name.lower() in db_names and config_db_name != db_names[config_db_name.lower()]:
            raise Exception((
                'Configured DB_NAME: "{0}" duplicated with already existed DB_NAME: "{1}"'
                '.(Please change DB_NAME to another name or use the exist DB_NAME: "{1}")'.format(
                    config_db_name,
                    db_names[config_db_name.lower()]
                ))
            )

    @staticmethod
    def _convert_uuid_condition_value(condition):
        """
        Check if condition contains _id then convert it to mongo compatible UUIDLegacy
        """
        if condition.get(MONGO_ID_FIELD_NAME, None):
            condition[MONGO_ID_FIELD_NAME] = convert_py_uuid_to_mongodb_uuid(
                condition.get(MONGO_ID_FIELD_NAME))
        return condition

    @staticmethod
    def _extract_set_values(update: dict = None):
        """

        """
        if update is None:
            return {}

        if '$set' in update:
            return update.pop('$set', dict())

        return {key: update.pop(key) for key in list(update.keys())[:] if not key.startswith('$')}

    def update(self, condition: dict = None, changed_value: dict = None, upsert: bool = False, array_filters=None,
               bypass_document_validation: bool = False, collation=None, session=None) -> (UpdateResult, dict):
        """
        Update the changed value and also update the updated_at field with default current time
        """
        condition = self._convert_uuid_condition_value(condition)

        set_values = self._extract_set_values(changed_value)

        # maintain updated_at field's value
        set_values.update(
            {'updated_at': datetime.now().astimezone(timezone.utc)}
        )

        changed_value.update({'$set': set_values})

        print(changed_value)
        try:
            return self.collection.update_many(condition, changed_value, upsert, array_filters,
                                               bypass_document_validation, collation, session), {}
        except Exception as e:
            return None, {'msg': str(e)}

    def find_one_and_update(self, condition: dict = None, changed_value: dict = None, projection: dict = None,
                            sort: list = None, upsert: bool = False, return_document: bool = ReturnDocument.AFTER,
                            array_filters=None, session=None, **kwargs):
        """
        Update one record which selected by conditions with the changed_value data
        """
        condition = self._convert_uuid_condition_value(condition)

        set_values = self._extract_set_values(changed_value)

        set_values.update(
            {'updated_at': datetime.now().astimezone(timezone.utc)})
        changed_value.update({'$set': set_values})

        print('changed value:', changed_value, '\n\n')
        return self.collection.find_one_and_update(filter=condition, update=changed_value, projection=projection,
                                                   sort=sort, upsert=upsert, return_document=return_document,
                                                   array_filters=array_filters, session=session, **kwargs)

    def filter(self, query: Union[MongoQuery, Dict] = None, projection=None, soft_delete: bool = True) -> (Cursor, int):
        """
        Do mongo query search with given query object,
        : param query: can be a MongoQuery object or dict object
        : param soft_delete: indicate if current delete strategy is soft delete or not to add an extra condition
        """
        query = query.to_dict() if isinstance(query, MongoQuery) else query

        if DefaultSettings.DEBUG:
            print('\nquery summary:', query, '\n\n')

        sort_fields = query.pop(SORT_KEY, None)
        skip = query.pop(SKIP_KEY, 0)
        limit = query.pop(LIMIT_KEY, DefaultSettings.API_DEFAULT_LIMIT)
        projection = query.pop(PROJECTION_KEY, None)
        query.pop(PAGE_KEY, 1)

        if soft_delete:
            query[RECORD_ACTIVE_FLAG_FIELD] = True

        count = self.collection.count_documents(query)
        results = self.find(condition=query, projection=projection,
                            sort=sort_fields, skip=skip, limit=limit)
        return results, count

    def find(self, condition: dict = None, projection: dict = None, skip=0, limit=0, no_cursor_timeout=False,
             cursor_type=CursorType.NON_TAILABLE, sort=None, allow_partial_results=False, oplog_replay=False,
             modifiers=None, batch_size=0, manipulate=True, collation=None, hint=None, max_scan=None, max_time_ms=None,
             max=None, min=None, return_key=False, show_record_id=False, snapshot=False, comment=None,
             session=None) -> Cursor:
        """
        pymongo's collection.find() method's original signature
        :return: pymongo's Cursor object
        """

        return self.collection.find(condition, projection, skip=skip, limit=limit, no_cursor_timeout=no_cursor_timeout,
                                    cursor_type=cursor_type,
                                    sort=sort, allow_partial_results=allow_partial_results, oplog_replay=oplog_replay,
                                    modifiers=modifiers, batch_size=batch_size, manipulate=manipulate,
                                    collation=collation, hint=hint, max_scan=max_scan, max_time_ms=max_time_ms, max=max,
                                    min=min, return_key=return_key, show_record_id=show_record_id,
                                    snapshot=snapshot, comment=comment, session=session)

    def find_id(self, id: str, soft_deleted: bool = True) -> Cursor:
        query = {'_id': convert_py_uuid_to_mongodb_uuid(id) }

        if soft_deleted:
            query.update({RECORD_ACTIVE_FLAG_FIELD: True})

        return self.collection.find_one(query)

    def delete(self, condition: dict = None, soft_delete: bool = True) -> (UpdateResult, dict):
        """
        Delete record from mongodb by given delete condition

        :param condition: Condition to filter which documents should be deleted
        :param soft_delete: Flag to indicate if delete action is hard deleted or not. If
                             soft_delete is true, then delete action is just set a flag,
                             not delete forever
        :return: tuple(UpdatedResult, dict)
        """
        condition = self._convert_uuid_condition_value(condition)
        if not soft_delete:
            return self.collection.delete_many(condition)

        condition[RECORD_ACTIVE_FLAG_FIELD] = True
        soft_delete_mark = {
            '$set': {RECORD_ACTIVE_FLAG_FIELD: False, 'deleted_at': datetime.now().astimezone(timezone.utc)}
        }
        try:
            return self.collection.update_many(condition, soft_delete_mark), {}
        except Exception as e:
            return None, {'errors': str(e)}

    def create(self, data: Union[List[Dict], Dict] = None, soft_delete: bool = True) -> (list, dict):
        """ Insert one or many record into MongoDB
        :param data: data to insert into Mongodb's database
        :param soft_delete: If set to True, then added an extra indicator field to database
        :return (list, dict): a list of id of created objects, error_info
        """
        if not data or (isinstance(data, list) and not data[0]):
            return [], {'errors': 'Empty data'}

        if not isinstance(data, list):
            data = [data]

        for obj in data:

            if soft_delete and RECORD_ACTIVE_FLAG_FIELD not in obj:
                obj[RECORD_ACTIVE_FLAG_FIELD] = True

        try:
            return [id for id in self.collection.insert_many(data).inserted_ids], {}

        except (BulkWriteError, DuplicateKeyError) as e:
            return [], {'errors': str(e)}


class Pagination:
    """
    Used to render a list of object with pagination metadata included
    """

    def __init__(self, query: MongoQuery, objects: Cursor, count: int):
        self.query = query
        self.objects = list(objects)
        self.count = count
        self.pages = ceil(self.count / self.query.limit)

    def serialize(self, schema: Schema = None):
        """
        Create the final serialized result data
        """
        return {
            'pagination': {
                'limit': self.query.limit,
                'page': self.query.page,
                'total_pages': ceil(self.count / self.query.limit),
                'total_count': self.count,
                'next_url': self.next_page_url,
                'previous_url': self.previous_page_url,
            },
            'objects': self._dump_object_by_schema(self.objects, schema)
        }

    @staticmethod
    def _dump_object_by_schema(objects: list = None, schema: Schema = None):
        if not schema:
            return objects

        serialized_data, errors = schema.dump(objects, many=True)
        if errors:
            raise ValidationError(str(errors))
        return serialized_data

    def has_next_page(self):
        return self.query.page < self.pages

    def has_previous_page(self):
        return self.query.page > 1

    @property
    def next_page_url(self):
        if not self.has_next_page():
            return None
        return self.query.base_query_string + '&page={}'.format(self.query.page + 1)

    @property
    def previous_page_url(self):
        if not self.has_previous_page():
            return None
        return self.query.base_query_string + '&page={}'.format(self.query.page - 1)


if __name__ == '__main__':
    pass
    # config = DefaultSettings.mongo_config_for_collection()
    # print(config)
    # db = MongoDBManager(DefaultSettings.mongo_db_config())
    # db = DefaultMongoDBManager()
