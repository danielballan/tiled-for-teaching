# Tiled for Teaching

Below I use `podman` and `podman-compose`, but `docker` and `docker-compose`
should work identically.

## One-time setup

```
git clone https://github.com/danielballan/tiled-for-teaching
cd tiled-for-teaching
cp env.example env
mkdir storage/

# TODO Make this initialize automatically if needed...
podman run -v ./storage:/storage ghcr.io/bluesky/tiled:v0.1.0a108 tiled admin initialize-database sqlite+aiosqlite:////storage/authn.db
```

Generate secret, using for example

```
openssl rand -hex 32
```

and copy this into `env` where indicated.

Go to https://orcid.org/developer-tools and register an application. Copy the
client ID and client secret into `env`.

In `config/config.yml`, find this section and enter authorized ORCIDs.

```yaml
instructors:
  # List ORCIDs of users who will distribute (write) data.
  - ...
students:
  # List ORCIDs of users who will consume (read) data.
  - ...
```

## Launch Tiled


```
source env
podman-compose up
```

