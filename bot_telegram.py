# bot_telegram.py - Archivo SEPARADO para el bot
import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class MaintenanceBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        if not self.token or self.token == 'tu_token_de_telegram_aqui':
            print("❌ ERROR: Configura TELEGRAM_TOKEN en el archivo .env")
            print("💡 Obtenlo de @BotFather en Telegram")
            return
        
        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()
        print("✅ Bot de Telegram configurado correctamente")
    
    def setup_handlers(self):
        """Configura los comandos del bot"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("simular", self.simulate_command))
        self.application.add_handler(CommandHandler("estado", self.status_command))
        self.application.add_handler(MessageHandler(filters.TEXT, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        welcome_text = """
        🤖 *Bot de Mantenimiento Predictivo*
        
        ¡Hola! Soy tu asistente de mantenimiento predictivo.
        
        📋 *Comandos disponibles:*
        /start - Muestra este mensaje
        /simular - Ejecuta una simulación
        /estado - Estado del sistema
        /help - Ayuda
        
        ¿En qué puedo ayudarte hoy?
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """
        🆘 *Ayuda - Comandos disponibles*
        
        /simular - Ejecuta simulación de mantenimiento
        /estado - Muestra el estado del sistema
        /help - Muestra esta ayuda
        
        Ejemplo: /simular
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def simulate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Ejecuta una simulación llamando a tu API Flask"""
        try:
            await update.message.reply_text("🔧 Iniciando simulación...")
            
            # Llama a tu propia API Flask para hacer la simulación
            response = requests.post('http://localhost:5000/simulate', json={
                'equipo': 'motor_principal',
                'horas_uso': 500,
                'telegram_user': update.message.from_user.username
            })
            
            if response.status_code == 200:
                result = response.json()
                await update.message.reply_text(
                    f"✅ *Simulación completada*\n\n"
                    f"📊 Resultados:\n"
                    f"• Condición: {result.get('condicion', 'N/A')}\n"
                    f"• Vida útil: {result.get('vida_util', 'N/A')}\n"
                    f"• Recomendación: {result.get('recomendacion', 'N/A')}\n\n"
                    f"🔄 Realizado por: @{update.message.from_user.username}",
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text("❌ Error en la simulación")
                
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Muestra el estado del sistema"""
        status_text = """
        📈 *Estado del Sistema*
        
        🟢 Aplicación Flask: Activa
        🤖 Bot Telegram: Activo
        📊 Simulaciones: Listas
        
        Todo funciona correctamente 👍
        """
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja mensajes de texto"""
        user_message = update.message.text.lower()
        
        if 'hola' in user_message:
            await update.message.reply_text("¡Hola! 👋 ¿En qué puedo ayudarte?")
        elif 'simular' in user_message:
            await self.simulate_command(update, context)
        elif 'estado' in user_message:
            await self.status_command(update, context)
        else:
            await update.message.reply_text(
                "🤔 No entendí. Usa /help para ver comandos"
            )
    
    def run(self):
        """Inicia el bot"""
        print("🤖 Iniciando bot de Telegram...")
        self.application.run_polling()

# Ejecutar solo si se llama directamente
if __name__ == "__main__":
    bot = MaintenanceBot()
    if hasattr(bot, 'application'):
        bot.run()
