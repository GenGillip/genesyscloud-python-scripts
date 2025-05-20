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
        # authApi = PureCloudPlatformClientV2.AuthorizationApi(apiclient)
        # print(authApi.get_authorization_permissions())
        ret = apiclient.access_token
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    return ret

# === Get Groups ===
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

# === Get Subjects ===
def getSubject(token, region, groupId):
    role_map = {}
    role_count = 0
    PureCloudPlatformClientV2.configuration.access_token = token
    PureCloudPlatformClientV2.configuration.host = region.get_api_host()
    # create an instance of the API class
    usersApi_instance = PureCloudPlatformClientV2.UsersApi()
    # subject_id = 'subject_id_example' # str | Subject ID (user or group)
    include_duplicates = False # bool | Include multiple entries with the same role and division but different subjects (optional) (default to False)
    try:
        # Get the list of Roles for the Group ID.
        api_response = usersApi_instance.get_authorization_subject(groupId, include_duplicates=include_duplicates).to_json()
        grants = json.loads(api_response)['grants']
        for grant in grants:
            role_name = grant.get("role", {}).get("name")
            division = grant.get("division", {})
            division_id = division.get("id")
            division_name = "*" if division_id == "*" else division.get("name")

            if role_name and division_name:
                role_map.setdefault(role_name, set()).add(division_name)
        role_count = len(role_map) 
    except ApiException as e:
        print("Exception when calling UsersApi->get_users: %s\n" % e)
    return [
        {
            "role": role,
            "divisions": ", ".join(sorted(divisions))
        }
        for role, divisions in role_map.items()
    ], role_count

# === Write CSV ===  
def write_json_to_csv(json_data, csv_filename):
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'name', 'rolesCount', 'role', 'divisions']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for group in json_data:
            group_id = group.get("id", "")
            name = group.get("name", "")
            roles_count = group.get("rolesCount", 0)
            subjects = group.get("subject", [])

            if not subjects:
                writer.writerow({
                    "id": group_id,
                    "name": name,
                    "rolesCount": roles_count,
                    "role": "",
                    "divisions": ""
                })
            else:
                for i, subj in enumerate(subjects):
                    writer.writerow({
                        "id": group_id, # if i == 0 else ""
                        "name": name,
                        "rolesCount": roles_count, # if i == 0 else ""
                        "role": subj.get("role", ""),
                        "divisions": subj.get("divisions", "")
                    })

def main():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    region = regionSelect(gcxRegion)
    gcxToken = getToken(clientId, clientSecret, region)
    print(f'Token Recived: {gcxToken}')
    groupList, groupCount = getGroups(gcxToken, region)
    print(f'Groups Count: {groupCount}')
    for group in groupList:
        group['subject'], group['rolesCount'] = getSubject(gcxToken, region, group['id'])
        # print(f'Group: {group}')

    # with open(f'Groups_Output_{timestamp}.json', "w") as outfile:
    #     json.dump(groupList, outfile, indent=2)
    
    write_json_to_csv(groupList, f'Groups_Output_{timestamp}.csv')

# === Run Script ===
if __name__ == "__main__":
    main()