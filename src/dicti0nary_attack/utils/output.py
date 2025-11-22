"""Output formatting and reporting."""

import json
import csv
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class OutputFormatter:
    """Handles output formatting and report generation."""

    def __init__(self, output_dir: str = "output"):
        """
        Initialize the output formatter.

        Args:
            output_dir: Directory for output files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def save_passwords(
        self,
        passwords: List[str],
        filename: str,
        format: str = 'text'
    ):
        """
        Save passwords to file.

        Args:
            passwords: List of passwords
            filename: Output filename
            format: Output format (text, json, csv)
        """
        filepath = os.path.join(self.output_dir, filename)

        try:
            if format == 'text':
                with open(filepath, 'w') as f:
                    for pwd in passwords:
                        f.write(f"{pwd}\n")

            elif format == 'json':
                with open(filepath, 'w') as f:
                    json.dump({'passwords': passwords}, f, indent=2)

            elif format == 'csv':
                with open(filepath, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['password'])
                    for pwd in passwords:
                        writer.writerow([pwd])

            logger.info(f"Saved {len(passwords)} passwords to {filepath}")
        except Exception as e:
            logger.error(f"Error saving passwords: {e}")

    def save_stats(self, stats: Dict[str, Any], filename: str = 'stats.json'):
        """
        Save statistics to JSON file.

        Args:
            stats: Statistics dictionary
            filename: Output filename
        """
        filepath = os.path.join(self.output_dir, filename)

        try:
            with open(filepath, 'w') as f:
                json.dump(stats, f, indent=2, default=str)

            logger.info(f"Saved statistics to {filepath}")
        except Exception as e:
            logger.error(f"Error saving statistics: {e}")

    def generate_html_report(
        self,
        title: str,
        stats: Dict[str, Any],
        results: Optional[Dict[str, Any]] = None,
        filename: str = 'report.html'
    ):
        """
        Generate an HTML report.

        Args:
            title: Report title
            stats: Statistics to include
            results: Optional results data
            filename: Output filename
        """
        filepath = os.path.join(self.output_dir, filename)

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #666;
            margin-top: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .stat-box {{
            display: inline-block;
            margin: 10px;
            padding: 20px;
            background-color: #f0f0f0;
            border-radius: 5px;
            min-width: 200px;
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        .warning {{
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <div class="warning">
            <strong>⚠ Security Notice:</strong> This tool is for authorized security testing only.
            Unauthorized access to computer systems is illegal.
        </div>

        <h2>Statistics</h2>
        <div>
"""

        for key, value in stats.items():
            html += f"""            <div class="stat-box">
                <div class="stat-value">{value}</div>
                <div class="stat-label">{key.replace('_', ' ').title()}</div>
            </div>
"""

        if results:
            html += """
        </div>

        <h2>Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
"""
            for key, value in results.items():
                html += f"""                <tr>
                    <td>{key}</td>
                    <td>{value}</td>
                </tr>
"""
            html += """            </tbody>
        </table>
"""

        html += """    </div>
</body>
</html>
"""

        try:
            with open(filepath, 'w') as f:
                f.write(html)

            logger.info(f"Generated HTML report: {filepath}")
        except Exception as e:
            logger.error(f"Error generating HTML report: {e}")

    def save_cracking_results(
        self,
        results: Dict[str, str],
        stats: Dict[str, Any],
        filename: str = 'cracking_results.json'
    ):
        """
        Save hash cracking results.

        Args:
            results: Dictionary mapping hashes to passwords
            stats: Cracking statistics
            filename: Output filename
        """
        filepath = os.path.join(self.output_dir, filename)

        data = {
            'timestamp': datetime.now().isoformat(),
            'stats': stats,
            'results': [
                {'hash': h, 'password': p}
                for h, p in results.items()
            ]
        }

        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)

            logger.info(f"Saved cracking results to {filepath}")
        except Exception as e:
            logger.error(f"Error saving cracking results: {e}")
