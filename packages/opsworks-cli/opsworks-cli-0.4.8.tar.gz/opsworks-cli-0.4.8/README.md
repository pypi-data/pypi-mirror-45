opsworks-cli
======================

A simple python module to work with aws opsworks

[![Build Status](https://travis-ci.org/chaturanga50/opsworks-cli.svg?branch=master)](https://travis-ci.org/chaturanga50/opsworks-cli)

How to install
--------------

You can download the updated release version from pypi repo

``` bash
pip install opsworks-cli
```

Usage
-----

You can see the list of parameters available via `opsworks-cli --help`

#### run update_custom_cookbook

```
* region - OpsWorks stack region (required)
* stack - OpsWorks stack ID (required)
* layer - OpsWorks layer ID (required)
```

```bash
opsworks-cli update-custom-cookbooks --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --layer ac0df176-104b-46ae-946e-7cf7367b816e
```

#### run execute-recipes
```
* region - OpsWorks stack region (required)
* stack - OpsWorks stack ID (required)
* layer - OpsWorks layer ID (required)
* cookbook - chef cookbook (required)
* custom-json - custom json file with extra vars (optional)
```

```bash
opsworks-cli execute-recipes --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --layer ac0df176-104b-46ae-946e-7cf7367b816e \
             --cookbook apache::default \
             --custom-json [{"lamp":{ "packages": { "app--sso": "17.1.6" } } }] # optional
```

```bash
opsworks-cli execute-recipes --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --layer ac0df176-104b-46ae-946e-7cf7367b816e \
             --cookbook apache
```

#### run setup
```
* region - OpsWorks stack region (required)
* stack - OpsWorks stack ID (required)
* layer - OpsWorks layer ID (required)
```

```bash
opsworks-cli setup --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --layer ac0df176-104b-46ae-946e-7cf7367b816e
```

### How it works

- sending opsworks commands via aws api to specific stack ID and layer ID
- according to the responces from servers script will show the final output.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* ***Chathuranga Abeyrathna*** - *Initial work* - [github](https://github.com/chaturanga50/)

## Contributors

* ***Iruka Rupasinghe*** - *Feature Improvements* - [github](https://github.com/Rupasinghe2012/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details