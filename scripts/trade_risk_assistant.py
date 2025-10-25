"""
🌐 Trade Risk AI Assistant
Agentic AI system for proactive global trade risk management

Author: Ganesh S K
Date: October 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json
from typing import Dict, List, Optional
import os

# Configure page
st.set_page_config(
    page_title="Trade Risk AI Assistant",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
    """Load trade and NTM data"""
    try:
        df = pd.read_csv('D:/Thesis/trade_ntm_combined.csv')
        df['hs_code'] = df['hs_code'].astype(str).str.strip()
        return df
    except FileNotFoundError:
        st.error("❌ Data file not found. Please ensure 'trade_ntm_combined.csv' is in the same directory.")
        return None

# ============================================================================
# AGENT 1: DATA RETRIEVAL AGENT
# ============================================================================

class DataRetrievalAgent:
    """Agent responsible for fetching and contextualizing trade data"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.name = "📊 Data Retrieval Agent"
    
    def get_product_data(self, hs_code: str, quarter: Optional[str] = None) -> Dict:
        """Retrieve data for specific product and quarter"""
        
        # Filter by HS code
        product_data = self.df[self.df['hs_code'] == str(hs_code)].copy()
        
        if product_data.empty:
            return {"error": f"No data found for HS code {hs_code}"}
        
        # Get latest quarter if not specified
        if quarter is None:
            quarter = product_data['date'].max()
        
        # Get specific quarter data
        latest = product_data[product_data['date'] == quarter].iloc[0].to_dict()
        
        # Calculate historical trends (last 4 quarters)
        recent = product_data.tail(4)
        
        context = {
            "hs_code": hs_code,
            "product_name": latest['product_name'],
            "quarter": quarter,
            "current_metrics": {
                "china_share": round(latest['china_share_us'], 2),
                "india_share": round(latest['india_share_us'], 2),
                "other_share": round(latest['other_share_us'], 2),
                "china_dependency_risk": round(latest['china_dependency_risk'], 2),
                "geopolitical_risk_score": round(latest['geopolitical_risk_score'], 2),
                "risk_level": latest['risk_level'],
                "hhi": round(latest['hhi_us_imports'], 4),
                "concentration_level": latest['concentration_level'],
                "diversification_score": round(latest['diversification_score'], 4)
            },
            "trade_indicators": {
                "china_rca": round(latest['china_rca'], 2),
                "india_rca": round(latest['india_rca'], 2),
                "rca_advantage": latest['rca_advantage'],
                "trade_intensity_china": round(latest['trade_intensity_china'], 2),
                "trade_intensity_india": round(latest['trade_intensity_india'], 2),
                "india_opportunity_score": round(latest['india_opportunity_score'], 2)
            },
            "trends": {
                "china_trend": latest['china_trend'],
                "india_trend": latest['india_trend'],
                "china_momentum": round(latest['china_momentum'], 2) if pd.notna(latest['china_momentum']) else 0,
                "india_momentum": round(latest['india_momentum'], 2) if pd.notna(latest['india_momentum']) else 0,
                "china_share_ma4": round(latest['china_share_ma4'], 2),
                "india_share_ma4": round(latest['india_share_ma4'], 2)
            },
            "ntm_data": {
                "ntm_count": int(latest['ntm_count']),
                "ntm_severity": latest['ntm_severity'],
                "has_sps": bool(latest['has_sps']),
                "has_tbt": bool(latest['has_tbt']),
                "has_export_restriction": bool(latest['has_export_restriction']),
                "technical_measures": int(latest['technical_measure_count']),
                "non_technical_measures": int(latest['non_technical_count']),
                "ntm_codes": latest['ntm_codes'] if latest['ntm_codes'] else "None"
            },
            "trade_values": {
                "us_import_china": int(latest['us_import_china']),
                "us_import_india": int(latest['us_import_india']),
                "us_import_world": int(latest['us_import_world'])
            },
            "historical_trend": {
                "quarters": recent['date'].tolist(),
                "china_shares": recent['china_share_us'].round(2).tolist(),
                "india_shares": recent['india_share_us'].round(2).tolist(),
                "risk_scores": recent['geopolitical_risk_score'].round(2).tolist()
            }
        }
        
        return context
    
    def get_all_products_summary(self) -> pd.DataFrame:
        """Get summary of all products (latest quarter)"""
        latest_data = self.df.sort_values('date').groupby('hs_code').last().reset_index()
        
        summary = latest_data[[
            'hs_code', 'product_name', 'date',
            'china_share_us', 'india_share_us', 
            'geopolitical_risk_score', 'risk_level',
            'ntm_count', 'ntm_severity',
            'india_opportunity_score'
        ]].copy()
        
        summary.columns = ['HS Code', 'Product', 'Quarter', 
                          'China %', 'India %', 'Risk Score', 'Risk Level',
                          'NTMs', 'NTM Severity', 'India Opportunity']
        
        return summary.sort_values('Risk Score', ascending=False)

