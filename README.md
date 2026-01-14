# py-obs

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Example Code](#example-code)

## Introduction

py-obs is a Python package that wraps the OBS WebSocket API functionality in order to provide easy programmatic access to OBS resources using Python. This package is designed to abstract as much configuration away so content creators can quickly and easily write scripts to automate tasks in OBS studio. Having dabbled in streaming myself, I was looking for a package like this with very clear documentation; this package was designed with my own experiences and desires in mind. This package will be open to contributions soon.

## Getting Started

### Installation

Getting started with py-obs is very simple. Make sure you have the package installed with

```
pip install py-obs
```

### OBS Studio Setup

In OBS Studio select `Tools` > `WebSocket Server Settings`

Under `Plugin Settings` make sure `Enable WebSocket server` is checked.

![WebSocket Server Settings](https://res.cloudinary.com/dvsvlcbec/image/upload/v1768430570/Screenshot_2026-01-14_at_5.42.31_PM_ffemfv.png "Plugin Settings")

Under `Server Settings` select a `Server Port` (`4455` is recommended). If you desire to set a password, check the `Enable Authentication` checkbox and set a strong `Server Password`. Keep all of this information, since it will be required to connect py-obs to your OBS WebSocket Server.

![WebSocket Server Settings](https://res.cloudinary.com/dvsvlcbec/image/upload/v1768430570/Screenshot_2026-01-14_at_5.42.40_PM_y9emxb.png "Server Settings")

### py-obs Setup

Now that your OBS WebSocket Server is setup, you can connect to it via py-obs.

```python
from py_obs.clients import OBS

obs = OBS()
obs.connect()
```

`OBS()` takes three parameters: `host` (default is `localhost`), `port` (default if `4455`), and `password` (default is `None`, meaning authentication is not enabled on the OBS WebSocket Server). Below is an example with a custom port and password.

```python
from py_obs.clients import OBS

obs = OBS(port=8000, password="StrongPassword1234!")
obs.connect()
```

## Documentation

- [OBS Clients](###obs-clients)
  - [Synchronous Client](####synchronous-client)
  - [Asynchronous Client](####asynchronous-client)
- [Scenes](###scenes)
- [Sources](###sources)

### OBS Clients

py-obs provides both synchronous and asynchronous clients.

#### Synchronous Client

The synchronous client is the default client. It is built on top of the asynchronous client. The synchronous client is ideal for simple use cases, like running individual commands.

To use the synchronous client import the `OBS` class from `py_obs.clients`

```python
from py_obs.clients import OBS

obs = OBS()
obs.connect()

obs.scene("Main").source("Camera").set_rotation(90)
```

#### Asynchronous Client

The asynchronous client is the recommended client for more advanced use cases, like FastAPI integration.

To use the asynchronous client import the `OBSAsync` class from `py_obs.clients`

```python
import asyncio
from py_obs.clients import OBSAsync

async def main():
    obs = OBSAsync()
    await obs.connect()

    await obs.scene("Main").source("Camera").set_rotation(90)

if __name__ == "__main__":
    asyncio.run(main())
```

### Scenes

### Sources

## Example Code

Using py-obs is very easy. Make sure you have the package installed with

```
pip install py-obs
```

Below is some example code to demonstrate basic operations in py-obs.

Set the rotation of the `Camera` source in the `Main` scene to 90 degrees.

```python
from py_obs.clients import OBS

obs = OBS()
obs.connect()

obs.scene("Main").source("Camera").set_rotation(90)
```

Alternatively you can format the same code in this format.

```python
from py_obs.clients import OBS

obs = OBS()
obs.connect()

main = obs.scene("Main")
camera = main.source("Camera")
camera.set_rotation(90)
```
