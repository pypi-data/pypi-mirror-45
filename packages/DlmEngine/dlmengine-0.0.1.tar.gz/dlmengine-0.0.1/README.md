Introduction
------------
Distributes Lock Manger, build on top of Python, MongoDB and Redis.

The tool is targeted for system operation tasks, where you need to make sure that only
a single system, or instance of a application, is performing a task at the same time.

The REST API is fully described using the OpenAPI specification.

It has an internal user database, and allows the usage of API tokens, instead of username and passwords.

For usage examples, please see the documentation of the CLI.


Installing
----------
dlmengine requires at least python 3.5, und is only tested linux.

pip install dlmengine

the configuration is expected to be placed in /etc/dlmengine/config.ini

an example configuration looks like this

```
[main]
host = 0.0.0.0
port = 9000

[file:logging]
acc_log = /var/log/dlmengine/access.log
acc_retention = 7
app_log = /var/log/dlmengine/app.log
app_retention = 7
app_loglevel = DEBUG

[session:redispool]
host = 127.0.0.1
pass = password

[main:mongopool]
hosts = 127.0.0.1
db = dlmengine
pass = dlmengine
user = password

[locks:mongocoll]
coll = locks
pool = main

[permissions:mongocoll]
coll = permissions
pool = main

[users:mongocoll]
coll = users
pool = main

[users_credentials:mongocoll]
coll = users_credentials
pool = main

```

Running
-------
HTTPS is not supported, it is suggested run DLMEngine behind a HTTP reverse proxy, like Apache or NGINX.

```
dlm_engine --help
usage: dlm_engine [-h] [--cfg CFG] {run,indices,create_admin} ...

DLM Engine Rest API

positional arguments:
  {run,indices,create_admin}
                        commands
    run                 Start DLM Engine Rest API API
    indices             create indices
    create_admin        create default admin user

optional arguments:
  -h, --help            show this help message and exit
  --cfg CFG             Full path to configuration

```

First you have to call the indices argument, which will setup all required indices in mongodb.

Next call the create_admin command, this will create a user named "admin" with the password "password".

After this you can run the Rest API using the run argument.

There also is a OpenAPI Documentation available at http://localhost:9000/static/swagger/index.html that can be used to explore the api.

or more conveniently install and use the CLI.

also see https://github.com/schlitzered/DLMEngineCLI or https://github.com/schlitzered/DLMEngineUpdater




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