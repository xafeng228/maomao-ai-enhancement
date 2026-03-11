# 🏗️ 架构设计文档

## 🎯 设计目标

### 核心目标
1. **超越单一工具**：从 akshare-stock 的数据工具升级为全面AI投研助手
2. **智能决策支持**：提供完整的投资分析和建议，不只是数据
3. **持续学习进化**：基于反馈和经验的持续优化能力
4. **多代理协作**：专业分工，协同决策
5. **系统可扩展**：易于添加新功能和新数据源

### 设计原则
- **模块化设计**：功能分离，易于维护和扩展
- **松耦合架构**：组件间通过清晰接口通信
- **错误容忍**：优雅降级，部分故障不影响整体
- **性能优化**：实时响应，高效数据处理
- **用户中心**：个性化服务，优秀用户体验

---

## 🏛️ 整体架构

### 四层架构设计
```
┌─────────────────────────────────────────┐
│           用户交互层                    │
│  (Telegram/Web/API/CLI)                │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│           AI决策层                      │
│  (毛毛核心 - 协调和决策)                │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│        多代理协作层                     │
│  (6个专业代理协同工作)                  │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│          数据服务层                     │
│  (多数据源集成和处理)                   │
└─────────────────────────────────────────┘
```

### 数据流
```
用户请求 → AI决策层 → 意图识别 → 代理分配 → 数据获取 → 分析计算 → 结果融合 → 格式化输出 → 用户响应
```

---

## 🔧 详细组件设计

### 1. 用户交互层

#### 1.1 通信接口
```python
class CommunicationInterface:
    """通信接口基类"""
    
    def __init__(self, platform):
        self.platform = platform  # telegram, web, api, cli
        
    def receive_message(self) -> Message:
        """接收用户消息"""
        pass
        
    def send_response(self, response: Response):
        """发送响应"""
        pass
        
    def format_for_platform(self, content: Dict) -> str:
        """平台特定的格式化"""
        pass
```

#### 1.2 平台适配器
- **Telegram适配器**：紧凑文本，支持emoji和分段
- **Web适配器**：富文本，支持图表和交互
- **API适配器**：JSON格式，供第三方调用
- **CLI适配器**：命令行界面，适合开发者

### 2. AI决策层

#### 2.1 核心决策引擎
```python
class DecisionEngine:
    """决策引擎"""
    
    def __init__(self):
        self.memory = MemorySystem()
        self.learning = LearningSystem()
        self.agent_manager = AgentManager()
        
    def process_request(self, user_request: Request) -> Response:
        """处理用户请求"""
        # 1. 理解意图
        intent = self._understand_intent(user_request)
        
        # 2. 检索上下文
        context = self.memory.retrieve_context(user_request)
        
        # 3. 分配任务给代理
        task_assignment = self._assign_to_agents(intent, context)
        
        # 4. 协调代理工作
        agent_results = self.agent_manager.coordinate(task_assignment)
        
        # 5. 融合结果并决策
        decision = self._make_decision(agent_results, context)
        
        # 6. 学习并更新记忆
        self.learning.record_experience(user_request, decision)
        
        return decision
```

#### 2.2 意图理解系统
```python
class IntentUnderstanding:
    """意图理解系统"""
    
    def __init__(self):
        self.router = Router()
        self.context_analyzer = ContextAnalyzer()
        
    def understand(self, query: str, context: Context) -> Intent:
        """理解用户意图"""
        # 1. 基础意图识别
        base_intent = self.router.parse_query(query)
        
        # 2. 上下文增强
        enhanced_intent = self.context_analyzer.enhance(base_intent, context)
        
        # 3. 意图验证
        validated_intent = self._validate_intent(enhanced_intent)
        
        return validated_intent
```

### 3. 多代理协作层

#### 3.1 代理管理器
```python
class AgentManager:
    """代理管理器"""
    
    def __init__(self):
        self.agents = {
            'technical': TechnicalAgent(),
            'fundamental': FundamentalAgent(),
            'risk': RiskManagementAgent(),
            'sentiment': SentimentAnalysisAgent(),
            'macro': MacroAnalysisAgent(),
            'learning': LearningAgent(),
        }
        
    def coordinate(self, task_assignment: TaskAssignment) -> Dict[str, Any]:
        """协调代理工作"""
        results = {}
        
        # 并行执行任务
        with ThreadPoolExecutor() as executor:
            futures = {}
            for agent_name, task in task_assignment.tasks.items():
                if agent_name in self.agents:
                    future = executor.submit(
                        self.agents[agent_name].execute, task
                    )
                    futures[agent_name] = future
            
            # 收集结果
            for agent_name, future in futures.items():
                try:
                    results[agent_name] = future.result(timeout=30)
                except Exception as e:
                    results[agent_name] = {'error': str(e)}
        
        return results
```

