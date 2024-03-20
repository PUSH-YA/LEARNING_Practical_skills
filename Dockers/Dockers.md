# Intro to Docker

| Physical server                                                  | Virtual server                                                                                                                   |
| ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| if something breaks, its 100% your resp. to fix it               | usually have multiple physical servers with same HYPERVISOR running multiple applications and moving applications when one fails |
| Scaling is a big problem with such servers                       | easily scalable bc multiple applications on the same server                                                                      |
| OS > runtime env > application (the rest of the space is wasted) | has HYPERVISOR allowing multiple VMs on the same physical server                                                                 |
| if running other app -> 1 crash -> server problem                | other VM don't know about each other                                                                                             |

## What are containers?

The VMware architecture is like this in order:

| App1       | App2     | App3     |
| ---------- | -------- | -------- |
| Lib1       | Lib2     | Lib3     |
| GuestOS1   | GuestOS2 | GuestOS3 |
| Hypervisor | <-       | <-       |
| HostOS     | <-       | <-       |
| Hardware   | <-       | <-       |

you have hardware with its one OS and hypervisors

- hypervisor runs multiple applications with their guestOS and libraries

the main difference with container is as following (Docker architecure):

| App1          | App2 | App3 |
| ------------- | ---- | ---- |
| Lib1          | Lib2 | Lib3 |
| Docker engine | <-   | <-   |
| HostOS        | <-   | <-   |
| Hardware      | <-   | <-   |

Docker engine is lighter than hypervisor 

they all share hostOS in lil container of application and library allowing them to be a lot lighter than VMware

#### Container architecture:

- containers runs on a container host
  
  - via container (docker) engine

- containers only run an app & libraries / runtime environment

- share container host OS

- lightweight - can be densely packed & started / restarted quickly

- can be impacted by other containers (noisy neighbours)
  
  - BIG CON -- VMware over containers

This was created for shipping products and not running servers

> "it works on my computer"; "ok, let's ship your computer"

# Docker 101 (architecture and commands)

**Docker host:**

- has docker daemon (brains of the operations) hosting API endpoints for *docker clients*

- There is also *registery(hub)*

- it has 
  
  - ***containers*** := builds and runs the docker using the images for  *docker client*
  
  - ***images*** := pulled by *registery (HUB)*

**Docker clients:**

- running the docker enginer on `command line` or `docker desktop`

**Registery (HUB)**:

- public / private storage for images -- docker hub

- images are used to run containers
  
  - such as linux or some specific game negine

- these images are pulled by `docker pull` by *docker host*

- can gain images from *docker host* using `docker push`

- sometimes people upload their own docker files `docker build` held here

> kinda works like `git` with docker images

![](C:\MINE\NERD%20STUFF\new%20skills\Fullstack%20ML-AI\Dockers\Screenshot_1.png)

## Docker commands

```bash
docker ps # list all the containers
docker images # list all the images
docker run image_name # run that specific image
docker rmi image_name:tag # delete that image
```

#### Listing and deleting images

```bash
docker images # liUntagged: welcome-to-docker:latest
#REPOSITORY                 TAG       IMAGE ID       CREATED         SIZE
#welcome-to-docker          latest    dde7fb5a2108   8 weeks ago     226MB
#docker/welcome-to-docker   latest    c1f619b6477e   4 months ago    18.6MB
#hello-world                latest    d2c94e258dcb   10 months ago   13.3
#kB

docker rmi image_name:tag # delete that image
#Deleted: sha256:dde7fb5a210818c48bc4dbf10c342a0f2d56e31028308cf650d0471f6f7fe3bbst all the image
```

#### Runnning docker images

```bash
docker run hello-world
#Unable to find image 'hello-world:latest' locally
#latest: Pulling from library/hello-world
#c1ec31eb5944: Pull complete
#Digest: sha256:6352af1ab4ba4b138648f8ee88e63331aae519946d3b67dae50c313c6fc8200f
#Status: Downloaded newer image for hello-world:latest
#
#Hello from Docker!
#This message shows that your installation appears to be working correctly.
#
#To generate this message, Docker took the following steps:
#1. The Docker client contacted the Docker daemon.
#2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
#   (amd64)
#3. The Docker daemon created a new container from that image which runs the
#   executable that produces the output you are currently reading.
#4. The Docker daemon streamed that output to the Docker client, which sent it
#   to your terminal.
```

