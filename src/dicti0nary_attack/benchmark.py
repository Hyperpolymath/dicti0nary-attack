"""Benchmarking and profiling tools."""

import time
import statistics
from typing import Dict, Any, List, Callable
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table

from dicti0nary_attack.generators import (
    LeetspeakGenerator,
    PhoneticGenerator,
    PatternGenerator,
    RandomGenerator,
    MarkovGenerator,
)
from dicti0nary_attack.crackers import HashCracker

console = Console()


@dataclass
class BenchmarkResult:
    """Results from a benchmark run."""
    name: str
    total_time: float
    operations: int
    ops_per_second: float
    mean_time: float
    median_time: float
    min_time: float
    max_time: float


class Benchmark:
    """Benchmarking tools for performance testing."""

    @staticmethod
    def benchmark_generator(generator_type: str, iterations: int = 5, passwords_per_run: int = 1000) -> BenchmarkResult:
        """
        Benchmark a password generator.

        Args:
            generator_type: Type of generator to benchmark
            iterations: Number of benchmark iterations
            passwords_per_run: Passwords to generate per iteration

        Returns:
            Benchmark results
        """
        generators = {
            'leetspeak': LeetspeakGenerator,
            'phonetic': PhoneticGenerator,
            'pattern': PatternGenerator,
            'random': RandomGenerator,
            'markov': MarkovGenerator,
        }

        if generator_type not in generators:
            raise ValueError(f"Unknown generator: {generator_type}")

        times = []
        total_ops = 0

        for _ in range(iterations):
            gen = generators[generator_type]()

            start = time.perf_counter()
            count = 0
            for _ in gen.generate(count=passwords_per_run):
                count += 1
            end = time.perf_counter()

            times.append(end - start)
            total_ops += count

        total_time = sum(times)
        ops_per_second = total_ops / total_time if total_time > 0 else 0

        return BenchmarkResult(
            name=f"{generator_type} generator",
            total_time=total_time,
            operations=total_ops,
            ops_per_second=ops_per_second,
            mean_time=statistics.mean(times),
            median_time=statistics.median(times),
            min_time=min(times),
            max_time=max(times),
        )

    @staticmethod
    def benchmark_hash_algorithm(algorithm: str, iterations: int = 5, passwords: int = 1000) -> BenchmarkResult:
        """
        Benchmark a hash algorithm.

        Args:
            algorithm: Hash algorithm to benchmark
            iterations: Number of benchmark iterations
            passwords: Number of passwords to hash per iteration

        Returns:
            Benchmark results
        """
        test_passwords = [f"password{i}" for i in range(passwords)]
        times = []
        total_ops = 0

        for _ in range(iterations):
            start = time.perf_counter()

            for pwd in test_passwords:
                HashCracker.hash_password(pwd, algorithm)

            end = time.perf_counter()

            times.append(end - start)
            total_ops += len(test_passwords)

        total_time = sum(times)
        ops_per_second = total_ops / total_time if total_time > 0 else 0

        return BenchmarkResult(
            name=f"{algorithm} hashing",
            total_time=total_time,
            operations=total_ops,
            ops_per_second=ops_per_second,
            mean_time=statistics.mean(times),
            median_time=statistics.median(times),
            min_time=min(times),
            max_time=max(times),
        )

    @staticmethod
    def benchmark_cracking(algorithm: str, passwords: int = 1000, parallel: bool = False) -> BenchmarkResult:
        """
        Benchmark hash cracking performance.

        Args:
            algorithm: Hash algorithm to use
            passwords: Number of passwords to test
            parallel: Whether to use parallel processing

        Returns:
            Benchmark results
        """
        # Create test data
        target_password = f"password{passwords // 2}"  # Middle password
        target_hash = HashCracker.hash_password(target_password, algorithm)

        # Generate password list
        password_list = [f"password{i}" for i in range(passwords)]

        # Benchmark
        cracker = HashCracker(config={'algorithm': algorithm, 'workers': 4})

        start = time.perf_counter()

        if parallel:
            result = cracker.crack_parallel(target_hash, iter(password_list))
        else:
            result = cracker.crack(target_hash, iter(password_list))

        end = time.perf_counter()

        total_time = end - start
        ops_per_second = passwords / total_time if total_time > 0 else 0

        mode = "parallel" if parallel else "serial"

        return BenchmarkResult(
            name=f"{algorithm} cracking ({mode})",
            total_time=total_time,
            operations=passwords,
            ops_per_second=ops_per_second,
            mean_time=total_time,
            median_time=total_time,
            min_time=total_time,
            max_time=total_time,
        )

    @staticmethod
    def run_all_benchmarks() -> List[BenchmarkResult]:
        """
        Run all benchmarks.

        Returns:
            List of benchmark results
        """
        results = []

        console.print("\n[bold cyan]Running Generator Benchmarks...[/bold cyan]\n")

        # Generator benchmarks
        for gen_type in ['leetspeak', 'phonetic', 'pattern', 'random', 'markov']:
            with console.status(f"Benchmarking {gen_type}..."):
                result = Benchmark.benchmark_generator(gen_type, iterations=3, passwords_per_run=500)
                results.append(result)

        console.print("\n[bold cyan]Running Hash Algorithm Benchmarks...[/bold cyan]\n")

        # Hash algorithm benchmarks
        for algo in ['md5', 'sha256', 'sha512']:
            with console.status(f"Benchmarking {algo}..."):
                result = Benchmark.benchmark_hash_algorithm(algo, iterations=3, passwords=500)
                results.append(result)

        console.print("\n[bold cyan]Running Cracking Benchmarks...[/bold cyan]\n")

        # Cracking benchmarks
        for algo in ['sha256']:
            for parallel in [False, True]:
                with console.status(f"Benchmarking cracking ({algo}, parallel={parallel})..."):
                    result = Benchmark.benchmark_cracking(algo, passwords=500, parallel=parallel)
                    results.append(result)

        return results

    @staticmethod
    def display_results(results: List[BenchmarkResult]):
        """
        Display benchmark results in a table.

        Args:
            results: List of benchmark results
        """
        table = Table(title="Benchmark Results")

        table.add_column("Benchmark", style="cyan")
        table.add_column("Total Time (s)", style="magenta")
        table.add_column("Operations", style="green")
        table.add_column("Ops/Second", style="yellow")
        table.add_column("Mean Time (s)", style="blue")

        for result in results:
            table.add_row(
                result.name,
                f"{result.total_time:.4f}",
                f"{result.operations:,}",
                f"{result.ops_per_second:,.2f}",
                f"{result.mean_time:.4f}",
            )

        console.print("\n")
        console.print(table)
        console.print("\n")


def main():
    """Run benchmarks from command line."""
    console.print("\n[bold]dicti0nary-attack Performance Benchmarks[/bold]\n")

    results = Benchmark.run_all_benchmarks()
    Benchmark.display_results(results)


if __name__ == '__main__':
    main()