# ============================================================================
# AGENT 2: RISK ASSESSMENT AGENT
# ============================================================================

class RiskAssessmentAgent:
    """Agent responsible for analyzing and assessing trade risks"""
    
    def __init__(self):
        self.name = "⚠️ Risk Assessment Agent"
    
    def assess_risk(self, data_context: Dict) -> Dict:
        """Perform comprehensive risk assessment"""
        
        current = data_context['current_metrics']
        ntm = data_context['ntm_data']
        trends = data_context['trends']
        
        # Calculate risk components
        concentration_risk = self._assess_concentration(current)
        dependency_risk = self._assess_dependency(current)
        ntm_risk = self._assess_ntm_impact(ntm)
        trend_risk = self._assess_trends(trends)
        
        # Overall risk calculation
        overall_risk_score = (
            concentration_risk['score'] * 0.3 +
            dependency_risk['score'] * 0.3 +
            ntm_risk['score'] * 0.25 +
            trend_risk['score'] * 0.15
        )
        
        # Determine risk level
        if overall_risk_score >= 70:
            risk_level = "HIGH"
            urgency = "URGENT"
        elif overall_risk_score >= 40:
            risk_level = "MEDIUM"
            urgency = "MONITOR"
        else:
            risk_level = "LOW"
            urgency = "STABLE"
        
        # Generate narrative
        vulnerabilities = self._identify_vulnerabilities(
            concentration_risk, dependency_risk, ntm_risk, trend_risk
        )
        
        key_drivers = self._identify_key_drivers(
            current, ntm, trends
        )
        
        assessment = {
            "overall_risk_level": risk_level,
            "overall_risk_score": round(overall_risk_score, 1),
            "urgency": urgency,
            "risk_components": {
                "concentration": concentration_risk,
                "dependency": dependency_risk,
                "ntm_impact": ntm_risk,
                "trend": trend_risk
            },
            "vulnerabilities": vulnerabilities,
            "key_drivers": key_drivers,
            "disruption_likelihood": self._calculate_disruption_likelihood(overall_risk_score),
            "disruption_impact": self._calculate_disruption_impact(current, ntm),
            "narrative": self._generate_narrative(
                risk_level, overall_risk_score, vulnerabilities, key_drivers
            )
        }
        
        return assessment
    
    def _assess_concentration(self, current: Dict) -> Dict:
        """Assess market concentration risk"""
        hhi = current['hhi']
        
        if hhi > 0.25:
            score = 90
            level = "HIGH"
            desc = "Highly concentrated market - limited alternatives available"
        elif hhi > 0.15:
            score = 60
            level = "MEDIUM"
            desc = "Moderately concentrated - diversification needed"
        else:
            score = 30
            level = "LOW"
            desc = "Well-diversified market structure"
        
        return {
            "score": score,
            "level": level,
            "description": desc,
            "hhi_value": hhi
        }
    
    def _assess_dependency(self, current: Dict) -> Dict:
        """Assess China dependency risk"""
        china_share = current['china_share']
        
        if china_share > 70:
            score = 95
            level = "CRITICAL"
            desc = f"Critical dependency on China ({china_share}%)"
        elif china_share > 50:
            score = 80
            level = "HIGH"
            desc = f"High dependency on China ({china_share}%)"
        elif china_share > 30:
            score = 50
            level = "MEDIUM"
            desc = f"Moderate China exposure ({china_share}%)"
        else:
            score = 20
            level = "LOW"
            desc = f"Low China dependency ({china_share}%)"
        
        return {
            "score": score,
            "level": level,
            "description": desc,
            "china_share": china_share
        }
    
    def _assess_ntm_impact(self, ntm: Dict) -> Dict:
        """Assess NTM-related risks"""
        count = ntm['ntm_count']
        severity = ntm['ntm_severity']
        
        if severity == "HIGH" or count >= 30:
            score = 80
            level = "HIGH"
            desc = f"{count} NTMs with {severity} severity - significant compliance burden"
        elif severity == "MEDIUM" or count >= 15:
            score = 55
            level = "MEDIUM"
            desc = f"{count} NTMs with {severity} severity - moderate barriers"
        elif count > 0:
            score = 30
            level = "LOW"
            desc = f"{count} NTMs - manageable compliance requirements"
        else:
            score = 10
            level = "MINIMAL"
            desc = "No significant NTM barriers"
        
        return {
            "score": score,
            "level": level,
            "description": desc,
            "ntm_count": count,
            "has_sps": ntm['has_sps'],
            "has_tbt": ntm['has_tbt']
        }
    
    def _assess_trends(self, trends: Dict) -> Dict:
        """Assess trend-based risks"""
        china_trend = trends['china_trend']
        momentum = trends['china_momentum']
        
        if china_trend == "INCREASING" and momentum > 3:
            score = 70
            level = "WORSENING"
            desc = f"China share increasing rapidly (+{momentum}%)"
        elif china_trend == "INCREASING":
            score = 50
            level = "CONCERN"
            desc = "China share trending upward"
        elif china_trend == "DECREASING" and momentum < -3:
            score = 20
            level = "IMPROVING"
            desc = f"China share declining ({momentum}%)"
        else:
            score = 35
            level = "STABLE"
            desc = "Trade patterns relatively stable"
        
        return {
            "score": score,
            "level": level,
            "description": desc,
            "trend": china_trend,
            "momentum": momentum
        }
    
    def _identify_vulnerabilities(self, conc, dep, ntm, trend) -> List[str]:
        """Identify key vulnerabilities"""
        vulns = []
        
        if dep['level'] in ["CRITICAL", "HIGH"]:
            vulns.append(f"🔴 {dep['description']}")
        
        if conc['level'] == "HIGH":
            vulns.append(f"🔴 {conc['description']}")
        
        if ntm['level'] in ["HIGH", "MEDIUM"]:
            vulns.append(f"🟡 {ntm['description']}")
        
        if trend['level'] in ["WORSENING", "CONCERN"]:
            vulns.append(f"⚠️ {trend['description']}")
        
        return vulns if vulns else ["✅ No critical vulnerabilities identified"]
    
    def _identify_key_drivers(self, current, ntm, trends) -> List[str]:
        """Identify key risk drivers"""
        drivers = []
        
        if current['china_share'] > 50:
            drivers.append("Concentration on single supplier (China)")
        
        if ntm['ntm_count'] > 20:
            drivers.append(f"High regulatory burden ({ntm['ntm_count']} NTMs)")
        
        if ntm['has_tbt'] and ntm['has_sps']:
            drivers.append("Multiple technical barriers (SPS + TBT)")
        
        if trends['china_trend'] == "INCREASING":
            drivers.append("Increasing China market share trend")
        
        if current['hhi'] > 0.25:
            drivers.append("Limited supplier diversification")
        
        return drivers if drivers else ["Diversified, stable market conditions"]
    
    def _calculate_disruption_likelihood(self, risk_score: float) -> Dict:
        """Calculate likelihood of trade disruption"""
        if risk_score >= 70:
            return {"score": 8, "label": "High (7-8/10)"}
        elif risk_score >= 50:
            return {"score": 6, "label": "Medium (5-6/10)"}
        else:
            return {"score": 3, "label": "Low (2-4/10)"}
    
    def _calculate_disruption_impact(self, current, ntm) -> Dict:
        """Calculate impact if disruption occurs"""
        china_share = current['china_share']
        
        if china_share > 70:
            return {"score": 9, "label": "Critical (8-9/10)"}
        elif china_share > 50:
            return {"score": 7, "label": "High (6-7/10)"}
        elif china_share > 30:
            return {"score": 5, "label": "Medium (4-5/10)"}
        else:
            return {"score": 3, "label": "Low (2-3/10)"}
    
    def _generate_narrative(self, level, score, vulns, drivers) -> str:
        """Generate human-readable risk narrative"""
        narrative = f"""
**Risk Assessment Summary**

Overall Risk: **{level}** (Score: {score}/100)

**Primary Vulnerabilities:**
{chr(10).join(f"- {v}" for v in vulns)}

**Key Risk Drivers:**
{chr(10).join(f"- {d}" for d in drivers)}
        """
        return narrative.strip()

