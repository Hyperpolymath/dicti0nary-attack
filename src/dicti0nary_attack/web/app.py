"""Flask web application for dicti0nary-attack."""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from datetime import datetime

from dicti0nary_attack.generators import (
    LeetspeakGenerator,
    PhoneticGenerator,
    PatternGenerator,
    RandomGenerator,
    MarkovGenerator,
)
from dicti0nary_attack.crackers import HashCracker
from dicti0nary_attack.utils.config import ConfigManager


def create_app(config_path=None):
    """
    Create and configure the Flask application.

    Args:
        config_path: Optional path to configuration file

    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Load configuration
    config_manager = ConfigManager(config_path)
    app.config['DICTI0NARY_CONFIG'] = config_manager

    @app.route('/')
    def index():
        """Main page."""
        return render_template('index.html')

    @app.route('/api/generators')
    def get_generators():
        """Get list of available generators."""
        generators = [
            {
                'id': 'leetspeak',
                'name': 'Leetspeak',
                'description': 'Converts words using character substitutions (a→4, e→3, etc.)'
            },
            {
                'id': 'phonetic',
                'name': 'Phonetic',
                'description': 'Uses phonetic substitutions (for→4, to→2, you→u)'
            },
            {
                'id': 'pattern',
                'name': 'Pattern',
                'description': 'Generates pattern-based passwords (keyboard walks, sequences)'
            },
            {
                'id': 'random',
                'name': 'Random',
                'description': 'Creates random character combinations'
            },
            {
                'id': 'markov',
                'name': 'Markov',
                'description': 'Statistical password generation using Markov chains'
            }
        ]
        return jsonify(generators)

    @app.route('/api/algorithms')
    def get_algorithms():
        """Get list of supported hash algorithms."""
        algorithms = [
            {'id': algo, 'name': algo.upper()}
            for algo in HashCracker.SUPPORTED_ALGORITHMS.keys()
        ]
        return jsonify(algorithms)

    @app.route('/api/generate', methods=['POST'])
    def generate_passwords():
        """Generate passwords via API."""
        data = request.get_json()

        generator_type = data.get('generator', 'leetspeak')
        count = min(int(data.get('count', 100)), 10000)  # Limit to 10k for web

        config_manager: ConfigManager = app.config['DICTI0NARY_CONFIG']
        gen_config = config_manager.get_generator_config(generator_type)

        # Override with request params
        if 'min_length' in data:
            gen_config['min_length'] = int(data['min_length'])
        if 'max_length' in data:
            gen_config['max_length'] = int(data['max_length'])

        try:
            if generator_type == 'leetspeak':
                gen = LeetspeakGenerator(config=gen_config)
            elif generator_type == 'phonetic':
                gen = PhoneticGenerator(config=gen_config)
            elif generator_type == 'pattern':
                gen = PatternGenerator(config=gen_config)
            elif generator_type == 'random':
                gen = RandomGenerator(config=gen_config)
            elif generator_type == 'markov':
                gen = MarkovGenerator(config=gen_config)
            else:
                return jsonify({'error': 'Invalid generator type'}), 400

            passwords = list(gen.generate(count=count))
            stats = gen.get_stats()

            return jsonify({
                'passwords': passwords,
                'stats': stats,
                'count': len(passwords)
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/hash', methods=['POST'])
    def hash_password():
        """Hash a password."""
        data = request.get_json()

        password = data.get('password')
        algorithm = data.get('algorithm', 'sha256')

        if not password:
            return jsonify({'error': 'Password required'}), 400

        try:
            hash_value = HashCracker.hash_password(password, algorithm)
            return jsonify({
                'password': password,
                'algorithm': algorithm,
                'hash': hash_value
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/crack', methods=['POST'])
    def crack_hash():
        """Crack a password hash."""
        data = request.get_json()

        target_hash = data.get('hash')
        algorithm = data.get('algorithm', 'sha256')
        generator_type = data.get('generator', 'pattern')
        max_attempts = min(int(data.get('max_attempts', 10000)), 50000)  # Limit for web

        if not target_hash:
            return jsonify({'error': 'Hash required'}), 400

        config_manager: ConfigManager = app.config['DICTI0NARY_CONFIG']
        gen_config = config_manager.get_generator_config(generator_type)

        try:
            # Create generator
            if generator_type == 'leetspeak':
                gen = LeetspeakGenerator(config=gen_config)
            elif generator_type == 'phonetic':
                gen = PhoneticGenerator(config=gen_config)
            elif generator_type == 'pattern':
                gen = PatternGenerator(config=gen_config)
            elif generator_type == 'random':
                gen = RandomGenerator(config=gen_config)
            elif generator_type == 'markov':
                gen = MarkovGenerator(config=gen_config)
            else:
                return jsonify({'error': 'Invalid generator type'}), 400

            # Create cracker
            cracker_config = config_manager.get_cracker_config()
            cracker_config['algorithm'] = algorithm
            cracker = HashCracker(config=cracker_config)

            # Limit password generation
            password_gen = gen.generate(count=max_attempts)

            # Crack
            result = cracker.crack(target_hash, password_gen)
            stats = cracker.get_stats()

            return jsonify({
                'found': result is not None,
                'password': result,
                'stats': stats
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/stats')
    def get_stats():
        """Get application statistics."""
        return jsonify({
            'version': '0.1.0',
            'generators': 5,
            'algorithms': len(HashCracker.SUPPORTED_ALGORITHMS),
            'timestamp': datetime.now().isoformat()
        })

    return app


def main():
    """Run the web application."""
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
