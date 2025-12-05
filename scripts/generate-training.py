#!/usr/bin/env python3
"""
Generate Training Data from Multilingual Wordlists

Creates training datasets for Markov chain password generation using
multilingual wordlists extracted from 1000Langs corpora.

SPDX-License-Identifier: GPL-3.0-or-later
SPDX-FileCopyrightText: 2025 Security Research Team
"""

import argparse
import json
import random
import sys
from pathlib import Path
from typing import List, Set


def load_wordlist(wordlist_path: Path) -> List[str]:
    """Load words from a wordlist file."""
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]
        return words
    except Exception as e:
        print(f"❌ Error loading {wordlist_path}: {e}", file=sys.stderr)
        return []


def generate_password_variations(
    word: str,
    variations_per_word: int = 5
) -> List[str]:
    """Generate password variations from a base word."""
    variations = [word]

    # Capitalize first letter
    variations.append(word.capitalize())

    # Add numbers at end
    for i in range(variations_per_word - 2):
        num_suffix = random.randint(0, 9999)
        variations.append(f"{word}{num_suffix}")

    # Leetspeak substitutions
    leet_map = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
    leet_word = ''.join(leet_map.get(c, c) for c in word)
    if leet_word != word:
        variations.append(leet_word)

    return variations


def generate_training_dataset(
    wordlists_dir: Path,
    output_file: Path,
    languages: List[str],
    samples_per_language: int = 1000,
    variations_per_word: int = 3,
) -> None:
    """Generate combined training dataset from multiple languages."""
    print("🎓 Generating training dataset...")
    print()

    all_training_data = []
    stats = {
        'languages': {},
        'total_words': 0,
        'total_variations': 0,
    }

    # Process each language
    for lang in languages:
        wordlist_file = wordlists_dir / f"{lang}.txt"

        if not wordlist_file.exists():
            print(f"⚠️  Wordlist not found: {wordlist_file}")
            print(f"   Run: just extract-wordlists {lang}")
            continue

        print(f"📖 Loading {lang} wordlist...")
        words = load_wordlist(wordlist_file)

        if not words:
            print(f"   ⚠️  No words loaded from {lang}")
            continue

        # Sample words
        sample_size = min(samples_per_language, len(words))
        sampled_words = random.sample(words, sample_size)

        # Generate variations
        lang_training_data = []
        for word in sampled_words:
            variations = generate_password_variations(word, variations_per_word)
            lang_training_data.extend(variations)

        all_training_data.extend(lang_training_data)

        stats['languages'][lang] = {
            'wordlist_size': len(words),
            'sampled_words': sample_size,
            'generated_variations': len(lang_training_data),
        }

        print(f"   ✓ {len(lang_training_data)} training examples generated")

    print()
    print(f"📊 Combined dataset: {len(all_training_data)} examples")
    print()

    # Shuffle combined dataset
    random.shuffle(all_training_data)

    # Write training data
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        for example in all_training_data:
            f.write(f"{example}\n")

    print(f"💾 Training data saved to: {output_file}")
    print()

    # Save statistics
    stats_file = output_file.with_suffix('.json')
    stats['total_words'] = sum(s['sampled_words'] for s in stats['languages'].values())
    stats['total_variations'] = len(all_training_data)

    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print(f"📊 Statistics saved to: {stats_file}")
    print()

    # Show breakdown
    print("Language Breakdown:")
    for lang, lang_stats in stats['languages'].items():
        print(f"  {lang:5s} - {lang_stats['generated_variations']:6d} variations "
              f"({lang_stats['sampled_words']:5d} words)")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='Generate training data from multilingual wordlists'
    )
    parser.add_argument(
        '--languages',
        nargs='+',
        default=['en', 'es', 'fr', 'de', 'zh', 'ar', 'hi'],
        help='Language codes to include (default: en es fr de zh ar hi)'
    )
    parser.add_argument(
        '--wordlists-dir',
        type=Path,
        default=Path(__file__).parent.parent / 'wordlists' / 'multilingual',
        help='Directory containing wordlists'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path(__file__).parent.parent / 'wordlists' / 'training_data.txt',
        help='Output file for training data'
    )
    parser.add_argument(
        '--samples-per-language',
        type=int,
        default=1000,
        help='Number of words to sample per language (default: 1000)'
    )
    parser.add_argument(
        '--variations',
        type=int,
        default=3,
        help='Password variations per word (default: 3)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Random seed for reproducibility (default: 42)'
    )

    args = parser.parse_args()

    # Set random seed
    random.seed(args.seed)

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  Training Data Generator")
    print("  Multilingual Password Research Dataset")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()

    generate_training_dataset(
        args.wordlists_dir,
        args.output,
        args.languages,
        args.samples_per_language,
        args.variations,
    )

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✓ Training data generation complete!")
    print()
    print("USAGE:")
    print(f"  • Train Markov model with Chapel:")
    print(f"    chapel src/generators/Markov.chpl --training={args.output}")
    print()
    print(f"  • Use in password generation:")
    print(f"    ./dicti0nary --command=generate --generator=markov")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


if __name__ == '__main__':
    main()
