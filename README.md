# genesyscloud-python-scripts
Common python scripts that I have built


config.js
Each python app uses the config.js in the same directory to be able to authenticate with the Genesys Cloud Org.  The SDK uses Client Credentials configuration, if you need help creating the oAuth, that can be found here --> https://developer.genesys.cloud/authorization/platform-auth/guides/oauth/module-1-client-credentials.
You also need to know the URL Region your org is in, example is mypurecloud.com or usw2.pure.cloud.  The full list can be found here --> https://developer.genesys.cloud/platform/api/


Python 3.6 and Above
Will need to install the SDK dependecy --> pip install PureCloudPlatformClientV2