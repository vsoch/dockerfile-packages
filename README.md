# Dockerfile Packages

This rpeository is a dinosaur dataset that provides the 
[vsoch/dockerfiles](https://www.github.com/vsoch/dockerfiles) package matrices, 
meaning for each Docker uri that still exists on Docker Hub, a feature matrix of 
packages (columns) by containers (rows) for docker URIs extracted in 2017 and 2019. 
It uses the [container-tree](https://www.github.com/singularityhub/container-tree) library 
to generate container package trees, and then export vectors for them.

## 0. Get Docker Container Names

We want to derive a list of Docker containers for 2019, to supplement the
original [vsoch/dockerfiles](https://www.github.com/vsoch/dockerfiles) 
container names that are provided in [dockerfiles-02-16-2017.pkl](dockerfiles-02-16-2017.pkl)
from two years earlier. To extract the new names, we use the script
[0.find-containers.py](0.find-containers.py) that uses the Docker command line
client with search, along with [search-terms.json](search-terms.json) to extract
a listing of approximately 423,541 new containers. We save this 2019 listing
to [dockerfiles-01-13-2019.pkl](dockerfiles-01-13-2019.pkl).


## 1. Generate Package Matrices

In [1.extract-matrices.py](1.extract-matrices.py) we first combine the two 
files to produce [dockerfiles-2017+2019.pkl](dockerfiles-2017+2019.pkl).
(N=129,463 + N=423,541 with some overlap for a total of 505,234 unique containers).
We then use [Container Package Trees](https://singularityhub.github.io/container-tree/examples/package_tree/) 
for Apt and Pip (thanks to Google ContainerDiff!) to create package trees for each, 
and we both save the trees:

 - [apt-tree.pkl](apt-tree.pkl)
 - [pip-tree.pkl](pip-tree.pkl)

And export the final package matrices, not including versions.

**in progress**

## 2. Package Metadata

### Pip

This approach was developed because it is no longer possible to scrape any sort
of metadata or Dockerfile from the update Docker website. Thus, we can retrieve
metadata about packages, and use that to say something about the container.
In order to do this, we need to extract metadata for pip packages from
pypi. While pypi has an API to get descriptions and basic package information,
the dependency graph must come from libraries.io. We use the script 
[2.package-metadata.py](2.package-metadata.py) to do this. Make sure that you
have the libraries.io API token exported into the environment before running
the script:

```bash
export LIBRARIESIO_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

When we finish this step, we have created [pypi-metadata.pkl](pypi-metadata.pkl)
and [pypi-metadata.json](pypi-metadata.json)

### Apt

Apt was harder to do because there isn't package data available on libraries.io.
Thus, I created a Docker container in the [docker](docker) folder that serves
one simple purpose - to install and then use `apt-cache depends` to extract
dependencies for a package. I chose a base image of 16.04 as an intermediate 
between much older Ubuntu (debian) bases (e.g., 14.04) and much newer (18.04).
It's not a perfect approach, but should serve to get a good set of data.

Usage of the Docker container looks like this:

```bash
$ docker run -it vanessa/apt-package-dependencies adduser
```

**still in progress too**
