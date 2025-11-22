"""Command-line interface for dicti0nary-attack."""

import click
import logging
import sys
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
from rich.panel import Panel

from dicti0nary_attack.generators import (
    LeetspeakGenerator,
    PhoneticGenerator,
    PatternGenerator,
    RandomGenerator,
    MarkovGenerator,
)
from dicti0nary_attack.crackers import HashCracker
from dicti0nary_attack.utils.config import ConfigManager
from dicti0nary_attack.utils.wordlist import WordlistManager
from dicti0nary_attack.utils.output import OutputFormatter

console = Console()


def setup_logging(level: str):
    """Setup logging configuration."""
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO

    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stderr)]
    )


@click.group()
@click.version_option(version='0.1.0')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.pass_context
def cli(ctx, config: Optional[str], verbose: bool):
    """
    dicti0nary-attack - Password cracking utility for non-dictionary words.

    WARNING: This tool is for authorized security testing only.
    Unauthorized access to computer systems is illegal.
    """
    ctx.ensure_object(dict)

    # Setup logging
    level = 'DEBUG' if verbose else 'INFO'
    setup_logging(level)

    # Load configuration
    ctx.obj['config_manager'] = ConfigManager(config)
    ctx.obj['console'] = console


@cli.command()
@click.option('--generator', '-g', type=click.Choice(['leetspeak', 'phonetic', 'pattern', 'random', 'markov']),
              default='leetspeak', help='Password generation strategy')
@click.option('--count', '-n', type=int, default=1000, help='Number of passwords to generate')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--format', '-f', type=click.Choice(['text', 'json', 'csv']), default='text',
              help='Output format')
@click.option('--min-length', type=int, help='Minimum password length')
@click.option('--max-length', type=int, help='Maximum password length')
@click.pass_context
def generate(ctx, generator: str, count: int, output: Optional[str], format: str,
             min_length: Optional[int], max_length: Optional[int]):
    """Generate non-dictionary passwords."""
    config_manager: ConfigManager = ctx.obj['config_manager']
    console: Console = ctx.obj['console']

    # Get generator configuration
    gen_config = config_manager.get_generator_config(generator)

    # Override with command-line options
    if min_length:
        gen_config['min_length'] = min_length
    if max_length:
        gen_config['max_length'] = max_length

    # Create generator
    console.print(f"\n[bold green]Generating passwords using {generator} strategy...[/bold green]\n")

    if generator == 'leetspeak':
        gen = LeetspeakGenerator(config=gen_config)
    elif generator == 'phonetic':
        gen = PhoneticGenerator(config=gen_config)
    elif generator == 'pattern':
        gen = PatternGenerator(config=gen_config)
    elif generator == 'random':
        gen = RandomGenerator(config=gen_config)
    elif generator == 'markov':
        gen = MarkovGenerator(config=gen_config)
    else:
        console.print(f"[red]Unknown generator: {generator}[/red]")
        return

    # Generate passwords with progress bar
    passwords = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task = progress.add_task(f"Generating passwords...", total=count)

        for password in gen.generate(count=count):
            passwords.append(password)
            progress.update(task, advance=1)

    # Display stats
    stats = gen.get_stats()
    stats_table = Table(title="Generation Statistics")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="magenta")

    for key, value in stats.items():
        stats_table.add_row(key.replace('_', ' ').title(), str(value))

    console.print(stats_table)

    # Save or display passwords
    if output:
        output_formatter = OutputFormatter()
        output_formatter.save_passwords(passwords, output, format=format)
        console.print(f"\n[green]✓ Saved {len(passwords)} passwords to {output}[/green]")
    else:
        # Display first 20 passwords
        console.print("\n[bold]Sample passwords (first 20):[/bold]")
        for i, pwd in enumerate(passwords[:20], 1):
            console.print(f"{i:3d}. {pwd}")

        if len(passwords) > 20:
            console.print(f"\n... and {len(passwords) - 20} more")


@cli.command()
@click.argument('target_hash')
@click.option('--algorithm', '-a', type=click.Choice(list(HashCracker.SUPPORTED_ALGORITHMS.keys())),
              default='sha256', help='Hash algorithm')
@click.option('--generator', '-g', type=click.Choice(['leetspeak', 'phonetic', 'pattern', 'random', 'markov']),
              default='pattern', help='Password generation strategy')
