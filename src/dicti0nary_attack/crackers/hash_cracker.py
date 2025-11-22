"""Hash cracking engine with multiple algorithm support."""

import hashlib
import logging
from typing import Optional, Dict, Any, Callable, Iterator, List
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

logger = logging.getLogger(__name__)


class HashCracker:
    """
    Multi-algorithm hash cracking engine.

    Supports various hashing algorithms and parallel processing for
    efficient password cracking in authorized security testing scenarios.
    """

    SUPPORTED_ALGORITHMS = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha224': hashlib.sha224,
        'sha256': hashlib.sha256,
        'sha384': hashlib.sha384,
        'sha512': hashlib.sha512,
        'blake2b': hashlib.blake2b,
        'blake2s': hashlib.blake2s,
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the hash cracker.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.algorithm = self.config.get('algorithm', 'sha256')
        self.workers = self.config.get('workers', 4)
        self.batch_size = self.config.get('batch_size', 1000)

        self.stats = {
            'attempts': 0,
            'matches': 0,
            'start_time': None,
            'end_time': None,
        }

        if self.algorithm not in self.SUPPORTED_ALGORITHMS:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")

    def crack(
        self,
        target_hash: str,
        password_generator: Iterator[str],
        callback: Optional[Callable[[str], None]] = None
    ) -> Optional[str]:
        """
        Attempt to crack a hash using generated passwords.

        Args:
            target_hash: The hash to crack
            password_generator: Iterator providing password candidates
            callback: Optional callback function called when match is found

        Returns:
            The cracked password if found, None otherwise
        """
        self.stats['start_time'] = time.time()
        self.stats['attempts'] = 0
        self.stats['matches'] = 0

        target_hash = target_hash.lower()
        hash_func = self.SUPPORTED_ALGORITHMS[self.algorithm]

        logger.info(f"Starting hash cracking with algorithm: {self.algorithm}")

        try:
            for password in password_generator:
                self.stats['attempts'] += 1

                # Compute hash
                computed_hash = hash_func(password.encode()).hexdigest()

                if computed_hash == target_hash:
                    self.stats['matches'] += 1
                    self.stats['end_time'] = time.time()

                    logger.info(f"Match found! Password: {password}")

                    if callback:
                        callback(password)

                    return password

                # Progress logging
                if self.stats['attempts'] % 10000 == 0:
                    elapsed = time.time() - self.stats['start_time']
                    rate = self.stats['attempts'] / elapsed if elapsed > 0 else 0
                    logger.debug(f"Attempts: {self.stats['attempts']}, Rate: {rate:.2f}/s")

        finally:
            self.stats['end_time'] = time.time()

        logger.info(f"Cracking complete. Total attempts: {self.stats['attempts']}")
        return None

    def crack_parallel(
        self,
        target_hash: str,
        password_generator: Iterator[str],
        callback: Optional[Callable[[str], None]] = None
    ) -> Optional[str]:
        """
        Attempt to crack a hash using parallel processing.

        Args:
            target_hash: The hash to crack
            password_generator: Iterator providing password candidates
            callback: Optional callback function called when match is found

        Returns:
            The cracked password if found, None otherwise
        """
        self.stats['start_time'] = time.time()
        self.stats['attempts'] = 0

        target_hash = target_hash.lower()

        logger.info(f"Starting parallel hash cracking with {self.workers} workers")

        with ProcessPoolExecutor(max_workers=self.workers) as executor:
            futures = []
            batch = []

            for password in password_generator:
                batch.append(password)

                if len(batch) >= self.batch_size:
                    future = executor.submit(
                        self._crack_batch,
                        target_hash,
                        batch,
                        self.algorithm
                    )
                    futures.append(future)
                    batch = []

            # Submit remaining passwords
            if batch:
                future = executor.submit(
                    self._crack_batch,
                    target_hash,
                    batch,
                    self.algorithm
                )
                futures.append(future)

            # Process results
            for future in as_completed(futures):
                result = future.result()
                self.stats['attempts'] += result['attempts']

                if result['match']:
                    self.stats['matches'] += 1
                    self.stats['end_time'] = time.time()

                    logger.info(f"Match found! Password: {result['match']}")

                    # Cancel remaining futures
                    for f in futures:
                        f.cancel()

                    if callback:
                        callback(result['match'])

                    return result['match']

        self.stats['end_time'] = time.time()
        logger.info(f"Cracking complete. Total attempts: {self.stats['attempts']}")
        return None

    @staticmethod
    def _crack_batch(target_hash: str, passwords: List[str], algorithm: str) -> Dict[str, Any]:
        """
        Process a batch of passwords (used in parallel processing).

        Args:
            target_hash: The target hash
            passwords: List of password candidates
            algorithm: Hash algorithm to use

        Returns:
            Dictionary with results
        """
        hash_func = HashCracker.SUPPORTED_ALGORITHMS[algorithm]
        attempts = 0

        for password in passwords:
            attempts += 1
            computed_hash = hash_func(password.encode()).hexdigest()

            if computed_hash == target_hash:
                return {
                    'match': password,
                    'attempts': attempts
                }

        return {
            'match': None,
            'attempts': attempts
        }

    def crack_multiple(
        self,
        target_hashes: List[str],
        password_generator: Iterator[str],
        callback: Optional[Callable[[str, str], None]] = None
    ) -> Dict[str, str]:
        """
        Attempt to crack multiple hashes simultaneously.

        Args:
            target_hashes: List of hashes to crack
            password_generator: Iterator providing password candidates
            callback: Optional callback(hash, password) called for each match

        Returns:
            Dictionary mapping hashes to cracked passwords
        """
        self.stats['start_time'] = time.time()
        self.stats['attempts'] = 0
        self.stats['matches'] = 0

        target_hashes = [h.lower() for h in target_hashes]
        remaining_hashes = set(target_hashes)
        results = {}

        hash_func = self.SUPPORTED_ALGORITHMS[self.algorithm]

        logger.info(f"Starting multi-hash cracking for {len(target_hashes)} hashes")

        for password in password_generator:
            if not remaining_hashes:
                break

            self.stats['attempts'] += 1
            computed_hash = hash_func(password.encode()).hexdigest()

            if computed_hash in remaining_hashes:
                results[computed_hash] = password
                remaining_hashes.remove(computed_hash)
                self.stats['matches'] += 1

                logger.info(f"Match found! Hash: {computed_hash[:16]}... Password: {password}")

                if callback:
                    callback(computed_hash, password)

        self.stats['end_time'] = time.time()
        logger.info(f"Multi-hash cracking complete. Cracked: {len(results)}/{len(target_hashes)}")

        return results

    def get_stats(self) -> Dict[str, Any]:
        """Get cracking statistics."""
        stats = self.stats.copy()

        if stats['start_time'] and stats['end_time']:
            elapsed = stats['end_time'] - stats['start_time']
            stats['elapsed_time'] = elapsed
            stats['rate'] = stats['attempts'] / elapsed if elapsed > 0 else 0
        else:
            stats['elapsed_time'] = None
            stats['rate'] = None

        return stats

    @staticmethod
    def hash_password(password: str, algorithm: str = 'sha256') -> str:
        """
        Hash a password using the specified algorithm.

        Args:
            password: Password to hash
            algorithm: Hash algorithm to use

        Returns:
            Hexadecimal hash string
        """
        if algorithm not in HashCracker.SUPPORTED_ALGORITHMS:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        hash_func = HashCracker.SUPPORTED_ALGORITHMS[algorithm]
        return hash_func(password.encode()).hexdigest()
