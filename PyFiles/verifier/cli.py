import json
import logging
import typer

from verifier.nfc.reader import tap_and_get_payload
from verifier.decode.cbor import decode_payload
from verifier.crypto.verify import verify_signature

logger = logging.getLogger(__name__)

# Pass `no_args_is_help=False` so Typer will call the function if no args
# are given
app = typer.Typer(no_args_is_help=False)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug output"),
):
    """If no subcommand is provided, run :func:`scan` directly."""
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)
    if ctx.invoked_subcommand is None:
        scan()


@app.command()
def scan():
    """
    Tap a (mock) mobile ID, decode, and verify.
    """
    try:
        raw = tap_and_get_payload()
    except RuntimeError as e:
        typer.secho(f"[error] {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    try:
        parsed = decode_payload(raw)
    except RuntimeError as e:
        typer.secho(f"[error] {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    valid = verify_signature(parsed)
    logger.debug("verification result: %s", valid)
    output = {
        "valid": valid,
        "fields": parsed.get("doc", parsed),
    }
    typer.secho(json.dumps(output, indent=2), fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
