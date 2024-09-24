import json
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

def getPhone(token, region, station_Id):
    phone = {}
    PureCloudPlatformClientV2.configuration.access_token = token
    PureCloudPlatformClientV2.configuration.host = region.get_api_host()
    # create an instance of the API class
    api_instance = PureCloudPlatformClientV2.TelephonyProvidersEdgeApi()
    # page_number = 1 # int | Page number (optional) (default to 1)
    # page_size = 25 # int | Page size (optional) (default to 25)
    # sort_by = ''name'' # str | The field to sort by (optional) (default to 'name')
    # sort_order = ''ASC'' # str | Sort order (optional) (default to 'ASC')
    # site_id = 'site_id_example' # str | Filter by site.id (optional)
    # web_rtc_user_id = 'web_rtc_user_id_example' # str | Filter by webRtcUser.id (optional)
    # phone_base_settings_id = 'phone_base_settings_id_example' # str | Filter by phoneBaseSettings.id (optional)
    # lines_logged_in_user_id = 'lines_logged_in_user_id_example' # str | Filter by lines.loggedInUser.id (optional)
    # lines_default_for_user_id = 'lines_default_for_user_id_example' # str | Filter by lines.defaultForUser.id (optional)
    # phone_hardware_id = 'phone_hardware_id_example' # str | Filter by phone_hardwareId (optional)
    # lines_id = 'lines_id_example' # str | Filter by lines.id (optional)
    # lines_name = 'lines_name_example' # str | Filter by lines.name (optional)
    # name = 'name_example' # str | Name of the Phone to filter by, comma-separated (optional)
    # status_operational_status = 'status_operational_status_example' # str | The primary status to filter by (optional)
    # secondary_status_operational_status = 'secondary_status_operational_status_example' # str | The secondary status to filter by (optional)
    # expand = ['expand_example'] # list[str] | Fields to expand in the response, comma-separated (optional)
    # fields = ['fields_example'] # list[str] | Fields and properties to get, comma-separated (optional)
    try:
        api_response = api_instance.get_telephony_providers_edges_phones(lines_id=station_Id).to_json()
        # print(f'Phone Found {api_response}')
        phone = api_response
    except ApiException as e:
        print("Exception when calling TelephonyProvidersEdgeApi->get_telephony_providers_edges_phones: %s\n" % e)
    return phone

def delPhone(token, region, phoneId):
    success = False
    PureCloudPlatformClientV2.configuration.access_token = token
    PureCloudPlatformClientV2.configuration.host = region.get_api_host()
    # create an instance of the API class
    api_instance = PureCloudPlatformClientV2.TelephonyProvidersEdgeApi()
    try:
        api_instance.delete_telephony_providers_edges_phone(phoneId)
        success = True
    except ApiException as e:
        print("Exception when calling TelephonyProvidersEdgeApi->delete_telephony_providers_edges_phone: %s\n" % e)
    return success

def main():
    # run here
    region = regionSelect(gcxRegion)
    gcxToken = getToken(clientId, clientSecret, region)
    print(f'Token Recived: {gcxToken}')

    PureCloudPlatformClientV2.configuration.access_token = gcxToken
    PureCloudPlatformClientV2.configuration.host = region.get_api_host()
    # create an instance of the API class
    api_instance = PureCloudPlatformClientV2.StationsApi()
    page_size = 5 # int | Page size (optional) (default to 25)
    page_number = 1 # int | Page number (optional) (default to 1)
    # sort_by = ''name'' # str | Sort by (optional) (default to 'name')
    # name = 'name_example' # str | Name (optional)
    # user_selectable = 'user_selectable_example' # str | True for stations that the user can select otherwise false (optional)
    # web_rtc_user_id = 'web_rtc_user_id_example' # str | Filter for the webRtc station of the webRtcUserId (optional)
    # id = 'id_example' # str | Comma separated list of stationIds (optional)
    # line_appearance_id = 'line_appearance_id_example' # str | lineAppearanceId (optional)
    try:
        loop = True
        page = 1
        while loop:
            # Get a group list
            api_response = api_instance.get_stations(page_size=page_size, page_number=page).to_json()
            entities = json.loads(api_response)['entities']
            pageCount = json.loads(api_response)['page_count']
            # print(f'Stations Response {api_response}')
            for station in entities:
                if station['type'] == 'inin_webrtc_softphone':
                    if station['web_rtc_user_id'] == None:
                        print(f'station {station['name']} does not have a web rtc user')
                        findPhone = getPhone(gcxToken, region, station['id'])
                        pEntities = json.loads(findPhone)['entities']
                        pCount = json.loads(findPhone)['total']
                        if pCount == 1:
                            # print(f'Phone {pEntities[0]['name']} was located')
                            removed = delPhone(gcxToken, region, pEntities[0]['id'])
                            if removed is True:
                                print(f'station {station['name']} was removed from the organization')
                            else:
                                print(f'station {station['name']} was NOT removed from the organization')
                        else:
                            print(f'Phone {pEntities[0]['name']} could not be located')
                        
            print(f'Page {page} of {pageCount}')
            page += 1
            if page > pageCount:
                loop = False
    except ApiException as e:
        print("Exception when calling GroupsApi->get_groups: %s\n" % e)

if __name__ == "__main__":
    main()