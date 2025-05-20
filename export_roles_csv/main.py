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

def getRoles(token, region):
    roles = []
    roles_count = 0
    PureCloudPlatformClientV2.configuration.access_token = token
    PureCloudPlatformClientV2.configuration.host = region.get_api_host()
    # create an instance of the API class
    api_instance = PureCloudPlatformClientV2.AuthorizationApi()
    page_size = 50 # int | The total page size requested (optional) (default to 25)
    # page_number = 1 # int | The page number requested (optional) (default to 1)
    # sort_by = 'sort_by_example' # str | variable name requested to sort by (optional)
    # expand = ['expand_example'] # list[str] | variable name requested by expand list (optional)
    # next_page = 'next_page_example' # str | next page token (optional)
    # previous_page = 'previous_page_example' # str | Previous page token (optional)
    # name = 'name_example' # str |  (optional)
    # permission = ['permission_example'] # list[str] |  (optional)
    # default_role_id = ['default_role_id_example'] # list[str] |  (optional)
    user_count = True # bool |  (optional) (default to True)
    # id = ['id_example'] # list[str] | id (optional)
    try:
        loop = True
        page = 1
        while loop:
            # Get the list of available users.
            api_response = api_instance.get_authorization_roles(page_size=page_size, page_number=page, user_count=user_count).to_json()
            entities = json.loads(api_response)['entities']
            pageCount = json.loads(api_response)['page_count']
            for entity in entities:
                roles.append(entity)
            print(f'Page {page} of {pageCount}')
            page += 1
            if page > pageCount:
                loop = False
        roles_count = len(roles)
    except ApiException as e:
        print("Exception when calling AuthorizationApi->get_authorization_roles: %s\n" % e)
    return roles, roles_count

def write_json_to_csv(json_data, csv_filename):
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['roleId', 'roleName', 'roleDescription', 'defaultRoleId', 'usersCount', 'base', 'default', 'domain', 'entityName', 'actionSet', 'allowConditions']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entity in json_data:
            entity_id = entity.get("id", "")
            entity_name = entity.get("name", "")
            entity_description = entity.get("description", "")
            default_role = entity.get("defaultRoleId", "")
            users_count = entity.get("rolesCount", 0)
            permissionPolicies = entity.get("permission_policies", [])
            base = entity.get("base", False)
            default = entity.get("default", False)
            if not permissionPolicies:
                writer.writerow({
                    "roleId": entity_id,
                    "roleName": entity_name,
                    "roleDescription": entity_description,
                    "defaultRoleId": default_role,
                    "usersCount": users_count,
                    "base": base,
                    "default": default,
                    "domain": "",
                    "entityName": "",
                    "actionSet": "",
                    "allowConditions": ""
                })
            else:
                for i, p in enumerate(permissionPolicies):
                    writer.writerow({
                        "roleId": entity_id, # if i == 0 else ""
                        "roleName": entity_name,
                        "roleDescription": entity_description, # if i == 0 else ""
                        "defaultRoleId": default_role, # if i == 0 else ""
                        "usersCount": users_count, # if i == 0 else ""
                        "base": base, # if i == 0 else ""
                        "default": default, # if i == 0 else ""
                        "domain": p.get("domain", ""),
                        "entityName": p.get("entity_name", ""),
                        "actionSet": p.get("action_set", ""),
                        "allowConditions": p.get("allow_conditions", False)
                    })

def main():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    region = regionSelect(gcxRegion)
    gcxToken = getToken(clientId, clientSecret, region)
    print(f'Token Recived: {gcxToken}')
    roles_list, roles_count = getRoles(gcxToken, region)
    print(f'Groups Count: {roles_count}')
    
    # with open(f'Roles_Output_{timestamp}.json', "w") as outfile:
    #     json.dump(roles_list, outfile, indent=2)
    
    write_json_to_csv(roles_list, f'Roles_Output_{timestamp}.csv')

# === Run Script ===
if __name__ == "__main__":
    main()