- we have an image but no containers at this point

## Container and image architecture

***Docker image***

- is a collection fo file system layers

- each layer containes only the differences from the layer below
  
  - base linux layer -> env/lib layer -> application layer

- These layers can be reused and avoids *unnecessary* uploads and downloads

- when running `docker pull`, each layer is independent
  
  - pulled only if it doesn't exist locally

***Docker container***

- container are like images (readonly) with writable layers

- each time you run it, it creates a new isolated container with its own writable layer

writable layers use the *union filesystem* which does have a performance hit as they are tightly couple to host  

- they are also linked to the lifecycle of the container 

## Build and run a containerised application

## Working with existing images

Run a `docker images` to show all images on the Docker Host.  
Locate the `dockerized-2048` image which you just created.  
This image, is running an application using `tcp/80` so we need to use the `-p` CLI option to run this on an alternative docker host post (this will be discussed in detail later in the course).

Run a docker container of 2048 using

`docker run -d -p 8081:80 dockerized-2048`

this will run in detached mode, so your terminal should return to the prompt immediately.

Verify the container is running with `docker ps`. Confirm the port mapping with `docker port <CONTAINERID>`.

Browse to `http://localhost:8081`

## Application 2 - Container of Cats

This dock file is intentionally less efficient than app1 above. I want you to understand WHY it's less efficient.

### Creating a Container of Cats Docker Image

Move into the `app2-containerofcats` folder.  
open the `Dockerfile` in a text editor of choice.

Let's review this `Dockerfile` and specifically identify how it's different from the previous `app1`.

- First, it uses a different base image. Instead of `nginx:latest` which is specifically designed for simple `ngnix` web use-cases, this uses `ubi8` which is a universal redhat 8 image (general purpose)
- This image is also larger than other lean image such as `alpine` and `nginx`.
- Because this is a general purpose image, we have to install a web server (apache2) in this case via the `RUN` statement. This creates a layer.
- Next, there are 2 x `COPY` statements which copy in `index.html` and `contaierandcat*.jpg` media files into the image. These two statements create *2* additional layers.

This dockerfile and resultant image are more generalised. 
This results in a larger image, and containers which consume more 
resources.

To create a docker image for the `containerofcats` dockerized application we run this command.

`docker build -t containerofcats .`

*notice how much longer it takes to create, vs the 2048
 image, even though it's a similar architecture .. web server & some
 files*

### Running a containerofcats Docker Container

Run a `docker images` to show all images on the Docker Host.  
Locate the `containerofcats` image which you just created.  
This image, is running an application using `tcp/80` so we need to use the `-p` CLI option to run this on an alternative docker host post (this will be discussed in detail later in the course).

Run a docker container of containerofcats using

`docker run -d -p 8081:80 containerofcats`

this will run in detached mode, so your terminal should return to the prompt immediately.

Verify the container is running with `docker ps`. Confirm the port mapping with `docker port <CONTAINERID>`.

Browse to `http://localhost:8081`

### Cleanup

Run a `docker stop <CONTAINERID>` to stop the containerofcats container app.  
Run a `docker rm <CONTAINERID>` to remove the containerofcats container.

can also use 

```bash
docker rm $(docker ps -aq) # list all the containers and remove them
docker rmi image_id # remove image

docker start container_id # start container
docker restart container_id # restart container
docker stop container_id # stop container
```

# More Docker

## Docker storage

Docker stores stuff in a writable layer on top of the base layer presenting as a *union file system*

- that allows all containers to be unique

***tmpfs:***

- fast host memory

- not persistent

- cant be shared between containers

- temp or sensitive files

***bind mounts:***

- multiple containers can access the same host folder

- map host folders to a container folder

- rely on a host folder structure as its not managed by a doctor

- persist outside the lifecycle of a container

### Bind mount

- allows us to mount a file or direcotry on the host machine into a container

- useful for accessing the shared files between containers or files from host filesystem

We can mount the data in either of the two formats in macos or linux

