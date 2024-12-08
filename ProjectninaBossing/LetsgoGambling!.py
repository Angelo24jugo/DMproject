import random
import time
from colorama import init, Fore, Style
import winsound
import os

# Initialize colorama for colored output
init()


class SlotMachine:
    def __init__(self):
        self.symbols = ['🍒', '🍊', '🍋', '💎', '7️⃣', '🎰']
        self.balance = 1000  # Starting balance
        self.sound_dir = os.path.join(os.path.dirname(__file__), 'sounds')

        # Create sounds directory if it doesn't exist
        if not os.path.exists(self.sound_dir):
            os.makedirs(self.sound_dir)

    def play_sound(self, sound_file):
        try:
            sound_path = os.path.join(self.sound_dir, sound_file)
            if os.path.exists(sound_path):
                winsound.PlaySound(sound_path, winsound.SND_FILENAME)
            else:
                # Use different beep frequencies for different events
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
        self.play_sound('win.wav')

    def play_jackpot_sound(self):
        self.play_sound('jackpot.wav')

    def play_lose_sound(self):
        self.play_sound('lose.wav')

    def play_out_of_balance_sound(self):
        self.play_sound('sorry.wav')  # New method for out of balance sound

    def play_spin_sound(self):
        self.play_sound('spin.wav')

    def display_balance(self):
        print(f"\n{Fore.YELLOW}Current Balance: ${self.balance}{Style.RESET_ALL}")

    def get_bet(self):
        while True:
            try:
                bet = int(input(f"{Fore.CYAN}Enter your bet amount (minimum $1): ${Style.RESET_ALL}"))
                if 1 <= bet <= self.balance:
                    return bet
                else:
                    print(f"{Fore.RED}Invalid bet! Must be between $1 and ${self.balance}{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number!{Style.RESET_ALL}")

    def spin(self):
        print(f"\n{Fore.GREEN}Spinning...{Style.RESET_ALL}")
        self.play_spin_sound()
        time.sleep(1)
        return [random.choice(self.symbols) for _ in range(3)]

    def check_win(self, result, bet):
        print(f"\n{Fore.MAGENTA}[{' '.join(result)}]{Style.RESET_ALL}")

        if all(symbol == result[0] for symbol in result):  # All symbols match
            if result[0] == '💎':
                winnings = bet * 10
                print(f"{Fore.GREEN}JACKPOT! All Diamonds! You won ${winnings}!{Style.RESET_ALL}")
                self.play_jackpot_sound()
            else:
                winnings = bet * 5
                print(f"{Fore.GREEN}Winner! Triple match! You won ${winnings}!{Style.RESET_ALL}")
                self.play_win_sound()
            return winnings

        elif result.count(result[0]) == 2 or result.count(result[1]) == 2:  # Two matching symbols
            winnings = bet * 2
            print(f"{Fore.GREEN}Nice! Double match! You won ${winnings}!{Style.RESET_ALL}")
            self.play_win_sound()
            return winnings

        else:
            print(f"{Fore.RED}Sorry, you lost ${bet}!{Style.RESET_ALL}")
            self.play_lose_sound()
            return -bet

    def play(self):
        print(f"\n{Fore.YELLOW}Welcome to the Python Slot Machine!{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Note: For custom sounds, place these .wav files in the 'sounds' folder:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}- win.wav: for winning sounds{Style.RESET_ALL}")
        print(f"{Fore.CYAN}- jackpot.wav: for jackpot wins{Style.RESET_ALL}")
        print(f"{Fore.CYAN}- lose.wav: for losing sounds{Style.RESET_ALL}")
        print(f"{Fore.CYAN}- spin.wav: for spinning sound{Style.RESET_ALL}")
        print(f"{Fore.CYAN}- sorry.wav: for out of balance sound{Style.RESET_ALL}")
        print(f"{Fore.CYAN}If sound files are not found, the game will use beep sounds{Style.RESET_ALL}")

        while self.balance > 0:
            self.display_balance()

            bet = self.get_bet()
            result = self.spin()
            self.balance += self.check_win(result, bet)

            if self.balance <= 0:
                print(f"\n{Fore.RED}Game Over! You're out of money!{Style.RESET_ALL}")
                self.play_out_of_balance_sound()  # Play "out of balance" sound
                break

            play_again = input(f"\n{Fore.CYAN}Would you like to play again? (y/n): {Style.RESET_ALL}").lower()
            if play_again != 'y':
                print(f"\n{Fore.YELLOW}Thanks for playing! You ended with ${self.balance}!{Style.RESET_ALL}")
                break

if __name__ == "__main__":
    game = SlotMachine()
    game.play()