from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
from io import BytesIO
import yfinance as yf
import matplotlib.pyplot as plt

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

# async def stock_chart(update: Update, context: CallbackContext) -> None:
#     try:
#         # Get the stock ticker from the user's message
#         ticker = context.args[0].upper()

#         # Retrieve stock data using yfinance
#         stock_data = yf.Ticker(ticker)
#         history = stock_data.history(period="1y")

#         # Check if historical data is available
#         if history.empty:
#             await update.message.reply_text(f"No historical data available for {ticker}")
#             return

#         # Generate a simple line chart using Matplotlib
#         plt.figure(figsize=(10, 6))
#         plt.plot(history.index, history['Close'], label='Closing Price')
#         plt.title(f"Stock Price Chart for {ticker}")
#         plt.xlabel("Date")
#         plt.ylabel("Closing Price")
#         plt.legend()

#         # Save the chart as an image in memory
#         image_stream = BytesIO()
#         plt.savefig(image_stream, format='png')
#         image_stream.seek(0)

#         # Send the image to the user
#         await update.message.reply_photo(photo=image_stream)

#     except IndexError:
#         await update.message.reply_text("Please provide a valid stock ticker. Usage: /stock <ticker>")
#     except Exception as e:
#         await update.message.reply_text(f"An error occurred: {str(e)}")
#     finally:
#         # Close the Matplotlib plot to avoid memory leaks
#         plt.close()

async def stock(update: Update, context: CallbackContext) -> None:
    try:
        # Get the stock ticker from the user's message
        ticker = context.args[0].upper()

        # Retrieve stock data using yfinance
        stock_data = yf.Ticker(ticker)
        info = stock_data.info

        print(info)

        # Function to format numbers in crore with commas
        def format_in_crore(number):
            return "{:,.2f} Cr".format(number / 1e7)
            

        # Customize the information you want to display
        response = f"Stock Analysis for {ticker}:\n"
        response += f"Company: {info.get('longName', 'N/A')}\n"
        response += f"Current Price: {info.get('currentPrice', 'N/A')}\n"
        response += f"Previous Close: {info.get('regularMarketPreviousClose', 'N/A')}\n"
        response += f"Open: {info.get('regularMarketOpen', 'N/A')}\n"
        response += f"Market Cap: {format_in_crore(info.get('marketCap', 0))}\n"
        response += f"P/E Ratio (TTM): {info.get('trailingPE', 'N/A')}\n"
        response += f"Return on Equity (ROE): {info.get('returnOnEquity', 'N/A')}\n"
        response += f"Dividend Yield: {format(info.get('dividendYield', 'N/A') * 100, '.2f')}\n"
        response += f"Book Value: {info.get('bookValue', 'N/A')}\n"

         # Check if profit, loss, and revenue are available
        if 'profitMargins' in info:
            response += f"Profit Margins: {info.get('profitMargins', 'N/A')}\n"

        if 'grossMargins' in info:
            response += f"Gross Margins: {info.get('grossMargins', 'N/A')}\n"

        if 'totalRevenue' in info:
            response += f"Total Revenue: {format_in_crore(info.get('totalRevenue', 0))}\n"

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
    #app.add_handler(CommandHandler("stock_chart", stock_chart))

    print('Polling...')
    app.run_polling(poll_interval=5)
    app.idle()
