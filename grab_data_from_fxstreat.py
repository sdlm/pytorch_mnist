import json
import time
from pprint import pprint

import requests

token = '4xLK5n8QtBBsWaUr6BKv06PW6VeuQNqF65015X8Se0BlVK3ZE46X_3RnxeAQNDiZTA8uVsh00UkM4AvNAMHv7fx' \
        'GO0q10YpGqJHhZYrOOr3QsXdr4PSGxVFFPCe6M6RLTEcksoBkTVQ_rLk0-3LL_0h7EoyGFJDzzoLa7-OiTXChcW' \
        '74IBThnICaj4KjvJclAf_qVNnme_HpEwsoJbZljjrr-3oNJxc10HueyZzSskTMVbjWQ8mOueKYL5PBK1KUPUUPd' \
        'ZKhpnNDDj_sqOvV1KqJNuP8wDTdv_O9SKL8SjQsMcj3dzfFEkIkcx0TUXfgkC4H2DA3oyeL_Vx4AjgdeMBNIH7T' \
        'hXs8-hErXce-I1jdy3KLhyHUqvcoVAmiljo5Awc3cGbe2r93rLVDP4hExFNHa6JI2poCBJvlN0KF4PgenlA7Kq6' \
        '_NZt4-Fk4mKU4fFBl_mgVRt9UFjoq4GjNDz-1GzcgWfZ3yyOakYEg2VYmTOKdVMw86FnSoFN7gW23I8193ux_DN' \
        'TtAtkRncF2c-qmDCNA_g0YviK1wrGOb34ZQCK-meh1DUd_TnVqJOeSREAvL5w4g4VzEvsCrzJ4hq7q4a0CmdSiX' \
        'evq8oYQeQSWIxt8vQdBdPbjuxz75YJ2AW6KrQL1S2mpisqtLTAeAH4yLCpfZ8BMs8BpJaQNd258D4heUnVSQ1di' \
        'tQcVngYvtBL_2aIuz1rc1fAAIXkK7zb3ksaQq48rCxZRUWGOGk5ZkSp3u-p3cQKGdpn8V4vbDb21WYMFKIeND_w' \
        '3Ui9yveLJXS9r5tOxQ1r8Vgq8GdCNasLmHo-zrTkMVi9bLwZKe4e4QtMI_5_MuF-EtEkS-UI7GNQShlyJ-AZeSj' \
        'XmBcAScFkFa3MW6ICBcAkkZKUbwa0FoXYBhjXXEKtGKQjqzYfYXn51Ph2CDXn24lENIjP3-3rN4rXyS5wnAi1VI' \
        'NB1148e3uvOMQuKQDrq7VlbeNlKQjp6k7nB7NK-Jt9qOuEtoNWTYMSz-XFb9N2_aDC6dUBSbZuQK9QKamvN-E4K' \
        'DivNCGQ1jMOoTDVLVSvWG6b7_RKVRM20hk9V7yQxznfwnuQauctVVtYtTMeK0YhjWFN3hIKCKdwKIi27diYZbHb' \
        'XtF707GibJxLuC2x5Xk2Rm2Ca1okO4rHQvJ3ECKOvn9vyHtvk9j3sjecqG7Q2Mb2mX_DVX6z_hRVQdJ1a9y29dZ' \
        'fRCyXVeIuRGQD91JTz9uvEY1O-nFheNrn7NzIeRASHrrx_7PArQMAupJsp4UvtA5OUIW60PCmSA8VMz7tYkE_up' \
        'm92jD5IhQknbkzBxwg0w-pj_xdcJKjVJDt6zpJo1zlKt-Djb8iRwMwphsZ7gT0kV7MKRejjByKnGTYPcBenhdTL' \
        'dFoGVJmAYoYIn7pbPS5Q01-gsd49Y6IZjbwN3QlBAGhhOdCxsDJgy0-AlZGTns4K98ubFZkULfp47ehP6mJRMAz' \
        'F9q-wf73EV4i8kcPv_pOecQX3Uphio9Nm_A-rRRq042TAVs3Qc-IQ1aDgl6LvCe5BXqurzfyauCEaQlcBxkCIUc' \
        '72qrXAPSVNZflkpnymrHqBPlDNDY8DrK8ahZLceDpMFVFydjrHAAike1ge15T7oVy7Lj-FhiSS0hOQJnYEeoOE-' \
        'GQIOZvzd56sr5pxqQKfTRC9hyjUL_1Dc6OfV_wonFxWzzNdaNBfDgyj25ubM3zZk4WYSNJJWYNvtm186akgFg5H' \
        'ftTvMPmV88OyGWDhdxn-tdSofmscOkvtZ7e9d_8dAyz5a05Xocqu7rV2UqeAFu3VccuMpyy8gvgL2EFMQYiMlxV' \
        '_9jkxTgJlS1JWRZ9aymDjs8QdRMclWy4LLA'

auth_headers={'Authorization': f'bearer {token}'}
url = 'https://subscriptions.fxstreet.com/v4/en-US/post/filter/GeneralFeed?page={page}'


if __name__ == '__main__':

    feeds = []

    i = 1
    while True:
        print(f'get page: {i}')
        resp = requests.get(url.format(page=i), headers=auth_headers)
        i += 1
        if resp.status_code != 200:
            break
        for feed in resp.json()['Values']:
            feeds.append({
                'company': feed['Company']['Name'],
                'tags': [t['Name'] for t in feed['Tags']] if feed['Tags'] else [],
                'timestamp': feed['PublicationDate'],
                'author': feed['Author']['Name'],
            })

        if i % 10 == 0:
            with open('data_temp.json', 'w') as outfile:
                json.dump(feeds, outfile)

        time.sleep(1)

        # if i == 500:
        #     print('we make 500 requests!!')
        #     break

    print(f'FINISH, collected {len(feeds)} feeds!')

    with open('data.json', 'w') as outfile:
        json.dump(feeds, outfile)
