Blackjack Strategy Simulator

Introduction

This project is designed to simulate blackjack strategies using the High-Low card counting method. It offers two main functionalities: building a strategy table and simulating gameplay based on the strategy.

Features

	•	Build Strategy Table: This feature allows users to create a table of strategies that can be tested in simulations.
	•	Simulation: After building the strategy table, users can simulate blackjack games to see how the strategy performs under various conditions.

Configuration Files

The project uses two configuration files to manage the simulation parameters:

	•	simulation_config.json: This file is used to configure the parameters for the simulation, such as the number of simulations, rounds per simulation, and the version of the strategy being tested.
	•	build_strategy_config.json: This file allows users to specify the settings for building the strategy table.

Getting Started

Prerequisites

	•	Python 3.x
	•	Required Python libraries: In the requirements.txt

Installation

	1.	Clone the repository:

    git clone [https://github.com/JonatanBeiruty15/21-]


    2.	Install the required Python packages:

    pip install -r requirements.txt



Usage

Running the Simulator and Strategy Builder

The main functionalities of this project are encapsulated in main.py. This script utilizes configurations from JSON files to either simulate blackjack strategies or build strategy tables. Below are the steps to run each functionality:

1. Simulating Blackjack Strategies

To simulate strategies, first configure simulation_configuration.json with your desired simulation parameters. Then, run the simulate_strategy() function from main.py to execute the simulation. The simulation will use the specified strategy version found in the strategies_tensors folder.

Output:

	•	After the simulation, you’ll receive a report including the average balance of players, the standard deviation, and the average lowest balance across the specified number of rounds and simulations.
	•	Two PNG files showcasing graphs of final balances and lowest balances for all players will be generated in the results folder.

    you can see an example in the results folder.

2. Building Strategy Table for a Specific True Count

To build a strategy table for a specific true count, configure create_strategy_configuration.json accordingly. Execute the build_strategy_from_config() function to generate a strategy tensor, which is saved as test_strategy.pt in the strategies_tensors folder.

Important Note:

	•	If you wish to test a new version of a strategy, rename test_strategy.pt to strategy_{new_version}.pt after completing all necessary true counts (from -3 to 3). Testing an incomplete strategy may result in errors due to invalid moves.

3. Building Complete Strategy Tables

To generate complete strategy tables for all true counts from -3 to 3, run the build_full_strategy(repetitions) function, specifying the number of repetitions desired. Each true count requires approximately 30 minutes for 10,000 repetitions based on performance metrics.

Example Configuration:
The version 3 of strategies was built using 10,000 repetitions (which took 30 min per true count). Adjust the repetitions according to your performance needs and computational power available.

General Instructions

	•	Ensure all necessary Python modules are installed as specified in requirements.txt.
	•	Run the functionalities through main.py by uncommenting the appropriate function calls in the if __name__ == "__main__": block as per your requirements:


if __name__ == "__main__":
    print('start')
    # simulate_strategy()
    # build_strategy_from_config()
    # build_full_strategy(repetitions=10000)  # Adjust repetitions as needed


Note: Direct execution and modification of main.py is recommended to integrate seamlessly with the existing codebase and ensure correct file paths and configurations are used.



Configuration

Configuration files are used to tailor the parameters for both simulating blackjack strategies and building strategy tables. Edit the following JSON configuration files according to your requirements:

    Simulation Configuration

        Edit the simulation_config.json to adjust the simulation settings. Parameters include:

            •	num_of_sim: Number of simulations to run.
            •	num_of_rounds: Number of rounds per simulation.
            •	num_of_players: Number of players participating in the simulation.
            •	num_decks: Number of decks used in the blackjack game.
            •	deck_penetration: How many decks are dealt before reshuffling occurs.
            •	strategy_version: Specify the version of the strategy to apply.

        Example of simulation_config.json:


            {
            "num_of_sim": 60000,
            "num_of_rounds": 30,
            "num_of_players": 3,
            "num_decks": 7,
            "deck_penetration": 4,
            "strategy_version": 3
        }


        Parameter Details

        The simulation_config.json file contains several key parameters that define how blackjack simulations are run. Below is a detailed description of each parameter:

            •	num_simulations: Represents the total number of times the simulation will be executed. Each simulation runs a set number of rounds, as defined by num_rounds.
            •	num_rounds: Specifies the number of blackjack rounds played in each simulation. After this number of rounds, the simulation resets, setting all player balances back to zero before starting a new simulation.
            •	num_of_players: Indicates the number of players participating in each round of blackjack.
            •	num_decks: Denotes the total number of decks used in the shoe for the blackjack game. This affects the complexity and the odds of the game, influencing strategy outcomes.
            •	deck_penetration: Refers to how many decks are dealt before the deck is reshuffled. This is a critical factor in card counting strategies as it affects the card composition of play.
            •	strategy_version: Specifies which strategy to test during the simulations. This corresponds to a file in the strategies_tensors folder; for example, strategy_3.pt if strategy_version is set to 3. This file contains the strategy tensor that dictates player actions based on the game state.




    Strategy Building Configuration

        Edit the create_strategy_configuration.json to configure the parameters for building the strategy table. Parameters include:

        •	true_count: Specifies the true count value for which the strategy table is built.
        •	repetitions: Number of repetitions for each scenario within the strategy table.

        Example of create_strategy_configuration.json:


                {
        "true_count": 0,
        "repetitions": 10000
}




These configuration files allow you to run simulations and build strategy tables with different parameters without altering the core program code, making it easy to test various scenarios and strategies.