```bash
docker run \
 --name db \
 -e MYSQL_ROOT_PASSWORD=somewordpress \
 -e MYSQL_PASSWORD=wordpress \
 -e MYSQL_DATABASE=wordpress \
 -e MYSQL_USER=wordpress \
 --mount type=bind,source="$(pwd)"/mariadb_data,target=/var/lib/mysql \
 -d \
 mariadb:10.6.4-focal \
 --default-authentication-plugin=mysql_native_password



docker run \
 --name db \
 -e MYSQL_ROOT_PASSWORD=somewordpress \
 -e MYSQL_PASSWORD=wordpress \
 -e MYSQL_DATABASE=wordpress \
 -e MYSQL_USER=wordpress \
 -v "$(pwd)"/mariadb_data:/var/lib/mysql \
 -d \
 mariadb:10.6.4-focal \
 --default-authentication-plugin=mysql_native_password
```

for windows, either of the two:

```bash
docker run --name db -e MYSQL_ROOT_PASSWORD=somewordpress -e MYSQL_PASSWORD=wordpress 
-e MYSQL_DATABASE=wordpress 
-e MYSQL_USER=wordpress 
--mount  type=bind,
source=%cd%/mariadb_data,target=/var/lib/mysql 
-d mariadb:10.6.4-focal 
--default-authentication-plugin=mysql_native_password

docker run --name db -e MYSQL_ROOT_PASSWORD=somewordpress
-e MYSQL_PASSWORD=wordpress -e MYSQL_DATABASE=wordpress 
-e MYSQL_USER=wordpress 
-v  %cd%/mariadb_data:/var/lib/mysql 
-d mariadb:10.6.4-focal 
--default-authentication-plugin=mysql_native_password
```

- make sure to state the correct path, `source = "C:\\folder1\mariadb_data"

- now the folder is connected to the docker directory
  
  - one to one, any change in one will change the other

### Volume

Volumes are the prefered way to adding storage to docker containers 
outside of the lifecycle of a container. They are managed entirely by 
docker and work flawlessly on windows container hosts.

To create volumes

```bash
docker volume create mariadb_data # create volumes
docker volume ls # list all the dockers
docker volume inspect name # check metadata
docker volume rm name # remove it
```

We can use the same instruction as before to create a volume the same way now but we list the source separately

```bash
docker run --name db -e MYSQL_ROOT_PASSWORD=somewordpress -e MYSQL_PASSWORD=wordpress 
-e MYSQL_DATABASE=wordpress 
-e MYSQL_USER=wordpress 
--mount  type=bind, source=mariadb_data,target=/var/lib/mysql 
-d mariadb:10.6.4-focal 
--default-authentication-plugin=mysql_native_password

