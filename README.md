# Superintent Auto Bot

🔗 **[Join Superintent AI Mission](https://mission.superintent.ai/?referralCode=LZ3v477zNF)**

Automated bot for daily check-ins on the Superintent.AI platform to consistently collect points.

## ✨ Features

- ✅ Auto login using Ethereum wallet private key
- ✅ Auto daily check-in to earn points
- ✅ Multiple accounts support
- ✅ Proxy support (optional)
- ✅ Check-in streak tracking
- ✅ Display total points and referral count
- ✅ Auto cycle every 24 hours
- ✅ Cloudflare clearance support
- ✅ Colorful console output with WIB timestamp

## 📋 Requirements

- Python 3.7 or higher
- Ethereum wallet with private key
- Stable internet connection

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/febriyan9346/Superintent-Auto-Bot.git
cd Superintent-Auto-Bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create the required configuration files:

### accounts.txt
Insert your Ethereum wallet private keys (one per line):
```
0xYourPrivateKey1
0xYourPrivateKey2
0xYourPrivateKey3
```

### proxy.txt (Optional)
Supported proxy formats:
```
http://username:password@ip:port
http://ip:port
socks5://username:password@ip:port
```

## 💻 How to Use

1. Run the bot:
```bash
python bot.py
```

2. Select operation mode:
   - **Option 1**: Run with proxy
   - **Option 2**: Run without proxy

3. The bot will automatically:
   - Login to each account
   - Perform daily check-in
   - Display statistics (points, referrals, streak)
   - Cycle again every 24 hours

## 📊 Console Output

The bot will display the following information for each account:
- Account number and proxy being used
- Login status
- Check-in results and reward points
- Current check-in streak
- Total points and referral count
- Countdown to next cycle

## ⚙️ Configuration

## 🔒 Security

- ⚠️ **NEVER** share your private keys with anyone
- Keep your `accounts.txt` file secure
- Do not commit `accounts.txt` to public repositories
- Use `.gitignore` to protect sensitive files

## 🛠️ Troubleshooting

### Login Failed
- Ensure private key is valid and wallet has access
- Check internet connection
- If using proxy, ensure proxy is active

### Check-in Failed
- You may have already checked in today
- Wait for the next cycle (24 hours)

## 📝 Notes

- Bot will cycle automatically every 24 hours
- Check-in can only be done once per day per account
- Streak will increase with consistent daily check-ins
- Points will be credited automatically after successful check-in

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork this repository
2. Create a new feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

## ⚖️ Disclaimer

This bot is created for educational purposes and personal automation. Use wisely and in accordance with Superintent.AI's Terms of Service. The developer is not responsible for any misuse of this bot.

## 📞 Support

If you encounter problems or have questions:
- Create an Issue on GitHub
- Join the Superintent.AI community

## 📜 License

MIT License - see the [LICENSE](LICENSE) file for complete details.

---

**Made with ❤️ by FEBRIYAN**

⭐ Don't forget to star this repository if it's useful!

🔗 **[Register Superintent.AI Now](https://mission.superintent.ai/?referralCode=LZ3v477zNF)**
