================================================================
Configuration initializer for Django services in dev environment
================================================================

Usage
-----
In your Django service, when you wish to load your local configuration (yaml) file, simply call `load_config()`.

Prerequisites
-------------
1. Name of the yaml should be config-<profile>.yml
2. <profile> should be set as environment variable `SWISS_PROFILE=<profile>`
3. If no such variable exists, default is `dev`

yaml
----
For every value in the yaml, its key will be flatten and used as the key for the environment variable.
For example:
settings:
  db:
    name: db_name

Will be converted to the following environment variable: `SETTINGS_DB_NAME=db_name`
