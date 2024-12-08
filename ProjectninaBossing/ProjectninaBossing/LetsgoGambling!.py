#Part 1: Game Initialization and Setup (Lines 1-37)
import random
import time
import winsound
import os

class SlotMachine:
    def __init__(self):
        self.symbols = ['🍒', '🍊', '🍋', '💎', '7️⃣', '🎰']
        self.balance = 1000  # Starting balance
        self.sound_dir = os.path.join(os.path.dirname(__file__), 'sounds')
        
        # Initialize statistics
        self.total_plays = 0
        self.total_wins = 0
        self.biggest_win = 0
        self.total_money_won = 0
        self.total_money_lost = 0

        # Add simple probability system
        self.symbol_chances = {
            '💎': 1,    # Super rare!
            '7️⃣': 2,    # Pretty rare
            '🎰': 3,    # Kind of rare
            '🍒': 4,    # Normal
            '🍊': 5,    # Common
            '🍋': 5     # Common
        }
        self.losing_streak = 0  # Track losing streak
        
        # Add symbol frequency tracking
        self.symbol_counts = {
            '🍒': 0, '🍊': 0, '🍋': 0,
            '💎': 0, '7️⃣': 0, '🎰': 0
        }

        #Part 2: Sound System (Lines 38-77)
        # Create sounds directory if it doesn't exist
        if not os.path.exists(self.sound_dir):
            os.makedirs(self.sound_dir)

    def play_sound(self, sound_file):
        try:
            sound_path = os.path.join(self.sound_dir, sound_file)
            if os.path.exists(sound_path):
                winsound.PlaySound(sound_path, winsound.SND_FILENAME)
            else:
                # Beep sounds for different events
                if 'win' in sound_file:
                    winsound.Beep(1000, 500)  # Higher pitch for winning
                elif 'jackpot' in sound_file:
                    for _ in range(3):  # Multiple beeps for jackpot
                        winsound.Beep(1500, 200)
                        time.sleep(0.1)
                elif 'spin' in sound_file:
                    winsound.Beep(800, 200)  # Medium pitch for spin
                else:
                    winsound.Beep(500, 500)  # Lower pitch for losing
        except:
            winsound.Beep(1000, 500)  # Default beep if something goes wrong

    def play_win_sound(self):
        self.play_sound('win.wav')  # Modified to your new sound

    def play_jackpot_sound(self):
        self.play_sound('jackpot.wav')

    def play_lose_sound(self):
        self.play_sound('lose.wav')

    def play_out_of_balance_sound(self):
        self.play_sound('sorry.wav')

    def play_spin_sound(self):
        self.play_sound('spin.wav')

    # Part 3: Game Display and Chances (Lines 78-114)
    def show_chances(self):
        print("\n=== YOUR CHANCES TO WIN ===")
        print("Diamond (💎): Very Rare!")
        print("Seven (7️⃣): Rare")
        print("Slot Machine (🎰): Uncommon")
        print("Other symbols: Normal")
        
        print("\nWinning combinations:")
        print("3 Diamonds = SUPER JACKPOT! (10x bet)")
        print("3 same symbols = Big win! (5x bet)")
        print("2 same symbols = Small win! (2x bet)")
        print("=" * 40)  # Add a line of 40 equal signs as a separator
        
        # Show current bonus from losing streak
        if self.losing_streak > 5:
            print(f"\nLosing Streak Bonus: Active! ({self.losing_streak} losses)")
            print("Your chance for rare symbols is increased!")
            
        # Add symbol frequency display
        if self.total_plays > 0:
            print("\n=== SYMBOL FREQUENCY ===")
            for symbol in self.symbols:
                percentage = (self.symbol_counts[symbol] / (self.total_plays * 3)) * 100
                print(f"{symbol} appeared: {self.symbol_counts[symbol]} times ({percentage:.1f}%)")

    def spin(self):
        print("\nSpinning...")
        self.play_spin_sound()
        time.sleep(1)
        
        # Make weighted random choice based on symbol chances
        weighted_symbols = []
        for symbol, chance in self.symbol_chances.items():
            weighted_symbols.extend([symbol] * chance)
        
        result = [random.choice(weighted_symbols) for _ in range(3)]
        
        # Update symbol frequencies
        # Part 4: Betting and Win Logic (Lines 115-172)
        for symbol in result:
            self.symbol_counts[symbol] += 1
            
        return result

    def display_balance(self):
        print(f"\nCurrent Balance: ${self.balance}")

    def get_bet(self):
        while True:
            try:
                bet = int(input("Enter your bet amount (minimum $1): $"))
                if 1 <= bet <= self.balance:
                    return bet
                else:
                    print(f"Invalid bet! Must be between $1 and ${self.balance}")
            except ValueError:
                print("Please enter a valid number!")

    def check_win(self, result, bet):
        print(f"\n[{' '.join(result)}]")
        self.total_plays += 1

        if all(symbol == result[0] for symbol in result):  # All symbols match
            if result[0] == '💎':
                winnings = bet * 10
                print(f"JACKPOT! All Diamonds! You won ${winnings}!")
                self.play_jackpot_sound()
            else:
                winnings = bet * 5
                print(f"Winner! Triple match! You won ${winnings}!")
                self.play_win_sound()
            self.total_wins += 1
            self.total_money_won += winnings
            self.biggest_win = max(self.biggest_win, winnings)
            self.losing_streak = 0  # Reset losing streak on win
            return winnings

        elif result.count(result[0]) == 2 or result.count(result[1]) == 2:  # Two matching symbols
            winnings = bet * 2
            print(f"Nice! Double match! You won ${winnings}!")
            self.play_win_sound()
            self.total_wins += 1
            self.total_money_won += winnings
            self.biggest_win = max(self.biggest_win, winnings)
            self.losing_streak = 0  # Reset losing streak on win
            return winnings

        else:
            print(f"Sorry, you lost ${bet}!")
            self.play_lose_sound()
            self.total_money_lost += bet
            self.losing_streak += 1  # Increase losing streak
            
            # Add bonus chance for rare symbols after many losses
            # Part 5: Statistics and Game Flow (Lines 173-218)
            if self.losing_streak > 5:
                print("Your luck is increasing!")
                self.symbol_chances['💎'] = 2  # Temporarily increase diamond chance
            else:
                self.symbol_chances['💎'] = 1  # Reset to normal
            
            return -bet

    def display_stats(self):
        win_rate = (self.total_wins / self.total_plays * 100) if self.total_plays > 0 else 0
        print("\n=== GAME STATISTICS ===")
        print(f"Total Plays: {self.total_plays}")
        print(f"Total Wins: {self.total_wins}")
        print(f"Win Rate: {win_rate:.2f}%")
        print(f"Biggest Win: ${self.biggest_win}")
        print(f"Total Money Won: ${self.total_money_won}")
        print(f"Total Money Lost: ${self.total_money_lost}")
        print("====================")

    def play(self):
        print("\nWelcome to the Python Slot Machine!")


        while self.balance > 0:
            self.display_balance()
            self.display_stats()  # Show statistics before each play
            self.show_chances()   # Show current chances to win

            bet = self.get_bet()
            result = self.spin()
            self.balance += self.check_win(result, bet)

            if self.balance <= 0:
                print("\nGame Over! You're out of money!")
                self.play_out_of_balance_sound()
                # Display final statistics
                self.display_stats()
                break

            play_again = input("\nWould you like to play again? (y/n): ").lower()
            if play_again != 'y':
                print(f"\nThanks for playing! You ended with ${self.balance}!")
                # Display final statistics
                self.display_stats()
                break

if __name__ == "__main__":
    game = SlotMachine()
    game.play()