@click.option('--wordlist', '-w', type=click.Path(exists=True), help='Use wordlist file instead of generator')
@click.option('--parallel', '-p', is_flag=True, help='Enable parallel processing')
@click.option('--workers', type=int, default=4, help='Number of worker processes for parallel mode')
@click.pass_context
def crack(ctx, target_hash: str, algorithm: str, generator: str, wordlist: Optional[str],
          parallel: bool, workers: int):
    """Crack a password hash."""
    config_manager: ConfigManager = ctx.obj['config_manager']
    console: Console = ctx.obj['console']

    # Display warning
    warning = Panel(
        "[bold yellow]WARNING[/bold yellow]: Hash cracking should only be performed on "
        "hashes you own or have explicit authorization to test.",
        title="Legal Notice",
        border_style="yellow"
    )
    console.print(warning)

    # Create hash cracker
    cracker_config = config_manager.get_cracker_config()
    cracker_config['algorithm'] = algorithm
    cracker_config['workers'] = workers

    cracker = HashCracker(config=cracker_config)

    console.print(f"\n[bold]Target hash:[/bold] {target_hash}")
    console.print(f"[bold]Algorithm:[/bold] {algorithm}")
    console.print(f"[bold]Parallel:[/bold] {parallel}\n")

    # Get password source
    if wordlist:
        console.print(f"[cyan]Using wordlist: {wordlist}[/cyan]\n")
        wordlist_manager = WordlistManager()
        password_gen = wordlist_manager.load_wordlist(wordlist)
    else:
        console.print(f"[cyan]Using generator: {generator}[/cyan]\n")
        gen_config = config_manager.get_generator_config(generator)

        if generator == 'leetspeak':
            gen = LeetspeakGenerator(config=gen_config)
        elif generator == 'phonetic':
            gen = PhoneticGenerator(config=gen_config)
        elif generator == 'pattern':
            gen = PatternGenerator(config=gen_config)
        elif generator == 'random':
            gen = RandomGenerator(config=gen_config)
        elif generator == 'markov':
            gen = MarkovGenerator(config=gen_config)
        else:
            console.print(f"[red]Unknown generator: {generator}[/red]")
            return

        password_gen = gen.generate()

    # Crack the hash
    with console.status("[bold green]Cracking hash...") as status:
        if parallel:
            result = cracker.crack_parallel(target_hash, password_gen)
        else:
            result = cracker.crack(target_hash, password_gen)

    # Display results
    stats = cracker.get_stats()

    if result:
        console.print(f"\n[bold green]✓ Hash cracked![/bold green]")
        console.print(f"[bold]Password:[/bold] {result}\n")
    else:
        console.print(f"\n[bold red]✗ Hash not cracked[/bold red]\n")

    # Display statistics
    stats_table = Table(title="Cracking Statistics")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="magenta")

    stats_table.add_row("Attempts", str(stats['attempts']))
    stats_table.add_row("Matches", str(stats['matches']))
    if stats['elapsed_time']:
        stats_table.add_row("Time Elapsed", f"{stats['elapsed_time']:.2f}s")
        stats_table.add_row("Rate", f"{stats['rate']:.2f} attempts/s")

    console.print(stats_table)


@cli.command()
@click.argument('wordlist_path', type=click.Path())
@click.option('--generator', '-g', type=click.Choice(['leetspeak', 'phonetic', 'pattern', 'random', 'markov']),
              required=True, help='Password generation strategy')
@click.option('--count', '-n', type=int, default=10000, help='Number of passwords to generate')
@click.pass_context
def create_wordlist(ctx, wordlist_path: str, generator: str, count: int):
    """Create a wordlist file."""
    config_manager: ConfigManager = ctx.obj['config_manager']
    console: Console = ctx.obj['console']

    console.print(f"\n[bold green]Creating wordlist with {generator} generator...[/bold green]\n")

    # Create generator
    gen_config = config_manager.get_generator_config(generator)

    if generator == 'leetspeak':
        gen = LeetspeakGenerator(config=gen_config)
    elif generator == 'phonetic':
        gen = PhoneticGenerator(config=gen_config)
    elif generator == 'pattern':
        gen = PatternGenerator(config=gen_config)
    elif generator == 'random':
        gen = RandomGenerator(config=gen_config)
    elif generator == 'markov':
        gen = MarkovGenerator(config=gen_config)
    else:
        console.print(f"[red]Unknown generator: {generator}[/red]")
        return

    # Generate and save
    wordlist_manager = WordlistManager()

    with console.status("[bold green]Generating wordlist..."):
        wordlist_manager.save_wordlist(wordlist_path, gen.generate(count=count), max_words=count)

    console.print(f"\n[green]✓ Created wordlist: {wordlist_path}[/green]")


@cli.command()
@click.argument('hash_value')
@click.option('--algorithm', '-a', type=click.Choice(list(HashCracker.SUPPORTED_ALGORITHMS.keys())),
              default='sha256', help='Hash algorithm')
@click.pass_context
def hash_password(ctx, hash_value: str, algorithm: str):
    """Hash a password (for testing purposes)."""
    console: Console = ctx.obj['console']

    result = HashCracker.hash_password(hash_value, algorithm)

    console.print(f"\n[bold]Input:[/bold] {hash_value}")
    console.print(f"[bold]Algorithm:[/bold] {algorithm}")
    console.print(f"[bold]Hash:[/bold] {result}\n")


@cli.command()
@click.pass_context
def info(ctx):
    """Display information about available generators and algorithms."""
    console: Console = ctx.obj['console']

    # Generators info
    generators_table = Table(title="Available Generators")
    generators_table.add_column("Generator", style="cyan")
    generators_table.add_column("Description", style="white")

    generators_table.add_row("leetspeak", "Converts normal words using leetspeak substitutions (a->4, e->3, etc.)")
    generators_table.add_row("phonetic", "Uses phonetic substitutions (for->4, to->2, you->u)")
    generators_table.add_row("pattern", "Generates pattern-based passwords (keyboard walks, sequences, etc.)")
    generators_table.add_row("random", "Creates random character combinations")
    generators_table.add_row("markov", "Uses Markov chains to generate statistically similar passwords")

    console.print(generators_table)

    # Algorithms info
    algorithms_table = Table(title="Supported Hash Algorithms")
    algorithms_table.add_column("Algorithm", style="cyan")
    algorithms_table.add_column("Bits", style="white")

    algorithms_table.add_row("md5", "128")
    algorithms_table.add_row("sha1", "160")
    algorithms_table.add_row("sha224", "224")
    algorithms_table.add_row("sha256", "256")
    algorithms_table.add_row("sha384", "384")
    algorithms_table.add_row("sha512", "512")
    algorithms_table.add_row("blake2b", "512")
    algorithms_table.add_row("blake2s", "256")

    console.print("\n")
    console.print(algorithms_table)


def main():
    """Entry point for the CLI."""
    cli(obj={})


if __name__ == '__main__':
    main()
