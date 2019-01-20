# Ubuntu Package Dependencies

If you are interested in studying package dependencies, these containers are
for you! Each one will take as input some Apt package, and output a json
structure that will list:

 - PreDepends
 - Depends
 - Conflicts
 - Replaces
 - Suggests

The container works by installing the package, and then using `apt-cache depends`
to show the list of dependencies, which are parsed into json. Each Dockerfile
shown below corresponds to a particular Ubuntu LTS release:

 - [Dockerfile.12.04](Dockerfile.12.04)
 - [Dockerfile.14.04](Dockerfile.14.04)
 - [Dockerfile.16.04](Dockerfile.16.04)
 - [Dockerfile.18.04](Dockerfile.18.04)


## Usage

```bash
$ docker run -it vanessa/ubuntu-dependencies:18.04 bash
```
```bash
{"Recommends": ["bash-completion"], "PreDepends": ["dash", "libc6", "libtinfo5"], "Suggests": ["bash-doc"], "Depends": ["base-files", "debianutils"], "Replaces": ["bash-completion", "bash-doc"], "Conflicts": ["bash-completion"]}
```

The output is provided non-pretty printed in case you need to pipe it somewhere else to parse.
If you want to build a container from scratch:

```bash
$ docker build -t vanessa/ubuntu-dependencies:18.04 .
```
