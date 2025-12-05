#!/usr/bin/env python3
"""
Extract Multilingual Wordlists from 1000Langs Corpora

Extracts common words from parallel corpora for password generation training.
Focuses on words that users might use in passwords across different languages.

SPDX-License-Identifier: GPL-3.0-or-later
SPDX-FileCopyrightText: 2025 Security Research Team
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import List, Set


def extract_words(text: str, min_length: int = 3, max_length: int = 15) -> List[str]:
    """Extract words from text with length constraints."""
    # Remove punctuation, split on whitespace
    words = re.findall(r'\b\w+\b', text.lower())

    # Filter by length
    words = [w for w in words if min_length <= len(w) <= max_length]

    return words


def process_corpus_file(corpus_path: Path, min_freq: int = 5) -> Counter:
    """Process a single corpus file and extract word frequencies."""
    word_counter = Counter()

    try:
        with open(corpus_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Handle different corpus formats
                if '\t' in line:
                    # Parallel corpus format: lang1\tlang2
                    parts = line.split('\t')
                    text = ' '.join(parts)
                else:
                    # Plain text format
                    text = line

                words = extract_words(text)
                word_counter.update(words)

    except Exception as e:
        print(f"⚠️  Error processing {corpus_path}: {e}", file=sys.stderr)
        return word_counter

    # Filter by minimum frequency
    word_counter = Counter({
        word: count for word, count in word_counter.items()
        if count >= min_freq
    })

    return word_counter


def find_corpus_files(langs_dir: Path, language: str) -> List[Path]:
    """Find corpus files for a given language."""
    corpus_files = []

    # Common corpus locations in 1000Langs
    search_paths = [
        langs_dir / 'corpora' / language,
        langs_dir / 'bible' / language,
        langs_dir / 'data' / language,
        langs_dir / language,
    ]

    for search_path in search_paths:
        if search_path.exists():
            # Find text files
            corpus_files.extend(search_path.glob('*.txt'))
            corpus_files.extend(search_path.glob('*.tsv'))
            corpus_files.extend(search_path.glob('**/*.txt'))
            corpus_files.extend(search_path.glob('**/*.tsv'))

    return list(set(corpus_files))  # Remove duplicates


def generate_wordlist(
    language: str,
    langs_dir: Path,
    output_dir: Path,
    top_n: int = 10000,
    min_freq: int = 5,
) -> None:
    """Generate wordlist for a specific language."""
    print(f"🌍 Extracting wordlist for language: {language}")
    print()

    # Find corpus files
    corpus_files = find_corpus_files(langs_dir, language)

    if not corpus_files:
        print(f"❌ No corpus files found for language: {language}")
        print(f"   Searched in: {langs_dir}")
        sys.exit(1)

    print(f"📚 Found {len(corpus_files)} corpus file(s)")
    for cf in corpus_files[:5]:  # Show first 5
        print(f"   • {cf.relative_to(langs_dir)}")
    if len(corpus_files) > 5:
        print(f"   ... and {len(corpus_files) - 5} more")
    print()

    # Process all corpus files
    print("🔍 Extracting words...")
    all_words = Counter()

    for i, corpus_file in enumerate(corpus_files, 1):
        print(f"   Processing {i}/{len(corpus_files)}: {corpus_file.name}...", end='\r')
        word_counts = process_corpus_file(corpus_file, min_freq=min_freq)
        all_words.update(word_counts)

    print()
    print(f"✓ Extracted {len(all_words)} unique words")
    print()

    # Get top N most common words
    top_words = [word for word, count in all_words.most_common(top_n)]

    # Write wordlist
    output_file = output_dir / f"{language}.txt"
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        for word in top_words:
            f.write(f"{word}\n")

    print(f"💾 Wordlist saved to: {output_file}")
    print(f"   Total words:  {len(top_words)}")
    print()

    # Save statistics
    stats_file = output_dir / f"{language}.json"
    stats = {
        'language': language,
        'total_unique_words': len(all_words),
        'wordlist_size': len(top_words),
        'corpus_files': [str(cf.relative_to(langs_dir)) for cf in corpus_files],
        'top_20_words': top_words[:20],
    }

    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print(f"📊 Statistics saved to: {stats_file}")
    print()

    # Show sample words
    print("Sample words (top 20):")
    for i, word in enumerate(top_words[:20], 1):
        print(f"  {i:2d}. {word}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='Extract multilingual wordlists from 1000Langs corpora'
    )
    parser.add_argument(
        'language',
        help='Language code (e.g., en, es, fr, de, zh, ar, hi)'
    )
    parser.add_argument(
        '--langs-dir',
        type=Path,
        default=Path(__file__).parent.parent / 'vendor' / '1000Langs',
        help='Path to 1000Langs repository'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path(__file__).parent.parent / 'wordlists' / 'multilingual',
        help='Output directory for wordlists'
    )
    parser.add_argument(
        '--top-n',
        type=int,
        default=10000,
        help='Number of top words to extract (default: 10000)'
    )
    parser.add_argument(
        '--min-freq',
        type=int,
        default=5,
        help='Minimum word frequency (default: 5)'
    )

    args = parser.parse_args()

    # Validate 1000Langs directory
    if not args.langs_dir.exists():
        print(f"❌ 1000Langs directory not found: {args.langs_dir}")
        print()
        print("Run setup first:")
        print("  just setup-1000langs")
        sys.exit(1)

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  Multilingual Wordlist Extractor")
    print("  dicti0nary-attack + 1000Langs Integration")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()

    generate_wordlist(
        args.language,
        args.langs_dir,
        args.output_dir,
        args.top_n,
        args.min_freq,
    )

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✓ Wordlist extraction complete!")
    print()
    print("NEXT STEPS:")
    print("  • Use wordlist for training: just generate-training")
    print(f"  • Train Markov model:        chapel Markov.chpl < {args.output_dir}/{args.language}.txt")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


if __name__ == '__main__':
    main()