# ============================================================================
# AGENT 3: STRATEGIC DIVERSIFICATION AGENT
# ============================================================================

class StrategicDiversificationAgent:
    """Agent responsible for recommending diversification strategies"""
    
    def __init__(self):
        self.name = "🌐 Strategic Diversification Agent"
    
    def generate_recommendations(self, data_context: Dict, risk_assessment: Dict) -> Dict:
        """Generate strategic diversification recommendations"""
        
        current = data_context['current_metrics']
        indicators = data_context['trade_indicators']
        risk_level = risk_assessment['overall_risk_level']
        
        # Analyze India opportunity
        india_analysis = self._analyze_india_opportunity(current, indicators)
        
        # Analyze other opportunities
        other_opportunities = self._identify_other_opportunities(current, indicators)
        
        # Generate prioritized strategies
        strategies = self._prioritize_strategies(
            india_analysis, other_opportunities, risk_level, current
        )
        
        # Calculate expected outcomes
        outcomes = self._calculate_expected_outcomes(strategies, current)
        
        # Implementation roadmap
        roadmap = self._create_implementation_roadmap(strategies, risk_level)
        
        recommendations = {
            "primary_recommendation": strategies[0] if strategies else None,
            "all_strategies": strategies,
            "india_opportunity": india_analysis,
            "other_opportunities": other_opportunities,
            "expected_outcomes": outcomes,
            "implementation_roadmap": roadmap,
            "timeline": self._estimate_timeline(risk_level),
            "summary": self._generate_summary(strategies, outcomes, risk_level)
        }
        
        return recommendations
    
    def _analyze_india_opportunity(self, current: Dict, indicators: Dict) -> Dict:
        """Analyze India as diversification target"""
        
        india_share = current['india_share']
        india_rca = indicators['india_rca']
        opportunity_score = indicators['india_opportunity_score']
        
        # Determine feasibility
        if india_rca > 1.5 and opportunity_score > 60:
            feasibility = "HIGH"
            priority = 1
            rationale = f"India has strong comparative advantage (RCA: {india_rca}) and high opportunity score ({opportunity_score})"
        elif india_rca > 1 and opportunity_score > 40:
            feasibility = "MEDIUM"
            priority = 2
            rationale = f"India has moderate advantage (RCA: {india_rca}) with decent opportunity ({opportunity_score})"
        else:
            feasibility = "LOW"
            priority = 3
            rationale = f"Limited India advantage (RCA: {india_rca}), opportunity score: {opportunity_score}"
        
        # Calculate target share
        current_india = india_share
        china_share = current['china_share']
        
        if feasibility == "HIGH":
            target_india_share = min(current_india + 15, 40)
        elif feasibility == "MEDIUM":
            target_india_share = min(current_india + 10, 30)
        else:
            target_india_share = min(current_india + 5, 20)
        
        return {
            "feasibility": feasibility,
            "priority": priority,
            "current_share": round(current_india, 1),
            "target_share": round(target_india_share, 1),
            "increase": round(target_india_share - current_india, 1),
            "india_rca": round(india_rca, 2),
            "opportunity_score": round(opportunity_score, 1),
            "rationale": rationale,
            "barriers": self._identify_india_barriers(indicators, current),
            "advantages": self._identify_india_advantages(india_rca, opportunity_score)
        }
    
    def _identify_india_barriers(self, indicators, current) -> List[str]:
        """Identify barriers to India diversification"""
        barriers = []
        
        if indicators['india_rca'] < 1:
            barriers.append("Lower comparative advantage vs global competitors")
        
        if current['india_share'] < 5:
            barriers.append("Currently low market presence - needs supplier development")
        
        # Could add NTM barriers if we had India-specific NTMs
        barriers.append("Compliance with US import regulations")
        
        return barriers if barriers else ["Minimal barriers identified"]
    
    def _identify_india_advantages(self, rca, opp_score) -> List[str]:
        """Identify India's advantages"""
        advantages = []
        
        if rca > 1.5:
            advantages.append(f"Strong competitive advantage (RCA: {rca})")
        elif rca > 1:
            advantages.append(f"Competitive advantage present (RCA: {rca})")
        
        if opp_score > 60:
            advantages.append("High diversification opportunity score")
        
        advantages.append("Democratic partner with stable trade relations")
        advantages.append("Growing manufacturing capabilities")
        
        return advantages
    
    def _identify_other_opportunities(self, current, indicators) -> List[Dict]:
        """Identify other diversification opportunities"""
        opportunities = []
        
        other_share = current['other_share']
        china_share = current['china_share']
        
        # ASEAN countries (proxy using "other" suppliers)
        if other_share > 20:
            opportunities.append({
                "region": "ASEAN (Vietnam, Thailand, Malaysia)",
                "potential": "MEDIUM-HIGH",
                "current_share": round(other_share, 1),
                "rationale": "Growing manufacturing hubs with established supply chains",
                "timeline": "12-18 months"
            })
        
        # Mexico/Latin America
        if china_share > 40:
            opportunities.append({
                "region": "Mexico (Nearshoring)",
                "potential": "MEDIUM",
                "current_share": "Included in other",
                "rationale": "USMCA benefits, reduced logistics costs, geographic proximity",
                "timeline": "18-24 months"
            })
        
        # Europe (for certain products)
        opportunities.append({
            "region": "European Union",
            "potential": "LOW-MEDIUM",
            "current_share": "Included in other",
            "rationale": "High quality standards, technological expertise",
            "timeline": "24+ months"
        })
        
        return opportunities
    
    def _prioritize_strategies(self, india, other_opps, risk_level, current) -> List[Dict]:
        """Prioritize diversification strategies"""
        strategies = []
        
        china_share = current['china_share']
        
        # Strategy 1: India diversification
        if india['feasibility'] in ["HIGH", "MEDIUM"]:
            strategies.append({
                "priority": 1,
                "name": "India Sourcing Expansion",
                "target": f"Increase India share from {india['current_share']}% to {india['target_share']}%",
                "action": f"Shift {india['increase']}% of sourcing to Indian suppliers",
                "timeline": "6-12 months" if india['feasibility'] == "HIGH" else "12-18 months",
                "feasibility": india['feasibility'],
                "expected_impact": f"Reduce China dependency to {round(china_share - india['increase'], 1)}%",
                "implementation_steps": [
                    "Identify and qualify Indian suppliers",
                    "Pilot orders (5% volume)",
                    "Quality validation and certification",
                    "Gradual scale-up to target volume"
                ]
            })
        
        # Strategy 2: Multi-country diversification
        if risk_level == "HIGH" and china_share > 60:
            strategies.append({
                "priority": 2,
                "name": "Multi-Country Diversification",
                "target": f"Distribute imports across 3-4 countries",
                "action": "Reduce single-country exposure below 50%",
                "timeline": "12-24 months",
                "feasibility": "MEDIUM",
                "expected_impact": "Lower HHI below 0.25 (competitive market)",
                "implementation_steps": [
                    "Develop ASEAN supplier network",
                    "Explore nearshoring to Mexico",
                    "Establish dual-sourcing arrangements",
                    "Implement risk-hedging contracts"
                ]
            })
        
        # Strategy 3: Domestic/nearshoring
        if risk_level == "HIGH":
            strategies.append({
                "priority": 3,
                "name": "Nearshoring Initiative",
                "target": "Establish North American supply base",
                "action": "Develop Mexico/US manufacturing capacity",
                "timeline": "18-36 months",
                "feasibility": "MEDIUM-LOW",
                "expected_impact": "Long-term supply chain resilience",
                "implementation_steps": [
                    "Partner with USMCA manufacturers",
                    "Invest in regional capacity building",
                    "Leverage government incentives",
                    "Gradual transition (5-10% initially)"
                ]
            })
        
        return strategies
    
    def _calculate_expected_outcomes(self, strategies, current) -> Dict:
        """Calculate expected outcomes of diversification"""
        
        if not strategies:
            return {}
        
        primary = strategies[0]
        china_share = current['china_share']
        hhi_current = current['hhi']
        
        # Parse target reduction from primary strategy
        if 'India' in primary['name']:
            # Assuming India expansion
            reduction = float(primary['target'].split()[-1].strip('%').split('to')[-1])
            new_china_share = china_share - reduction
        else:
            new_china_share = china_share * 0.85  # Assume 15% reduction
        
        # Estimate new HHI (simplified)
        new_hhi = hhi_current * 0.8  # Assume 20% reduction in concentration
        
        outcomes = {
            "risk_reduction": {
                "from": current['risk_level'],
                "to": "MEDIUM" if current['risk_level'] == "HIGH" else "LOW",
                "timeline": primary['timeline']
            },
            "china_dependency": {
                "current": round(china_share, 1),
                "target": round(new_china_share, 1),
                "reduction": round(china_share - new_china_share, 1)
            },
            "market_concentration": {
                "current_hhi": round(hhi_current, 3),
                "target_hhi": round(new_hhi, 3),
                "improvement": round((hhi_current - new_hhi) / hhi_current * 100, 1)
            },
            "cost_impact": {
                "initial": "+5-8% (transition costs)",
                "long_term": "Neutral (competitive pricing)",
                "roi_period": "12-18 months"
            }
        }
        
        return outcomes
    
    def _create_implementation_roadmap(self, strategies, risk_level) -> List[Dict]:
        """Create phased implementation roadmap"""
        
        if risk_level == "HIGH":
            urgency = "IMMEDIATE"
        elif risk_level == "MEDIUM":
            urgency = "30 DAYS"
        else:
            urgency = "90 DAYS"
        
        roadmap = [
            {
                "phase": "Immediate (0-30 days)",
                "actions": [
                    "🔍 Conduct supplier audit in target countries",
                    "📊 Establish baseline metrics and KPIs",
                    "🤝 Engage with trade associations",
                    "📋 Review and update procurement policies"
                ]
            },
            {
                "phase": "Short-term (30-90 days)",
                "actions": [
                    "🏭 Identify and qualify 3-5 alternative suppliers",
                    "📦 Initiate pilot orders (5-10% volume)",
                    "✅ Quality validation and compliance checks",
                    "💼 Negotiate commercial terms"
                ]
            },
            {
                "phase": "Medium-term (3-12 months)",
                "actions": [
                    "📈 Scale pilot to 15-25% of volume",
                    "🔄 Implement dual-sourcing strategy",
                    "📉 Monitor cost and quality metrics",
                    "🎯 Adjust targets based on results"
                ]
            },
            {
                "phase": "Long-term (12+ months)",
                "actions": [
                    "🌐 Achieve target diversification ratios",
                    "🏆 Establish strategic partnerships",
                    "📊 Continuous monitoring and optimization",
                    "🔄 Periodic risk reassessment"
                ]
            }
        ]
        
        return roadmap
    
    def _estimate_timeline(self, risk_level) -> str:
        """Estimate overall timeline"""
        if risk_level == "HIGH":
            return "6-12 months (accelerated due to high risk)"
        elif risk_level == "MEDIUM":
            return "12-18 months (standard implementation)"
        else:
            return "18-24 months (gradual optimization)"
    
    def _generate_summary(self, strategies, outcomes, risk_level) -> str:
        """Generate executive summary"""
        
        if not strategies:
            return "Current sourcing strategy is adequately diversified. Continue monitoring."
        
        primary = strategies[0]
        
        summary = f"""
**Strategic Diversification Recommendation**

**Priority Action:** {primary['name']}
- **Target:** {primary['target']}
- **Timeline:** {primary['timeline']}
- **Feasibility:** {primary['feasibility']}

**Expected Impact:**
- Reduce China dependency by {outcomes['china_dependency']['reduction']}%
- Improve market concentration (HHI) by {outcomes['market_concentration']['improvement']}%
- Risk level: {outcomes['risk_reduction']['from']} → {outcomes['risk_reduction']['to']}

**Implementation:** Start with pilot phase, scale gradually based on validation results.
        """
        
        return summary.strip()

