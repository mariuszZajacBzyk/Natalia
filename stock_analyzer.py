#!/usr/bin/env python3
"""
Payton Stock Analysis Application
Analyzes stock performance based on financial metrics and calculates valuation indices.

Features:
- Load stock data from CSV files
- Calculate EPS (Earnings Per Share)
- Calculate ROI (Return on Investment)
- Calculate Valuation Index based on ROI, Growth, and Risk
- Filter stocks by valuation index and risk criteria
- Export results to CSV format
- Interactive mode for custom filtering
"""

import csv
import sys
import os
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Stock:
    """Represents a stock with its financial metrics."""
    bedrijf: str  # Company name (Dutch: bedrijf)
    sector: str   # Sector (Dutch: sector)
    koers: float  # Stock price (Dutch: koers)
    eps: float    # Earnings per share (Dutch: winst_per_aandeel)
    dividend: float = 0.0  # Dividend (Dutch: dividend)
    groei_percentage: float = 0.0  # Growth percentage (Dutch: groei_percentage)
    risico: float = 0.0  # Risk score (Dutch: risico)
    
    # Calculated fields
    roi: float = field(default=0.0)  # Return on Investment
    valuatie_index: float = field(default=0.0)  # Valuation index (Dutch: valuatie_index)
    
    def calculate_metrics(self) -> None:
        """
        Calculate ROI and valuation index based on financial metrics.
        
        Formulas:
        - ROI = ((EPS + Dividend) / Price) × 100
        - Valuation Index = (ROI × Growth%) / Risk
        """
        # Calculate ROI: ROI = ((EPS + Dividend) / Price) × 100
        if self.koers > 0:
            self.roi = ((self.eps + self.dividend) / self.koers) * 100
        else:
            self.roi = 0.0
        
        # Calculate Valuation Index: Index = (ROI × Growth%) / Risk
        if self.risico > 0:
            self.valuatie_index = (self.roi * self.groei_percentage) / self.risico
        else:
            self.valuatie_index = 0.0
    
    def to_dict(self) -> Dict:
        """Convert stock to dictionary for export."""
        return {
            'bedrijf': self.bedrijf,
            'sector': self.sector,
            'koers': f"{self.koers:.2f}",
            'winst_per_aandeel': f"{self.eps:.2f}",
            'dividend': f"{self.dividend:.2f}",
            'groei_percentage': f"{self.groei_percentage:.2f}",
            'risico': f"{self.risico:.2f}",
            'roi': f"{self.roi:.2f}",
            'valuatie_index': f"{self.valuatie_index:.2f}"
        }