#### 3.2 代理基类
```python
class BaseAgent(ABC):
    """代理基类"""
    
    def __init__(self, name: str, expertise: str):
        self.name = name
        self.expertise = expertise
        self.cache = CacheManager()
        
    @abstractmethod
    def execute(self, task: Task) -> Dict[str, Any]:
        """执行任务"""
        pass
        
    def get_data(self, data_request: DataRequest) -> Any:
        """获取数据（带缓存）"""
        cache_key = self._generate_cache_key(data_request)
        
        # 检查缓存
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # 获取新数据
        fresh_data = self._fetch_data(data_request)
        
        # 缓存数据
        self.cache.set(cache_key, fresh_data, ttl=300)  # 5分钟缓存
        
        return fresh_data
```

### 4. 数据服务层

#### 4.1 数据适配器模式
```python
class DataAdapter:
    """数据适配器基类"""
    
    def __init__(self, source_name: str):
        self.source_name = source_name
        
    @abstractmethod
    def fetch(self, request: DataRequest) -> Any:
        """获取数据"""
        pass
        
    @abstractmethod
    def transform(self, raw_data: Any) -> StandardizedData:
        """转换为标准格式"""
        pass

class AkshareAdapter(DataAdapter):
    """akshare数据适配器"""
    
    def __init__(self):
        super().__init__('akshare')
        import akshare as ak
        self.ak = ak
        
    def fetch(self, request: DataRequest) -> pd.DataFrame:
        """获取akshare数据"""
        if request.data_type == 'stock_kline':
            return self.ak.stock_zh_a_hist(**request.params)
        elif request.data_type == 'index_spot':
            return self.ak.stock_zh_index_spot()
        # ... 其他数据类型
        
    def transform(self, raw_data: pd.DataFrame) -> StandardizedData:
        """标准化akshare数据"""
        # 统一列名、数据类型、时间格式等
        pass
```

#### 4.2 数据融合引擎
```python
class DataFusionEngine:
    """数据融合引擎"""
    
    def __init__(self):
        self.adapters = {
            'akshare': AkshareAdapter(),
            'agent_reach': AgentReachAdapter(),
            'tavily': TavilyAdapter(),
            'qveris': QVerisAdapter(),
        }
        
    def get_integrated_data(self, request: IntegratedRequest) -> IntegratedData:
        """获取融合数据"""
        results = {}
        
        # 从多个数据源获取数据
        for source, adapter in self.adapters.items():
            if source in request.sources:
                try:
                    data = adapter.fetch(request.get_source_request(source))
                    transformed = adapter.transform(data)
                    results[source] = transformed
                except Exception as e:
                    results[source] = {'error': str(e)}
        
        # 数据融合
        fused_data = self._fuse_data(results)
        
        return fused_data
        
    def _fuse_data(self, source_data: Dict[str, Any]) -> IntegratedData:
        """融合多源数据"""
        # 1. 时间对齐
        # 2. 数据验证（交叉检查）
        # 3. 冲突解决（优先级、置信度）
        # 4. 数据补全（用其他源补充缺失数据）
        pass
```

---

## 🗄️ 数据架构

### 数据模型设计

#### 1. 股票数据模型
```python
@dataclass
class StockData:
    """股票数据模型"""
    symbol: str
    name: str
    current_price: float
    change_percent: float
    volume: int
    market_cap: float
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    roe: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
@dataclass
class TechnicalIndicators:
    """技术指标模型"""
    symbol: str
    ma5: float
    ma10: float
    ma20: float
    rsi: float
    macd: float
    bollinger_upper: float
    bollinger_lower: float
    timestamp: datetime
```

#### 2. 投资组合模型
```python
@dataclass
class Portfolio:
    """投资组合模型"""
    id: str
    name: str
    owner: str
    positions: List[Position]
    total_value: float
    cash_balance: float
    created_at: datetime
    updated_at: datetime
    
@dataclass
class Position:
    """持仓模型"""
    symbol: str
    quantity: int
    avg_cost: float
    current_price: float
    market_value: float
    profit_loss: float
    profit_loss_percent: float
    weight: float  # 在组合中的权重
```

#### 3. 决策记录模型
```python
@dataclass
class DecisionRecord:
    """决策记录模型"""
    id: str
    user_id: str
    query: str
    intent: str
    analysis_results: Dict[str, Any]
    decision: Decision
    reasoning: str
    timestamp: datetime
    outcome: Optional[Outcome] = None  # 后续补充结果
    learning_notes: Optional[str] = None
```

### 数据存储策略

#### 1. 缓存策略
```python
class CacheStrategy:
    """缓存策略"""
    
    TTL_CONFIG = {
        'realtime_price': 30,      # 30秒
        'kline_data': 300,         # 5分钟
        'financial_data': 3600,    # 1小时
        'stock_list': 86400,       # 1天
        'news_sentiment': 1800,    # 30分钟
    }
    
    def get_ttl(self, data_type: str) -> int:
        """获取缓存时间"""
        return self.TTL_CONFIG.get(data_type, 300)  # 默认5分钟
```

#### 2. 数据持久化
- **实时数据**：内存缓存 + Redis
- **历史数据**：SQLite/PostgreSQL
- **分析结果**：JSON文件 + 数据库
- **学习记录**：Markdown文件 + 数据库

