import random
import time
import matplotlib.pyplot as plt
import pandas as pd

def roll_dice():
    """Roll three dice and return their values as a tuple."""
    time.sleep(1) # Simulate dice rolling delay
    return tuple(random.randint(1, 6) for _ in range(3))

def display_scores(scores):
    """Display the current scores of all players."""
    print("\nCurrent Scores:")
    for player, score in scores.items():
        print(f"{player}: {score} points")
    print()

def tuple_out(dice):
    """Check if all three dice have the same value."""
    return len(set(dice)) == 1

def fixed_dice(dice):
    """Identify dice that are fixed (appear twice)."""
    counts = {num: dice.count(num) for num in set(dice)}
    return [num for num, count in counts.items() if count == 2]

def play_turn(player):
    """Handle a single player's turn."""
    print(f"\n{player}'s turn!")
    start_time = time.process_time()

    dice = roll_dice()
    print(f"Initial roll: {dice}")

    while True:
        if tuple_out(dice):
            print("Tuple out! You score 0 points this turn.")
            elapsed_time = time.process_time() - start_time
            print(f"Turn duration: {elapsed_time:.2f} seconds")
            return 0, elapsed_time
        
        fixed = fixed_dice(dice)
        if fixed:
            print(f"Fixed dice: {fixed}")
        else:
            print("No fixed dice.")

        re_roll = input("Would you like to re-roll non-fixed dice? (y/n): ").lower()
        if re_roll != 'y':
            break

        dice = tuple(num if num in fixed else random.randint(1, 6) for num in dice)
        print(f"Re-roll result: {dice}")

    score = sum(dice)
    elapsed_time = time.process_time() - start_time
    print(f"Turn duration: {elapsed_time:.2f} seconds")
    print(f"{player} scores {score} points this turn.")
    return score, elapsed_time

def visualize_scores(score_data):
    """Visualize scores over rounds using Matplotlib."""
    df = pd.DataFrame(score_data)
    df.plot(x="Round", y=list(df.columns[1:]), kind="line", marker="o")
    plt.title("Player Scores Over Rounds")
    plt.xlabel("Round")
    plt.ylabel("Scores")
    plt.legend(title="Players")
    plt.grid(True)
    plt.show()

def main():
    print("Welcome to the Tuple Out Dice Game!")
    num_players = int(input("Enter the number of players: "))
    players = [input(f"Enter player {i+1}'s name: ") for i in range(num_players)]
    target_score = int(input("Enter the target score to win: "))

    scores = {player: 0 for player in players}
    turn_durations = []
    round_data = {"Round": []}
    for player in players:
        round_data[player] = []

        round_number = 0
        while max(scores.values()) < target_score:
            round_number += 1
            print(f"\n--- Round {round_number} ---")
            round_data["Round"].append(round_number)

            for player in players:
                score, duration = play_turn(player)
                scores[player] += score
                turn_durations.append((player, duration))
                round_data[player].append(scores[player])

            display_scores(scores)
            visualize_scores(round_data) # Update visualization after each round

        winner = max(scores, key=scores.get)
        print(f"\nCongratulations, {winner}! You won the game with {scores[winner]} points. ")

        # Save results to a CSV file
        df = pd.DataFrame(turn_durations, columns=["Player", "Duration"])
        df.to_csv("player_turn_durations.csv", index=False)
        print("Turn durations saved to 'player_turn_durationa.csv'.")

    if __name__ == "__main__":
        main()
    
