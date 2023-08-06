from .utils import dataclass

#
# @DockerExecution:
#    image: @DockerImage
#    environment: @dict(@string)
#    entrypoint?:
#    command: @list(@string)
#
# @DockerComposeConfiguration:
#    directory: @Directory
#    services: @dict(@DockerExecution)
#
#
# @DockerView:
#    organizations: @dict(@DockerOrganizations)
#
#
# @Dockerfile:
#    commands: @list(@DockerCommands)
#
# @DockerDaemon:
#    containers: @dict(@DockerContainers)
#
