# Getting started

The SMS API sends SMS messages to Australian mobile phones in a single request. This API allows you to send and receive messages. You can also query the status of a previously sent SMS message.

## Authentication

This API uses OAuth v2 Bearer Token for its authentication.

The parameters that are needed to be sent for this type of authentication are as follows:

+ `CONSUMER_KEY` - your consumer key

+ `CONSUMER_SECRET` - your consumer secret

## How to Build


You must have Python ```2 >=2.7.9``` or Python ```3 >=3.4``` installed on your system to install and run this SDK. This SDK package depends on other Python packages like nose, jsonpickle etc. 
These dependencies are defined in the ```requirements.txt``` file that comes with the SDK.
To resolve these dependencies, you can use the PIP Dependency manager. Install it by following steps at [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/).

Python and PIP executables should be defined in your PATH. Open command prompt and type ```pip --version```.
This should display the version of the PIP Dependency Manager installed if your installation was successful and the paths are properly defined.

* Using command line, navigate to the directory containing the generated files (including ```requirements.txt```) for the SDK.
* Run the command ```pip install -r requirements.txt```. This should install all the required dependencies.

![Building SDK - Step 1](https://apidocs.io/illustration/python?step=installDependencies&workspaceFolder=Aazar%20Khan%20Telstra%20SMS%20API-Python)


## How to Use

The following section explains how to use the Aazarkhantelstrasmsapi SDK package in a new project.

### 1. Open Project in an IDE

Open up a Python IDE like PyCharm. The basic workflow presented here is also applicable if you prefer using a different editor or IDE.

![Open project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=pyCharm)

Click on ```Open``` in PyCharm to browse to your generated SDK directory and then click ```OK```.

![Open project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=openProject0&workspaceFolder=Aazar%20Khan%20Telstra%20SMS%20API-Python)     

The project files will be displayed in the side bar as follows:

![Open project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=openProject1&workspaceFolder=Aazar%20Khan%20Telstra%20SMS%20API-Python&projectName=testinweweewewe)     

### 2. Add a new Test Project

Create a new directory by right clicking on the solution name as shown below:

![Add a new project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=createDirectory&workspaceFolder=Aazar%20Khan%20Telstra%20SMS%20API-Python&projectName=testinweweewewe)

Name the directory as "test"

![Add a new project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=nameDirectory)
   
Add a python file to this project with the name "testsdk"

![Add a new project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=createFile&workspaceFolder=Aazar%20Khan%20Telstra%20SMS%20API-Python&projectName=testinweweewewe)

Name it "testsdk"

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=nameFile)

In your python file you will be required to import the generated python library using the following code lines

```Python
from testinweweewewe.testinweweewewe_client import TestinweweeweweClient
```

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=projectFiles&workspaceFolder=Aazar%20Khan%20Telstra%20SMS%20API-Python&libraryName=testinweweewewe.testinweweewewe_client&projectName=testinweweewewe&className=TestinweweeweweClient)

After this you can write code to instantiate an API client object, get a controller object and  make API calls. Sample code is given in the subsequent sections.

### 3. Run the Test Project

To run the file within your test project, right click on your Python file inside your Test project and click on ```Run```

![Run Test Project - Step 1](https://apidocs.io/illustration/python?step=runProject&workspaceFolder=Aazar%20Khan%20Telstra%20SMS%20API-Python&libraryName=testinweweewewe.testinweweewewe_client&projectName=testinweweewewe&className=TestinweweeweweClient)


## How to Test

You can test the generated SDK and the server with automatically generated test
cases. unittest is used as the testing framework and nose is used as the test
runner. You can run the tests as follows:

  1. From terminal/cmd navigate to the root directory of the SDK.
  2. Invoke ```pip install -r test-requirements.txt```
  3. Invoke ```nosetests```

## Initialization

### Authentication
In order to setup authentication and initialization of the API client, you need the following information.

| Parameter | Description |
|-----------|-------------|
| o_auth_access_token | OAuth 2.0 Access Token |



API client can be initialized as following.

```python
# Configuration parameters and credentials
o_auth_access_token = 'o_auth_access_token' # OAuth 2.0 Access Token

client = TestinweweeweweClient(o_auth_access_token)
```



# Class Reference

## <a name="list_of_controllers"></a>List of Controllers

* [APIController](#api_controller)

## <a name="api_controller"></a>![Class: ](https://apidocs.io/img/class.png ".APIController") APIController

### Get controller instance

An instance of the ``` APIController ``` class can be accessed from the API Client.

```python
 client_controller = client.client
```

### <a name="create_send_sms"></a>![Method: ](https://apidocs.io/img/method.png ".APIController.create_send_sms") create_send_sms

> The Send SMS method sends an SMS message to a single Australian mobile phone number. A unique identifier (messageId) returned in the response, which may be used to query for the delivery status of the message.

```python
def create_send_sms(self,
                        content_type,
                        body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| contentType |  ``` Required ```  | TODO: Add a parameter description |
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
content_type = 'application/json'
body_value = "{  \"to\": \"\",  \"body\": \"\"}"
body = json.loads(body_value)

result = client_controller.create_send_sms(content_type, body)

```


### <a name="get_authentication"></a>![Method: ](https://apidocs.io/img/method.png ".APIController.get_authentication") get_authentication

> To get an OAuth 2.0 Authentication token, pass through your Consumer Key and Consumer Secret that you received when you registered for the SMS API key. The grant_type should be left as ?client_credentials? and the scope as ?SMS?. The token will expire in one hour.

```python
def get_authentication(self,
                           client_id,
                           client_secret,
                           grant_type=None,
                           scope=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| clientId |  ``` Required ```  | client's id |
| clientSecret |  ``` Required ```  | client's secret |
| grantType |  ``` Optional ```  | value set by default |
| scope |  ``` Optional ```  | value set by default |



#### Example Usage

```python
client_id = 'client_id'
client_secret = 'client_secret'
grant_type = 'grant_type'
scope = 'scope'

result = client_controller.get_authentication(client_id, client_secret, grant_type, scope)

```


### <a name="get_message_response"></a>![Method: ](https://apidocs.io/img/method.png ".APIController.get_message_response") get_message_response

> The recipients of your SMS messages can send a reply which you can retrieve using the Get Message Response method. Pass through the unique identifier (messageId) returned as returned in the response from the Send SMS method and you will receive the reply and the timestamp.

```python
def get_message_response(self,
                             message_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| mESSAGEID |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
message_id = 'MESSAGE_ID'

result = client_controller.get_message_response(message_id)

```


### <a name="get_message_status"></a>![Method: ](https://apidocs.io/img/method.png ".APIController.get_message_status") get_message_status

> Use the unique identifier (messageId) returned as returned in the response from the Send SMS method to get the status.

```python
def get_message_status(self)
```

#### Example Usage

```python

result = client_controller.get_message_status()

```


[Back to List of Controllers](#list_of_controllers)



