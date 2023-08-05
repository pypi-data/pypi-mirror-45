#!python
# -*- coding: utf-8 -*-

from datetime import date, datetime as dt
import json
import os
import requests
import urllib
import traceback
from time import sleep

SERVER  = os.environ.get("DREMIO_SERVER") or 'http://localhost'
API     = SERVER + '/api'
OLD_VERSIONS    = {"login": "v2/"}
CURRENT_VERSION = "/v3/"

## HTTP ENCAPSULATION ##

def _parseResponse(res):
    if res.status_code == 204: return {}
    res.raise_for_status()
    return res.json()

def _buildURL(route):
    version = OLD_VERSIONS[route] if route in OLD_VERSIONS.keys() else CURRENT_VERSION
    url = API + version + route
    return url

def _post(route="/", payload=None, headers=None): # OK 
    url = _buildURL(route)
    res = requests.post(url, json=payload, headers=headers)
    return _parseResponse(res)

def _put(route="/", payload=None, headers=None): # OK 
    url = _buildURL(route)
    res = requests.put(url, json=payload, headers=headers)
    return res.json()

def _get(route="/", payload=None, headers=None): # OK 
    url = _buildURL(route)
    res = requests.get(url, json=payload, headers=headers)
    res.raise_for_status()
    json = res.json()
    return json

# remove fields that should not go on the request. Otherwise will raise a bad request
def _removeUnnecessaryFromReflection(refl):
    # remove unnecessary fields
    refl.pop('id', None)
    refl.pop("status", None)
    refl.pop("createdAt", None)
    refl.pop("updatedAt", None)
    refl.pop("currentSizeBytes", None)
    refl.pop("totalSizeBytes", None)
    refl.pop('tag', None)
    return json


## DREMIO METHODS :::


def authenticate(login): # OK 
    token = _post(route='login', payload=login)['token']
    accessHeader = {
        "authorization": "_dremio{token}".format(token=token),
        "content-type": "application/json",
    }
    return accessHeader

# REFLECTION MANIPULATION

# async, returns a job
def dropReflection(path='', reflection='', headers={}): # OK --- could also be done with reflection api 
    query = f'ALTER DATASET {path} DROP REFLECTION {reflection}'
    job = createJob(sql=query, headers=headers)
    return job

def getReflectionById(id='', headers={}):
    return _get(route=f'reflection/{id}', headers=headers)

def getReflectionsFromVDS(vdsFullPath, headers={}):
    return getReflectionsWithFilters('dataset', vdsFullPath, headers)

# async, returns a job
def getAllMaterializationsDataFromVDS(vdsPath='', headers={}):
    return getAllMaterializationsDataWithFilters('dataset', vdsPath, headers)

def getMaterializationsFromReflection(reflectionId, headers={}):
    return getMaterializationsWithFilters('reflection_id', reflectionId, headers)

def getReflAndMaterIdFromVDS(vdsPath='', headers={}):
    query = f"""
    SELECT r.reflection_id, m.materialization_id, m."create" as created_at, m.last_refresh_from_pds, m.bytes
        FROM sys.reflections r 
        INNER JOIN sys.materializations m ON r.reflection_id = m.reflection_id
        WHERE r.dataset like '%{vdsPath}' 
        and r.type = 'RAW' and m.state = 'DONE'
    """
    job = createJob(sql=query, headers=headers)
    return job

# async, returns a job
def getMaterializationsWithFilters(filterField, filterValue, headers={}):
    query = f"SELECT * FROM sys.materializations WHERE {filterField} = '{filterValue}'"
    job = createJob(sql=query, headers=headers)
    return job

def getAllMaterializationsDataWithFilters(filterField, filterValue, headers={}):
    query = f"""
        select  r.dataset, r.reflection_id, m.materialization_id, f.refresh_id, r.name, r.type, r.status, r.num_failures,
            m.bytes, m.state as materialization_state, m.failure_msg, m.bytes as materialization_size_bytes, m.last_refresh_from_pds, m.expiration as materialization_has_expired,
            f.path as s3_path, f.job_id, f.job_start, f.job_end, f.created_at as refresh_created_at, f.modified_at as refresh_modified_at, f.input_bytes, f.output_bytes, f.input_records, f.output_records, f.partitions
        from sys.reflections r
        left join sys.materializations m on m.reflection_id = r.reflection_id
        left join sys.refreshes f ON f.series_id = m.seriesid
        order by r.dataset, f.job_start
        WHERE r.{filterField} = {filterValue}
    """
    job = createJob(sql=query, headers=headers)
    return job

