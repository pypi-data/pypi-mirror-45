# ClientDOAPI

This is a module to manage Digital Ocean API v2

You can manage:
* Account info
* Domains (Create, get, delete)
* Domain records (Create, Get record ID, Delete)
* TODO: other endpoints available from DO

[API Reference from Digital Ocean](https://developers.digitalocean.com/documentation/v2/)

## Example:


### Get info from account
```
import clientdoapi as cdo
import json

client = cdoapi.ClientDOApi("tokenfromDigitalOcean")

try:
    info = client.get_account_info()
    print(info.droplet_limit)
    print(info.email)
    print(info.uuid)
    #or get the object as a dictionary:
    info_dict = info.to_json()
    #so you can dump it to json
    json_obj = json.dumps(info_dict)
except Exception as identifier:
    print(identifier)
```

### Create Domain

```
try:
     #Returns a DomainDO object with ne info created
     new_domain = client.create_domain("testmydomain.com", "123.45.6.7")
     print(f"name: {new_domain.name}")
     print(f"name: {new_domain.ttl}")

 except Exception as e:
     print(e)
```
