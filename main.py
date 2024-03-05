from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import yfinance as yf

TOKEN = '6729416197:AAFqmCy-nvI6n6clB7yeSlYXGNY8LzTfcps'

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Welcome to Stock Market Analysis Bot! Use /stock <ticker> to get stock information.')

async def help_command(update: Update, context: CallbackContext) -> None:
    help_message = (
        "Welcome to Stock Market Analysis Bot!\n\n"
        "Available Commands:\n"
        "/start - Start the bot and get a welcome message.\n"
        "/help - Get information about how to use the bot and the available commands.\n"
        "/stock <ticker> - Get stock market analysis for the specified ticker."
    )
    await update.message.reply_text(help_message)

async def stock(update: Update, context: CallbackContext) -> None:
    try:
        # Get the stock ticker from the user's message
        ticker = context.args[0].upper()

        # Retrieve stock data using yfinance
        stock_data = yf.Ticker(ticker)
        info = stock_data.info

        # Customize the information you want to display
        response = f"Stock Analysis for {ticker}:\n"
        response += f"Company: {info.get('longName', 'N/A')}\n"
        response += f"Current Price: {info.get('currentPrice', 'N/A')}\n"
        response += f"Previous Close: {info.get('regularMarketPreviousClose', 'N/A')}\n"
        response += f"Open: {info.get('regularMarketOpen', 'N/A')}\n"

        # Send the response back to the user
        await update.message.reply_text(response)
    except IndexError:
        await update.message.reply_text("Please provide a valid stock ticker. Usage: /stock <ticker>")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

if __name__ == '__main__':
 
    # Telegram bot setup
    app = Application.builder().token(TOKEN).build()

    #Declaring the commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stock", stock))

    print('Polling...')
    app.run_polling(poll_interval=5)
