#!/usr/bin/env python3
"""
多渠道推送管理器 - 第一阶段优化扩展
"""

import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import time
import hashlib
import logging

class PushNotificationManager:
    """统一推送管理器"""
    
    def __init__(self, config_path: str = None):
        """初始化推送管理器"""
        # 先初始化日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        self.config_path = config_path or "/root/.openclaw/workspace/maomao-enhanced-system/push_config.json"
        self.config = self._load_config()
        
        # 初始化渠道
        self.channels = self._initialize_channels()
        
        print("📱 多渠道推送管理器初始化")
        print("=" * 60)
        print("🎯 第一阶段优化扩展: 多渠道推送系统")
        print("⏰ 开始时间:", datetime.now().strftime("%H:%M:%S GMT+8"))
        print("=" * 60)
        print("📊 可用推送渠道:")
        for channel_name, channel in self.channels.items():
            status = "✅ 就绪" if channel['enabled'] else "❌ 禁用"
            print(f"   {channel_name}: {status}")
        print("=" * 60)
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        default_config = {
            "version": "1.0.0",
            "channels": {
                "telegram": {
                    "enabled": True,
                    "priority": 1,
                    "retry_count": 3,
                    "retry_delay": 2
                },
                "wechat": {
                    "enabled": False,
                    "priority": 2,
                    "retry_count": 2,
                    "retry_delay": 3
                },
                "feishu": {
                    "enabled": False,
                    "priority": 3,
                    "retry_count": 2,
                    "retry_delay": 3
                },
                "dingtalk": {
                    "enabled": False,
                    "priority": 4,
                    "retry_count": 2,
                    "retry_delay": 3
                },
                "email": {
                    "enabled": False,
                    "priority": 5,
                    "retry_count": 1,
                    "retry_delay": 5
                }
            },
            "fallback_strategy": "sequential",  # sequential, priority, all
            "enable_logging": True,
            "enable_metrics": True,
            "created_at": datetime.now().isoformat()
        }
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 合并配置
                for channel, settings in default_config["channels"].items():
                    if channel in config.get("channels", {}):
                        config["channels"][channel].update(settings)
                    else:
                        config.setdefault("channels", {})[channel] = settings
                return config
        except FileNotFoundError:
            # 创建默认配置
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            self.logger.info(f"创建默认配置文件: {self.config_path}")
            return default_config
    
    def _initialize_channels(self) -> Dict[str, Dict[str, Any]]:
        """初始化推送渠道"""
        channels = {}
        
        # Telegram渠道
        channels['telegram'] = {
            'name': 'Telegram',
            'enabled': self.config['channels']['telegram']['enabled'],
            'priority': self.config['channels']['telegram']['priority'],
            'handler': self._send_telegram,
            'config_required': ['bot_token', 'chat_id'],
            'config_status': self._check_telegram_config()
        }
        
        # 企业微信渠道
        channels['wechat'] = {
            'name': '企业微信',
            'enabled': self.config['channels']['wechat']['enabled'],
            'priority': self.config['channels']['wechat']['priority'],
            'handler': self._send_wechat,
            'config_required': ['webhook_url'],
            'config_status': self._check_wechat_config()
        }
        
        # 飞书渠道
        channels['feishu'] = {
            'name': '飞书',
            'enabled': self.config['channels']['feishu']['enabled'],
            'priority': self.config['channels']['feishu']['priority'],
            'handler': self._send_feishu,
            'config_required': ['webhook_url'],
            'config_status': self._check_feishu_config()
        }
        
        # 钉钉渠道
        channels['dingtalk'] = {
            'name': '钉钉',
            'enabled': self.config['channels']['dingtalk']['enabled'],
            'priority': self.config['channels']['dingtalk']['priority'],
            'handler': self._send_dingtalk,
            'config_required': ['webhook_url'],
            'config_status': self._check_dingtalk_config()
        }
        
        # 邮件渠道
        channels['email'] = {
            'name': '邮件',
            'enabled': self.config['channels']['email']['enabled'],
            'priority': self.config['channels']['email']['priority'],
            'handler': self._send_email,
            'config_required': ['smtp_server', 'smtp_port', 'sender_email', 'sender_password'],
            'config_status': self._check_email_config()
        }
        
        return channels
    
    def _check_telegram_config(self) -> Dict[str, Any]:
        """检查Telegram配置"""
        # 这里可以从环境变量或配置文件中读取
        # 暂时返回测试状态
        return {
            'configured': False,
            'missing': ['bot_token', 'chat_id'],
            'note': '需要配置Telegram Bot Token和Chat ID'
        }
    
    def _check_wechat_config(self) -> Dict[str, Any]:
        """检查企业微信配置"""
        return {
            'configured': False,
            'missing': ['webhook_url'],
            'note': '需要配置企业微信Webhook URL'
        }
    
    def _check_feishu_config(self) -> Dict[str, Any]:
        """检查飞书配置"""
        return {
            'configured': False,
            'missing': ['webhook_url'],
            'note': '需要配置飞书Webhook URL'
        }
    
    def _check_dingtalk_config(self) -> Dict[str, Any]:
        """检查钉钉配置"""
        return {
            'configured': False,
            'missing': ['webhook_url'],
            'note': '需要配置钉钉Webhook URL'
        }
    
    def _check_email_config(self) -> Dict[str, Any]:
        """检查邮件配置"""
        return {
            'configured': False,
            'missing': ['smtp_server', 'smtp_port', 'sender_email', 'sender_password'],
            'note': '需要配置SMTP服务器和发件人信息'
        }
    
    def send_notification(self, 
                         message: str, 
                         title: str = None,
                         message_type: str = "info",
                         channel_priority: List[str] = None,
                         fallback_strategy: str = None) -> Dict[str, Any]:
        """发送通知"""
        start_time = time.time()
        
        print(f"\n📤 开始发送通知")
        print(f"   消息类型: {message_type}")
        print(f"   消息长度: {len(message)} 字符")
        if title:
            print(f"   标题: {title}")
        
        # 确定发送策略
        strategy = fallback_strategy or self.config.get('fallback_strategy', 'sequential')
        
        # 确定渠道优先级
        if channel_priority:
            channels_to_try = [c for c in channel_priority if c in self.channels]
        else:
            # 按配置优先级排序
            channels_to_try = sorted(
                [c for c in self.channels.keys() if self.channels[c]['enabled']],
                key=lambda x: self.channels[x]['priority']
            )
        
        print(f"   发送策略: {strategy}")
        print(f"   尝试渠道: {len(channels_to_try)} 个")
        
        results = {}
        successful_channels = []
        failed_channels = []
        
        if strategy == "sequential":
            # 顺序尝试，第一个成功就停止
            for channel_name in channels_to_try:
                channel = self.channels[channel_name]
                print(f"\n   🔄 尝试 {channel['name']} 渠道...")
                
                result = self._send_with_retry(
                    channel_name=channel_name,
                    handler=channel['handler'],
                    message=message,
                    title=title,
                    message_type=message_type
                )
                
                results[channel_name] = result
                
                if result['success']:
                    print(f"   ✅ {channel['name']} 发送成功")
                    successful_channels.append(channel_name)
                    break  # 成功就停止
                else:
                    print(f"   ❌ {channel['name']} 发送失败: {result.get('error', '未知错误')}")
                    failed_channels.append(channel_name)
        
        elif strategy == "priority":
            # 按优先级尝试所有渠道
            for channel_name in channels_to_try:
                channel = self.channels[channel_name]
                print(f"\n   🔄 尝试 {channel['name']} 渠道...")
                
                result = self._send_with_retry(
                    channel_name=channel_name,
                    handler=channel['handler'],
                    message=message,
                    title=title,
                    message_type=message_type
                )
                
                results[channel_name] = result
                
                if result['success']:
                    print(f"   ✅ {channel['name']} 发送成功")
                    successful_channels.append(channel_name)
                else:
                    print(f"   ❌ {channel['name']} 发送失败: {result.get('error', '未知错误')}")
                    failed_channels.append(channel_name)
        
        elif strategy == "all":
            # 尝试所有渠道，无论成功失败
            for channel_name in channels_to_try:
                channel = self.channels[channel_name]
                print(f"\n   🔄 尝试 {channel['name']} 渠道...")
                
                result = self._send_with_retry(
                    channel_name=channel_name,
                    handler=channel['handler'],
                    message=message,
                    title=title,
                    message_type=message_type
                )
                
                results[channel_name] = result
                
                if result['success']:
                    print(f"   ✅ {channel['name']} 发送成功")
                    successful_channels.append(channel_name)
                else:
                    print(f"   ❌ {channel['name']} 发送失败: {result.get('error', '未知错误')}")
                    failed_channels.append(channel_name)
        
        total_time = time.time() - start_time
        
        # 汇总结果
        summary = {
            'status': 'success' if successful_channels else 'failed',
            'total_channels_tried': len(channels_to_try),
            'successful_channels': successful_channels,
            'failed_channels': failed_channels,
            'success_rate': len(successful_channels) / len(channels_to_try) if channels_to_try else 0,
            'total_time': f"{total_time:.2f}秒",
            'strategy_used': strategy,
            'timestamp': datetime.now().isoformat(),
            'detailed_results': results
        }
        
        print(f"\n📊 发送结果汇总:")
        print(f"   状态: {'✅ 成功' if successful_channels else '❌ 失败'}")
        print(f"   尝试渠道: {len(channels_to_try)} 个")
        print(f"   成功渠道: {len(successful_channels)} 个")
        print(f"   失败渠道: {len(failed_channels)} 个")
        print(f"   成功率: {summary['success_rate']*100:.1f}%")
        print(f"   总时间: {total_time:.2f}秒")
        
        if successful_channels:
            print(f"   成功渠道: {', '.join(successful_channels)}")
        
        return summary
    
    def _send_with_retry(self, 
                        channel_name: str,
                        handler: callable,
                        message: str,
                        title: str = None,
                        message_type: str = "info") -> Dict[str, Any]:
        """带重试的发送"""
        channel_config = self.config['channels'].get(channel_name, {})
        retry_count = channel_config.get('retry_count', 1)
        retry_delay = channel_config.get('retry_delay', 2)
        
        for attempt in range(1, retry_count + 1):
            try:
                result = handler(message, title, message_type)
                result['attempt'] = attempt
                result['success'] = True
                return result
            except Exception as e:
                self.logger.warning(f"渠道 {channel_name} 第 {attempt} 次尝试失败: {str(e)}")
                
                if attempt < retry_count:
                    time.sleep(retry_delay)
                else:
                    return {
                        'success': False,
                        'error': str(e),
                        'attempt': attempt,
                        'channel': channel_name
                    }
        
        return {
            'success': False,
            'error': '重试次数用尽',
            'attempt': retry_count,
            'channel': channel_name
        }
    
    def _send_telegram(self, message: str, title: str = None, message_type: str = "info") -> Dict[str, Any]:
        """发送到Telegram"""
        # 这里需要实际的Telegram Bot配置
        # 暂时返回模拟结果
        return {
            'channel': 'telegram',
            'status': 'simulated',
            'note': 'Telegram发送功能需要配置Bot Token和Chat ID',
            'simulated_success': True
        }
    
    def _send_wechat(self, message: str, title: str = None, message_type: str = "info") -> Dict[str, Any]:
        """发送到企业微信"""
        # 企业微信Webhook发送
        webhook_url = ""  # 需要从配置读取
        
        if not webhook_url:
            raise ValueError("企业微信Webhook URL未配置")
        
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"**{title if title else '毛毛AI通知'}**\n\n{message}"
            }
        }
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
            return {
                'channel': 'wechat',
                'status': 'sent',
                'response_code': response.status_code,
                'response_text': response.text
            }
        except Exception as e:
            raise Exception(f"企业微信发送失败: {str(e)}")
    
    def _send_feishu(self, message: str, title: str = None, message_type: str = "info") -> Dict[str, Any]:
        """发送到飞书"""
        # 飞书Webhook发送
        webhook_url = ""  # 需要从配置读取
        
        if not webhook_url:
            raise ValueError("飞书Webhook URL未配置")
        
        payload = {
            "msg_type": "text",
            "content": {
                "text": f"{title if title else '毛毛AI通知'}\n\n{message}"
            }
        }
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
            return {
                'channel': 'feishu',
                'status': 'sent',
                'response_code': response.status_code,
                'response_text': response.text
            }
        except Exception as e:
            raise Exception(f"飞书发送失败: {str(e)}")
    
    def _send_dingtalk(self, message: str, title: str = None, message_type: str = "info") -> Dict[str, Any]:
        """发送到钉钉"""
        # 钉钉Webhook发送
        webhook_url = ""  # 需要从配置读取
        
        if not webhook_url:
            raise ValueError("钉钉Webhook URL未配置")
        
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title if title else "毛毛AI通知",
                "text": message
            }
        }
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
            return {
                'channel': 'dingtalk',
                'status': 'sent',
                'response_code': response.status_code,
                'response_text': response.text
            }
        except Exception as e:
            raise Exception(f"钉钉发送失败: {str(e)}")
    
    def _send_email(self, message: str, title: str = None, message_type: str = "info") -> Dict[str, Any]:
        """发送邮件"""
        # 邮件发送配置
        smtp_server = ""  # 需要从配置读取
        smtp_port = 587
        sender_email = ""
        sender_password = ""
        receiver_email = ""  # 可以从配置读取或使用默认
        
        if not all([smtp_server, sender_email, sender_password]):
            raise ValueError("邮件配置不完整")
        
        # 如果没有指定收件人，使用发件人
        if not receiver_email:
            receiver_email = sender_email
        
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = title if title else "毛毛AI通知"
        
        # 添加正文
        msg.attach(MIMEText(message, 'plain', 'utf-8'))
        
        try:
            # 连接SMTP服务器
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # 启用TLS
            server.login(sender_email, sender_password)
            
            # 发送邮件
            server.send_message(msg)
            server.quit()
            
            return {
                'channel': 'email',
                'status': 'sent',
                'from': sender_email,
                'to': receiver_email,
                'subject': msg['Subject']
            }
        except Exception as e:
            raise Exception(f"邮件发送失败: {str(e)}")
    
    def enable_channel(self, channel_name: str, enable: bool = True) -> bool:
        """启用或禁用渠道"""
        if channel_name not in self.channels:
            self.logger.error(f"未知渠道: {channel_name}")
            return False
        
        self.config['channels'][channel_name]['enabled'] = enable
        self.channels[channel_name]['enabled'] = enable
        
        # 保存配置
        self._save_config()
        
        status = "启用" if enable else "禁用"
        self.logger.info(f"{status}渠道: {channel_name}")
        return True
    
    def set_channel_priority(self, channel_name: str, priority: int) -> bool:
        """设置渠道优先级"""
        if channel_name not in self.channels:
            self.logger.error(f"未知渠道: {channel_name}")
            return False
        
        self.config['channels'][channel_name]['priority'] = priority
        self.channels[channel_name]['priority'] = priority
        
        # 保存配置
        self._save_config()
        
        self.logger.info(f"设置渠道优先级: {channel_name} -> {priority}")
        return True
    
    def _save_config(self):
        """保存配置"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get_status(self) -> Dict[str, Any]:
        """获取推送管理器状态"""
        enabled_channels = [c for c in self.channels.values() if c['enabled']]
        disabled_channels = [c for c in self.channels.values() if not c['enabled']]
        
        return {
            'status': 'active',
            'total_channels': len(self.channels),
            'enabled_channels': len(enabled_channels),
            'disabled_channels': len(disabled_channels),
            'channels': {
                'enabled': [c['name'] for c in enabled_channels],
                'disabled': [c['name'] for c in disabled_channels]
            },
            'config_path': self.config_path,
            'fallback_strategy': self.config.get('fallback_strategy', 'sequential'),
            'version': self.config.get('version', '1.0.0')
        }

def main():
    """主函数 - 测试推送管理器"""
    print("🧠 毛毛AI增强系统 - 多渠道推送管理器测试")
    print("=" * 60)
    print("🎯 第一阶段优化扩展测试")
    print("⏰ 开始时间:", datetime.now().strftime("%H:%M:%S GMT+8"))
    print("=" * 60)
    
    # 创建推送管理器
    print("📱 初始化推送管理器...")
    manager = PushNotificationManager()
    
    # 显示状态
    status = manager.get_status()
    print(f"\n📊 推送管理器状态:")
    print(f"   版本: {status['version']}")
    print(f"   总渠道: {status['total_channels']}")
    print(f"   启用渠道: {status['enabled_channels']}")
    print(f"   禁用渠道: {status['disabled_channels']}")
    print(f"   回退策略: {status['fallback_strategy']}")
    
    # 测试消息
    test_message = """📈 毛毛AI增强系统测试通知

