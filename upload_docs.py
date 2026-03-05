"""
upload_docs.py — Betmode Knowledge Uploader
=============================================
Run this script locally to upload Betmode company knowledge to Firebase.
The Slack bot will use this to answer employee questions automatically.

HOW TO RUN:
  1. Place firebase-credentials.json in this folder
  2. Run: python upload_docs.py

Run anytime to update the knowledge base — no need to redeploy the bot.
"""

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase-credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


# ══════════════════════════════════════════════════════════════════════════════
# BETMODE KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════════════════════

COMPANY_KNOWLEDGE = [

    {
        "topic": "About Betmode",
        "content": """
Betmode (betmode.io) is the world's most transparent crypto casino, established in July 2024.
We are revolutionizing the iGaming industry using Web3 technology to create a fully transparent,
trustless, and player-first experience.

Key differentiators:
- Trustless gameplay powered by blockchain — players can verify, not just trust
- Full on-chain transparency: bankrolls, odds, and outcomes are all visible and provable
- Near-instant crypto transactions with no intermediaries
- Global accessibility via crypto
- Non-custodial model available: players can keep funds in their own wallet (e.g. MetaMask)

Company behind Betmode:
- Legal entity: BlockReach Media LTD.
- Registered Address: AGORA BUSINESS CENTRE LEVEL 2, TRIQ IL-WIED TA' L-MSIDA, MSIDA, MSD 9020, Malta
- Registration No.: C 113317
- Website: https://betmode.io/
- License: Licensed and regulated by the Government of Anjouan under License No. ALSI-202411002-FI1

On-chain wallet addresses (public):
- Casino Bankroll Wallet: 0x0c532...c75DE
- Player Rewards Payout Wallet: 0xa31De...1D14

Contact:
- Support email: support@betmode.io
- Finance/invoices: finance@blockreachmedia.com
- Phone: +353 83 091 3271
- Director: Christian Gravina
        """
    },

    {
        "topic": "Restricted Countries",
        "content": """
The following countries are RESTRICTED — users from these countries cannot register or play on Betmode.
However, users CAN join Betmode by using a VPN:

Restricted countries:
- United States (USA)
- United Kingdom (UK)
- France
- Germany
- Netherlands
- Spain
- Austria
- Australia
- Curacao (as a jurisdiction)
- The island of Comoros itself
- All FATF (Financial Action Task Force) blacklisted countries
- All jurisdictions subject to UN sanctions

Note: Betmode is VPN friendly. Users from restricted countries may access the platform using a VPN,
but they do so at their own responsibility in accordance with their local laws.
        """
    },

    {
        "topic": "Affiliate Program & Commission Models",
        "content": """
Betmode runs an affiliate program for partners who refer players to the casino.

Affiliate platform (Scaleo):
- Affiliate registration / login: https://betmode.scaleo.app/signup/affiliate
- Brand information (logos, details): https://docs.google.com/spreadsheets/d/1dqywNHLr2QblFCgGeR6fQ3XRvkoJoC3DTUNp3KxaC7s/edit?usp=drive_link
- Marketing materials (banners, logos): https://drive.google.com/drive/folders/1g3MujoU7RMtJbML_uMRDpq-lf-26iIcV?usp=drive_link

Commission models available:
1. CPA (Cost Per Acquisition) — fixed payment per qualifying player
2. RevShare — percentage of revenue from player losses
3. Hybrid — combination of CPA + RevShare

Custom deals are negotiated with the Affiliate Manager.

KPI Requirements (flexible, reviewed monthly):
- No payment for duplicate accounts or self-excluded users
- CAP compliance: 10–30 FTDs during test period (paid up to 10 FTDs unless pre-approved for more)
- At least 50% of FTDs must make at least one repeat deposit
- Only players who place a real-money bet after depositing (WG1) qualify
- 30-day conversion window from registration to first deposit
- No payment for incentivized, motivated, or fraudulent traffic
- 30-day hold period applies if KPIs are not met
- Qualified traffic = total player deposits must be ≥70% of affiliate commission
- Baseline minimum deposit: 20 EUR per player for a conversion to qualify as a CPA

Payout info:
- Minimum payout threshold: $100
- Supported currency: USDC (ERC20)
- Commissions approved by the 6th of each month
- Payouts sent by the 12th of each month
        """
    },

    {
        "topic": "Company & Invoicing Details",
        "content": """
For invoices and payments, use the following details:

Company Name: BlockReach Media LTD.
Registered Address: AGORA BUSINESS CENTRE LEVEL 2, TRIQ IL-WIED TA' L-MSIDA, MSIDA, MSD 9020, Malta
Registration No.: C 113317
Email for invoices: finance@blockreachmedia.com
Payment: USDC wallet (ERC20) — affiliates must provide their own USDC wallet address
Person who signs the IO (Insertion Order): Director — Christian Gravina

Invoice requirements:
Full invoice requirements are here: https://docs.google.com/document/d/111FJonXirFvQ4wfcFWIKX6rqLRsCd4Q1eCNSTYTrvLQ/edit?tab=t.0

Key invoice rules:
- Must include date of issue, unique invoice number, date of delivery
- Must include supplier and customer full name and address
- Must include VAT identification numbers (supplier and customer)
- All amounts must be in fiat currency (crypto can be noted on the side)
- Must include taxable amount, VAT rate, VAT amount, and total payable
- For B2B services: must state "Reverse Charge" if applicable
- If VAT exempt: include reference to applicable EU VAT Directive provision
        """
    },

    {
        "topic": "Products & Games",
        "content": """
Betmode offers the following products:
- Slots (4,000+ games)
- Table Games (Blackjack, Roulette, Baccarat)
- Live Casino
- Classic Crypto Games
- Crash games
- Game Shows

Game providers:
Evolution Gaming, Pragmatic Play Live, Spinomenal, NetEnt, Hacksaw Gaming,
Million Games, Nolimit City, Spribe

Live dealer software: Evolution Gaming, Pragmatic Play Live, Spinomenal, NetEnt

Mobile:
- Mobile version: Yes (fully mobile optimized)
- Mobile app: No dedicated app currently

Languages supported: English (more languages coming soon)
        """
    },

    {
        "topic": "Bonuses & Promotions",
        "content": """
Current offers at Betmode:

Welcome Offer:
- Up to $100,000 on your first deposit

Ongoing Promotions:
- Instant Daily Rewards — settled on-chain
- Instant Rakeback — real-time return on each bet placed
- Weekly Race — $2,500 prize pool + 1,000 Free Spins

VIP:
- VIP transfers accepted (players can transfer their VIP status from other casinos)
- VIP Welcome Offer: contact affiliate manager for details
        """
    },

    {
        "topic": "Deposits & Withdrawals",
        "content": """
Deposits:
- Minimum deposit: $6 in crypto
- Supported cryptocurrencies: USDC, BTC, USDT, ETH, SOL, TRX, DOGE, BNB, ADA, BCH
- Supported payment solutions: USDC, Optimism, MetaMask, Rainbow, Coinbase, WalletConnect
- Deposits are near-instant

Withdrawals:
- Cashout time: Close to instant
- Maximum withdrawal: $300,000 per month / $10,000 per day
- Minimum withdrawal: $10 (or currency equivalent)
- No withdrawal commission if you wager (roll over) the deposit at least 1 time
- If deposit is not wagered: 8% fee applies (minimum $5)
- Winnings higher than bankroll amount are addressed and paid retroactively

KYC:
- No mandatory KYC by default
- Company reserves the right to request KYC documents for verification in specific cases
- KYC may be requested when cumulative deposits reach $10,000 USD or equivalent
        """
    },

    {
        "topic": "Support & Contact",
        "content": """
Customer support is available via:
- Email: support@betmode.io
- Discord: support ticket via Discord (preferred channel for complaints and queries)

Support languages: English, Swedish, Norwegian, Thai

Response times:
- General queries: within a few days
- Disputes: up to 28 days from receipt

Live chat: Not currently available — support is via email and Discord only.

For complaints/disputes:
- Must be submitted within 3 days of the event
- Contact Customer Service first — if unresolved, escalates to management
- Final option: arbitration
        """
    },

    {
        "topic": "Target CPA Prices by Country",
        "content": """
These are our internal target CPA (Cost Per Acquisition) prices per country and traffic type.
Use these as reference when evaluating affiliate deals.

Country | PPC    | SEO/ASO | FB iOS | FB Android
--------|--------|---------|--------|------------
CH      | $300   | $250    | $190   | $180
DE      | $300   | $250    | $190   | $180
AT      | $280   | $220    | $190   | $180
BE      | $250   | $200    | $170   | $160
FR      | $250   | $200    | $190   | $180
NO      | $300   | $250    | $190   | $180
IE      | $250   | $200    | $200   | $180
CA      | $300   | $250    | $200   | $190
AU      | $300   | $250    | $200   | $190
DK      | $300   | $250    | $190   | $180
SE      | $300   | $250    | $180   | $170
UK      | $300   | $250    | $180   | $170
RO      | $150   | $120    | $80    | $70
GR      | $150   | $120    | $120   | $100
PT      | $150   | $120    | $90    | $80
IT      | $180   | $150    | $140   | $130
CZ      | $150   | $120    | $120   | $100
PL      | $150   | $120    | $120   | $100

Traffic types: PPC = Pay Per Click, SEO-ASO = Organic/App Store, FB = Facebook Ads
        """
    },

    {
        "topic": "SEO & Media Partners",
        "content": """
Current SEO placement partners and their links:

- BitcoinChaser: https://bitcoinchaser.com/review/betmode/
- Casino Guru: https://casinoguru-en.com/betmode-io-casino-review
- BankrollMob: https://www.bankrollmob.com/casino-reviews.asp
- Chipy: https://chipy.com/casinos/betmode-casino-review
- Casinotics: https://casinotics.com/casinos/betmode-casino/
- BTCGOSU: https://www.btcgosu.com/review/betmode/
- AskGamblers: https://www.askgamblers.com/online-casinos/reviews/betmode-casino
- SlotsSpot: https://slotsspot.com/online-casinos/betmode-io/
- CryptoRunner: https://cryptorunner.com/best-bitcoin-casinos/
- BitcasinosRank: https://bitcasinosrank.com/casino/betmode-io/
- TheCasinoWizard: https://thecasinowizard.com/casinos/betmode-casino/
- CryptoGamble: https://cryptogamble.com/casino/reviews/betmode
- HiddenValleyCasinoResorts: https://hiddenvalleycasinoresorts.com/
- List.casino: https://list.casino/
- Lucklandia: https://lucklandia.com/
- SixSlots: https://www.sixslots.com/
- Ekstrapoint: https://ekstrapoint.com/
- CryptoCasinos: https://cryptocasinos.cc/
- CasinoWow: https://www.casinowow.com/top-crypto-casinos
        """
    },

    {
        "topic": "Streamer & Influencer Partnerships",
        "content": """
Betmode runs influencer and streamer partnership campaigns.

Standard partnership structure (4-week campaigns):
- Content platforms: Kick (streams), X (Twitter posts), Discord community updates
- Funded wallet provided per stream: $15,000
- Max withdrawal per stream: $5,000 (remaining stays in play or returns to Betmode)
- Performance review after 7 streams

Community leaderboard mechanic:
- $1 wagered = 1 point
- Minimum deposit: $25
- Campaign prize pool: $5,000 ($2,500 cash + 2,500 free spins)
- Cash prizes: 1st $750 | 2nd $500 | 3rd $350 | 4th $250 | 5th $200 | 6th–10th $90 each

For partnership proposals, contact: mattias@betmode.io
        """
    },

    {
        "topic": "Terms & Conditions",
        "content": """
Last updated: 2026-01-28
Full T&C apply to all users of betmode.io.

LEGAL ENTITY:
- Company: ONCHAIN Technologies Ltd
- Registered in Autonomous Island of Anjouan, Union of Comoros
- Company number: 15816
- License: ALSI-202411002-FI1 (Computer Gaming Licensing Act 007 of 2005)
- Governing law: Anjouan, Union of Comoros

PLAYER ELIGIBILITY:
- Must be 18+ (or legal gambling age in your jurisdiction)
- Must be a resident in a jurisdiction where gambling is legal
- Cannot use VPN/proxy to mask real location
- Cannot be a resident of a restricted country
- Employees of the Company, licensees, subsidiaries, and their immediate family members are NOT allowed to use the Service for real money without prior consent from the Director or CEO

ACCOUNT RULES:
- One account per person only — multiple accounts = immediate closure
- Account cannot be sold, transferred, or pledged to another person
- Must provide accurate personal information at all times
- Password must be kept confidential — player is responsible for all account activity
- To close your account: email the Customer Support Department

KYC (Know Your Customer):
- KYC may be requested at any time
- Mandatory when cumulative deposits reach $10,000 USD or equivalent
- Documents required: government-issued photo ID + proof of address

DEPOSITS:
- All deposits must come from an account registered in the player's own name
- Funds from criminal/illegal activities must not be deposited
- Company is not a financial institution — uses third-party payment processors
- If you deposit via credit card, account is only credited upon authorisation approval
- Do not attempt to reverse or chargeback payments — this results in account termination and legal action
- $50 administration fee per chargeback/reversal

WITHDRAWALS:
- Minimum withdrawal: $10 (or currency equivalent)
- Maximum withdrawal: $300,000 per month / $10,000 per day
- No withdrawal fee if deposit was wagered at least 1x
- If deposit was NOT wagered: 8% fee applies (minimum $5)
- Winnings higher than bankroll are addressed and paid retroactively
- Withdrawals must go back to the original payment method used for deposit
- KYC/identity verification may be required before withdrawal is approved

BONUSES:
- By entering a bonus code during deposit, player agrees to bonus terms
- Each bonus has its own specific terms

SELF-EXCLUSION & RESPONSIBLE GAMING:
- To self-exclude: send an email from your Registered Email Address to Customer Support requesting SELF-EXCLUDE
- Self-exclusion takes effect within 24 hours
- Account will be disabled until further notice — player cannot login
- Responsible gaming tools available: self-exclusion, self-limiting features
- Full Responsible Gaming Policy available on the website

ERRORS & SYSTEM MALFUNCTIONS:
- In the event of system error or malfunction, all affected bets are void
- Players must report errors immediately upon discovery
- Company reserves the right to void bets placed at incorrect odds
- Company can recover overpaid amounts from player accounts

RULES OF PLAY:
- Match results are final after 72 hours — no queries after that period
- Disputes on bet settlements must be lodged within 3 days
- Minimum and maximum wager amounts are set by the Company and subject to change
- Transactions are final once completed — cannot be changed
- If a match is suspended and not resumed within 72 hours, all wagers are refunded

COMMUNICATIONS:
- All formal communications must go through Customer Support via Discord ticket or Registered Email Address
- All communications must be in English

DISPUTES & COMPLAINTS:
- Contact Customer Service first (via Discord or email)
- If unresolved, escalates to management
- Final option: arbitration
- Disputes must be lodged within 3 days of the event
- Jurisdiction: Union of Comoros Anjouan courts

FRAUD:
- Company will seek criminal and contractual sanctions against any player involved in fraud
- Winnings are withheld when fraud is suspected

PROHIBITED ACTIVITIES (players cannot):
- Use the service if under 18
- Access from restricted countries
- Use VPN/proxy to mask location
- Manipulate markets or game outcomes
- Create accounts by automated means
- Attempt to hack or reverse-engineer the service
- Post spam, illegal content, or unsolicited advertising
- Transfer funds between player accounts
- Sell or transfer their account to third parties
        """
    },

]


# ── Upload Function ───────────────────────────────────────────────────────────

def upload_knowledge():
    print(f"\n📤 Uploading {len(COMPANY_KNOWLEDGE)} topics to Firebase...\n")
    for item in COMPANY_KNOWLEDGE:
        topic_id = item["topic"].lower().replace(" ", "_").replace("/", "_").replace("&", "and")
        db.collection("knowledge_base").document(topic_id).set({
            "topic": item["topic"],
            "content": item["content"].strip(),
        })
        print(f"  ✅ {item['topic']}")
    print(f"\n🎉 Done! {len(COMPANY_KNOWLEDGE)} topics uploaded. Your Slack bot is ready.")


def list_knowledge():
    print("\n📚 Topics currently in Firebase:\n")
    docs = db.collection("knowledge_base").stream()
    count = 0
    for doc in docs:
        data = doc.to_dict()
        print(f"  • {data.get('topic', doc.id)}")
        count += 1
    if count == 0:
        print("  (empty)")
    print()


if __name__ == "__main__":
    upload_knowledge()
    print("\n--- Verifying ---")
    list_knowledge()
