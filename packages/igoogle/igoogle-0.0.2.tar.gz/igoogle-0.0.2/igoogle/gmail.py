
db명 = 'gmail'
data_path = '/Users/sambong/p/gmail/data/'

from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import errors
import base64
import email
import pandas as pd
from pymongo import MongoClient
from pandas.io.json import json_normalize
from datetime import datetime

import sys
sys.path.append('/Users/sambong/p/lib/')
import list_handler as lh
import mongodb as mg

from gmail import db명, data_path
from datetime import datetime, timezone, timedelta
import pandas as pd

mg_client = MongoClient()
db = mg_client[db명]

class Collector:

    def Setup_the_Gmail_API():
        lib_path = '/Users/sambong/p/lib/'
        SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
        store = file.Storage(lib_path+'credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(lib_path+'google_client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('gmail', 'v1', http=creds.authorize(Http()))
        return service
        #https://www.googleapis.com/gmail/v1/users/userId/messages

    def Call_the_Gmail_API():
        service = Setup_the_Gmail_API()
        results = service.users().labels().list(userId='me').execute()
        print('\n results :\n', results)
        labels = results.get('labels', [])
        print('\n labels :\n', labels)
        print('\n labels_len :\n', len(labels))

        if not labels:
            print('No labels found.')
        else:
            print('Labels:')
            for label in labels:
                print(label['name'])

    def ListMessagesMatchingQuery(user_id='me', query=''):
        service = Setup_the_Gmail_API()
        try:
            response = service.users().messages().list(userId=user_id, q=query).execute()
            messages = []
            if ('messages' in response):
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages().list(userId=user_id, q=query,
                                                 pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except (errors.HttpError, error):
            print ('An error occurred: %s' % error)

    def ListMessagesWithLabels(user_id='me', label_ids=[]):
        service = Setup_the_Gmail_API()
        try:
            response = service.users().messages().list(userId=user_id, labelIds=label_ids).execute()
            messages = []
            if ('messages' in response):
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages().list(userId=user_id,
                                                         labelIds=label_ids,
                                                         pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except (errors.HttpError, error):
            print ('An error occurred: %s' % error)

    def GetMessage(msg_id, user_id='me'):
        service = Setup_the_Gmail_API()
        try:
            message = service.users().messages().get(userId=user_id, id=msg_id).execute()

            print ('Message snippet: %s' % message['snippet'])

            return message
        except (errors.HttpError, error):
            print ('An error occurred: %s' % error)

    def gmail_핵심정보_원본_저장(m_id_li):
        tbl명 = 'gmail_핵심정보_원본'

        for m_id in m_id_li:
            message = GetMessage(m_id)
            m_snippet = message['snippet']
            message_jn = json_normalize(message)
            p_headers = pd.DataFrame( message_jn['payload.headers'][0] )

            p_headers = p_headers[ p_headers.name.isin(['From','To','Date','Subject']) ]
            p_headers_dicli = p_headers.to_dict('records')
            dic = {
                'm_id':m_id,
                'm_snippet':m_snippet,
            }
            for ph_dic in p_headers_dicli:
                dic[ph_dic['name']] = ph_dic['value']

            # 저장
            db[tbl명].insert_one(dic)

        # 백업

        mg.테이블의_중복제거(db명, tbl명)
        mg.테이블의_백업csv_생성(db명, tbl명, data_path)

    def gmail_핵심정보_원본_파싱(df):
        df = df.rename(columns={
            'Date':'일시',
            'From':'발신자',
            'To':'수신자',
            'Subject':'제목',
            'm_snippet':'본문요약',
        })
        df = __발신자_문자열_파싱후_새로운_컬럼으로_추가(df)
        return df

    def __발신자_문자열_파싱후_새로운_컬럼으로_추가(df):
        # 발신자 --> 발신_이름, 발신_메일주소->(발신_메일계정, 발신_메일도메인)

        df0 = df.copy()
        # 두가지 타입으로 나누기
        df1 = df[ df['발신자'].str.contains(pat='<',case=False,na=False) ]
        df2 = df[ ~df['발신자'].str.contains(pat='<',case=False,na=False) ]

        # 개수가 맞는지 확인
        df0_len = len(df0)
        df1_len = len(df1)
        df2_len = len(df2)
        print('원본 df 길이 : ',df0_len)
        print('발신자 컬럼에 "<" 기호를 포함한 "df1" 의 길이 : ',df1_len)
        print('발신자 컬럼에 "<" 기호를 미포함한 "df2" 의 길이 : ',df2_len)
        if df0_len == df1_len + df2_len:
            print('분리된 길이의 합 {}은 원본의 길이 {}와 같다.'.format(df1_len + df2_len, df0_len))


        df1_1 = df1['발신자'].str.partition('<').loc[:,[0,2]].rename(columns={0:'발신_이름',2:'발신_메일주소'})
        df1_1['발신_이름'] = df1_1['발신_이름'].apply(lambda x: '_' if x == '' else x)
        df1_1['발신_메일주소'] = df1_1['발신_메일주소'].apply(lambda x: x.replace('>',''))
        df1_2 = df1_1['발신_메일주소'].str.partition('@').loc[:,[0,2]].rename(columns={0:'발신_메일계정',2:'발신_메일도메인'})
        df1 = pd.concat([df1, df1_1, df1_2], axis=1)
        print('\n df1.columns :\n', sorted(list(df1.columns)))
        #df1 = df1.groupby(['발신_이름','발신_메일주소','발신자','발신_메일계정','발신_메일도메인']).count()
        #return df1


        df2 = df2.assign(발신_메일주소=df2['발신자'])
        df2 = df2.assign(발신_이름='_')
        df2_1 = df2['발신_메일주소'].str.partition('@').loc[:,[0,2]].rename(columns={0:'발신_메일계정',2:'발신_메일도메인'})
        df2 = pd.concat([df2, df2_1], axis=1)
        print('\n df2.columns :\n', sorted(list(df2.columns)))
        #return df2.groupby(['발신_메일도메인','발신_메일계정','발신자']).count()

        # 합치기
        print('\n 리스트1과_리스트2의_교집합을_찾기 :\n', sorted(lh.리스트1과_리스트2의_교집합을_찾기(df1.columns, df2.columns)))
        print('\n 리스트1로부터_리스트2를_제거 :\n', sorted(lh.리스트1로부터_리스트2를_제거(df1.columns, df2.columns)))
        df = pd.concat([df1, df2], ignore_index=True)

        df = df.fillna('_')
        print('\n 최종 df 길이 : ',len(df))
        print('\n 최종 df 컬럼 :\n', list(df.columns))
        return df

import pandas as pd
from pymongo import MongoClient
from pandas.io.json import json_normalize
import sys
sys.path.append('/Users/sambong/p/lib/')
import list_handler as lh
import mongodb as mg
import df_handler as dh
from gmail import db명, data_path
mg_client = MongoClient()
db = mg_client[db명]
gmail_핵심정보_컬럼순서 = ['발신자','발신_이름','발신_메일주소','발신_메일계정','발신_메일도메인','수신자','일시','제목','본문요약','m_id','_id']

class Analyzer:

    def 분류정보를_덧붙인_gmail_핵심정보_df():
        df1 = 발신_메일도메인에_분류정보_덧붙이기()
        df2 = 발신_이름에_분류정보_덧붙이기()
        df = pd.concat([df1, df2])
        return df

    def 분류안된_gmail_핵심정보_df():
        df = 분류정보를_덧붙인_gmail_핵심정보_df()
        df = pd.DataFrame(list( db['gmail_핵심정보'].find({
            '_id':{'$nin':list(df['_id'])}
        }) ))
        return df

    def 메일도메인기준_분류정보_df():
        #메일도메인_분류값li_분류명_결합
        df1 = json_normalize(
            list( mg_client['데이터맵']['분류명_분류값li_맵'].find() ), '분류값_li', ['분류명']
        ).rename(columns={0:'분류값'})
        df2 = json_normalize(list( db['메일도메인_분류값li_맵'].find() ), '분류값_li', ['메일도메인']).rename(columns={0:'분류값'})

        df = df2.join(df1.set_index('분류값'), on='분류값')
        df = df.fillna('_')
        return df

    def 발신_메일도메인에_분류정보_덧붙이기():
        메일도메인_li = list( db['메일도메인_분류값li_맵'].distinct('메일도메인') )
        df = pd.DataFrame(list( db['gmail_핵심정보'].find({'발신_메일도메인':{'$in':메일도메인_li}}) ))

        df = df.join(메일도메인기준_분류정보_df().set_index('메일도메인'), on='발신_메일도메인')
        df = df.fillna('_')
        return df

    def 발신이름기준_분류정보_df():
        #메일도메인_분류값li_분류명_결합
        df = json_normalize(list( db['발신이름_분류값li_맵'].find() ), '분류값_li', ['발신이름']).rename(columns={0:'분류값'})
        df1  = json_normalize(
            list( mg_client['데이터맵']['분류명_분류값li_맵'].find() ), '분류값_li', ['분류명']
        ).rename(columns={0:'분류값'})

        df = df.join(df1.set_index('분류값'), on='분류값')
        df = df.fillna('_')
        return df

    def 발신_이름에_분류정보_덧붙이기():
        발신이름_li = list( db['발신이름_분류값li_맵'].distinct('발신이름') )
        df = pd.DataFrame(list( db['gmail_핵심정보'].find({'발신_이름':{'$in':발신이름_li}}) ))

        df = df.join(발신이름기준_분류정보_df().set_index('발신이름'), on='발신_이름')
        df = df.fillna('_')
        return df

    def 발신자의_이름과_메일주소와_메일계정과_메일도메인_간의_연계성(df):
        df1 = df.copy()
        df1 = df1.loc[:, ['발신_이름','발신_메일주소','발신_메일계정','발신_메일도메인']]
        df1 = df1.drop_duplicates()

        print('발신_이름 : ', len( list(df1.발신_이름.unique()) ) )
        print('발신_메일주소 : ', len( list(df1.발신_메일주소.unique()) ) )
        print('발신_메일계정 : ', len( list(df1.발신_메일계정.unique()) ) )
        print('발신_메일도메인 : ', len( list(df1.발신_메일도메인.unique()) ) )
        return df1

    def df에_분류맵을_적용(df, 검색컬럼):
        def 키워드_기준으로_분류명_컬럼을_df에_추가(df, 검색컬럼, 키워드, 분류명):
            df1 = df[ df[검색컬럼].str.contains(pat=키워드,case=False,na=False) ]
            df1 = df1.assign(분류 = 분류명)

            if ('분류' in list(df.columns))==False:
                df = df.assign(분류 = '_')

            df.update(df1)
            return df

        df1 = df.copy()
        분류_df = pd.DataFrame(list( db.분류맵.find({},{'_id':False}) ))
        분류_df = json_normalize(분류_df.to_dict('records'),'키워드_li',['분류명']).rename(columns={0:'키워드'})

        분류_df의_값_tpl_li = list(분류_df.to_records())
        for 값_tpl in 분류_df의_값_tpl_li:
            키워드 = 값_tpl[1]
            분류명 = 값_tpl[2]
            df1 = 키워드_기준으로_분류명_컬럼을_df에_추가(df1, 검색컬럼, 키워드, 분류명)

        return df1
