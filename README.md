# FastAPI Weather Service

This is simple fastAPI weather app.
Weather cached in redis for 1 hour (or you can force update favorite weather by clicking refresh button)
Favorites are stored in browser localStorage

To start project on your machine you can run the commands below.

### Base commands

```bash
bin/setup  # Setup project in docker container and run app

docker-compose up  # To run FastAPI application server

# Useful commands
bin/pytest # Run tests
bin/shell  # Run python shell
```

### Style guides and name conventions

#### Linters and code-formatters

We use git-hooks to run linters and formatters before any commit.
It installs git-hooks automatically if you used `bin/setup` command.
So, if your commit is failed then check console to see details and fix linter issues.

We use:

* black - code formatter
* mypy - static type checker
* flake8 - logical and stylistic lint
* flake8-bandit - security linter
* safety - security check for requirements

and few other flake8 plugins, check `requirements/development.txt` for more details.
