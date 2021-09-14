#!/usr/bin/env python3

from rest3client import RESTclient
import streamlit as st
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Api:

    def __init__(self, url, username, password, client_id, secret):
        self.url = url
        self.username = username
        self.password = password
        self.client_id = client_id
        self.secret = secret

    def generateToken(self):
        client = RESTclient(
            self.url, username=self.client_id, password=self.secret)
        auth = client.post('/api/oauth/v1/token',
                           json={'username': self.username, 'password': self.password, 'grant_type': 'password'})

        return auth['access_token']

    @st.cache(allow_output_mutation=True)
    def getProducts(self):
        items = self.getAllData('/api/rest/v1/products')
        return pd.json_normalize(items)

    @st.cache(allow_output_mutation=True)
    def getCategories(self):
        items = self.getAllData('/api/rest/v1/categories')
        return pd.json_normalize(items)

    @st.cache(allow_output_mutation=True)
    def getFamilies(self):
        items = self.getAllData('/api/rest/v1/families')
        return pd.json_normalize(items)

    @st.cache(allow_output_mutation=True)
    def getAttributes(self):
        items = self.getAllData('/api/rest/v1/attributes')
        return pd.json_normalize(items)

    @st.cache(allow_output_mutation=True)
    def getAttributeOptions(self):

        attributes_df = self.getAttributes()
        attributes_df = attributes_df[attributes_df['type'].isin(
            ['pim_catalog_multiselect', 'pim_catalog_select'])]

        items = self.getDependendEntities(
            '/api/rest/v1/attributes/{code}/options', attributes_df)
        return pd.json_normalize(items)

    @st.cache(allow_output_mutation=True)
    def getFamilyVariants(self):

        families_df = self.getFamilies()
        items = self.getDependendEntities(
            '/api/rest/v1/families/{code}/variants', families_df)
        return pd.json_normalize(items)

    def getDependendEntities(self, path, main_entities_df):
        items = []
        for index, row in main_entities_df.iterrows():
            if row.get("code") is not None:
                entityPath = path.format(code=row['code'])
                data = self.getAllData(entityPath)
                if isinstance(data, list):
                    items.extend(data)
                else:
                    items.append(data)

        return items

    def getAllData(self, path):
        client = RESTclient(self.url, bearer_token=self.generateToken())
        items = []
        while True:
            response = client.get(path)
            if response:
                data = response['_embedded']['items']
                if isinstance(data, list):
                    items.extend(data)
                else:
                    items.append(data)

                if '_links' in response and 'next' in response['_links']:
                    path = response['_links']['next']['href']
                else:
                    break
            else:
                break
        return items