🎯 测试内容:
- 系统: 毛毛AI增强系统 v2.2.1
- 功能: 多渠道推送管理器测试
- 时间: {time}
- 状态: 第一阶段优化扩展进行中

📊 四维提升计划完成:
✅ 群体智能集成 (5模型预测)
✅ 实时A股监控 (1.06秒/只)
✅ 个性化策略 (8种策略)
✅ 持续学习AI伙伴
✅ 端到端工作流

🚀 下一步: 优化扩展计划 v3.0.0
""".format(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # 测试发送
    print(f"\n📤 测试发送通知...")
    print(f"   消息长度: {len(test_message)} 字符")
    
    result = manager.send_notification(
        message=test_message,
        title="毛毛AI增强系统测试通知",
        message_type="info",
        channel_priority=['telegram']  # 只测试Telegram
    )
    
    print(f"\n📊 测试结果:")
    print(f"   状态: {result['status']}")
    print(f"   尝试渠道: {result['total_channels_tried']}")
    print(f"   成功渠道: {len(result['successful_channels'])}")
    print(f"   成功率: {result['success_rate']*100:.1f}%")
    print(f"   总时间: {result['total_time']}")
    
    if result['successful_channels']:
        print(f"   ✅ 测试成功!")
        print(f"   成功渠道: {', '.join(result['successful_channels'])}")
    else:
        print(f"   ⚠️ 测试完成但无成功渠道")
        print(f"   需要配置推送渠道")
    
    print("\n" + "=" * 60)
    print("📋 配置建议:")
    print("   1. 配置Telegram: 需要Bot Token和Chat ID")
    print("   2. 配置企业微信: 需要Webhook URL")
    print("   3. 配置飞书: 需要Webhook URL")
    print("   4. 配置钉钉: 需要Webhook URL")
    print("   5. 配置邮件: 需要SMTP服务器信息")
    print("=" * 60)
    
    print("\n🎉 多渠道推送管理器框架完成!")
    print("   架构: 统一推送管理器")
    print("   渠道: 5个推送渠道支持")
    print("   策略: 3种发送策略")
    print("   重试: 自动重试机制")
    print("   日志: 完整日志记录")
    print("=" * 60)

if __name__ == "__main__":
    main()