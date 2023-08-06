# dockercomposeHelp
dockercomposeHelp is a python package for building complex docker-compose files quickly and without errors. It only supports Compose file version 3.
## Usage:
It follows a very simple usage procedure:
```python
from dockerCompose.compose import Compose
my_compose = Compose() #create a compose instance
service_db = Service('db') #create a service instance
service_db.image('mysql')
service_db.command('--default-authentication-plugin=mysql_native_password')
service_db.restart('always')
service_db.environment({'MYSQL_ROOT_PASSWORD': 'example'})
service_db.ports(['8080:8080'])

my_compose.add_service(service_db) #add service to compose
my_compose.make_compose() #output compose
```
The above code snippet will produce the following yaml file:
```yaml
services:
  db:
    command: --default-authentication-plugin=mysql_native_password
    environment:
      MYSQL_ROOT_PASSWORD: example
    image: mysql
    ports:
      - 8080:8080
    restart: always
version: '3.7'
```

## To be added:
 - service.deploy.rollback_config
 - service.deploy.update_config
 - service.pid
 - service.secrets
 - service.security_opt
 - service.stop_grace_period
 - service.stop_signal
 - service.sysctls
 - service.tmpfs
 - service.ulimits
 - service.userns_mode
## Unsupported:
 - service.links -- LEGACY FEATURE