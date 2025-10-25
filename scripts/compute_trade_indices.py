#!/usr/bin/env python3
"""
Trade Data Analysis - Compute Indices & Key Ratios
==================================================
This script computes trade indicators, concentration indices, and risk metrics
for US-China-India bilateral trade analysis.

Input: master_data_us_china_india.csv
Output: trade_data_with_indices.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime

def load_data(filepath):
    """Load and validate trade data"""
    print("📊 Loading trade data...")
    df = pd.read_csv(filepath)
    print(f"   ✓ Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"   ✓ Products: {df['hs_code'].nunique()}")
    print(f"   ✓ Time periods: {df['date'].nunique()}")
    return df

def compute_market_shares(df):
    """Compute market share percentages"""
    print("\n📈 Computing market shares...")
    
    # China's share of US imports
    df['china_share_us'] = (df['us_import_china'] / df['us_import_world'] * 100).round(2)
    
    # India's share of US imports
    df['india_share_us'] = (df['us_import_india'] / df['us_import_world'] * 100).round(2)
    
    # US share of China's total exports
    df['us_share_china_exports'] = (df['us_import_china'] / df['china_export_world'] * 100).round(2)
    
    # US share of India's total exports
    df['us_share_india_exports'] = (df['us_import_india'] / df['india_export_world'] * 100).round(2)
    
    # Other countries' share (rest of world)
    df['other_share_us'] = (100 - df['china_share_us'] - df['india_share_us']).round(2)
    
    print(f"   ✓ Market shares calculated")
    return df

def compute_concentration_hhi(df):
    """Compute Hirschman-Herfindahl Index (HHI) for concentration"""
    print("\n📊 Computing HHI concentration indices...")
    
    # HHI based on supplier concentration to US market
    # HHI = sum of squared market shares (higher = more concentrated)
    df['hhi_us_imports'] = (
        (df['china_share_us'] / 100) ** 2 + 
        (df['india_share_us'] / 100) ** 2 + 
        (df['other_share_us'] / 100) ** 2
    ).round(4)
    
    # Concentration level classification
    def classify_concentration(hhi):
        if hhi > 0.25:
            return 'HIGH'
        elif hhi > 0.15:
            return 'MODERATE'
        else:
            return 'LOW'
    
    df['concentration_level'] = df['hhi_us_imports'].apply(classify_concentration)
    
    print(f"   ✓ HHI indices calculated")
    return df

def compute_trade_intensity(df):
    """Compute Trade Intensity Index"""
    print("\n🔄 Computing Trade Intensity Index...")
    
    # Trade Intensity = (bilateral trade / total trade) / (partner's world trade / world total trade)
    # Simplified version: US import share from partner relative to partner's global export capacity
    
    # For China-US trade intensity
    world_trade_proxy = df['us_import_world'].sum()  # Simplified proxy
    df['trade_intensity_china'] = (
        (df['us_import_china'] / df['us_import_world']) / 
        (df['china_export_world'] / world_trade_proxy)
    ).round(4)
    
    # For India-US trade intensity
    df['trade_intensity_india'] = (
        (df['us_import_india'] / df['us_import_world']) / 
        (df['india_export_world'] / world_trade_proxy)
    ).round(4)
    
    print(f"   ✓ Trade Intensity indices calculated")
    return df

def compute_growth_rates(df):
    """Compute quarter-over-quarter growth rates"""
    print("\n📈 Computing growth rates...")
    
    # Sort by product and date
    df = df.sort_values(['hs_code', 'date']).reset_index(drop=True)
    
    # Growth rates for each flow
    for col in ['us_import_china', 'us_import_india', 'us_import_world', 
                'china_export_world', 'india_export_world']:
        growth_col = f'{col}_growth'
        df[growth_col] = df.groupby('hs_code')[col].pct_change() * 100
        df[growth_col] = df[growth_col].round(2)
    
    print(f"   ✓ Growth rates calculated")
    return df

def compute_diversification_metrics(df):
    """Compute diversification and dependency metrics"""
    print("\n🌐 Computing diversification metrics...")
    
    # Diversification score (inverse of concentration)
    # Higher score = more diversified = less dependent on single source
    df['diversification_score'] = (1 - df['hhi_us_imports']).round(4)
    
    # China dependency risk score (0-100, higher = more dependent on China)
    df['china_dependency_risk'] = df['china_share_us'].round(2)
    
    # Import penetration ratio (how much of domestic market is imports)
    # This would require domestic production data, so we use a proxy:
    # US import intensity = total imports / (theoretical domestic demand proxy)
    
    # Trade balance implications
    df['china_india_ratio'] = (df['us_import_china'] / (df['us_import_india'] + 1)).round(2)  # +1 to avoid div by zero
    
    print(f"   ✓ Diversification metrics calculated")
    return df

def compute_revealed_comparative_advantage(df):
    """Compute Revealed Comparative Advantage (RCA) indices"""
    print("\n💪 Computing RCA (Revealed Comparative Advantage)...")
    
    # RCA = (Product's share in country's exports) / (Product's share in world exports)
    # RCA > 1 indicates comparative advantage
    
    # For each time period, we need world totals
    # Simplified: Using US import world as proxy for world demand
    
    # China RCA for each product
    china_total_exports = df.groupby('date')['china_export_world'].sum()
    world_total_proxy = df.groupby('date')['us_import_world'].sum()
    
    df['china_rca'] = df.apply(
        lambda row: (
            (row['china_export_world'] / china_total_exports[row['date']]) /
            (row['us_import_world'] / world_total_proxy[row['date']])
        ) if china_total_exports[row['date']] > 0 and world_total_proxy[row['date']] > 0 else 0,
        axis=1
    ).round(4)
    
    # India RCA for each product
    india_total_exports = df.groupby('date')['india_export_world'].sum()
    
    df['india_rca'] = df.apply(
        lambda row: (
            (row['india_export_world'] / india_total_exports[row['date']]) /
            (row['us_import_world'] / world_total_proxy[row['date']])
        ) if india_total_exports[row['date']] > 0 and world_total_proxy[row['date']] > 0 else 0,
        axis=1
    ).round(4)
    
    # RCA comparison: which country has stronger comparative advantage
    df['rca_advantage'] = df.apply(
        lambda row: 'CHINA' if row['china_rca'] > row['india_rca'] 
        else 'INDIA' if row['india_rca'] > row['china_rca'] 
        else 'NEUTRAL',
        axis=1
    )
    
    print(f"   ✓ RCA indices calculated")
    return df

def compute_risk_scores(df):
    """Compute composite risk scores"""
    print("\n⚠️  Computing risk scores...")
    
    # Geopolitical risk score (0-100)
    # Based on: concentration + China dependency + trade intensity
    df['geopolitical_risk_score'] = (
        (df['china_share_us'] * 0.5) +  # 50% weight on China share
        (df['hhi_us_imports'] * 100 * 0.3) +  # 30% weight on concentration
        (df['trade_intensity_china'].clip(upper=5) * 4)  # 20% weight on trade intensity (scaled)
    ).round(2)
    
    # Normalize to 0-100
    df['geopolitical_risk_score'] = df['geopolitical_risk_score'].clip(upper=100)
    
    # Risk level classification
    def classify_risk(score):
        if score >= 70:
            return 'HIGH'
        elif score >= 40:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    df['risk_level'] = df['geopolitical_risk_score'].apply(classify_risk)
    
    # Diversification opportunity score (0-100, higher = better opportunity for India)
    df['india_opportunity_score'] = (
        (100 - df['india_share_us']) * 0.4 +  # Room to grow
        (df['india_rca'].clip(upper=5) * 10) +  # India's comparative advantage
        (df['china_share_us'] * 0.4)  # Current China dominance creates opportunity
    ).round(2)
    
    df['india_opportunity_score'] = df['india_opportunity_score'].clip(upper=100)
    
    print(f"   ✓ Risk scores calculated")
    return df

def compute_trend_indicators(df):
    """Compute trend indicators (moving averages, momentum)"""
    print("\n📉 Computing trend indicators...")
    
    # Sort by product and date
    df = df.sort_values(['hs_code', 'date']).reset_index(drop=True)
    
    # 4-quarter moving average for China share
    df['china_share_ma4'] = df.groupby('hs_code')['china_share_us'].transform(
        lambda x: x.rolling(window=4, min_periods=1).mean()
    ).round(2)
    
    # 4-quarter moving average for India share
    df['india_share_ma4'] = df.groupby('hs_code')['india_share_us'].transform(
        lambda x: x.rolling(window=4, min_periods=1).mean()
    ).round(2)
    
    # Trend direction (comparing current to MA)
    df['china_trend'] = df.apply(
        lambda row: 'INCREASING' if row['china_share_us'] > row['china_share_ma4']
        else 'DECREASING' if row['china_share_us'] < row['china_share_ma4']
        else 'STABLE',
        axis=1
    )
    
    df['india_trend'] = df.apply(
        lambda row: 'INCREASING' if row['india_share_us'] > row['india_share_ma4']
        else 'DECREASING' if row['india_share_us'] < row['india_share_ma4']
        else 'STABLE',
        axis=1
    )
    
    # Momentum (rate of change in market share)
    df['china_momentum'] = df.groupby('hs_code')['china_share_us'].diff().round(2)
    df['india_momentum'] = df.groupby('hs_code')['india_share_us'].diff().round(2)
    
    print(f"   ✓ Trend indicators calculated")
    return df

def add_metadata(df):
    """Add metadata and timestamps"""
    print("\n🏷️  Adding metadata...")
    
    # Quarter number (for easier sorting/analysis)
    def extract_quarter(date_str):
        year, quarter = date_str.split('-')
        return int(year) * 10 + int(quarter[1])
    
    df['quarter_num'] = df['date'].apply(extract_quarter)
    
    # Time period (for grouping)
    df['year'] = df['date'].str.split('-').str[0]
    
    # Analysis timestamp
    df['analysis_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"   ✓ Metadata added")
    return df

def generate_summary_stats(df):
    """Generate and print summary statistics"""
    print("\n" + "="*80)
    print("📊 SUMMARY STATISTICS")
    print("="*80)
    
    # Overall stats
    print(f"\n🌍 Overall Trade Volume (Average per Quarter):")
    print(f"   US Imports from China: ${df['us_import_china'].mean():,.0f}K")
    print(f"   US Imports from India:  ${df['us_import_india'].mean():,.0f}K")
    print(f"   US Imports from World:  ${df['us_import_world'].mean():,.0f}K")
    
    # Market share averages
    print(f"\n📊 Average Market Shares:")
    print(f"   China's share of US imports: {df['china_share_us'].mean():.2f}%")
    print(f"   India's share of US imports:  {df['india_share_us'].mean():.2f}%")
    
    # Concentration
    print(f"\n📈 Concentration Metrics:")
    print(f"   Average HHI: {df['hhi_us_imports'].mean():.4f}")
    print(f"   High concentration periods: {(df['concentration_level'] == 'HIGH').sum()} quarters")
    
    # Risk distribution
    print(f"\n⚠️  Risk Distribution:")
    risk_counts = df['risk_level'].value_counts()
    for level in ['HIGH', 'MEDIUM', 'LOW']:
        count = risk_counts.get(level, 0)
        pct = count / len(df) * 100
        print(f"   {level}: {count} observations ({pct:.1f}%)")
    
    # RCA comparison
    print(f"\n💪 Comparative Advantage (RCA > 1):")
    print(f"   China has advantage: {(df['china_rca'] > 1).sum()} observations")
    print(f"   India has advantage:  {(df['india_rca'] > 1).sum()} observations")
    
    # Product-level summary
    print(f"\n📦 Product-Level Insights:")
    product_summary = df.groupby('hs_code').agg({
        'china_share_us': 'mean',
        'india_share_us': 'mean',
        'geopolitical_risk_score': 'mean'
    }).round(2)
    
    print("\n   Product    China Share    India Share    Avg Risk Score")
    print("   " + "-"*60)
    for idx, row in product_summary.iterrows():
        print(f"   {idx:<10} {row['china_share_us']:>10.2f}%    {row['india_share_us']:>10.2f}%    {row['geopolitical_risk_score']:>10.2f}")
    
    print("\n" + "="*80)

def save_results(df, output_path):
    """Save processed data to CSV"""
    print(f"\n💾 Saving results to {output_path}...")
    
    # Reorder columns for better readability
    base_cols = ['date', 'quarter_num', 'year', 'hs_code', 'product_name']
    
    trade_cols = ['us_import_china', 'us_import_india', 'us_import_world', 
                  'china_export_world', 'india_export_world']
    
    share_cols = ['china_share_us', 'india_share_us', 'other_share_us',
                  'us_share_china_exports', 'us_share_india_exports']
    
    concentration_cols = ['hhi_us_imports', 'concentration_level', 'diversification_score']
    
    growth_cols = [col for col in df.columns if '_growth' in col]
    
    trend_cols = ['china_share_ma4', 'india_share_ma4', 'china_trend', 'india_trend',
                  'china_momentum', 'india_momentum']
    
    index_cols = ['trade_intensity_china', 'trade_intensity_india', 
                  'china_rca', 'india_rca', 'rca_advantage']
    
    risk_cols = ['china_dependency_risk', 'geopolitical_risk_score', 'risk_level',
                 'india_opportunity_score', 'china_india_ratio']
    
    meta_cols = ['analysis_timestamp']
    
    # Combine in logical order
    ordered_cols = (base_cols + trade_cols + share_cols + concentration_cols + 
                   growth_cols + trend_cols + index_cols + risk_cols + meta_cols)
    
    # Only include columns that exist
    final_cols = [col for col in ordered_cols if col in df.columns]
    
    df_output = df[final_cols]
    df_output.to_csv(output_path, index=False)
    
    print(f"   ✓ Saved {len(df_output)} rows with {len(df_output.columns)} columns")
    print(f"   ✓ File size: ~{len(df_output) * len(df_output.columns) * 10 / 1024:.1f} KB")

def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("🚀 TRADE DATA ANALYSIS - COMPUTING INDICES & KEY RATIOS")
    print("="*80)
    
    # File paths
    input_file = '/mnt/user-data/uploads/master_data_us_china_india.csv'
    output_file = '/mnt/user-data/outputs/trade_data_with_indices.csv'
    
    # Load data
    df = load_data(input_file)
    
    # Compute all metrics
    df = compute_market_shares(df)
    df = compute_concentration_hhi(df)
    df = compute_trade_intensity(df)
    df = compute_growth_rates(df)
    df = compute_diversification_metrics(df)
    df = compute_revealed_comparative_advantage(df)
    df = compute_risk_scores(df)
    df = compute_trend_indicators(df)
    df = add_metadata(df)
    
    # Generate summary
    generate_summary_stats(df)
    
    # Save results
    save_results(df, output_file)
    
    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE!")
    print("="*80)
    print(f"\n📂 Output file: {output_file}")
    print("\n📋 Computed Metrics:")
    print("   ✓ Market shares (China, India, Others)")
    print("   ✓ HHI concentration indices")
    print("   ✓ Trade intensity indices")
    print("   ✓ Growth rates (quarter-over-quarter)")
    print("   ✓ Diversification scores")
    print("   ✓ RCA (Revealed Comparative Advantage)")
    print("   ✓ Risk scores (Geopolitical, Dependency)")
    print("   ✓ Trend indicators (Moving averages, Momentum)")
    print("   ✓ India opportunity scores")
    print("\n🎯 Ready for Gen AI analysis and visualization!")
    print("\n")

if __name__ == "__main__":
    main()
