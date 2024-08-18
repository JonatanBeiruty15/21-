# Blackjack Strategy Simulator

## Introduction
This project is designed to simulate blackjack strategies using the High-Low card counting method. It offers two main functionalities: building a strategy table and simulating gameplay based on the strategy.

## Features
- **Build Strategy Table:** Allows users to create a table of strategies that can be tested in simulations.
- **Simulation:** Simulate blackjack games to evaluate how the strategy performs under various conditions.

## Configuration Files
The project utilizes two configuration files to manage the simulation parameters:
- `simulation_config.json`: Configure the parameters for the simulation.
- `build_strategy_config.json`: Specify the settings for building the strategy table.

## Getting Started

### Prerequisites
- Python 3.x
- Required Python libraries are listed in `requirements.txt`.

### Installation
1. **Clone the repository:**
git clone https://github.com/JonatanBeiruty15/21-

2. **Install the required Python packages:**
pip install -r requirements.txt


## Usage

### Running the Simulator and Strategy Builder
The main functionalities of this project are encapsulated in `main.py`. This script utilizes configurations from JSON files to either simulate blackjack strategies or build strategy tables. 

#### 1. Simulating Blackjack Strategies
Configure `simulation_config.json` with your desired simulation parameters, then run the `simulate_strategy()` function from `main.py`.

**Output:**
- Receive a report including the average balance of players, the standard deviation, and the average lowest balance.
- Two PNG files showcasing graphs of final and lowest balances for all players in the results folder.

#### 2. Building Strategy Table for a Specific True Count
Configure `create_strategy_configuration.json` accordingly and execute the `build_strategy_from_config()` function.

**Important Note:**
- Rename `test_strategy.pt` to `strategy_{new_version}.pt` after completing all necessary true counts (from -3 to 3) to avoid errors due to invalid moves.

#### 3. Building Complete Strategy Tables
Run the `build_full_strategy(repetitions)` function with the number of repetitions desired.

### Example Configuration
The version 3 of strategies was built using 10,000 repetitions, which took approximately 30 min per true count. Adjust the repetitions based on your performance needs.

### General Instructions
- Ensure all necessary Python modules are installed as specified in `requirements.txt`.
- Run functionalities through `main.py` by uncommenting the appropriate function calls in the `if __name__ == "__main__":` block as needed.

## Configuration

### Simulation Configuration
Edit `simulation_config.json` to adjust the simulation settings.

**Parameters include:**
- `num_of_sim`: Number of simulations to run.
- `num_of_rounds`: Number of rounds per simulation.
- `num_of_players`: Number of players participating.
- `num_decks`: Number of decks used.
- `deck_penetration`: How many decks are dealt before reshuffling.
- `strategy_version`: Specifies the strategy version to test.

**Example of `simulation_config.json`:**
```json
{
"num_of_sim": 60000,
"num_of_rounds": 30,
"num_of_players": 3,
"num_decks": 7,
"deck_penetration": 4,
"strategy_version": 3
}



Strategy Building Configuration

Edit create_strategy_configuration.json to configure parameters for building the strategy table.

Parameters include:

	•	true_count: Specifies the true count value.
	•	repetitions: Number of repetitions for each scenario.

Example of create_strategy_configuration.json:

{
  "true_count": 0,
  "repetitions": 10000
}