docker run --name db -e MYSQL_ROOT_PASSWORD=somewordpress
-e MYSQL_PASSWORD=wordpress -e MYSQL_DATABASE=wordpress 
-e MYSQL_USER=wordpress 
-v mariadb_data:/var/lib/mysql -d mariadb:10.6.4-focal 
--default-authentication-plugin=mysql_native_password
```

- we can maintain the data even if the container deletes

## Docker networking

We can not run multiple containers on the same part bc

container1 -> port1 -host-> user

conteiners2 -> port2 -host-> user

however we can use bridge network which can allow multiple on the same port  but we have to publish the bridge network

container1 -> bridge-ip/port1 -> `-p dockerport:hostport`  -host-> user

conteiners2 -> bridge-ip/port2 -> `-p dockerport:hostport`  -host-> user

### Docker environment variables

We first create the php admin page with 

```bash
docker run --name phpmyadmin -d -p 8081:80 -e 
PMA_ARBITRARY=1 phpmyadmin/phpmyadmin
```

first we need to pull down the mariaDB image.  
`docker pull mariadb:10.6.4-focal` lets inspect it and review all metadata.  
`docker inspect mariadb:10.6.4-focal`

Now let's run a container and note how we use environment variables.

- using `-e` we specify a key=value pair
- it's convention for NAMES to be in caps
- in this case we create `MYSQL_ROOT_PASSWORD`, `MYSQL_PASSWORD`, `MYSQL_DATABASE` and `MYSQL_USER`
- The container is configured to accept these variables and take action on them
- `MYSQL_ROOT_PASSWORD` sets the mariaDB root password
- `MYSQL_DATABASE` creates a database with the name of the env variable value `wordpress` in this example
- `MYSQL_USER` creates a mariaDB user
- `MYSQL_PASSWORD` creates a password for that user
- `--default-authentication-plugin=mysql_native_password` is an argument for the process running in the docker container, extra options.

```bash
docker run --name db -e MYSQL_ROOT_PASSWORD=somewordpress 
-e MYSQL_PASSWORD=wordpress 
-e MYSQL_DATABASE=wordpress 
-e MYSQL_USER=wordpress -d mariadb:10.6.4-focal 
--default-authentication-plugin=mysql_native_password
```

- we create an environment variable with the user above

confirm the docker container is running with a `docker ps -a`

and get the container ID... note this down as `MARIADB_ID`  
run the command below to show the metadata for the running container for mariaDB.  
`docker inspect MARIADB_ID`

look for "IPAddress": "XXXXXXXXXX", this is the internal 
docker network IP that the DB container is running on. note this down as
 `DB_IP`

open [http://localhost:8081](http://localhost:8081) to access phpmyadmin
enter `DB_IP` for server  
enter `root` for username  
enter `somewordpress` for password

You are now accessing the db container, from the phpmyadmin container

- Go to `User Accounts` and confirm a wordpress user has been created.
- Look on the menubar on the left and confirm there is a `wordpress` database

we can execute commands in our container

```bash
docker exec -it container_id # to run exec commands in the container
```

We can run bash command in our 

```bash
docker exec -it db bash
#root@container_id/#
df -k # list all the drives and mounts in the container
ls -la # see the data in the database
```

- there are no externally mapped drives/mounts. All storage that this container uses, is within this container.
  This means the storage is linked to the lifecycle of this container, if the container is deleted, so is the storage.

## Docker compose

Used to create, manage and cleanup

- multi container application

- reads a docker compose file

- `compose.yaml` file
  
  - creates, updates and deletes based on the that file

it is used to run/update containers, volumes and networks

### Using Docker compose

`yaml` files can't have tabs inside them so make sure to convert it to spaces

an example of a docker compose file is

```yaml
services:
  db:
    image: mariadb:10.6.4-focal
    command: '--default-authentication-plugin=mysql_native_password'
    volumes:
      - mariadb_data:/var/lib/mysql
    restart: always
    environment:
      - MYSQL_ROOT_PASSWORD=somewordpress
      - MYSQL_DATABASE=wordpress
      - MYSQL_USER=wordpress
      - MYSQL_PASSWORD=wordpress
    expose:
      - 3306
      - 33060
  wordpress:
    image: wordpress:latest
    volumes:
      - wordpress_data:/var/www/html
    ports:
      - 8081:80
    restart: always
    environment:
      - WORDPRESS_DB_HOST=db
      - WORDPRESS_DB_USER=wordpress
      - WORDPRESS_DB_PASSWORD=wordpress
      - WORDPRESS_DB_NAME=wordpress
volumes:
  mariadb_data:
  wordpress_data:
```

- mentiones the image, command, env var and volumes

We create the docker compose as following 

```bash
docker compose up -d # creates the containers and vol detached

# can check if it worked with
docker ps 
docker volume ls
```

- once we upload the photo -> volume stores photo & container stores $\Delta$ metadata 

We can remove all the containers defined in the compose file 

```bash
docker compose down # containers won't show in ps or ps -a
docker volume ls # will still show the same stuff
docker comose up -d # creates it detached using the volume above
```

- once we create new containers, it will use the volumes from above

## Docker container registry

- Container registries are like GitHubn for docker images

- *Docker Hub* is an example of a registry

- - you can run private registries on cloud or on premiste

- regitreis are split into repositories

- you can `dockerp pull` and `docker push` to repositories

### 

### Using Docker container registry

We will be using *Docker Hub* for keeping our repositories

We can pull and push as following

```bash
docker pull reponame:tag # get the following docker image
docker login --username = your_username # login to your github
#pwd: your_pwd or access_token
docker tag containername:tagname # adds the tag to it
docker push containername:tagname # push our docker to the repo
```

Just like GitHub:

we can create repos

set it private or public repo as we want

create an access token with custom permissions -- use for pwd
