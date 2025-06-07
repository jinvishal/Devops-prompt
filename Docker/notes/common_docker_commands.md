# Common Docker CLI Commands

This file lists some of the most commonly used Docker CLI commands.

## Building Images
- **`docker build -t <image_name>:<tag> .`**: Build an image from a Dockerfile in the current directory.
  - `-t`: Tag the image with a name and optional tag.
  - `.`: Specifies the build context (current directory).

## Running Containers
- **`docker run [OPTIONS] <image_name>:<tag> [COMMAND] [ARG...]`**: Run a command in a new container.
  - `-d`: Run container in detached mode (in the background).
  - `-p <host_port>:<container_port>`: Publish a container's port(s) to the host.
  - `--name <container_name>`: Assign a name to the container.
  - `-v <host_path>:<container_path>`: Mount a volume.
  - `-e <KEY>=<VALUE>`: Set environment variables.

## Managing Containers
- **`docker ps`**: List running containers.
  - `-a`: List all containers (running and stopped).
- **`docker stop <container_id_or_name>`**: Stop one or more running containers.
- **`docker start <container_id_or_name>`**: Start one or more stopped containers.
- **`docker rm <container_id_or_name>`**: Remove one or more containers.
  - `-f`: Force the removal of a running container.
- **`docker logs <container_id_or_name>`**: Fetch the logs of a container.
  - `-f`: Follow log output.

## Managing Images
- **`docker images`**: List images.
- **`docker rmi <image_id_or_name>`**: Remove one or more images.
  - `-f`: Force removal of the image.
- **`docker pull <image_name>:<tag>`**: Pull an image or a repository from a registry.
- **`docker push <image_name>:<tag>`**: Push an image or a repository to a registry.

## Inspecting
- **`docker inspect <container_id_or_name_or_image_id>`**: Return low-level information on Docker objects.
- **`docker exec -it <container_id_or_name> <command>`**: Run a command in a running container.
  - `-i`: Keep STDIN open even if not attached.
  - `-t`: Allocate a pseudo-TTY.

This is not an exhaustive list but covers many common use cases. Refer to the [official Docker documentation](https://docs.docker.com/engine/reference/commandline/cli/) for more details.
