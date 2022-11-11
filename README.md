# HTTP Service Skeleton

This is an HTTP microservice template for a quick start of development.

To get started, copy all the files from here into a new repository, replace 'service_name' in /bin/* and
docker-compose.yml files, and also set valid KAFKA_APPLICATION_ID and PROJECT_NAME envs.

After that you can run all the commands below.

## Local development

### Setup

We highly recommend to use provided script to setup everything by single command.
Just run the following command from project's root directory and follow instructions:

* `bin/setup`

That's all!

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

In order to run checkers manually use the following bash script:

```bash
bin/pre-commit
```

#### Branch and commit naming convention

We follow gitflow's branch model:

* `feature/NAME` - for any tasks, improvements
* `bugfix/NAME` - for bugs that will be released to staging/dev only
* `hotfix/NAME` - for hotfixes that will be released to the live

NAME should follow these rules:

* NAME should start with task ID, eg. `feature/MYPROJ-2020`
* add a short description to name with lowercase and using hyphen between words: e.g `feature/MYPROJ-2020-add-new-button-to-create-user`

All commit's comments should start with task ID and then a short description. For example:

* `MYPROJ-2895 - fixed bug related to some feature`
* `MYPROJ-2859 - Implemented new functionality`

### Pull request merge flow

#### Regular flow

The developer pulls the `develop` branch, and creates a feature or bugfix branch from it.
After completing the task, the developer should create a file with short task description.
Command for creating `feature` file:
```bash
bin/towncrier create XXX.feature
```
and command for creating `bugfix` file:
```bash
bin/towncrier create XXX.bugfix
```
where XXX - is the number of Jira task (without LM- prefix).
Do not forget commit this file.
After that, the developer should create MR into the develop branch, and after passing the tests and getting at least
one approve from team members, he can merge it. This merge will trigger the deployment to the dev server.

To fully test the product before release, the `develop` branch is merged into the `staging` branch, and a tag like
`vX.X.X-rc.X` (where X is number from 0 to 9) is created to run the deployment to the stage server.

After full testing on the stage server, the `staging` branch is merged into the `master` branch, and then a tag like
`vX.X.X` (where X is number from 0 to 9) is created. This starts the deployment to the prod server.

#### Hotfixes

A hotfix branch is created from the `staging` branch, and after the MR tests are passed and the team members approve it,
it is merged into `staging`, which is followed by the same process of deploying to the stage server, testing, and
deploying to prod with regular flow.
This hotfix branch is then also merged into the `develop` branch.

### Base commands

```bash
docker-compose up  # To run FastAPI application server

# Useful commands
bin/pytest # Run tests
bin/shell  # Run python shell

# Build release notes from existing files
bin/towncrier build --version X.Y.Z
```
