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
			
		],
		"readwrite" : [
			
		]
	},
	"repository" : {
		"dataFolder" : "test_data_folder"
	}
}
```

**server** - server configuration like port

**keys** - hash with two keys readonly and readwrite which are arrays of strings 
each containing base64 encoded hashed passwords. 

To create entries you can use `hash-password.py` script.

If no keys specified then security is turned off and anyone can access api.

**repository** - repository data configuration 