# Local Spaces

Local spaces is a simple Flask application to show a list of hackspaces, within a defined radius, and show their current status. This was designed to use be used on a rotating dashboard within Leigh Hackspace, and show that the hackspace scene exists outside of the walls of the hackspace they're in.

This app makes use of the [SpaceAPI](https://spaceapi.io).

## Under the hood

## Installation

### Local Install

```
$ poetry install
$ flask
```

### Docker

```
docker pull ghcr.io/leigh-hackspace/local-spaces:latest
```

## Configuration

| Variable Name | Default Value | Required? | Description |
|---------------|---------------|-|------------|
| `LOCALSPACES_DISTANCE` | `None` | **Yes** |Maximum distance to search for hackspaces |
| `LOCALSPACES_LOCAL_ENDPOINT` | `None` | **Yes** |API endpoint for your hackspace's Space API endpoint | 
| `LOCALSPACES_SPACEAPI_ENDPOINT` | `https://api.spaceapi.io` | No |API endpoint for the aggregated Space API | 
