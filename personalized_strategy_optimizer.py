#!/usr/bin/env python3
"""
个性化策略优化器 - 四维提升深化
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum

class RiskTolerance(Enum):
    """风险承受能力"""
    CONSERVATIVE = "保守型"  # 低风险，稳定收益
    MODERATE = "稳健型"     # 中等风险，平衡收益
    AGGRESSIVE = "进取型"   # 高风险，高收益

class InvestmentGoal(Enum):
    """投资目标"""
    CAPITAL_PRESERVATION = "保值"      # 保持本金安全
    INCOME_GENERATION = "收益"         # 获取稳定收益
    CAPITAL_GROWTH = "增值"           # 追求资本增值
    SPECULATION = "投机"              # 短期投机获利

class PersonalizedStrategyOptimizer:
    """个性化策略优化器"""
    
    def __init__(self, user_profile: Dict[str, Any], investment_history: List[Dict[str, Any]] = None):
        """
        初始化个性化策略优化器
        
        Args:
            user_profile: 用户画像数据
            investment_history: 投资历史记录
        """
        self.user_profile = user_profile
        self.investment_history = investment_history or []
        
        # 策略库
        self.strategy_library = self._load_strategy_library()
        
        print("🧠 个性化策略优化器初始化")
        print("=" * 60)
        print("📊 用户画像分析:")
        print(f"   风险偏好: {user_profile.get('risk_tolerance', '未知')}")
        print(f"   投资目标: {user_profile.get('investment_goal', '未知')}")
        print(f"   投资经验: {user_profile.get('investment_experience', '未知')}")
        print(f"   历史记录: {len(investment_history) if investment_history else 0} 条")
        print("=" * 60)
    
    def recommend_strategies(self, market_conditions: Dict[str, Any], 
                           current_portfolio: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """推荐个性化策略"""
        print(f"\n🎯 开始个性化策略推荐")
        print(f"   市场条件: {market_conditions.get('market_trend', '未知')}")
        print(f"   当前持仓: {len(current_portfolio) if current_portfolio else 0} 只股票")
        print("-" * 50)
        
        start_time = datetime.now()
        
        try:
            # 1. 用户画像深度分析
            print("1. 👤 深度分析用户画像...")
            user_analysis = self._analyze_user_profile()
            
            # 2. 市场条件分析
            print("2. 🌍 分析市场条件...")
            market_analysis = self._analyze_market_conditions(market_conditions)
            
            # 3. 投资历史分析
            print("3. 📊 分析投资历史...")
            history_analysis = self._analyze_investment_history()
            
            # 4. 当前持仓分析
            print("4. 💼 分析当前持仓...")
            portfolio_analysis = self._analyze_current_portfolio(current_portfolio) if current_portfolio else {}
            
            # 5. 策略筛选和匹配
            print("5. 🔍 筛选和匹配策略...")
            candidate_strategies = self._filter_and_match_strategies(
                user_analysis, market_analysis, history_analysis, portfolio_analysis
            )
            
            # 6. 策略效果预测
            print("6. 📈 预测策略效果...")
            strategy_predictions = self._predict_strategy_performance(candidate_strategies, market_analysis)
            
            # 7. 个性化推荐生成
            print("7. 🎯 生成个性化推荐...")
            recommendations = self._generate_personalized_recommendations(strategy_predictions, user_analysis)
            
            total_time = (datetime.now() - start_time).total_seconds()
            
            return {
                'status': 'success',
                'recommendation_time': datetime.now().isoformat(),
                'processing_time': f'{total_time:.2f}秒',
                'user_analysis': user_analysis,
                'market_analysis': market_analysis,
                'history_analysis': history_analysis,
                'portfolio_analysis': portfolio_analysis,
                'strategy_analysis': {
                    'total_strategies': len(self.strategy_library),
                    'candidate_strategies': len(candidate_strategies),
                    'recommended_strategies': len(recommendations)
                },
                'recommendations': recommendations,
                'confidence': self._calculate_recommendation_confidence(recommendations),
                'personalization_level': self._assess_personalization_level(user_analysis, history_analysis)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': f'策略推荐失败: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def _load_strategy_library(self) -> List[Dict[str, Any]]:
        """加载策略库"""
        strategies = [
            {
                'id': 'strategy_001',
                'name': '价值投资策略',
                'description': '寻找被低估的优质公司，长期持有',
                'risk_level': '低',
                'time_horizon': '长期',
                'suitable_for': ['保值', '收益'],
                'required_experience': '中级',
                'key_metrics': ['PE', 'PB', 'ROE', '股息率'],
                'success_rate': 0.65
            },
            {
                'id': 'strategy_002',
                'name': '成长投资策略',
                'description': '投资高成长性公司，追求资本增值',
                'risk_level': '高',
                'time_horizon': '中长期',
                'suitable_for': ['增值'],
                'required_experience': '高级',
                'key_metrics': ['营收增长率', '净利润增长率', '研发投入'],
                'success_rate': 0.55
            },
            {
                'id': 'strategy_003',
                'name': '趋势跟踪策略',
                'description': '跟随市场趋势，顺势而为',
                'risk_level': '中',
                'time_horizon': '短期',
                'suitable_for': ['增值', '投机'],
                'required_experience': '中级',
                'key_metrics': ['趋势强度', '成交量', '技术指标'],
                'success_rate': 0.60
            },
            {
                'id': 'strategy_004',
                'name': '股息投资策略',
                'description': '投资高股息公司，获取稳定现金流',
                'risk_level': '低',
                'time_horizon': '长期',
                'suitable_for': ['保值', '收益'],
                'required_experience': '初级',
                'key_metrics': ['股息率', '分红稳定性', '现金流'],
                'success_rate': 0.70
            },
            {
                'id': 'strategy_005',
                'name': '动量策略',
                'description': '投资近期表现强势的股票',
                'risk_level': '高',
                'time_horizon': '短期',
                'suitable_for': ['投机'],
                'required_experience': '高级',
                'key_metrics': ['近期涨幅', '成交量变化', '资金流向'],
                'success_rate': 0.50
            },
            {
                'id': 'strategy_006',
                'name': '分散投资策略',
                'description': '通过分散投资降低风险',
                'risk_level': '低',
                'time_horizon': '中长期',
                'suitable_for': ['保值', '收益'],
                'required_experience': '初级',
                'key_metrics': ['相关性', '行业分布', '仓位控制'],
                'success_rate': 0.75
            },
            {
                'id': 'strategy_007',
                'name': '技术分析策略',
                'description': '基于技术图表和指标进行交易',
                'risk_level': '中',
                'time_horizon': '短期',
                'suitable_for': ['增值', '投机'],
                'required_experience': '中级',
                'key_metrics': ['技术指标', '图表形态', '支撑阻力'],
                'success_rate': 0.58
            },
            {
                'id': 'strategy_008',
                'name': '基本面轮动策略',
                'description': '根据基本面变化轮动投资不同行业',
                'risk_level': '中',
                'time_horizon': '中期',
                'suitable_for': ['增值'],
                'required_experience': '高级',
                'key_metrics': ['行业景气度', '估值变化', '政策影响'],
                'success_rate': 0.62
            }
        ]
        
        return strategies
    
    def _analyze_user_profile(self) -> Dict[str, Any]:
        """深度分析用户画像"""
        profile = self.user_profile
        
        # 风险偏好分析
        risk_tolerance = profile.get('risk_tolerance', '稳健型')
        if risk_tolerance == '保守型':
            risk_score = 25
            risk_description = '偏好低风险稳定收益'
        elif risk_tolerance == '稳健型':
            risk_score = 50
            risk_description = '平衡风险和收益'
        else:  # 进取型
            risk_score = 75
            risk_description = '追求高收益，能承受较高风险'
        
        # 投资目标分析
        investment_goal = profile.get('investment_goal', '增值')
        if investment_goal == '保值':
            goal_priority = '安全性'
        elif investment_goal == '收益':
            goal_priority = '现金流'
        elif investment_goal == '增值':
            goal_priority = '成长性'
        else:  # 投机
            goal_priority = '短期收益'
        
        # 投资经验分析
        experience = profile.get('investment_experience', '中级')
        if experience == '初级':
            experience_level = 1
            suitable_complexity = '简单'
        elif experience == '中级':
            experience_level = 2
            suitable_complexity = '中等'
        else:  # 高级
            experience_level = 3
            suitable_complexity = '复杂'
        
        # 投资期限偏好
        time_horizon = profile.get('time_horizon', '中长期')
        
        return {
            'risk_analysis': {
                'risk_tolerance': risk_tolerance,
                'risk_score': risk_score,
                'risk_description': risk_description,
                'max_drawdown_tolerance': f'{100 - risk_score}%'  # 最大回撤容忍度
            },
            'goal_analysis': {
                'investment_goal': investment_goal,
                'goal_priority': goal_priority,
                'expected_return': self._estimate_expected_return(risk_score, investment_goal)
            },
            'experience_analysis': {
                'investment_experience': experience,
                'experience_level': experience_level,
                'suitable_complexity': suitable_complexity,
                'learning_capacity': '高' if experience_level >= 2 else '中'
            },
            'preference_analysis': {
                'time_horizon': time_horizon,
                'active_management': profile.get('active_management', True),
                'diversification_preference': profile.get('diversification', True)
            }
        }
    
    def _estimate_expected_return(self, risk_score: int, goal: str) -> str:
        """估计预期收益率"""
        base_return = 5  # 基础收益率
        
        if goal == '保值':
            expected = base_return + risk_score * 0.1
        elif goal == '收益':
            expected = base_return + risk_score * 0.15
        elif goal == '增值':
            expected = base_return + risk_score * 0.2
        else:  # 投机
            expected = base_return + risk_score * 0.25
        
        return f'{expected:.1f}%'
    
    def _analyze_market_conditions(self, market_conditions: Dict[str, Any]) -> Dict[str, Any]:
        """分析市场条件"""
        trend = market_conditions.get('market_trend', '震荡')
        volatility = market_conditions.get('volatility', '中等')
        sentiment = market_conditions.get('market_sentiment', '中性')
        
        # 市场状态评估
        if trend == '上涨' and sentiment == '乐观':
            market_state = '牛市'
            opportunity_level = '高'
        elif trend == '下跌' and sentiment == '悲观':
            market_state = '熊市'
            opportunity_level = '低'
        elif trend == '震荡' and volatility == '高':
            market_state = '震荡市'
            opportunity_level = '中'
        else:
            market_state = '平衡市'
            opportunity_level = '中'
        
        # 适合的策略类型
        suitable_strategy_types = []
        if market_state == '牛市':
            suitable_strategy_types.extend(['成长投资', '趋势跟踪', '动量策略'])
        elif market_state == '熊市':
            suitable_strategy_types.extend(['价值投资', '股息投资', '分散投资'])
        elif market_state == '震荡市':
            suitable_strategy_types.extend(['技术分析', '基本面轮动', '分散投资'])
        else:  # 平衡市
            suitable_strategy_types.extend(['价值投资', '成长投资', '分散投资'])
        
        return {
            'market_state': market_state,
            'trend_analysis': {
                'trend': trend,
                'strength': market_conditions.get('trend_strength', '中等'),
                'duration': market_conditions.get('trend_duration', '短期')
            },
            'volatility_analysis': {
                'volatility': volatility,
                'risk_level': '高' if volatility == '高' else '中' if volatility == '中等' else '低'
            },
            'sentiment_analysis': {
                'sentiment': sentiment,
                'confidence': market_conditions.get('confidence', 0.5)
            },
            'opportunity_assessment': {
                'opportunity_level': opportunity_level,
                'suitable_strategy_types': suitable_strategy_types,
                'market_timing': '适合投资' if opportunity_level in ['高', '中'] else '谨慎投资'
            }
        }
    
    def _analyze_investment_history(self) -> Dict[str, Any]:
        """分析投资历史"""
        if not self.investment_history:
            return {
                'history_available': False,
                'analysis': '无历史数据',
                'recommendation': '建议开始记录投资历史'
            }
        
        # 简单历史分析
        total_trades = len(self.investment_history)
        profitable_trades = sum(1 for trade in self.investment_history if trade.get('profit', 0) > 0)
        total_profit = sum(trade.get('profit', 0) for trade in self.investment_history)
        avg_profit = total_profit / total_trades if total_trades > 0 else 0
        
        # 投资风格分析
        holding_periods = []
        for trade in self.investment_history:
            if 'buy_date' in trade and 'sell_date' in trade:
                buy_date = datetime.strptime(trade['buy_date'], '%Y-%m-%d')
                sell_date = datetime.strptime(trade['sell_date'], '%Y-%m-%d')
                holding_days = (sell_date - buy_date).days
                holding_periods.append(holding_days)
        
        if holding_periods:
            avg_holding_days = sum(holding_periods) / len(holding_periods)
            if avg_holding_days < 30:
                trading_style = '短线交易'
            elif avg_holding_days < 180:
                trading_style = '中线投资'
            else:
                trading_style = '长线投资'
        else:
            avg_holding_days = 0
            trading_style = '未知'
        
        # 成功率分析
        success_rate = profitable_trades / total_trades * 100 if total_trades > 0 else 0
        
        if success_rate >= 60:
            performance = '优秀'
        elif success_rate >= 50:
            performance = '良好'
        elif success_rate >= 40:
            performance = '一般'
        else:
            performance = '需改进'
        
        return {
            'history_available': True,
            'summary': {
                'total_trades': total_trades,
                'profitable_trades': profitable_trades,
                'success_rate': f'{success_rate:.1f}%',
                'total_profit': total_profit,
                'avg_profit': avg_profit,
                'performance': performance
            },
            'style_analysis': {
                'trading_style': trading_style,
                'avg_holding_days': avg_holding_days,
                'risk_taking': '积极' if avg_profit > 0 else '保守'
            },
            'improvement_suggestions': self._generate_improvement_suggestions(success_rate, trading_style)
        }
    
    def _generate_improvement_suggestions(self, success_rate: float, trading_style: str) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        if success_rate < 50:
            suggestions.append('投资成功率较低，建议加强研究和风险控制')
        
        if trading_style == '短线交易' and success_rate < 60:
            suggestions.append('短线交易难度较大，建议考虑中线或长线投资')
        
        if success_rate >= 60:
            suggestions.append('投资表现良好，建议保持当前策略并适当优化')
        
        if not suggestions:
            suggestions.append('建议继续积累投资经验，优化投资策略')
        
        return suggestions
    
    def _analyze_current_portfolio(self, portfolio: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析当前持仓"""
        if not portfolio:
            return {'portfolio_available': False, 'analysis': '无持仓'}
        
        total_value = sum(item.get('current_value', 0) for item in portfolio)
        total_cost = sum(item.get('cost', 0) for item in portfolio)
        
        # 计算盈亏
        total_profit = total_value - total_cost
        profit_rate = total_profit / total_cost * 100 if total_cost > 0 else 0
        
        # 行业分布
        industries = {}
        for item in portfolio:
            industry = item.get('industry', '未知')
            value = item.get('current_value', 0)
            industries[industry] = industries.get(industry, 0) + value
        
        # 集中度分析
        if industries:
            top_industry = max(industries.items(), key=lambda x: x[1])
            concentration = top_industry[1] / total_value * 100 if total_value > 0 else 0
        else:
            concentration = 0
            top_industry = ('未知', 0)
        
        # 风险评估
        if concentration > 50:
            diversification = '低'
            risk_note = '持仓过于集中，风险较高'
        elif concentration > 30:
            diversification = '中'
            risk_note = '持仓有一定集中度，风险中等'
        else:
            diversification = '高'
            risk_note = '持仓分散，风险较低'
        
        return {
            'portfolio_available': True,
            'summary': {
                'total_positions': len(portfolio),
                'total_value': total_value,
                'total_cost': total_cost,
                'total_profit': total_profit,
                'profit_rate': f'{profit_rate:.1f}%',
                'performance': '盈利' if profit_rate > 0 else '亏损'
            },
            'diversification_analysis': {
                'industries_count': len(industries),
                'top_industry': f'{top_industry[0]} ({top_industry[1]/total_value*100:.1f}%)',
                'concentration': f'{concentration:.1f}%',
                'diversification_level': diversification,
                'risk_note': risk_note
            },
            'optimization_suggestions': self._generate_portfolio_suggestions(profit_rate, diversification)
        }
    
    def _generate_portfolio_suggestions(self, profit_rate: float, diversification: str) -> List[str]:
        """生成持仓优化建议"""
        suggestions = []
        
        if profit_rate < 0:
            suggestions.append('当前持仓亏损，建议重新评估投资标的')
        
        if diversification == '低':
            suggestions.append('持仓过于集中，建议增加分散投资')
        elif diversification == '中':
            suggestions.append('持仓有一定集中度，可考虑适当分散')
        
        if profit_rate > 10 and diversification == '高':
            suggestions.append('持仓表现良好且分散，建议保持当前策略')
        
        if not suggestions:
            suggestions.append('建议定期回顾和调整持仓结构')
        
        return suggestions
    
    def _filter_and_match_strategies(self, user_analysis: Dict[str, Any], 
                                   market_analysis: Dict[str, Any],
                                   history_analysis: Dict[str, Any],
                                   portfolio_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """筛选和匹配策略"""
        candidate_strategies = []
        
        user_risk = user_analysis['risk_analysis']['risk_tolerance']
        user_goal = user_analysis['goal_analysis']['investment_goal']
        user_experience = user_analysis['experience_analysis']['investment_experience']
        
        market_state = market_analysis['market_state']
        suitable_types = market_analysis['opportunity_assessment']['suitable_strategy_types']
        
        for strategy in self.strategy_library:
            # 风险匹配
            risk_match = self._assess_risk_match(strategy['risk_level'], user_risk)
            
            # 目标匹配
            goal_match = user_goal in strategy['suitable_for']
            
            # 经验匹配
            experience_match = self._assess_experience_match(strategy['required_experience'], user_experience)
            
            # 市场匹配
            market_match = any(stype in strategy['name'] for stype in suitable_types)
            
            # 综合匹配度
            match_score = (
                (3 if risk_match else 0) +
                (3 if goal_match else 0) +
                (2 if experience_match else 0) +
                (2 if market_match else 0)
            )
            
            if match_score >= 5:  # 至少匹配5分
                strategy_copy = strategy.copy()
                strategy_copy['match_score'] = match_score
                strategy_copy['match_details'] = {
                    'risk_match': risk_match,
                    'goal_match': goal_match,
                    'experience_match': experience_match,
                    'market_match': market_match
                }
                candidate_strategies.append(strategy_copy)
        
        # 按匹配度排序
        candidate_strategies.sort(key=lambda x: x['match_score'], reverse=True)
        
        return candidate_strategies
    
    def _assess_risk_match(self, strategy_risk: str, user_risk: str) -> bool:
        """评估风险匹配"""
        risk_levels = {'低': 1, '中': 2, '高': 3}
        user_level = risk_levels.get(user_risk, 2)  # 默认中等
        
        # 保守型用户只适合低风险策略
        if user_risk == '保守型':
            return strategy_risk == '低'
        # 稳健型用户适合低和中风险策略
        elif user_risk == '稳健型':
            return strategy_risk in ['低', '中']
        # 进取型用户适合所有风险策略
        else:  # 进取型
            return True
    
    def _assess_experience_match(self, required_exp: str, user_exp: str) -> bool:
        """评估经验匹配"""
        exp_levels = {'初级': 1, '中级': 2, '高级': 3}
        required_level = exp_levels.get(required_exp, 2)
        user_level = exp_levels.get(user_exp, 2)
        
        return user_level >= required_level
    
    def _predict_strategy_performance(self, candidate_strategies: List[Dict[str, Any]],
                                    market_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """预测策略效果"""
        predictions = []
        
        market_state = market_analysis['market_state']
        opportunity_level = market_analysis['opportunity_assessment']['opportunity_level']
        
        for strategy in candidate_strategies:
            base_success = strategy['success_rate']
            
            # 根据市场状态调整成功率
            market_adjustment = self._get_market_adjustment(strategy['name'], market_state)
            
            # 根据机会水平调整
            if opportunity_level == '高':
                opportunity_adjustment = 0.1
            elif opportunity_level == '中':
                opportunity_adjustment = 0
            else:  # 低
                opportunity_adjustment = -0.1
            
            # 计算调整后的成功率
            adjusted_success = base_success + market_adjustment + opportunity_adjustment
            adjusted_success = max(0.3, min(0.9, adjusted_success))  # 限制在30%-90%之间
            
            # 估计预期收益率
            expected_return = self._estimate_strategy_return(strategy, market_state)
            
            predictions.append({
                'strategy_id': strategy['id'],
                'strategy_name': strategy['name'],
                'base_success_rate': base_success,
                'adjusted_success_rate': adjusted_success,
                'expected_return': expected_return,
                'risk_level': strategy['risk_level'],
                'suitability_score': strategy['match_score'],
                'market_adjustment': market_adjustment,
                'recommendation_level': self._determine_recommendation_level(adjusted_success, expected_return)
            })
        
        # 按推荐级别排序
        predictions.sort(key=lambda x: (
            -x['recommendation_level']['priority'],
            -x['adjusted_success_rate'],
            -self._parse_return_to_number(x['expected_return'])  # 转换为数字排序
        ))
        
        return predictions
    
    def _get_market_adjustment(self, strategy_name: str, market_state: str) -> float:
        """获取市场调整因子"""
        adjustments = {
            ('价值投资策略', '熊市'): 0.15,
            ('价值投资策略', '牛市'): -0.05,
            ('成长投资策略', '牛市'): 0.15,
            ('成长投资策略', '熊市'): -0.10,
            ('趋势跟踪策略', '牛市'): 0.10,
            ('趋势跟踪策略', '熊市'): -0.15,
            ('股息投资策略', '震荡市'): 0.05,
            ('动量策略', '牛市'): 0.12,
            ('动量策略', '熊市'): -0.20,
            ('分散投资策略', '熊市'): 0.08,
            ('技术分析策略', '震荡市'): 0.07,
            ('基本面轮动策略', '平衡市'): 0.05
        }
        
        return adjustments.get((strategy_name, market_state), 0)
    
    def _parse_return_to_number(self, return_str: str) -> float:
        """将收益率字符串转换为数字"""
        try:
            # 处理 "8-12%" 或 "12+%" 格式
            if '+' in return_str:
                # 如 "12+%"
                num = float(return_str.replace('+%', ''))
                return num + 5  # 给一个加成
            elif '-' in return_str:
                # 如 "8-12%"
                lower, upper = return_str.split('-')
                lower_num = float(lower)
                upper_num = float(upper.replace('%', ''))
                return (lower_num + upper_num) / 2  # 取平均值
            else:
                # 如 "10%"
                return float(return_str.replace('%', ''))
        except:
            return 10.0  # 默认值
    
    def _estimate_strategy_return(self, strategy: Dict[str, Any], market_state: str) -> str:
        """估计策略预期收益率"""
        base_returns = {
            '价值投资策略': '8-12%',
            '成长投资策略': '12-20%',
            '趋势跟踪策略': '10-15%',
            '股息投资策略': '6-9%',
            '动量策略': '15-25%',
            '分散投资策略': '7-10%',
            '技术分析策略': '9-14%',
            '基本面轮动策略': '10-16%'
        }
        
        base_return = base_returns.get(strategy['name'], '8-12%')
        
        try:
            # 根据市场状态调整
            if market_state == '牛市':
                # 牛市取上限，并增加预期
                lower, upper = base_return.split('-')
                lower_num = int(lower)
                upper_num = int(upper.replace('%', ''))
                return f"{upper_num}+%"
            elif market_state == '熊市':
                # 熊市降低预期
                lower, upper = base_return.split('-')
                lower_num = int(lower) - 3
                upper_num = int(upper.replace('%', '')) - 3
                return f"{lower_num}%-{upper_num}%"
            else:
                return base_return
        except:
            # 如果解析失败，返回默认值
            return '8-12%'
    
    def _determine_recommendation_level(self, success_rate: float, expected_return: str) -> Dict[str, Any]:
        """确定推荐级别"""
        if success_rate >= 0.7:
            level = '强烈推荐'
            priority = 1
            color = 'green'
        elif success_rate >= 0.6:
            level = '推荐'
            priority = 2
            color = 'blue'
        elif success_rate >= 0.5:
            level = '可考虑'
            priority = 3
            color = 'yellow'
        else:
            level = '谨慎考虑'
            priority = 4
            color = 'orange'
        
        return {
            'level': level,
            'priority': priority,
            'color': color,
            'success_threshold': f'{success_rate*100:.0f}%'
        }
    
    def _generate_personalized_recommendations(self, strategy_predictions: List[Dict[str, Any]],
                                             user_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成个性化推荐"""
        recommendations = []
        
        # 只取前3个最佳策略
        top_strategies = strategy_predictions[:3]
        
        for i, strategy in enumerate(top_strategies, 1):
            recommendation = {
                'rank': i,
                'strategy_id': strategy['strategy_id'],
                'strategy_name': strategy['strategy_name'],
                'recommendation_level': strategy['recommendation_level']['level'],
                'success_probability': f'{strategy["adjusted_success_rate"]*100:.1f}%',
                'expected_return': strategy['expected_return'],
                'risk_level': strategy['risk_level'],
                'suitability_score': strategy['suitability_score'],
                'key_reasons': self._generate_key_reasons(strategy, user_analysis),
                'implementation_steps': self._generate_implementation_steps(strategy),
                'risk_warnings': self._generate_risk_warnings(strategy)
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_key_reasons(self, strategy: Dict[str, Any], user_analysis: Dict[str, Any]) -> List[str]:
        """生成关键理由"""
        reasons = []
        
        user_risk = user_analysis['risk_analysis']['risk_tolerance']
        user_goal = user_analysis['goal_analysis']['investment_goal']
        
        reasons.append(f"风险匹配: 策略风险({strategy['risk_level']})适合您的风险偏好({user_risk})")
        reasons.append(f"目标匹配: 策略适合{user_goal}目标")
        reasons.append(f"成功概率: 预计成功率{strategy['adjusted_success_rate']*100:.1f}%")
        reasons.append(f"预期收益: {strategy['expected_return']}")
        
        return reasons
    
    def _generate_implementation_steps(self, strategy: Dict[str, Any]) -> List[str]:
        """生成实施步骤"""
        steps_map = {
            '价值投资策略': [
                '1. 筛选低估值股票(PE、PB低于行业平均)',
                '2. 分析公司基本面(财务健康、竞争优势)',
                '3. 分批建仓，控制仓位',
                '4. 长期持有，定期回顾'
            ],
            '成长投资策略': [
                '1. 寻找高成长性行业和公司',
                '2. 分析成长驱动因素(技术、市场、管理)',
                '3. 合理估值，避免追高',
                '4. 动态跟踪，及时调整'
            ],
            '趋势跟踪策略': [
                '1. 识别主要趋势方向',
                '2. 等待回调入场机会',
                '3. 设置止损止盈',
                '4. 趋势反转时及时退出'
            ],
            '股息投资策略': [
                '1. 筛选高股息率股票',
                '2. 分析分红稳定性和可持续性',
                '3. 建立股息投资组合',
                '4. 定期收取股息，复利投资'
            ]
        }
        
        return steps_map.get(strategy['strategy_name'], [
            '1. 深入研究策略原理',
            '2. 制定具体实施方案',
            '3. 小规模测试验证',
            '4. 根据效果调整优化'
        ])
    
    def _generate_risk_warnings(self, strategy: Dict[str, Any]) -> List[str]:
        """生成风险警告"""
        warnings = []
        
        if strategy['risk_level'] == '高':
            warnings.append('高风险策略，可能面临较大亏损')
            warnings.append('建议严格控制仓位，设置止损')
        
        if strategy['adjusted_success_rate'] < 0.6:
            warnings.append('成功率中等，需要谨慎操作')
        
        if '短期' in strategy.get('time_horizon', ''):
            warnings.append('短期策略需要密切监控市场')
        
        if not warnings:
            warnings.append('投资有风险，决策需谨慎')
        
        return warnings
    
    def _calculate_recommendation_confidence(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """计算推荐置信度"""
        if not recommendations:
            return {'confidence': 0, 'level': '低', 'reason': '无推荐策略'}
        
        # 基于推荐级别计算置信度
        level_scores = {'强烈推荐': 0.9, '推荐': 0.7, '可考虑': 0.5, '谨慎考虑': 0.3}
        
        total_score = 0
        for rec in recommendations:
            total_score += level_scores.get(rec['recommendation_level'], 0.5)
        
        avg_score = total_score / len(recommendations)
        
        if avg_score >= 0.8:
            confidence_level = '高'
        elif avg_score >= 0.6:
            confidence_level = '中'
        else:
            confidence_level = '低'
        
        return {
            'confidence_score': avg_score,
            'confidence_level': confidence_level,
            'calculation_basis': f'基于{len(recommendations)}个推荐策略的平均推荐级别',
            'improvement_suggestions': '增加用户数据可以提高推荐准确性' if confidence_level != '高' else '推荐质量良好'
        }
    
    def _assess_personalization_level(self, user_analysis: Dict[str, Any], 
                                    history_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """评估个性化程度"""
        factors = []
        
        # 用户画像完整性
        profile_completeness = 0
        if user_analysis['risk_analysis']['risk_tolerance'] != '未知':
            profile_completeness += 1
        if user_analysis['goal_analysis']['investment_goal'] != '未知':
            profile_completeness += 1
        if user_analysis['experience_analysis']['investment_experience'] != '未知':
            profile_completeness += 1
        
        if profile_completeness >= 2:
            factors.append('用户画像完整')
            profile_score = 0.8
        else:
            factors.append('用户画像需要完善')
            profile_score = 0.4
        
        # 历史数据可用性
        if history_analysis.get('history_available', False):
            factors.append('有投资历史数据')
            history_score = 0.9
        else:
            factors.append('无投资历史数据')
            history_score = 0.3
        
        # 综合个性化程度
        personalization_score = (profile_score * 0.6 + history_score * 0.4)
        
        if personalization_score >= 0.8:
            level = '高'
            description = '高度个性化，基于完整的用户画像和历史数据'
        elif personalization_score >= 0.6:
            level = '中'
            description = '中等个性化，基于基本用户信息'
        else:
            level = '低'
            description = '基础个性化，需要更多用户数据'
        
        return {
            'personalization_score': personalization_score,
            'personalization_level': level,
            'description': description,
            'factors': factors,
            'improvement_suggestions': [
                '完善用户风险偏好和投资目标',
                '记录投资历史以便分析',
                '定期更新用户画像'
            ] if personalization_score < 0.8 else ['个性化程度良好，继续保持']
        }

def main():
    """主函数"""
    print("🧠 毛毛AI增强系统 - 个性化策略优化器")
    print("=" * 60)
    print("📊 四维提升深化: 个性化策略优化")
    print("🎯 目标: 完善个性化策略推荐系统")
    print("⏰ 开始时间: 09:12 GMT+8")
    print("=" * 60)
    
    # 创建测试用户画像
    test_user_profile = {
        'risk_tolerance': '稳健型',
        'investment_goal': '增值',
        'investment_experience': '中级',
        'time_horizon': '中长期',
        'active_management': True,
        'diversification': True
    }
    
    # 创建测试投资历史
    test_investment_history = [
        {'symbol': '603039', 'buy_date': '2026-02-01', 'sell_date': '2026-03-01', 'profit': 1500},
        {'symbol': '000001', 'buy_date': '2026-02-15', 'sell_date': '2026-03-10', 'profit': -800},
        {'symbol': '600036', 'buy_date': '2026-01-20', 'sell_date': '2026-03-05', 'profit': 2200}
    ]
    
    # 创建测试市场条件
    test_market_conditions = {
        'market_trend': '震荡',
        'trend_strength': '中等',
        'trend_duration': '短期',
        'volatility': '中等',
        'market_sentiment': '中性',
        'confidence': 0.6
    }
    
    # 创建测试持仓
    test_portfolio = [
        {'symbol': '603039', 'industry': '软件开发', 'shares': 100, 'cost': 5000, 'current_value': 5720},
        {'symbol': '000001', 'industry': '银行', 'shares': 200, 'cost': 3000, 'current_value': 2800},
        {'symbol': '600036', 'industry': '银行', 'shares': 150, 'cost': 6000, 'current_value': 6300}
    ]
    
    # 创建个性化策略优化器
    print("\n👤 用户画像:")
    print(f"   风险偏好: {test_user_profile['risk_tolerance']}")
    print(f"   投资目标: {test_user_profile['investment_goal']}")
    print(f"   投资经验: {test_user_profile['investment_experience']}")
    
    optimizer = PersonalizedStrategyOptimizer(test_user_profile, test_investment_history)
    
    # 测试个性化策略推荐
    print("\n🎯 开始个性化策略推荐...")
    result = optimizer.recommend_strategies(test_market_conditions, test_portfolio)
    
    if result['status'] == 'success':
        print("\n✅ 个性化策略推荐成功!")
        print(f"   处理时间: {result['processing_time']}")
        print(f"   个性化程度: {result['personalization_level']['personalization_level']}")
        print(f"   推荐置信度: {result['confidence']['confidence_level']}")
        
        # 显示用户分析
        user_analysis = result['user_analysis']
        print(f"\n👤 用户分析:")
        print(f"   风险评分: {user_analysis['risk_analysis']['risk_score']}/100")
        print(f"   预期收益: {user_analysis['goal_analysis']['expected_return']}")
        print(f"   适合复杂度: {user_analysis['experience_analysis']['suitable_complexity']}")
        
        # 显示市场分析
        market_analysis = result['market_analysis']
        print(f"\n🌍 市场分析:")
        print(f"   市场状态: {market_analysis['market_state']}")
        print(f"   趋势方向: {market_analysis['trend_analysis']['trend']}")
        print(f"   机会水平: {market_analysis['opportunity_assessment']['opportunity_level']}")
        
        # 显示历史分析
        history_analysis = result['history_analysis']
        if history_analysis['history_available']:
            print(f"\n📊 历史分析:")
            summary = history_analysis['summary']
            print(f"   交易次数: {summary['total_trades']}")
            print(f"   成功率: {summary['success_rate']}")
            print(f"   投资风格: {history_analysis['style_analysis']['trading_style']}")
        
        # 显示持仓分析
        portfolio_analysis = result['portfolio_analysis']
        if portfolio_analysis['portfolio_available']:
            print(f"\n💼 持仓分析:")
            summary = portfolio_analysis['summary']
            print(f"   持仓数量: {summary['total_positions']}")
            print(f"   总收益率: {summary['profit_rate']}")
            print(f"   分散程度: {portfolio_analysis['diversification_analysis']['diversification_level']}")
        
        # 显示策略推荐
        print(f"\n🎯 个性化策略推荐 (Top 3):")
        recommendations = result['recommendations']
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['strategy_name']}")
            print(f"   推荐级别: {rec['recommendation_level']}")
            print(f"   成功概率: {rec['success_probability']}")
            print(f"   预期收益: {rec['expected_return']}")
            print(f"   风险等级: {rec['risk_level']}")
            print(f"   关键理由:")
            for reason in rec['key_reasons'][:2]:  # 只显示前2个理由
                print(f"     • {reason}")
        
        # 显示策略分析
        strategy_analysis = result['strategy_analysis']
        print(f"\n📊 策略分析总结:")
        print(f"   策略库总数: {strategy_analysis['total_strategies']}")
        print(f"   候选策略: {strategy_analysis['candidate_strategies']}")
        print(f"   推荐策略: {strategy_analysis['recommended_strategies']}")
        
    else:
        print(f"\n❌ 策略推荐失败: {result.get('error', '未知错误')}")
    
    print("\n" + "=" * 60)
    print("🎉 个性化策略优化完成!")
    print("   深度用户画像分析")
    print("   多维度策略匹配")
    print("   个性化推荐生成")
    print("   实施步骤和风险提示")
    print("=" * 60)

if __name__ == "__main__":
    main()