class StockAnalyzer:
    """
    Analyzes stocks and generates filtered reports.
    
    Handles CSV loading, metric calculation, filtering, and report generation.
    """
    
    def __init__(self, min_valuation_index: float = 10.0, max_risk_score: float = 5.0):
        """
        Initialize the stock analyzer with filter criteria.
        
        Args:
            min_valuation_index: Minimum acceptable valuation index
            max_risk_score: Maximum acceptable risk score
        """
        self.min_valuation_index = min_valuation_index
        self.max_risk_score = max_risk_score
        self.stocks: List[Stock] = []
        self.csv_filename: Optional[str] = None
    
    def load_from_csv(self, filename: str) -> bool:
        """
        Load stock data from a CSV file with Dutch column names.
        
        Expected CSV columns (semicolon-separated):
        - bedrijf: Company name
        - sector: Sector
        - koers: Stock price
        - winst_per_aandeel: Earnings per share (EPS)
        - dividend: Dividend per share
        - groei_percentage: Growth percentage
        - risico: Risk score
        
        Args:
            filename: Path to CSV file
            
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                if reader.fieldnames is None:
                    print(f"Error: CSV file '{filename}' is empty or invalid", file=sys.stderr)
                    return False
                
                required_fields = {'bedrijf', 'sector', 'koers', 'winst_per_aandeel'}
                if not required_fields.issubset(set(reader.fieldnames)):
                    print(f"Error: CSV must contain columns: {required_fields}", file=sys.stderr)
                    print(f"Found columns: {set(reader.fieldnames)}", file=sys.stderr)
                    return False
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Normalize whitespace in field names and values
                        row = {k.strip(): v.strip() for k, v in row.items()}
                        
                        stock = Stock(
                            bedrijf=row['bedrijf'],
                            sector=row['sector'],
                            koers=float(row['koers']),
                            eps=float(row['winst_per_aandeel']),
                            dividend=float(row.get('dividend', 0.0)),
                            groei_percentage=float(row.get('groei_percentage', 0.0)),
                            risico=float(row.get('risico', 1.0))
                        )
                        
                        # Validate data
                        if stock.koers <= 0:
                            print(f"Warning: Row {row_num}: Stock '{stock.bedrijf}' has invalid price", file=sys.stderr)
                            continue
                        
                        stock.calculate_metrics()
                        self.stocks.append(stock)
                    
                    except (ValueError, KeyError) as e:
                        print(f"Warning: Row {row_num}: Failed to parse stock data - {e}", file=sys.stderr)
                        continue
            
            return len(self.stocks) > 0
        
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found", file=sys.stderr)
            return False
        except Exception as e:
            print(f"Error: Failed to load CSV file - {e}", file=sys.stderr)
            return False
    
    def filter_stocks(self, 
                     min_valuation_index: Optional[float] = None, 
                     max_risk_score: Optional[float] = None) -> List[Stock]:
        """
        Filter stocks based on criteria.
        
        Filters by:
        - Valuation index >= min_valuation_index
        - Risk score <= max_risk_score
        
        Results are sorted by valuation index (highest first).
        
        Args:
            min_valuation_index: Override default minimum valuation index
            max_risk_score: Override default maximum risk score
            
        Returns:
            List of filtered stocks sorted by valuation index (descending)
        """
        # Support both English CLI arg names and internal Dutch names
        min_idx = min_valuation_index if min_valuation_index is not None else self.min_valuation_index
        max_risk = max_risk_score if max_risk_score is not None else self.max_risk_score

        filtered = [
            stock for stock in self.stocks
            if stock.valuatie_index >= min_idx and stock.risico <= max_risk
        ]

        # Sort by valuatie_index descending
        filtered.sort(key=lambda s: s.valuatie_index, reverse=True)
        return filtered
    
    def get_statistics(self) -> Dict:
        """
        Calculate statistics for all loaded stocks.
        
        Returns:
            Dictionary with statistics
        """
        if not self.stocks:
            return {}
        
        rois = [s.roi for s in self.stocks]
        valuations = [s.valuation_index for s in self.stocks]
        risks = [s.risk_score for s in self.stocks]
        
        return {
            'total_stocks': len(self.stocks),
            'avg_roi': sum(rois) / len(rois),
            'avg_valuation': sum(valuations) / len(valuations),
            'avg_risk': sum(risks) / len(risks),
            'max_roi': max(rois),
            'min_roi': min(rois),
            'max_valuation': max(valuations),
            'min_valuation': min(valuations),
            'max_risk': max(risks),
            'min_risk': min(risks)
        }
    
    def generate_report(self, 
                       min_valuation_index: Optional[float] = None,
                       max_risk_score: Optional[float] = None) -> str:
        """
        Generate a formatted report of filtered stocks.
        
        Args:
            min_valuation_index: Override default minimum valuation index
            max_risk_score: Override default maximum risk score
            
        Returns:
            Report string
        """
        min_idx = min_valuation_index if min_valuation_index is not None else self.min_valuation_index
        max_risk = max_risk_score if max_risk_score is not None else self.max_risk_score
        
        filtered_stocks = self.filter_stocks(min_idx, max_risk)
        
        report = []
        report.append("=" * 130)
        report.append("PAYTON STOCK ANALYSIS REPORT")
        report.append("=" * 130)
        report.append("")
        report.append(f"Filter Criteria:")
        report.append(f"  • Minimum Valuation Index: {min_idx}")
        report.append(f"  • Maximum Risk Score:      {max_risk}")
        report.append(f"  • Total stocks analyzed:   {len(self.stocks)}")
        report.append(f"  • Stocks meeting criteria: {len(filtered_stocks)}")
        report.append("")
        report.append("-" * 130)
        report.append(f"{'Symbol':<8} {'Name':<30} {'Price':<10} {'EPS':<10} {'ROI %':<10} "
                     f"{'Growth %':<10} {'Risk':<8} {'Valuation':<12}")
        report.append("-" * 130)
        
        if filtered_stocks:
            for stock in filtered_stocks:
                report.append(
                    f"{stock.symbol:<8} {stock.name:<30} {stock.price:<10.2f} "
                    f"{stock.eps:<10.2f} {stock.roi:<10.2f} "
                    f"{stock.growth_percentage:<10.2f} {stock.risk_score:<8.2f} "
                    f"{stock.valuation_index:<12.2f}"
                )
        else:
            report.append("No stocks meet the specified criteria.")
        
        report.append("-" * 130)
        report.append("")
        
        return "\n".join(report)
    
    def print_report(self,
                    min_valuation_index: Optional[float] = None,
                    max_risk_score: Optional[float] = None) -> None:
        """Print the stock analysis report to console."""
        print(self.generate_report(min_valuation_index, max_risk_score))

    def print_filtered_table(self, min_valuatie_index: float, max_risico: float) -> None:
        """Print filtered stocks in the concise table format requested by the user.

        Columns: Bedrijf, Sector, Risico, ROI (%), Index
        """
        filtered = self.filter_stocks(min_valuatie_index, max_risico)

        print()
        print("{:-<60}".format(""))
        print(f"{'Bedrijf':<15} {'Sector':<13} {'Risico':>7} {'ROI (%)':>10} {'Index':>10}")
        print("{:-<60}".format(""))

        if filtered:
            for s in filtered:
                print(f"{s.bedrijf:<15} {s.sector:<13} {s.risico:7.2f} {s.roi:10.2f} {s.valuatie_index:10.2f}")
        else:
            print("Geen aandelen voldoen aan de opgegeven criteria.")

        print("{:-<60}".format(""))
    
    def export_to_csv(self, filename: str,
                     min_valuation_index: Optional[float] = None,
                     max_risk_score: Optional[float] = None) -> bool:
        """
        Export filtered results to a CSV file.
        
        Args:
            filename: Output CSV file path
            min_valuation_index: Override default minimum valuation index
            max_risk_score: Override default maximum risk score
            
        Returns:
            True if exported successfully, False otherwise
        """
        try:
            filtered_stocks = self.filter_stocks(min_valuation_index, max_risk_score)

            with open(filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'bedrijf', 'sector', 'koers', 'winst_per_aandeel', 'dividend',
                    'groei_percentage', 'risico', 'roi', 'valuatie_index'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()

                for stock in filtered_stocks:
                    writer.writerow(stock.to_dict())

            print(f"✓ Report exported to {filename} ({len(filtered_stocks)} stocks)", file=sys.stderr)
            return True
        
        except Exception as e:
            print(f"Error: Failed to export to CSV - {e}", file=sys.stderr)
            return False


def main():
    """Main entry point for the application."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Payton Stock Analysis Tool - Analyze stock performance metrics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze with default filters (min_index=10.0, max_risk=5.0)
  python stock_analyzer.py sample_stocks.csv

  # Custom filters and export results
  python stock_analyzer.py sample_stocks.csv -m 20.0 -r 3.5 -o results.csv

  # Interactive mode
  python stock_analyzer.py sample_stocks.csv -i
        """
    )
    parser.add_argument(
        'input_csv',
        help='Input CSV file with stock data (required columns: symbol, name, price, earnings)'
    )
    parser.add_argument(
        '-m', '--min-index',
        type=float,
        default=10.0,
        help='Minimum valuation index (default: 10.0)'
    )
    parser.add_argument(
        '-r', '--max-risk',
        type=float,
        default=5.0,
        help='Maximum risk score (default: 5.0)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output CSV file for filtered results (optional)'
    )
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Interactive mode for custom filtering'
    )
    parser.add_argument(
        '-s', '--stats',
        action='store_true',
        help='Show statistics for all loaded stocks'
    )
    
    args = parser.parse_args()
    
    # Create analyzer
    analyzer = StockAnalyzer(
        min_valuation_index=args.min_index,
        max_risk_score=args.max_risk
    )
    
    # Load data
    if not analyzer.load_from_csv(args.input_csv):
        sys.exit(1)
    
    # Show statistics if requested
    if args.stats:
        print_statistics(analyzer)

    # Prompt user for filter values (with defaults) and print concise table
    print("\nVoer filterwaarden in (druk Enter om default te gebruiken):")
    min_idx = get_float_input(f"Minimum waarderingsindex (default {args.min_index}): ", args.min_index)
    max_risk = get_float_input(f"Maximale risicoscore (default {args.max_risk}): ", args.max_risk)

    analyzer.print_filtered_table(min_idx, max_risk)

    # Export if requested
    if args.output:
        analyzer.export_to_csv(args.output, min_idx, max_risk)


def print_statistics(analyzer: StockAnalyzer) -> None:
    """Print statistics for loaded stocks."""
    stats = analyzer.get_statistics()
    
    if not stats:
        print("No statistics available")
        return
    
    print("\n" + "=" * 80)
    print("STOCK PORTFOLIO STATISTICS")
    print("=" * 80)
    print(f"Total stocks loaded:     {stats['total_stocks']}")
    print("")
    print("Return on Investment (ROI):")
    print(f"  Average ROI:           {stats['avg_roi']:.2f}%")
    print(f"  Maximum ROI:           {stats['max_roi']:.2f}%")
    print(f"  Minimum ROI:           {stats['min_roi']:.2f}%")
    print("")
    print("Valuation Index:")
    print(f"  Average Valuation:     {stats['avg_valuation']:.2f}")
    print(f"  Maximum Valuation:     {stats['max_valuation']:.2f}")
    print(f"  Minimum Valuation:     {stats['min_valuation']:.2f}")
    print("")
    print("Risk Score:")
    print(f"  Average Risk:          {stats['avg_risk']:.2f}")
    print(f"  Maximum Risk:          {stats['max_risk']:.2f}")
    print(f"  Minimum Risk:          {stats['min_risk']:.2f}")
    print("=" * 80 + "\n")


def interactive_mode(analyzer: StockAnalyzer) -> None:
    """Interactive mode for custom filtering and exploration."""
    print("\n" + "=" * 80)
    print("INTERACTIVE STOCK ANALYSIS MODE")
    print("=" * 80)
    print("Type 'help' for commands, 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("> ").strip().lower()
            
            if not user_input:
                continue
            
            if user_input == 'quit':
                print("Goodbye!")
                break
            
            elif user_input == 'help':
                print_help()
            
            elif user_input == 'stats':
                print_statistics(analyzer)
            
            elif user_input == 'list':
                analyzer.print_report()
            
            elif user_input == 'filter':
                min_idx = get_float_input("Enter minimum valuation index: ", 0.0)
                max_risk = get_float_input("Enter maximum risk score: ", 0.0)
                analyzer.print_report(min_idx, max_risk)
            
            elif user_input == 'export':
                filename = input("Enter output filename: ").strip()
                if filename:
                    analyzer.export_to_csv(filename)
            
            elif user_input == 'show_all':
                # Show all stocks without filtering
                print("\n" + "=" * 130)
                print("ALL LOADED STOCKS (No Filtering)")
                print("=" * 130)
                report = []
                report.append(f"{'Symbol':<8} {'Name':<30} {'Price':<10} {'EPS':<10} {'ROI %':<10} "
                             f"{'Growth %':<10} {'Risk':<8} {'Valuation':<12}")
                report.append("-" * 130)
                
                # Sort by valuation index
                sorted_stocks = sorted(analyzer.stocks, key=lambda s: s.valuation_index, reverse=True)
                for stock in sorted_stocks:
                    report.append(
                        f"{stock.symbol:<8} {stock.name:<30} {stock.price:<10.2f} "
                        f"{stock.eps:<10.2f} {stock.roi:<10.2f} "
                        f"{stock.growth_percentage:<10.2f} {stock.risk_score:<8.2f} "
                        f"{stock.valuation_index:<12.2f}"
                    )
                report.append("-" * 130)
                print("\n".join(report))
            
            else:
                print("Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def print_help() -> None:
    """Print help information."""
    print("""
Available Commands:
  list       - Show filtered stocks based on current criteria
  filter     - Apply custom filter (min valuation index and max risk)
  show_all   - Display all loaded stocks (sorted by valuation index)
  stats      - Display portfolio statistics
  export     - Export filtered results to CSV
  help       - Show this help message
  quit       - Exit the program
    """)


def get_float_input(prompt: str, default: float = 0.0) -> float:
    """Get float input from user with default fallback."""
    try:
        value = input(prompt).strip()
        if not value:
            return default
        return float(value)
    except ValueError:
        print(f"Invalid input. Using default: {default}")
        return default


if __name__ == '__main__':
    main()
