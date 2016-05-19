# How to contribute

Third-party contributions are essential for keeping Open365 great. We want to keep it as easy as possible to contribute changes that get things working in your environment.

## Install Open365 on your own server

The Open365 installer is available in [Open365 github](https://github.com/Open365/Open365/) you'll find the documentation there in the README file. 
It is a bash script that launches all the docker containers needed to run Open365 in a certain machine.

## Start contributing

- Make sure you have a [GitHub account](https://github.com/signup/free).
- Make sure you have an IRC client to connect to #Open365 and #Open365-dev channels.
- Submit a ticket for your issue in github, assuming one does not already exist.
  + Clearly describe the issue including steps to reproduce when it is a bug.

## Making changes

- Fork a new branch in github.
- Make commits of logical units.
- Check for unnecessary whitespace with git diff --check before committing.
- Make sure your commit messages are in the following format:
```
[Name of the issue] Fixing bug of max connections to mysql

151 is the default value of max_connections for mysql. Setting a greater
value of max_connections increment the resources needed (memory) to
start mysql, as it seems to allocate all the needed memory at startup.
So set a sane default for everybody and whoever needs a greater value
can modify it in their `settings.cfg` file.
```
- Make sure you have added the necessary tests for your changes.
- Run all the tests to assure nothing else was accidentally broken.
- Make a pull request so that we can merge it.*

*To merge your changes in open365 you will need to accept the third-party contributions agreement.

## Coding style

Almost all our codebase is Javascript and we have a short list of coding style conventions:

- Use tabs instead of spaces.
- End every file with newline.

Some parts are written in python in that case we use the PEP-8 convention to parse if a code is well coding styled.
