# =============================================
# Blue Collar Budget
# Stupid Simple Paycheck Calculator
# =============================================

import json
import os
from datetime import datetime

DATA_FILE = "budget_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    data = load_data()
    current_month = datetime.now().strftime("%Y-%m")
    
    print("=====================================")
    print("     BLUE COLLAR BUDGET")
    print("   Stupid Simple Edition")
    print("=====================================\n")

    while True:
        print("\nWhat would you like to do?")
        print("1. Calculate new paycheck")
        print("2. View previous paychecks")
        print("3. Monthly Overview")
        print("4. Add Monthly Expense")
        print("5. Big Purchase Calculator")
        print("6. Start New Month (Reset)")
        print("7. Exit")
        
        choice = input("\nEnter 1-7: ").strip()

        if choice == "1":
            rate = float(input("\nHourly rate? $"))
            total_hours = float(input("Total hours worked this pay period? "))

            if total_hours <= 80:
                regular_hours = total_hours
                ot_hours = 0
            else:
                regular_hours = 80
                ot_hours = total_hours - 80

            regular_pay = regular_hours * rate
            ot_pay = ot_hours * rate * 1.5
            gross_pay = regular_pay + ot_pay

            fed_rate = float(input("Federal tax %: ")) / 100
            state_rate = float(input("State tax %: ")) / 100
            retirement_percent = float(input("401k %: ") or 0) / 100

            federal_tax = gross_pay * fed_rate
            state_tax = gross_pay * state_rate
            retirement = gross_pay * retirement_percent
            insurance = float(input("Insurance: $") or 0)
            other = float(input("Other deductions: $") or 0)

            total_deductions = federal_tax + state_tax + retirement + insurance + other
            net_pay = gross_pay - total_deductions

            print("\n" + "="*55)
            print("                PAYCHECK SUMMARY")
            print("="*55)
            print(f"Gross Pay: ${gross_pay:,.2f}")
            print(f"Take Home: ${net_pay:,.2f}")
            print("="*55)

            data.setdefault("paychecks", []).append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "month": current_month,
                "gross": round(gross_pay, 2),
                "net": round(net_pay, 2)
            })
            save_data(data)

        elif choice == "2":
            paychecks = data.get("paychecks", [])
            if not paychecks:
                print("No previous paychecks saved yet.")
            else:
                print(f"\nLast {min(10, len(paychecks))} paychecks:")
                for i, p in enumerate(paychecks[-10:], 1):
                    print(f"{i}. {p.get('date', 'Unknown')} | Gross: ${p['gross']:,.2f} | Take Home: ${p['net']:,.2f}")

        elif choice == "3":
            paychecks = [p for p in data.get("paychecks", []) if p.get("month") == current_month]
            expenses = data.get("expenses", [])

            total_gross = sum(p['gross'] for p in paychecks)
            total_net = sum(p['net'] for p in paychecks)
            total_expenses = sum(e['amount'] for e in expenses)

            print("\n" + "="*60)
            print(f"           MONTHLY OVERVIEW - {current_month}")
            print("="*60)
            print(f"Total Gross Pay     : ${total_gross:,.2f}")
            print(f"Total Take Home     : ${total_net:,.2f}")
            print(f"Total Expenses      : ${total_expenses:,.2f}")
            print("-" * 60)
            print(f"ESTIMATED REMAINING : ${total_net - total_expenses:,.2f}")
            print("="*60)

        elif choice == "4":
            print("\n--- Add Monthly Expense ---")
            name = input("Expense name (e.g. Truck Payment): ")
            amount = float(input("Amount: $"))
            
            data.setdefault("expenses", []).append({
                "name": name,
                "amount": round(amount, 2),
                "date": datetime.now().strftime("%Y-%m-%d")
            })
            save_data(data)
            print(f"✅ Added ${amount:,.2f} for {name}")

        elif choice == "5":
            print("\n--- Big Purchase Calculator ---")
            item = input("What are you trying to buy? (e.g. New Rifle): ")
            cost = float(input("How much does it cost? $"))

            paychecks = [p for p in data.get("paychecks", []) if p.get("month") == current_month]
            expenses = data.get("expenses", [])
            
            total_net = sum(p['net'] for p in paychecks)
            total_expenses = sum(e['amount'] for e in expenses)
            remaining = total_net - total_expenses

            if remaining >= cost:
                print(f"\n✅ You can afford the {item} with your current remaining money.")
            else:
                needed = cost - remaining
                hourly_rate = float(input("What's your overtime hourly rate? $"))
                ot_needed = needed / (hourly_rate * 1.5)
                print(f"\nYou need an extra ${needed:,.2f}.")
                print(f"You'll need about {ot_needed:.1f} hours of overtime to afford the {item}.")

        elif choice == "6":
            confirm = input("Start a new month? This will clear this month's data. (y/n): ").lower()
            if confirm == 'y':
                data["paychecks"] = [p for p in data.get("paychecks", []) if p.get("month") != current_month]
                data["expenses"] = []
                save_data(data)
                print("✅ New month started.")

        elif choice == "7":
            print("See you next paycheck, brother.")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()