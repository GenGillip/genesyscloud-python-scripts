import json
import csv
import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException

with open(f'config.json') as configFile:
    jConfig = json.load(configFile)

clientId = jConfig['clientId']
clientSecret = jConfig['clientSecret']
gcxRegion = jConfig['region']
csvFileName = 'import.csv'

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

def searchUser(token, region, csvUsersList):
    usersList= []
    PureCloudPlatformClientV2.configuration.access_token = token
    PureCloudPlatformClientV2.configuration.host = region.get_api_host()
    # create an instance of the API class
    usersApi_instance = PureCloudPlatformClientV2.UsersApi()
    userCount = 0
    for user in csvUsersList:
        query = PureCloudPlatformClientV2.UserSearchCriteria()
        query.type = 'STARTS_WITH'
        query.value = user["email"]
        query.fields = ['username']
        query.operator = 'AND'
        body = PureCloudPlatformClientV2.UserSearchRequest()
        body.types = ['USERS']
        body.query = [query]
        try:
            # Search users
            api_response = usersApi_instance.post_users_search(body).to_json()
            total = json.loads(api_response)['total']
            if total > 0:
                if total < 1:
                    print(f'User: {user["email"]} returned to many results')
                else:
                    results = json.loads(api_response)['results']
                    user["id"] = results[0]["id"]
                    usersList.append(user)
                    userCount += 1
            else:
                print(f'User: {user["email"]} was not found')
        except ApiException as e:
            print("Exception when calling UsersApi->post_users_search: %s\n" % e)

    return usersList, userCount

def updateUserRing(token, region, userId, userRing, userEmail):
    PureCloudPlatformClientV2.configuration.access_token = token
    PureCloudPlatformClientV2.configuration.host = region.get_api_host()
    api_instance = PureCloudPlatformClientV2.VoicemailApi()
    user_id = userId # str | User ID
    body = PureCloudPlatformClientV2.VoicemailUserPolicy() # VoicemailUserPolicy | The user's voicemail policy
    body.alert_timeout_seconds = userRing # int
    try:
        # Update a user's voicemail policy
        api_response = api_instance.patch_voicemail_userpolicy(user_id, body).to_json()
        #print(api_response)
        print(f'User {userEmail} Timeout Seconds was udpated to {userRing} seconds')
    except ApiException as e:
        print("Exception when calling VoicemailApi->patch_voicemail_userpolicy: %s\n" % e)
    return

def readCsv():
    users = []
    with open(csvFileName, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            users.append({"email": row["email"], "ringSec": row["ring"]})
            line_count += 1
        print(f'CSV Processed {line_count} rows')
    return users

def main():
    region = regionSelect(gcxRegion)
    gcxToken = getToken(clientId, clientSecret, region)
    print(f'Token Recived: {gcxToken}')
    csvUsers = readCsv()
    users, count = searchUser(gcxToken, region, csvUsers)
    print(f'{count} Users that where found')
    for user in users:
        updateUserRing(gcxToken, region, user['id'], user['ringSec'], user['email'])
    print(f'Users Updated Finished!')

if __name__ == "__main__":
    main()