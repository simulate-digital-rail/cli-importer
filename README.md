# CLI-Importer
This commandline tool can be used to quickly generate railway topology in the [yaramo](https://github.com/simulate-digital-rail/yaramo) format.

## Import

To use the importer as a library, install it via:

`pip3 install git+https://github.com/simulate-digital-rail/planpro-exporter`

Afterwards you can import it to your application with:
```python
   from cli_importer.cli import CLI

    _cli = CLI()
    _cli.run()
    print(_cli.topology)
```

## Usage
The basic commands are explained as part of the script. The user may create `Nodes`, `Edges` and `Signals`.
