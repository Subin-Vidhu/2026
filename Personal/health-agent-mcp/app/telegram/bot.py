import logging
import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from app.mcp_client.orchestrator import HealthAgentOrchestrator
from app.config import get_settings
from app.database import SessionLocal, User, WearableData
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
settings = get_settings()


class HealthAgentBot:
    """Telegram bot for Personal Health Agent."""
    
    def __init__(self, orchestrator: HealthAgentOrchestrator):
        self.orchestrator = orchestrator
        self.app = None
    
    def setup(self):
        """Setup bot with handlers."""
        self.app = Application.builder().token(settings.telegram_bot_token).build()
        
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("stats", self.stats_command))
        self.app.add_handler(CommandHandler("goals", self.goals_command))
        
        # Callback query handler for buttons
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Message handler for general queries
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        logger.info("Telegram bot setup complete")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        telegram_id = update.effective_user.id
        user_name = update.effective_user.first_name or "there"
        
        # Check if user exists in database
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            
            if not user:
                # Create demo user (in production, you'd have a registration flow)
                user = User(
                    telegram_id=telegram_id,
                    name=user_name,
                    age=30,  # Default
                    gender="not_specified"
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                logger.info(f"Created new user: {user_name} (telegram_id: {telegram_id})")

            # Seed demo wearable data if none exists for this user
            data_count = db.query(WearableData).filter(WearableData.user_id == user.id).count()
            if data_count == 0:
                self._seed_demo_wearable_data(db, user.id)
                logger.info(f"Seeded demo wearable data for user_id={user.id}")
        finally:
            db.close()
        
        keyboard = [
            [InlineKeyboardButton("📊 Analyze My Data", callback_data='mode_analyze')],
            [InlineKeyboardButton("🩺 Ask Health Question", callback_data='mode_medical')],
            [InlineKeyboardButton("💪 Health Coaching", callback_data='mode_coach')],
            [InlineKeyboardButton("ℹ️ Help", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = f"""👋 **Welcome to your Personal Health Agent, {user_name}!**

I'm your AI-powered health companion with three specialized agents:

📊 **Data Science Agent**
Analyze your health trends and patterns

🩺 **Domain Expert Agent**  
Get medical knowledge and insights

💪 **Health Coach Agent**
Receive personalized coaching and motivation

**How to use:**
• Choose a mode below, or
• Just chat naturally about your health!

*Note: This is for educational purposes only, not medical advice.*
"""
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_text = """🤖 **Personal Health Agent Help**

**Available Commands:**
/start - Restart the bot
/help - Show this help message
/stats - Get your weekly health summary
/goals - View your active health goals

**Example Queries:**

📊 **Data Analysis:**
• "Has my sleep improved this month?"
• "Show my heart rate trends"
• "Compare my activity levels"

🩺 **Medical Questions:**
• "What does my resting heart rate mean?"
• "Is my cholesterol level normal?"
• "Should I be concerned about my HRV?"

💪 **Health Coaching:**
• "Help me sleep better"
• "I want to be more active"
• "How can I stay motivated?"

**Tips:**
✓ Be specific in your questions
✓ Include time ranges when relevant
✓ Ask follow-up questions anytime

*All data is demo data for testing purposes.*
"""
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command - show weekly summary."""
        telegram_id = update.effective_user.id
        user = self._get_user_by_telegram_id(telegram_id)
        
        if not user:
            await update.message.reply_text("User not found. Please /start first.")
            return
        
        await update.message.chat.send_action("typing")
        
        # Query weekly summary via orchestrator
        response = await self.orchestrator.process_query(
            user_id=user.id,
            message="Show me my weekly health summary with all metrics"
        )
        
        await update.message.reply_text(f"📊 **Weekly Health Summary**\n\n{response['response']}", parse_mode='Markdown')
    
    async def goals_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /goals command - show active goals."""
        telegram_id = update.effective_user.id
        user = self._get_user_by_telegram_id(telegram_id)
        
        if not user:
            await update.message.reply_text("User not found. Please /start first.")
            return
        
        await update.message.chat.send_action("typing")
        
        # Get goals via orchestrator
        response = await self.orchestrator.process_query(
            user_id=user.id,
            message="What are my current health goals and progress?"
        )
        
        await update.message.reply_text(f"🎯 **Your Health Goals**\n\n{response['response']}", parse_mode='Markdown')
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks."""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'help':
            help_text = "Just ask me anything about your health! I'll route your question to the right agent."
            await query.message.reply_text(help_text)
        
        elif query.data.startswith('mode_'):
            mode = query.data.replace('mode_', '')
            mode_messages = {
                'analyze': "📊 Great! Ask me anything about your health data trends.",
                'medical': "🩺 Sure! What health question do you have?",
                'coach': "💪 I'm here to help! What would you like to work on?"
            }
            await query.message.reply_text(mode_messages.get(mode, "How can I help?"))
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle user messages."""
        telegram_id = update.effective_user.id
        message = update.message.text
        
        # Get user from database
        user = self._get_user_by_telegram_id(telegram_id)
        
        if not user:
            await update.message.reply_text(
                "Please start the bot first with /start"
            )
            return
        
        # Show typing indicator
        await update.message.chat.send_action("typing")
        
        # Get conversation history from context
        if 'history' not in context.user_data:
            context.user_data['history'] = []
        
        try:
            # Process query through orchestrator
            response = await self.orchestrator.process_query(
                user_id=user.id,
                message=message,
                conversation_history=context.user_data['history']
            )
            
            # Add to history
            context.user_data['history'].append({
                'role': 'user',
                'content': message
            })
            context.user_data['history'].append({
                'role': 'assistant',
                'content': response['response']
            })
            
            # Keep history manageable (last 20 messages)
            if len(context.user_data['history']) > 20:
                context.user_data['history'] = context.user_data['history'][-20:]
            
            # Send response
            agent_emoji = {
                "Data Science": "📊",
                "Domain Expert": "🩺",
                "Health Coach": "💪",
                "Multi-Agent": "🤖"
            }
            emoji = agent_emoji.get(response['agent'], "🤖")
            
            response_text = f"{emoji} **{response['agent']} Agent**\n\n{response['response']}"
            
            await update.message.reply_text(response_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await update.message.reply_text(
                "Sorry, I encountered an error processing your request. Please try again."
            )
    
    def _get_user_by_telegram_id(self, telegram_id: int):
        """Get user by telegram ID."""
        db = SessionLocal()
        try:
            return db.query(User).filter(User.telegram_id == telegram_id).first()
        finally:
            db.close()

    def _seed_demo_wearable_data(self, db: SessionLocal, user_id: int, days: int = 30) -> None:
        """Seed basic wearable data for a user if none exists."""
        hr_base = 72
        steps_base = 6500
        sleep_base = 6.8
        hrv_base = 50

        for day in range(days):
            date = datetime.now() - timedelta(days=days - day)
            # 10% missing data
            if random.random() < 0.10:
                continue

            wearable = WearableData(
                user_id=user_id,
                date=date,
                heart_rate=int(hr_base + random.gauss(0, 6)),
                steps=int(max(0, steps_base + random.gauss(0, 1200))),
                sleep_hours=round(max(4, min(10, sleep_base + random.gauss(0, 0.9))), 1),
                hrv=int(max(20, hrv_base + random.gauss(0, 8))),
                calories=int(1800 + random.gauss(0, 250)),
                active_minutes=int(max(0, (steps_base / 100) + random.gauss(0, 15)))
            )
            db.add(wearable)

        db.commit()
    
    async def start_polling(self):
        """Start the bot."""
        logger.info("Starting Telegram bot polling...")
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()
        logger.info("Telegram bot is running")
    
    async def stop(self):
        """Stop the bot."""
        logger.info("Stopping Telegram bot...")
        await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()
        logger.info("Telegram bot stopped")
