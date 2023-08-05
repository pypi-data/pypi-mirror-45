import click

from queso.versions import get_versions


def version_option(*idens, **attrs):
    """Add a version option to the CLI.
    
    Prints out the version number and immediately ends the program.

    Inspired by `click.version_option`.

    # Parameters
    *idens (str): identifiers for the option. Defaults to `"--version"`.
    """

    def decorator(f):
        attrs.setdefault("is_flag", True)
        attrs.setdefault("expose_value", False)
        attrs.setdefault("is_eager", True)
        attrs.setdefault("help", "Show the version and exit.")

        def callback(ctx, param, value):
            if not value or ctx.resilient_parsing:
                return
            versions = get_versions()
            click.echo(str(versions))
            ctx.exit(0)

        attrs["callback"] = callback
        option = click.option(*(idens or ("--version",)), **attrs)
        return option(f)

    return decorator
