from abc import ABCMeta

from boto3.dynamodb.conditions import Key

from metagenomi.base import MgObj
from metagenomi.logger import logger
from metagenomi.helpers import get_time


class MgModel(MgObj):
    '''
    MgModel - base class for all models
    '''
    __metaclass__ = ABCMeta

    def __init__(self, mgid, **data):
        # print('updated')
        MgObj.__init__(self, mgid, **data)

        # If data not passed, object is loaded in the MgObj base class
        self.associated = self.d.get('associated', {})

        if 'created' in self.d:
            self.created = self.d['created']
        else:
            self.created = get_time()

        if 'mgproject' in self.d:
            self.mgproject = self.d['mgproject'].upper()
        else:
            self.mgproject = self.mgid[:4].upper()

        self.alt_id = self.d.get('alt_id')

        self.schema = {
            **self.schema, **{
                'alt_id': {'type': 'string', 'required': False, 'regex': "^[a-zA-Z0-9]*$"},
                'mgtype': {'type': 'string', 'required': True,
                           'allowed': ['sequencing', 'assembly', 'sample']},
                'associated': {'type': 'dict', 'required': True, 'schema': {
                    'sequencing': {'type': 'list', 'schema': {'type': 'mgid'}},
                    'assembly':  {'type': 'list', 'schema': {'type': 'mgid'}},
                    'sample':  {'type': 'list', 'schema': {'type': 'mgid'}},
                    }
                },
                'created': {'type': 'datestring', 'required': True},
                'mgproject': {'type': 'string', 'required': True,
                              'maxlength': 4, 'minlength': 4}
            }
        }

    def update_alt_id(self, new_alt_id, write=True):
        self.alt_id = new_alt_id
        if write:
            if self.validate():
                self.update('alt_id', new_alt_id)

    def write(self, force=False, ignore_exceptions=True, dryrun=False):
        '''
        Write this object to the database - over-ridden in other derived
        classes when needed
        '''

        d = self.to_dict(validate=True, clean=True)

        # Add it back in at the appropriate spot
        d['mgid'] = self.mgid

        response = self.db.table.query(
            KeyConditionExpression=Key('mgid').eq(self.mgid))

        if dryrun:
            print('--- dry run ----')
            print(f'Would write to {self.db.table}')
            print(d)
            return

        if len(response['Items']) < 1:
            # new document
            response = self.db.table.put_item(
                Item=d
            )
            # TODO: validate we got a good response from db
            logger.info(f'Wrote {response} to db')

        else:
            if force:
                response = self.db.table.put_item(
                    Item=d
                )
                # TODO: validate we got a good response from db
                logger.info(f'Wrote {response} to db')
            else:
                msg = f'{self.mgid} is already in DB - cannot re-write'
                logger.debug(msg)
                if ignore_exceptions:
                    print(f'WARNING: {msg}')
                else:
                    raise ValueError(msg)

    def update(self, key, value, dryrun=False):
        '''
        TODO: VALIDATION???

        '''

        if dryrun:
            print('Dry run')
            print(f'Would update {key} to {value}')

        else:
            response = self.db.table.update_item(
                                Key={
                                    'mgid': self.mgid
                                },
                                UpdateExpression=f"set {key} = :r",
                                ExpressionAttributeValues={
                                    ':r': value
                                },
                                ReturnValues="UPDATED_NEW"
                            )
            return response
