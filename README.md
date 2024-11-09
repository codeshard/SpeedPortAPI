<p style="text-align:center;">
  <strong>SpeedPort Rest Proxy</strong> <em>- Telekom Speedport Router REST Proxy</em>
</p>

---
[![codecov](https://img.shields.io/codecov/c/github/codeshard/speedport-proxy?logo=codecov&logoColor=white&style=for-the-badge)](https://codecov.io/gh/codeshard/speedport-proxy)
[![tests](https://img.shields.io/github/actions/workflow/status/codeshard/speedport-proxy/ci-tests.yaml?branch=main&label=tests&logo=github&logoColor=white&style=for-the-badge)](https://github.com/codeshard/speedport-proxy/actions/workflows/ci-tests.yaml)
![checks](https://img.shields.io/github/check-runs/codeshard/speedport-proxy/main?style=for-the-badge&logo=github&label=checks)
[![release](https://img.shields.io/github/actions/workflow/status/codeshard/speedport-proxy/ci-cd-docker.yaml?branch=main&label=release&logo=docker&logoColor=white&style=for-the-badge)](https://github.com/codeshard/speedport-proxy/actions/workflows/ci-cd-docker.yaml)

This is a FastAPI-based REST proxy for managing and accessing Telekom Speedport routers. This application provides an interface to communicate with the router’s internal APIs, making it easier to retrieve and modify settings through standardized REST endpoints.


## Features

- **Router Status**: Get real-time information about the router’s current status, including uptime, connection status, and connected devices.

## Requirements

- Docker / docker-compose.
- Telekom SpeedPort Router.
- Network access to the router from the machine running this proxy.


## Getting Started

### Download docker image

```bash
docker pull ghcr.io/codeshard/speedportapi:main
```

### Environment Variables
Create a .env file in the root directory to configure environment variables:

```dotenv
SPEEDPORT_HOST=192.168.1.1
SPEEDPORT_PASSWORD=your_password
```

### Docker Setup
Run the Docker container:

```bash
docker run -d --name speedport-proxy -p 8000:8000 --env-file .env speedport-proxy
```

or just pass the env vars to docker directly:



```bash
docker run -d --name speedport-proxy -p 8000:8000 -e SPEEDPORT_HOST='192.168.1.1' -e SPEEDPORT_PASSWORD='your_password' speedport-proxy
```

This will start the proxy on port 8000 of your host machine.


## Usage
The application exposes several endpoints to interact with your SpeedPort router.

- GET /router/status

  Retrieve the current status of the router.


Each endpoint's parameters and expected responses are available in the automatically generated FastAPI documentation at:

```bash
http://localhost:8000/docs
```

## Example requests
Here's an example using curl to check the router's status:

```bash
curl -X GET "http://localhost:8000/router/status"
```

## Contributing
- Fork the repository.
- Create a new branch for your feature.
- Commit your changes.
- Open a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## References
https://github.com/aaronk6/dsl-monitoring

https://github.com/Andre0512/speedport-api

http://speedport.ip/engineer/html/module_versions.stm
