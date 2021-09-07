# ziprepo-server

## Installation

### Configuration file

Create configuration file:

```json
{
	"server" : {
		"port" : 7001
	},
	"keys" : {
		"readonly" : [
            {
				"key" : "some_key",
				"name": "readonly_user_name"
			}
		],
		"readwrite" : [
            {
				"key" : "some_key2",
				"name": "readwrite_user_name"
			}
		]
	},
	"repository" : {
		"dataFolder" : "test_data_folder"
	},
    "retention": {
		"maxVersionsStoredPerPackage": "3",
		"packagesCleanIntervalHours": "24"
	},
    "logsFolder" : "/var/log/opt/zippero-server"
}
```

**server** - server configuration like port

**keys** - hash with two keys readonly and readwrite which are arrays of 
hashes with following keys:
- **key** - base64 encoded hashed password with salt created using bcrypt

To create entries you can use `hash-password.py` script. For example:

```
pipenv run python hash-password.py some_password
```

- **name** - name of a key for reference purposes for example name of a user

If no keys specified then security is turned off and anyone can access api.

**repository** - repository data configuration 

**retention** - packages retention policies
  - `maxVersionsStoredPerPackage` - sets how many last packages needs to be stored. Oldest packages will be removed till limit
  - `packagesCleanIntervalHours` - sets interval time in hours between cleanups of server
