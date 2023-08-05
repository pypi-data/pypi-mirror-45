Introduction
------------
This is the command line interface to the DLM Engine REST API.

it can be used to interact with all aspects of the API,
and also offers a convenient way to execute a command using DLM Engine 

Installing
----------

pip install dlmenginecli

the configuration is expected to be placed in ~/.dlm_engine_cli.ini

an example configuration looks like this

```
[main]
# optional path to the ca to sign the API ssl certificate
# ca = /path/to/ca.crt
endpoint = http://localhost:9000/api/v1/
secret_id = $SECRED_ID
secret = $SECRET
```

Usage
-----
Before you can use the CLI tool, you first need to acquire API credentials.

For this you create a dummy dlm_engine_cli.ini file, that contains placeholders
for secret_id and secret.

You can then use the CLI to acquire a secret_id and secret using the CLI:

```
dlm_engine_cli user_credentials add_login --user admin
Password: 
secret_id is: b3228145-c7dd-43fe-91b0-40dc25e2f60a
secret is: hFnR39FtLeTkfSGxQ9IyZX6-eGekgImRZu-xVSJbHHytCOiYM4UlTsNKegVXYuXyZlKs_j20V-nrWxmFluI.HqjiNysQ8WjsC9BBqA.huCFM-VLunmbBMjL.Mdz9-BwU
```

You then have to place these credentials in you dlm_engine_cli.ini file.

After this, you are able to use all other CLI sub commands.

Some sub commands require admin permissions, others can be used by non admin users.

The locks as well as the user sub commands, that relate to the current user (do not specify a user id), 
are accessible by non admin users.

All other sub commands require admin permissions.

Examples
--------

Create a non admin user:

```
dlm_engine_cli users add --id NonAdmin --email dummy@example.com --name "Non Admin User"
Password: 
   ID      admin        name              email      
=====================================================
NonAdmin   0       Non Admin User   dummy@example.com
```

List all currently hold locks:

```
dlm_engine_cli locks list
 ID          acquired_by                 acquired_since         
================================================================
dummy   schlitzer-XPS-13-9360   2019-04-20T16:18:57.124000+00:00

```

execute command using lock:


```
dlm_engine_cli shield --lock test_lock --cmd sleep 10
DEBUG - waiting is set to False
DEBUG - max wait time is set to 3600
INFO - trying to acquire: test_lock
DEBUG - http status_code is: 201
DEBUG - http_response is {'data': {'acquired_by': 'schlitzer-XPS-13-9360', 'id': 'test_lock', 'acquired_since': '2019-04-20T16:21:44.703000+00:00'}}
INFO - success acquiring lock
INFO - running command: ['sleep', '10']
INFO - finished running command: ['sleep', '10']
INFO - trying to release: test_lock
DEBUG - http status_code is: 200
DEBUG - http_response is None
INFO - success releasing lock
```

Author
------

Stephan Schultchen <stephan.schultchen@gmail.com>

License
-------

Unless stated otherwise on-file foreman-dlm-updater uses the MIT license,
check LICENSE file.

Contributing
------------

If you'd like to contribute, fork the project, make a patch and send a pull
request.