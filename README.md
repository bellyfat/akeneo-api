# Akeno API Client Library

# Install
```
pip install virtualenv
virtualenv <your-env>
source <your-env>/bin/activate
<your-env>/bin/pip install git+ssh://git@github.com/joshmuente/akeneo-api@<TAG_VERSION>
```

## Without virtualenv
`pip install git+ssh://git@github.com/joshmuente/akeneo-api@<TAG_VERSION>`

# Usage
```
from akeneoapi import Api

akeneo = Api(url, username, password, client_id, secret)
```
