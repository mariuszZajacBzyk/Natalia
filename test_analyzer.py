#!/usr/bin/env python3
"""
Test script for the Stock Analyzer application.
Demonstrates various filtering, analysis, and export scenarios.
"""

import os
from stock_analyzer import StockAnalyzer


def main():
    print("\n" + "=" * 100)
    print("PAYTON STOCK ANALYZER - COMPREHENSIVE TEST SUITE")
    print("=" * 100)
    
    csv_file = 'sample_stocks.csv'
    
    # Check if CSV file exists
    if not os.path.isfile(csv_file):
        print(f"Error: {csv_file} not found!")
        return
    
    print(f"\n📊 Loading data from: {csv_file}\n")
    
    # ========== TEST 1: Default Filters ==========
    print("\n" + "=" * 100)
    print("TEST 1: Default filters (Min Index: 10.0, Max Risk: 5.0)")
    print("=" * 100 + "\n")
    analyzer1 = StockAnalyzer(min_valuation_index=10.0, max_risk_score=5.0)
    if analyzer1.load_from_csv(csv_file):
        analyzer1.print_report()
    
    # ========== TEST 2: Stricter Filters ==========
    print("\n" + "=" * 100)
    print("TEST 2: Stricter filters (Min Index: 20.0, Max Risk: 3.0)")
    print("=" * 100 + "\n")
    analyzer2 = StockAnalyzer(min_valuation_index=20.0, max_risk_score=3.0)
    if analyzer2.load_from_csv(csv_file):
        analyzer2.print_report()
    
    # ========== TEST 3: Permissive Filters ==========
    print("\n" + "=" * 100)
    print("TEST 3: Permissive filters (Min Index: 5.0, Max Risk: 5.5)")
    print("=" * 100 + "\n")
    analyzer3 = StockAnalyzer(min_valuation_index=5.0, max_risk_score=5.5)
    if analyzer3.load_from_csv(csv_file):
        analyzer3.print_report()
    
    # ========== TEST 4: High-Growth Stocks ==========
    print("\n" + "=" * 100)
    print("TEST 4: High-growth stocks (Min Index: 15.0, Max Risk: 4.0)")
    print("=" * 100 + "\n")
    analyzer4 = StockAnalyzer(min_valuation_index=15.0, max_risk_score=4.0)
    if analyzer4.load_from_csv(csv_file):
        analyzer4.print_report()
        print("\n📈 Exporting results to: filtered_results.csv")
        analyzer4.export_to_csv('filtered_results.csv')
    
    # ========== TEST 5: Statistics ==========
    print("\n" + "=" * 100)
    print("TEST 5: Portfolio Statistics")
    print("=" * 100 + "\n")
    analyzer5 = StockAnalyzer()
    if analyzer5.load_from_csv(csv_file):
        stats = analyzer5.get_statistics()
        if stats:
            print(f"Total Stocks:           {stats['total_stocks']}")
            print(f"Average ROI:            {stats['avg_roi']:.2f}%")
            print(f"Average Valuation:      {stats['avg_valuation']:.2f}")
            print(f"Average Risk:           {stats['avg_risk']:.2f}")
            print(f"Max Valuation:          {stats['max_valuation']:.2f}")
            print(f"Min Valuation:          {stats['min_valuation']:.2f}")
    
    # ========== TEST 6: Custom Filters in Report ==========
    print("\n" + "=" * 100)
    print("TEST 6: Dynamic filtering with custom parameters")
    print("=" * 100 + "\n")
    analyzer6 = StockAnalyzer(min_valuation_index=10.0, max_risk_score=5.0)
    if analyzer6.load_from_csv(csv_file):
        # Use different filters than defaults
        analyzer6.print_report(min_valuation_index=25.0, max_risk_score=3.5)
    
    print("\n" + "=" * 100)
    print("✓ TEST SUITE COMPLETED")
    print("=" * 100 + "\n")


if __name__ == '__main__':
    main()