def getReflectionsWithFilters(filterField, filterValue, headers={}):
    query = f"SELECT * FROM sys.reflections WHERE {filterField} = '{filterValue}'"
    job = createJob(sql=query, headers=headers)
    return job

def updateReflection(refl={}, headers={}):
    id = refl.pop('id', None)
    return _put(route=f"reflection/{id}", payload=refl, headers=headers)

def getReflectionRecommendation(datasetId='', headers={}):
    return _post(f'dataset/{datasetId}/reflection/recommendation', headers=headers)

def createReflection(refl={}, headers={}):
    _removeUnnecessaryFromReflection(refl)
    refl['enable']
    return _post(route='reflection',payload=refl, headers=headers)

def createReflectionToVDS(vdsName, recomendation, headers={}):
    vds = getCatalogByPath(vdsName, headers)
    # refl[0] is RAW, refl[1] is AGGREGATED
    refId = []
    for ref in recomendation:
        ref['datasetId'] = vds['id']
        ref['name'] = f"Recommended-{dt.now().strftime('%Y%m%d-%H%M')}"
        try:
            refId += [createReflection(ref, headers)['id']]
        except Exception as e:
            print(f"Could not create reflection to {vdsName}.")
            traceback.print_tb(e.__traceback__)
            pass
    return refId

## VDS and PDS and CATALOG MANIPULATION

def refreshPDSById(id='', headers={}):
    return _post(route=f'catalog/{id}/refresh', headers=headers)

# async, returns a job
def refreshPDS(fullPath=None, headers={}):
    query =   f"""
                ALTER PDS {fullPath} REFRESH METADATA
                AUTO PROMOTION FORCE UPDATE DELETE WHEN MISSING
               """
    job = createJob(sql=query, headers=headers)

    return job

# async, returns a job
def dropVDS(fullPath='', headers={}): #
    query = f"DROP VDS {fullPath}"
    job = createJob(sql=query, headers=headers)
    return job

def getVDS(path=None, id=None, headers={}):
    if id != None:
        return _get(f'catalog/{id}', headers=headers)
    path = urllib.parse.quote(path, safe='')
    return _get(f'catalog/by-path/{path}', headers=headers)

def getCatalog(headers={}): # OK
    return _get('catalog', headers=headers)

def getCatalogByPath(path='', headers={}): # OK, use '.' (point) as path separator
    path = path.replace('.', '/')
    return _get('catalog/by-path/' + path, headers=headers)

# async, returns a job
def createTableAs(vds=None, sql=None, context='', tableName='', headers={}):
    #     CREATE TABLE <source>.<TABLE_NAME>
    #       [HASH PARTITION BY (column, . .) ]
    #       [LOCALSORT BY (column) ]
    #       AS <QUERY>
    select = vds.sql if vds.sql != None else sql

    query = f"CREATE TABLE {context}.{tableName} AS {select}"
    job = createJob(sql=query, headers=headers)

    return job

# async, returns a job
def createVDS(vdsFullPath='', select=None, context=[], headers={}): # OK = createVDS(vdsName='Lims_Full_Comparisons.Test_1', select='select * from lims_full.bra.jcb.lims.test.parquet',headers=cred_header)
    query = f"CREATE VDS {vdsFullPath} AS {select}"
    job = createJob(sql=query, context=context, headers=headers)
    return job

## JOB MANIPULATION

def getJob(jobId='', headers={}): # OK
    return _get(route=f'job/{jobId}', headers=headers)

def getJobResults(jobId, headers={}):
    return _get(route=f'job/{jobId}/results', headers=headers)

def createJob(sql='', context=[], headers={}):  # OK
    payload = {"sql": sql, "context": context}
    res = _post(route="sql", headers=headers, payload=payload)
    return res

def waitCompletion(id, isReflection=False, headers={}):
    retry = 3
    state = 'UNKNOWN'
    while retry:
        if isReflection: 
            job = getReflectionById(id, headers) 
            state = job['status']['availability']
        else:
            job = getJob(id, headers)
            state = job['jobState']
        print(f'Waiting job {id} to complete. State is {state}')
        if (state in ['FAILED', 'CANCELED', 'COMPLETED', 'AVAILABLE']): break
        sleep(1)
        retry -= 1
    return job