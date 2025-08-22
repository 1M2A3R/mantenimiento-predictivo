# bot_telegram.py - Conecta al API separado
import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

class MaintenanceBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.api_url = "http://localhost:5001/simulate"  # URL del API
        
        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("simular", self.simulate_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🤖 Bot de Mantenimiento Predictivo activo!")
    
    async def simulate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            await update.message.reply_text("🔧 Conectando con simulador...")
            
            # Llama al API separado
            response = requests.post(self.api_url, json={
                'telegram_user': update.message.from_user.username,
                'equipo': 'motor_principal',
                'horas_uso': 500
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                mensaje = f"""
✅ *Simulación completada*

📊 *Resultados:*
• Condición: {data.get('condicion', 'N/A')}
• Vida útil: {data.get('vida_util', 'N/A')}
• Equipo: {data.get('equipo', 'N/A')}
• Horas uso: {data.get('horas_uso', 'N/A')}

🎯 *Recomendación:*
{data.get('recomendacion', 'N/A')}

👤 Usuario: @{data.get('usuario', 'anonimo')}
                """
                await update.message.reply_text(mensaje, parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Error conectando con el simulador")
                
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("✅ Bot activo y funcionando")

    def run(self):
        self.application.run_polling()

if __name__ == "__main__":
    bot = MaintenanceBot()
    bot.run()