# ============================================================================
# AGENT ORCHESTRATOR
# ============================================================================

class AgentOrchestrator:
    """Main orchestrator coordinating all agents"""
    
    def __init__(self, df: pd.DataFrame):
        self.data_agent = DataRetrievalAgent(df)
        self.risk_agent = RiskAssessmentAgent()
        self.diversification_agent = StrategicDiversificationAgent()
    
    def analyze_product(self, hs_code: str, quarter: Optional[str] = None) -> Dict:
        """Complete analysis for a product"""
        
        # Step 1: Retrieve data
        data_context = self.data_agent.get_product_data(hs_code, quarter)
        
        if "error" in data_context:
            return data_context
        
        # Step 2: Assess risk
        risk_assessment = self.risk_agent.assess_risk(data_context)
        
        # Step 3: Generate recommendations
        diversification_recs = self.diversification_agent.generate_recommendations(
            data_context, risk_assessment
        )
        
        # Combine all results
        complete_analysis = {
            "product_info": {
                "hs_code": data_context['hs_code'],
                "name": data_context['product_name'],
                "quarter": data_context['quarter']
            },
            "data_context": data_context,
            "risk_assessment": risk_assessment,
            "diversification_recommendations": diversification_recs,
            "timestamp": datetime.now().isoformat()
        }
        
        return complete_analysis