---

## 🔄 工作流程

### 典型工作流程：智能选股

```python
# 1. 用户请求
request = Request(
    query="帮我筛选市盈率小于20，ROE大于15%的股票",
    user_id="user123",
    context=Context(risk_tolerance="medium", investment_horizon="medium")
)

# 2. 意图理解
intent = intent_understanding.understand(request.query, request.context)
# intent = {
#     'type': 'stock_screening',
#     'filters': {'max_pe': 20, 'min_roe': 15},
#     'top_n': 20
# }

# 3. 任务分配
task_assignment = TaskAssignment(
    tasks={
        'fundamental': FundamentalTask(filters=intent['filters']),
        'technical': TechnicalTask(symbols='all'),
        'risk': RiskAssessmentTask(risk_tolerance=request.context.risk_tolerance),
    }
)

# 4. 代理执行
results = agent_manager.coordinate(task_assignment)

# 5. 结果融合
screened_stocks = data_fusion_engine.fuse_screening_results(results)

# 6. 决策制定
decision = decision_engine.make_screening_decision(
    screened_stocks, 
    request.context
)

# 7. 响应生成
response = formatter.format_screening_response(decision)

# 8. 学习记录
learning_system.record_screening_experience(request, decision, response)
```

### 错误处理流程
```python
try:
    # 正常处理流程
    result = process_request(request)
except DataSourceError as e:
    # 数据源错误：使用缓存数据或备选数据源
    result = handle_data_source_error(e, request)
except AnalysisError as e:
    # 分析错误：简化分析或提供基础建议
    result = handle_analysis_error(e, request)
except TimeoutError as e:
    # 超时错误：返回部分结果或提示稍后重试
    result = handle_timeout_error(e, request)
except Exception as e:
    # 未知错误：记录错误，提供友好提示
    result = handle_unknown_error(e, request)
    learning_system.record_error(e, request)
```

---

## 📊 性能设计

### 1. 并发处理
```python
class ConcurrentProcessor:
    """并发处理器"""
    
    def process_multiple_stocks(self, symbols: List[str], 
                               analysis_func: Callable) -> Dict[str, Any]:
        """并发处理多只股票"""
        results = {}
        
        # 使用线程池并发处理
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_symbol = {
                executor.submit(analysis_func, symbol): symbol 
                for symbol in symbols
            }
            
            for future in as_completed(future_to_symbol):
                symbol = future_to_symbol[future]
                try:
                    results[symbol] = future.result(timeout=10)
                except Exception as e:
                    results[symbol] = {'error': str(e)}
        
        return results
```

### 2. 懒加载和缓存
```python
class LazyDataLoader:
    """懒加载数据"""
    
    def __init__(self, data_fetcher: Callable):
        self.data_fetcher = data_fetcher
        self._data = None
        self._loaded = False
        
    @property
    def data(self):
        """属性访问时加载数据"""
        if not self._loaded:
            self._data = self.data_fetcher()
            self._loaded = True
        return self._data
```

### 3. 增量更新
```python
class IncrementalUpdater:
    """增量更新器"""
    
    def update_stock_data(self, symbol: str, new_data: Dict):
        """增量更新股票数据"""
        # 1. 获取现有数据
        existing_data = self.get_existing_data(symbol)
        
        # 2. 合并新数据（只更新变化的部分）
        updated_data = self._merge_incremental(existing_data, new_data)
        
        # 3. 保存更新后的数据
        self.save_data(symbol, updated_data)
        
        # 4. 触发相关更新（如技术指标重新计算）
        self._trigger_dependent_updates(symbol, updated_data)
```

---

## 🔐 安全设计

### 1. 数据安全
```python
class DataSecurity:
    """数据安全"""
    
    def sanitize_input(self, user_input: str) -> str:
        """输入清洗"""
        # 移除危险字符
        sanitized = re.sub(r'[<>"\']', '', user_input)
        return sanitized
        
    def validate_symbol(self, symbol: str) -> bool:
        """验证股票代码"""
        # 检查格式
        if not re.match(r'^[0-9]{6}\.(SZ|SH)$', symbol):
            return False
        
        # 检查是否在允许的股票列表中
        return symbol in self.allowed_symbols
        
    def rate_limit(self, user_id: str, endpoint: str) -> bool:
        """速率限制"""
        key = f"{user_id}:{endpoint}"
        current = self.redis.incr(key)
        
        if current == 1:
            self.redis.expire(key, 60)  # 60秒窗口
            
        return current <= self.limit_config[endpoint]
```

### 2. API安全
- **认证**：API密钥 + 时间戳 + 签名
- **授权**：基于角色的访问控制
- **加密**：HTTPS传输，敏感数据加密存储
- **审计**：完整的操作日志

---

## 🧪 测试架构

### 1. 测试金字塔
```
        ┌─────────────────┐
        │    E2E测试      │  (10%)
        └─────────────────┘
                │
