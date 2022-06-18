import docker
import sys

def pull(source_url: str):
    print(f'Pulling {source_url}')
    client = docker.from_env()
    client.images.pull(source_url)
    restart_all_containers(client, source_url)

def restart_all_containers(docker, source_url: str):
    image = source_url.rsplit(':', 1)[0]
    for container in docker.containers.list():
        if image in container.image:
            container.restart()
            
if __name__ == '__main__':
    pull(sys.argv[1])