
# Paradigm
This project include both basic and advanced usages which are implemented commonly
among projects.

Always come here to get the latest setup for development

- development
  - pyenv
  - gitignore
  - pre-commit
  - Makefile
- Docker
  - Dockerfile
  - Docker Compose
- Testing
  - Unit
  - Integration

## Makefile

| Make Recipe     | Description                                                   |
|-----------------|---------------------------------------------------------------|
| uninstall       | Uninstall the package                                         |
| clean           | Clean up unneeded stuff generated during build                |
| install         | Install package                                               |
| prune           | Clean up stuff generated by code linting and formatting tools |
| build-ci        | Build the docker image                                        |
| test            | Perform unit testing                                          |
| check-container | Run a container to check for its setup                        |


## Environment Variable
To run for local checking, may need environment variables below set:
- REQUESTS_CA_BUNDLE: usually "/etc/ssl/certs/ca-bundle.crt" to set up TLS
  > urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='<host url>',
  > port=443): Max retries exceeded with url: /RestApi/v1/Authentication/RequestToken
  > (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED]
  > certificate verify failed: unable to get local issuer certificate (_ssl.c:997)')))
