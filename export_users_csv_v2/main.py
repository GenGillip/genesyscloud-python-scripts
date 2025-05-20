import os
import sys
import json
import csv
import time
from datetime import datetime
import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException

with open(f'config.json') as configFile:
    jConfig = json.load(configFile)

clientId = jConfig['clientId']
clientSecret = jConfig['clientSecret']
gcxRegion = jConfig['region']

def regionSelect(region):
    if region == 'mypurecloud.com':
        return PureCloudPlatformClientV2.PureCloudRegionHosts.us_east_1
    elif region == 'usw2.pure.cloud':
        return PureCloudPlatformClientV2.PureCloudRegionHosts.us_west_2
    elif region == 'use2.us-gov-pure.cloud':
        return PureCloudPlatformClientV2.PureCloudRegionHosts.us_east_2
    elif region == 'cac1.pure.cloud':
        return PureCloudPlatformClientV2.PureCloudRegionHosts.ca_central_1
    elif region == 'mypurecloud.ie':
        return PureCloudPlatformClientV2.PureCloudRegionHosts.eu_west_1
    elif region == 'euw2.pure.cloud':
        return PureCloudPlatformClientV2.PureCloudRegionHosts.eu_west_2
    elif region == 'mypurecloud.de':
        return PureCloudPlatformClientV2.PureCloudRegionHosts.eu_central_1
    elif region == 'aps1.pure.cloud':
        return PureCloudPlatformClientV2.PureCloudRegionHosts.ap_south_1
    elif region == 'mypurecloud.jp':
        return PureCloudPlatformClientV2.PureCloudRegionHosts.ap_northeast_1
    elif region == 'apne2.pure.cloud':
        return PureCloudPlatformClientV2.PureCloudRegionHosts.ap_northeast_2
    elif region == 'mypurecloud.com.au':
        return PureCloudPlatformClientV2.PureCloudRegionHosts.ap_southeast_2
    elif region == 'sae1.pure.cloud':
        return PureCloudPlatformClientV2.PureCloudRegionHosts.sa_east_1
    else:
        return PureCloudPlatformClientV2.PureCloudRegionHosts.us_east_1

def getToken(clientId, clientSecret, region):
    ret = ''
    try:
        PureCloudPlatformClientV2.configuration.host = region.get_api_host()
        apiclient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(clientId, clientSecret)
        ret = apiclient.access_token
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    return ret

def search_json(json_list, key, value):
    """
    Search for objects in a JSON list where the specified key matches the given value.

    Parameters:
    - json_list (list): The list of JSON objects to search.
    - key (str): The key to search for.
    - value: The value to search for.

    Returns:
    - list: A list of matching JSON objects.
    """
    return [obj for obj in json_list if obj.get(key) == value]

def getGroups(token, region):
    groupList = []
    groupCount = 0
    PureCloudPlatformClientV2.configuration.access_token = token
    PureCloudPlatformClientV2.configuration.host = region.get_api_host()
    api_instance = PureCloudPlatformClientV2.GroupsApi()
    page_size = 100 # int | Page size (optional) (default to 25)
    # page_number = 1 # int | Page number (optional) (default to 1)
    sort_order = 'ASC' # str | Ascending or descending sort order (optional) (default to 'ASC')
    try:
        loop = True
        page = 1
        while loop:
            # Get a group list
            api_response = api_instance.get_groups(page_size=page_size, page_number=page, sort_order=sort_order).to_json()
            entities = json.loads(api_response)['entities']
            pageCount = json.loads(api_response)['page_count']
            for group in entities:
                groupList.append({"id": group['id'], "name": group['name']})
                groupCount += 1
            print(f'Page {page} of {pageCount}')
            page += 1
            if page > pageCount:
                loop = False
    except ApiException as e:
        print("Exception when calling GroupsApi->get_groups: %s\n" % e)
    return groupList, groupCount

def getUser(token, region, groupList):
    users = []
    userCount = 0
    user_json = []
    PureCloudPlatformClientV2.configuration.access_token = token
    PureCloudPlatformClientV2.configuration.host = region.get_api_host()
    # create an instance of the API class
    usersApi_instance = PureCloudPlatformClientV2.UsersApi()
    page_size = 100 # int | Page size (optional) (default to 25)
    # page_number = 1 # int | Page number (optional) (default to 1)
    # id = ['id_example'] # list[str] | A list of user IDs to fetch by bulk (optional)
    # jabber_id = ['jabber_id_example'] # list[str] | A list of jabberIds to fetch by bulk (cannot be used with the \"id\" parameter) (optional)
    #sort_order = 'ASC' # str | Ascending or descending sort order (optional) (default to 'ASC')
    expand = ['groups', 'skills'] # list[str] | Which fields, if any, to expand (optional)
    #integration_presence_source = 'integration_presence_source_example' # str | Gets an integration presence for users instead of their defaults. This parameter will only be used when presence is provided as an \"expand\". When using this parameter the maximum number of users that can be returned is 100. (optional)
    state = 'active' # str | Only list users of this state (optional) (default to 'active')
    try:
        loop = True
        page = 1
        while loop:
            # Get the list of available users.
            api_response = usersApi_instance.get_users(page_size=page_size, page_number=page, expand=expand, state=state).to_json()
            entities = json.loads(api_response)['entities']
            pageCount = json.loads(api_response)['page_count']
            for entity in entities:
                userGroups = entity['groups']
                usrGrpList = []
                usrGrpString = ''
                # print(f'User Groups: {userGroups}')
                if len(userGroups) > 0:
                    for group in userGroups:
                        groupName = search_json(groupList, 'id', group['id'])
                        usrGrpList.append(groupName[0]['name'])
                        separator = ','
                        usrGrpString = separator.join(map(str, usrGrpList))
                found_extension = None
                if "addresses" in entity and isinstance(entity["addresses"], list):
                    for address_item in entity["addresses"]:
                        if address_item.get("extension") is not None:
                            found_extension = address_item["extension"]
                            break  # Stop processing once a non-null extension is found
                
                users.append({"id": entity['id'], "name": entity['name'], "email": entity['username'], "extension": found_extension, "groups": usrGrpString})
                user_json.append(entity)
                userCount += 1
            # print(userEntities[0]['id'])
            print(f'Page {page} of {pageCount}')
            page += 1
            if page > pageCount:
                loop = False
        # print(api_response['entities'].count())
    except ApiException as e:
        print("Exception when calling UsersApi->get_users: %s\n" % e)
    return users, userCount, user_json

def writeCsv(json_data, csv_filename):
    print()
    data_file = open(csv_filename, mode='w', newline='', encoding='utf-8')
    csv_writer = csv.writer(data_file)
    count = 0
    for entity in json_data:
        if count == 0:
            header = entity.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(entity.values())
    data_file.close()

def main():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    region = regionSelect(gcxRegion)
    gcxToken = getToken(clientId, clientSecret, region)
    print(f'Token Recived: {gcxToken}')
    groupList, groupCount = getGroups(gcxToken, region)
    print(f'Groups Count: {groupCount}')
    userList, userCount, user_json  = getUser(gcxToken, region, groupList)
    print(f'Users Count: {userCount}')

    # with open(f'Users_Output_{timestamp}.json', "w") as outfile:
    #     json.dump(user_json, outfile, indent=2)
  
    writeCsv(userList, f'Users_Output_{timestamp}.csv')

# === Run Script ===
if __name__ == "__main__":
    main()