# ============================================================================
# STREAMLIT UI
# ============================================================================

def main():
    """Main Streamlit application"""
    
    # Title and intro
    st.title("🌐 Trade Risk AI Assistant")
    st.markdown("""
    **Agentic AI Framework for Proactive Global Trade Risk Management**
    
    Analyze US-China-India bilateral trade risks and get strategic diversification recommendations
    powered by specialized AI agents.
    """)
    
    # Load data
    df = load_data()
    
    if df is None:
        st.stop()
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator(df)
    
    # Sidebar - Scope and Info
    with st.sidebar:
        st.header("📊 Scope")
        st.info("""
        **Coverage:**
        - **Countries:** USA, China, India
        - **Products:** 12 HS4 codes
        - **Period:** 2020-Q3 to 2025-Q2
        - **Data:** Trade flows + NTM measures
        """)
        
        st.header("🤖 Active Agents")
        st.success("✅ Data Retrieval Agent")
        st.success("✅ Risk Assessment Agent")
        st.success("✅ Diversification Agent")
        
        st.header("ℹ️ About")
        st.markdown("""
        This system uses three specialized AI agents:
        
        1. **📊 Data Agent**: Retrieves trade data
        2. **⚠️ Risk Agent**: Assesses vulnerabilities
        3. **🌐 Strategy Agent**: Recommends actions
        
        """)
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["💬 Chat Interface", "📊 Dashboard", "📚 Case Studies"])
    
    with tab1:
        st.header("💬 Conversational Analysis")
        
        # Product selector
        products = orchestrator.data_agent.get_all_products_summary()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_hs = st.selectbox(
                "Select Product (HS Code):",
                options=products['HS Code'].tolist(),
                format_func=lambda x: f"{x} - {products[products['HS Code']==x]['Product'].iloc[0][:50]}..."
            )
        
        with col2:
            available_quarters = df[df['hs_code'] == str(selected_hs)]['date'].unique()
            selected_quarter = st.selectbox(
                "Quarter:",
                options=sorted(available_quarters, reverse=True)
            )
        
        # Analyze button
        if st.button("🔍 Analyze", type="primary", use_container_width=True):
            
            with st.spinner("🤖 AI Agents analyzing..."):
                
                # Run analysis
                analysis = orchestrator.analyze_product(selected_hs, selected_quarter)
                
                if "error" in analysis:
                    st.error(analysis["error"])
                else:
                    # Display results
                    st.success("✅ Analysis Complete!")
                    
                    # Product info
                    st.subheader(f"📦 {analysis['product_info']['name']}")
                    st.caption(f"HS Code: {analysis['product_info']['hs_code']} | Quarter: {analysis['product_info']['quarter']}")
                    
                    # Risk Assessment
                    st.markdown("---")
                    st.subheader("⚠️ Risk Assessment")
                    
                    risk = analysis['risk_assessment']
                    
                    # Risk level badge
                    risk_color = {
                        "HIGH": "🔴",
                        "MEDIUM": "🟡",
                        "LOW": "🟢"
                    }
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Risk Level", f"{risk_color.get(risk['overall_risk_level'], '')} {risk['overall_risk_level']}")
                    col2.metric("Risk Score", f"{risk['overall_risk_score']}/100")
                    col3.metric("Urgency", risk['urgency'])
                    
                    # Vulnerabilities
                    st.markdown("**Key Vulnerabilities:**")
                    for vuln in risk['vulnerabilities']:
                        st.markdown(f"- {vuln}")
                    
                    # Risk components
                    with st.expander("📊 Detailed Risk Breakdown"):
                        components = risk['risk_components']
                        
                        cols = st.columns(4)
                        cols[0].metric("Concentration", f"{components['concentration']['score']}/100", 
                                      components['concentration']['level'])
                        cols[1].metric("Dependency", f"{components['dependency']['score']}/100",
                                      components['dependency']['level'])
                        cols[2].metric("NTM Impact", f"{components['ntm_impact']['score']}/100",
                                      components['ntm_impact']['level'])
                        cols[3].metric("Trend", f"{components['trend']['score']}/100",
                                      components['trend']['level'])
                    
                    # Diversification Recommendations
                    st.markdown("---")
                    st.subheader("🌐 Strategic Diversification")
                    
                    divs = analysis['diversification_recommendations']
                    
                    if divs['primary_recommendation']:
                        primary = divs['primary_recommendation']
                        
                        st.success(f"**Priority Action:** {primary['name']}")
                        st.markdown(f"**Target:** {primary['target']}")
                        st.markdown(f"**Timeline:** {primary['timeline']}")
                        st.markdown(f"**Feasibility:** {primary['feasibility']}")
                        
                        # Implementation steps
                        with st.expander("📋 Implementation Steps"):
                            for step in primary['implementation_steps']:
                                st.markdown(f"- {step}")
                        
                        # Expected outcomes
                        if divs['expected_outcomes']:
                            st.markdown("**Expected Impact:**")
                            outcomes = divs['expected_outcomes']
                            
                            col1, col2 = st.columns(2)
                            col1.metric(
                                "China Dependency", 
                                f"{outcomes['china_dependency']['target']}%",
                                f"-{outcomes['china_dependency']['reduction']}%"
                            )
                            col2.metric(
                                "Market Concentration",
                                f"HHI {outcomes['market_concentration']['target_hhi']}",
                                f"-{outcomes['market_concentration']['improvement']}%"
                            )
                    
                    # Implementation Roadmap
                    with st.expander("🗓️ Implementation Roadmap"):
                        for phase in divs['implementation_roadmap']:
                            st.markdown(f"**{phase['phase']}**")
                            for action in phase['actions']:
                                st.markdown(f"  {action}")
                    
                    # Current Metrics
                    st.markdown("---")
                    with st.expander("📊 Current Trade Metrics"):
                        context = analysis['data_context']
                        current = context['current_metrics']
                        indicators = context['trade_indicators']
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("China Share", f"{current['china_share']}%")
                        col1.metric("China RCA", indicators['china_rca'])
                        
                        col2.metric("India Share", f"{current['india_share']}%")
                        col2.metric("India RCA", indicators['india_rca'])
                        
                        col3.metric("HHI", current['hhi'])
                        col3.metric("NTM Count", context['ntm_data']['ntm_count'])
    
    with tab2:
        st.header("📊 Portfolio Dashboard")
        
        # Show all products summary
        summary_df = orchestrator.data_agent.get_all_products_summary()
        
        # Style the dataframe
        st.dataframe(
            summary_df.style.background_gradient(subset=['Risk Score'], cmap='RdYlGn_r'),
            use_container_width=True,
            height=500
        )
        
        # Risk distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Risk Distribution")
            risk_counts = summary_df['Risk Level'].value_counts()
            st.bar_chart(risk_counts)
        
        with col2:
            st.subheader("Top Risks")
            top_risks = summary_df.nlargest(5, 'Risk Score')[['HS Code', 'Product', 'Risk Score']]
            st.dataframe(top_risks, use_container_width=True, hide_index=True)
    
    with tab3:
        st.header("📚 Case Study Validation")
        st.info("Case study validation is available in the Jupyter notebook: `case_study_validation.ipynb`")
        
        st.markdown("""
        ### Available Case Studies:
        
        1. **US-China Section 301 Tariffs (2018-2020)**
           - Telecom equipment (HS 8517)
           - Computing machines (HS 8471)
           - Semiconductors (HS 8542)
        
        2. **India Rice Export Ban (2022)**
           - Rice (HS 1006)
        
        3. **China Graphite Export Controls (2023)**
           - Natural graphite (HS 2504)
        
        Open the notebook to run retrospective validation and see how the system would have predicted these events.
        """)

if __name__ == "__main__":
    main()
